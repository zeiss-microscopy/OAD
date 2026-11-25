"""Regression checks for independently versioned ZEN API documentation and artifacts."""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from packaging.version import Version


@pytest.fixture
def builder():
    path = Path(__file__).resolve().parents[1] / "build_zen_api_docs.py"
    spec = importlib.util.spec_from_file_location("build_zen_api_docs", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def sources(tmp_path):
    script = tmp_path / ".github/scripts/build_zen_api_docs.py"
    script.parent.mkdir(parents=True)
    shutil.copy2(Path(__file__).resolve().parents[1] / "build_zen_api_docs.py", script)
    api_root = tmp_path / "ZEN-API"
    package = api_root / "python_packages" / "zen_api-2026.7.1"
    module = package / "src" / "zen_api" / "common" / "v1"
    module.mkdir(parents=True)
    (module / "__init__.py").write_text('"""API definitions."""\n', encoding="utf-8")
    (package / "pyproject.toml").write_text(
        '[project]\nname = "zen_api"\nversion = "2026.7.1"\nrequires-python = ">=3.12,<3.16"\n',
        encoding="utf-8",
    )
    utils = api_root / "zen_api_utils"
    utils_source = utils / "src" / "zen_api_utils"
    utils_source.mkdir(parents=True)
    (utils_source / "__init__.py").write_text("", encoding="utf-8")
    (utils_source / "misc.py").write_text('"""Utility helpers."""\n', encoding="utf-8")
    (utils / "pyproject.toml").write_text(
        '[project]\nname = "zen_api_utils"\nversion = "0.1.0"\nrequires-python = ">=3.12,<3.16"\n'
        'dependencies = ["zen_api>=2026.5.1,<=2026.11.1"]\n',
        encoding="utf-8",
    )
    guide = utils / "mkdocs_docs"
    guide.mkdir()
    (guide / "index.md").write_text("# Utilities\n", encoding="utf-8")
    proto = api_root / "protofiles" / "proto_2026.7.1" / "zen_api" / "common" / "v1"
    proto.mkdir(parents=True)
    (proto / "sample.proto").write_text(
        'syntax = "proto3";\npackage zen_api.common.v1;\n'
        "// Request documentation.\nmessage Request {\n"
        "  // Value description.\n  string value = 1;\n"
        "  optional int32 count = 2;\n"
        "  map<string, string> labels = 3;\n"
        "  oneof choice { string text = 4; int32 number = 5; }\n"
        "  enum State { UNKNOWN = 0; READY = 1; }\n"
        "  State state = 6;\n}\n"
        "service SampleService {\n  // Streaming documentation.\n"
        "  rpc Watch (stream Request) returns (stream Request);\n}\n",
        encoding="utf-8",
    )
    return tmp_path


def test_separate_navigation_and_versions(builder, sources, monkeypatch):
    """Keep API URLs and give utilities their own reference and version selector."""
    configs = []
    monkeypatch.setattr(builder, "run_mkdocs", lambda path, **kwargs: configs.append(path))
    monkeypatch.setattr(builder, "generate_proto_pages", lambda *args: [{"Overview": "proto/index.md"}])
    builder.build_version_page(sources, sources / "build", sources / "site", "2026.7.1")
    builder.build_utility_page(sources, sources / "build", sources / "site")
    config = yaml.safe_load(configs[0].read_text(encoding="utf-8"))
    docs = Path(config["docs_dir"])
    assert config["extra"]["documented_versions"] == {"zen_api": "2026.7.1"}
    assert config["extra"]["version"]["provider"] == "mike"
    assert (docs / "reference/common/v1.md").is_file()
    assert not (docs / "reference/zen_api_utils").exists()
    assert not (docs / "guides/zen_api_utils").exists()
    assert {"Utilities Documentation": "https://zeiss-microscopy.github.io/OAD/zen_api_utils/"} in config["nav"]
    assert config["nav"][-1] == {"Protocol Buffer Reference": [{"Overview": "proto/index.md"}]}
    handler = config["plugins"][-1]["mkdocstrings"]["handlers"]["python"]
    assert len(handler["paths"]) == 1
    assert config["strict"] is True
    assert ">=3.12,<3.16" in (docs / "index.md").read_text(encoding="utf-8")
    utility_config = yaml.safe_load(configs[1].read_text(encoding="utf-8"))
    utility_docs = Path(utility_config["docs_dir"])
    assert utility_config["site_url"] == "https://zeiss-microscopy.github.io/OAD/zen_api_utils/0.1.0/"
    assert Path(utility_config["site_dir"]) == sources / "site/zen_api_utils/0.1.0"
    assert utility_config["extra"]["documented_versions"] == {"zen_api_utils": "0.1.0"}
    assert utility_config["extra"]["version"]["provider"] == "mike"
    assert "::: zen_api_utils.misc" in (utility_docs / "reference/zen_api_utils/misc.md").read_text(encoding="utf-8")
    assert not (utility_docs / "proto").exists()
    assert {"ZEN API Documentation": "https://zeiss-microscopy.github.io/OAD/"} in utility_config["nav"]


def test_build_keeps_utility_history_and_separate_selectors(builder, sources, monkeypatch):
    """A full Pages deployment must not erase previously published utility versions."""
    previous = sources / "previous-utilities"
    (previous / "0.0.9").mkdir(parents=True)
    (previous / "0.0.9/index.html").write_text("Historical utilities", encoding="utf-8")
    (previous / "0.1.0").mkdir()
    (previous / "0.1.0/index.html").write_text("Previous current snapshot", encoding="utf-8")
    (previous / "versions.json").write_text(
        json.dumps([
            {"version": "0.1.0", "title": "0.1.0", "aliases": ["latest"]},
            {"version": "0.0.9", "title": "0.0.9", "aliases": []},
        ]),
        encoding="utf-8",
    )
    monkeypatch.setattr(builder.shutil, "which", lambda command: "protoc")
    monkeypatch.setattr(builder, "generate_proto_pages", lambda *args: [])

    def build_site(path, **kwargs):
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
        output = Path(config["site_dir"])
        output.mkdir(parents=True, exist_ok=True)
        (output / "index.html").write_text(config["site_name"], encoding="utf-8")

    monkeypatch.setattr(builder, "run_mkdocs", build_site)
    monkeypatch.setattr(
        sys, "argv",
        ["builder", "--repo-root", str(sources), "--versions", "2026.7.1",
         "--previous-utils-site-dir", str(previous)],
    )
    builder.main()
    site = sources / "site"
    assert (site / "zenapi/2026.7.1/index.html").read_text(encoding="utf-8") == "ZEN API 2026.7.1"
    assert (site / "zen_api_utils/0.0.9/index.html").read_text(encoding="utf-8") == "Historical utilities"
    assert (site / "zen_api_utils/0.1.0/index.html").read_text(encoding="utf-8") == "ZEN API Utilities 0.1.0"
    api_versions = json.loads((site / "zenapi/versions.json").read_text(encoding="utf-8"))
    utility_versions = json.loads((site / "zen_api_utils/versions.json").read_text(encoding="utf-8"))
    assert api_versions == [{"version": "2026.7.1", "title": "2026.7.1", "aliases": ["latest"]}]
    assert utility_versions == [
        {"version": "0.1.0", "title": "0.1.0", "aliases": ["latest"]},
        {"version": "0.0.9", "title": "0.0.9", "aliases": []},
    ]
    assert "0.1.0/" in (site / "zen_api_utils/index.html").read_text(encoding="utf-8")


@pytest.mark.parametrize("manifest", [
    {"not": "a version list"},
    [{"version": "../outside"}],
    [{"version": "0.0.9"}],
])
def test_invalid_utility_history_preserves_output(builder, sources, monkeypatch, manifest):
    previous = sources / "previous-utilities"
    previous.mkdir()
    (previous / "versions.json").write_text(json.dumps(manifest), encoding="utf-8")
    site = sources / "site"
    site.mkdir()
    marker = site / "keep.txt"
    marker.write_text("keep", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", [
        "builder", "--repo-root", str(sources), "--versions", "2026.7.1",
        "--previous-utils-site-dir", str(previous),
    ])
    with pytest.raises(SystemExit):
        builder.main()
    assert marker.read_text(encoding="utf-8") == "keep"


def test_proto_reference_and_original_sources(builder, sources):
    """Compile real descriptors and preserve comments, maps, presence and RPCs."""
    protoc = shutil.which("protoc")
    if protoc is None:
        pytest.skip("Protocol Buffers compiler unavailable")
    docs = sources / "build" / "docs"
    docs.mkdir(parents=True)
    proto_root = sources / "ZEN-API/protofiles/proto_2026.7.1"
    nav = builder.generate_proto_pages(proto_root, docs, "2026.7.1", protoc)
    relative = "zen_api/common/v1/sample.proto"
    page = (docs / builder.proto_page(relative)).read_text(encoding="utf-8")
    assert "Request documentation." in page
    assert "Value description." in page
    assert "Streaming documentation." in page
    assert "stream zen_api.common.v1.Request" in page
    assert "map&lt;`string`, `string`&gt;" in page
    assert "optional" in page
    assert "oneof `choice`" in page
    assert "Enum `State`" in page
    assert (docs / "proto/source" / relative).read_bytes() == (proto_root / relative).read_bytes()
    assert nav[0] == {"Overview": "proto/index.md"}


@pytest.mark.parametrize(
    "version",
    ["../2026.7.1", "2026.7.1;echo", "2026.07.1", "2026.0.1", "2026.13.1", "2026.7.01", "2026.11.1"],
)
def test_invalid_or_missing_version_preserves_output(builder, sources, monkeypatch, version):
    """Invalid or absent version inputs must fail before deleting previous output."""
    site = sources / "site"
    site.mkdir()
    marker = site / "previous.txt"
    marker.write_text("keep", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["builder", "--repo-root", str(sources), "--versions", version])
    with pytest.raises(SystemExit):
        builder.main()
    assert marker.read_text(encoding="utf-8") == "keep"


@pytest.mark.parametrize(
    "failure",
    [
        "missing-utils",
        "missing-proto",
        "mismatched-version",
        "wrong-utils-name",
        "missing-api-range",
        "unsupported-api",
    ],
)
def test_preflight_failure_preserves_all_output(builder, sources, monkeypatch, failure):
    """Reject invalid pairs and missing inputs before clearing any existing output."""
    api_root = sources / "ZEN-API"
    package = api_root / "python_packages/zen_api-2026.7.1"
    utils = api_root / "zen_api_utils"
    versions = ["2026.7.1"]
    if failure == "missing-utils":
        shutil.rmtree(utils)
    elif failure == "missing-proto":
        shutil.rmtree(api_root / "protofiles/proto_2026.7.1")
    elif failure == "mismatched-version":
        metadata = package / "pyproject.toml"
        metadata.write_text(metadata.read_text().replace('version = "2026.7.1"', 'version = "2026.07.1"'))
    elif failure == "wrong-utils-name":
        metadata = utils / "pyproject.toml"
        metadata.write_text(metadata.read_text().replace('name = "zen_api_utils"', 'name = "other"'))
    elif failure == "missing-api-range":
        metadata = utils / "pyproject.toml"
        metadata.write_text(metadata.read_text().replace("zen_api>=2026.5.1,<=2026.11.1", "zen_api"))
    else:
        historical = api_root / "python_packages/zen_api-2025.10.1"
        shutil.copytree(package, historical)
        metadata = historical / "pyproject.toml"
        metadata.write_text(metadata.read_text().replace("2026.7.1", "2025.10.1"))
        shutil.copytree(api_root / "protofiles/proto_2026.7.1", api_root / "protofiles/proto_2025.10.1")
        versions.append("2025.10.1")
        with pytest.raises(ValueError, match="outside.*supported range"):
            builder.build_version_page(sources, sources / "new-build", sources / "new-site", "2025.10.1")
        assert not (sources / "new-build").exists()
    markers = []
    for directory in (sources / "build", sources / "site"):
        directory.mkdir()
        marker = directory / "previous.txt"
        marker.write_text("keep", encoding="utf-8")
        markers.append(marker)
    monkeypatch.setattr(
        sys, "argv", ["builder", "--repo-root", str(sources), "--build-dir", "build", "--versions", *versions]
    )
    with pytest.raises(SystemExit):
        builder.main()
    assert all(marker.read_text(encoding="utf-8") == "keep" for marker in markers)


def test_workflow_builds_fresh_versioned_artifacts_and_opt_in_releases():
    """Upload fresh wheels/sdists independently of the opt-in release publication."""
    workflow = Path(__file__).resolve().parents[2] / "workflows/deploy-zen-api-docs.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    assert config["on"]["workflow_dispatch"]["inputs"]["publish_releases"]["default"] is False
    jobs = config["jobs"]
    steps = jobs["build-packages"]["steps"]
    commands = "\n".join(step.get("run", "") for step in steps)
    assert "python -m build" in commands
    assert "--outdir" in commands and "RUNNER_TEMP" in commands
    assert "hatchling==1.27.0" in commands and "--no-isolation" in commands
    assert "twine check" in commands
    upload = next(step for step in steps if step.get("uses", "").startswith("actions/upload-artifact@"))
    assert upload["with"]["name"] == "zen_api-${{ matrix.version }}-python-package"
    assert "*.whl" in upload["with"]["path"] and "*.tar.gz" in upload["with"]["path"]
    assert upload["with"]["if-no-files-found"] == "error"
    compatibility = jobs["test-utilities"]
    assert compatibility["needs"] == ["settings", "build-packages", "build-utilities"]
    assert compatibility["strategy"]["matrix"]["python"] == ["3.12", "3.13", "3.14", "3.15"]
    assert compatibility["strategy"]["matrix"]["version"] == "${{ fromJSON(needs.settings.outputs.versions) }}"
    matching = next(
        step for step in compatibility["steps"] if step.get("uses", "").startswith("actions/download-artifact@")
    )
    assert matching["with"]["name"] == upload["with"]["name"]
    checks = "\n".join(step.get("run", "") for step in compatibility["steps"])
    assert checks.index("/zen-api-dist/*.whl") < checks.index("utility_wheels[0]")
    assert "pip check" in checks
    assert "pytest ZEN-API/zen_api_utils/tests" in checks
    assert "test-utilities" in jobs["deploy-docs"]["needs"]
    assert "inputs.publish_releases" in jobs["publish-releases"]["if"]
    assert "deploy-docs" in jobs["publish-releases"]["needs"]
    assert "zen_api_utils_package" not in workflow.read_text(encoding="utf-8")


def test_workflow_publishes_separate_docs_and_retains_utility_snapshots():
    workflow = Path(__file__).resolve().parents[2] / "workflows/deploy-zen-api-docs.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    job = config["jobs"]["deploy-docs"]
    assert job["permissions"]["contents"] == "write"
    steps = job["steps"]
    commands = "\n".join(step.get("run", "") for step in steps)
    assert "git ls-remote --exit-code origin refs/heads/zen-api-utils-docs-history" in commands
    assert '"$status" != "2"' in commands
    assert '--previous-utils-site-dir "$PREVIOUS_UTILS_SITE"' in commands
    artifacts = [step["with"] for step in steps if step.get("uses", "").startswith("actions/upload-artifact@")]
    assert {artifact["path"] for artifact in artifacts} == {
        "site/zenapi", "site/zen_api_utils/${{ needs.settings.outputs.utils_version }}"
    }
    pages = next(step for step in steps if step.get("uses", "").startswith("actions/upload-pages-artifact@"))
    assert pages["with"]["path"] == "site"
    artifact_name = "github-pages-${{ github.run_id }}-${{ github.run_attempt }}"
    assert pages["with"]["name"] == artifact_name
    deployment = next(step for step in steps if step.get("uses", "").startswith("actions/deploy-pages@"))
    assert deployment["with"]["artifact_name"] == artifact_name
    readiness = next(step for step in steps if step.get("id") == "pages_artifact_ready")
    install = next(step for step in steps if "npm ci --prefix .github/scripts" in step.get("run", ""))
    assert steps.index(install) < steps.index(readiness)
    assert steps.index(pages) < steps.index(readiness) < steps.index(deployment)
    assert job["permissions"]["actions"] == "read"
    assert readiness["env"]["ARTIFACT_NAME"] == artifact_name
    assert readiness["env"]["ARTIFACT_ID"] == "${{ steps.pages_upload.outputs.artifact_id }}"
    assert pages["id"] == "pages_upload"
    history = next(step for step in steps if step.get("uses", "").startswith("peaceiris/actions-gh-pages@"))
    assert history["with"]["publish_branch"] == "zen-api-utils-docs-history"
    assert history["with"]["publish_dir"] == "site/zen_api_utils"
    assert config["concurrency"]["cancel-in-progress"] is False


@pytest.mark.parametrize(
    "scenario", ["immediate", "delayed", "timeout", "duplicate", "api-error", "wrong-id", "missing-size", "empty"]
)
def test_pages_artifact_readiness_handles_visibility_delay(scenario):
    """Execute the actual workflow script with deterministic artifact API responses."""
    workflow = Path(__file__).resolve().parents[2] / "workflows/deploy-zen-api-docs.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    step = next(step for step in config["jobs"]["deploy-docs"]["steps"] if step.get("id") == "pages_artifact_ready")
    harness = r"""
const assert = require("node:assert/strict");
const { script, scenario } = JSON.parse(require("node:fs").readFileSync(0, "utf8"));
let calls = 0;
const sleeps = [];
const logs = [];
const artifact = {id: 42, name: "pages-test", size: 123};
const artifactRequire = name => {
  assert.ok(name.endsWith("/.github/scripts/node_modules/@actions/artifact"));
  return {DefaultArtifactClient: class {
  async listArtifacts() {
    calls++;
    if (scenario === "api-error") throw new Error("Forbidden");
    if (scenario === "timeout" || (scenario === "delayed" && calls < 3))
      return {artifacts: [{...artifact, name: "another-artifact"}]};
    if (scenario === "duplicate") return {artifacts: [artifact, {...artifact, id: 43}]};
    if (scenario === "wrong-id") return {artifacts: [{...artifact, id: 43}]};
    if (scenario === "missing-size") return {artifacts: [{...artifact, size: undefined}]};
    if (scenario === "empty") return {artifacts: [{...artifact, size: 0}]};
    return {artifacts: [artifact]};
  }}};
};
const core = {info: message => logs.push(message)};
const wait = (callback, milliseconds) => { sleeps.push(milliseconds); callback(); };
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
(async () => {
  const execute = () => new AsyncFunction("require", "core", "setTimeout", script)(
    artifactRequire, core, wait
  );
  if (scenario === "timeout") {
    await assert.rejects(execute, /not visible after 12 attempts/);
    assert.equal(calls, 12);
    assert.equal(sleeps.length, 11);
  } else if (scenario === "duplicate") {
    await assert.rejects(execute, /Multiple artifacts/);
    assert.equal(calls, 1);
    assert.equal(sleeps.length, 0);
  } else if (scenario === "api-error") {
    await assert.rejects(execute, /Forbidden/);
    assert.equal(calls, 1);
    assert.equal(sleeps.length, 0);
  } else if (["wrong-id", "missing-size", "empty"].includes(scenario)) {
    await assert.rejects(execute, /unexpected ID or size/);
    assert.equal(calls, 1);
    assert.equal(sleeps.length, 0);
  } else {
    await execute();
    assert.equal(calls, scenario === "delayed" ? 3 : 1);
    assert.equal(sleeps.length, calls - 1);
    assert.ok(logs.some(message => message.includes("ready")));
  }
  assert.ok(sleeps.every(delay => delay === 5000));
})().catch(error => { console.error(error); process.exitCode = 1; });
"""
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is required to exercise the GitHub Actions JavaScript")
    result = subprocess.run(
        [node, "-e", harness],
        input=json.dumps({"script": step["with"]["script"], "scenario": scenario}),
        env={**os.environ, "ARTIFACT_NAME": "pages-test", "ARTIFACT_ID": "42", "GITHUB_WORKSPACE": "/workspace"},
        capture_output=True,
        encoding="utf-8",
        check=False,
        timeout=15,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_utility_release_uses_tested_wheels_and_explicit_approval():
    """Publish one utility artifact only after testing its wheel, never editable sources."""
    workflow = Path(__file__).resolve().parents[2] / "workflows/deploy-zen-api-docs.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    inputs = config["on"]["workflow_dispatch"]["inputs"]
    assert inputs["publish_utils_release"]["default"] is False
    jobs = config["jobs"]
    for job_name in ("publish-releases", "publish-utilities-release"):
        steps = jobs[job_name]["steps"]
        guard = next(step for step in steps if step.get("id") == "release_check")
        assert "prepare_release.cjs" in guard["with"]["script"]
        for step in steps:
            if step.get("uses", "").startswith(("actions/download-artifact@", "softprops/action-gh-release@")):
                assert step["if"] == "steps.release_check.outputs.publish == 'true'"
    build = jobs["build-utilities"]
    assert "matrix" not in build.get("strategy", {})
    commands = "\n".join(step.get("run", "") for step in build["steps"])
    assert 'python -m build "ZEN-API/zen_api_utils"' in commands
    assert "twine check" in commands
    upload = next(step for step in build["steps"] if step.get("uses", "").startswith("actions/upload-artifact@"))
    assert upload["with"]["name"] == "zen_api_utils-${{ needs.settings.outputs.utils_version }}-python-package"
    assert "*.whl" in upload["with"]["path"] and "*.tar.gz" in upload["with"]["path"]
    assert upload["with"]["if-no-files-found"] == "error"
    compatibility = jobs["test-utilities"]
    assert "build-utilities" in compatibility["needs"]
    downloads = [
        step for step in compatibility["steps"] if step.get("uses", "").startswith("actions/download-artifact@")
    ]
    assert upload["with"]["name"] in [step["with"]["name"] for step in downloads]
    checks = "\n".join(step.get("run", "") for step in compatibility["steps"])
    assert "zen-api-utils-dist/*.whl" in checks
    assert '"${utility_wheels[0]}[all]"' in checks
    assert " -e " not in checks
    assert "-o pythonpath=" in checks and "--import-mode=importlib" in checks
    assert 'version("zen_api_utils") == os.environ["UTILS_VERSION"]' in checks
    assert 'version("zen_api") == os.environ["API_VERSION"]' in checks
    assert "is_relative_to" in checks
    publish = jobs["publish-utilities-release"]
    assert "workflow_dispatch" in publish["if"] and "inputs.publish_utils_release" in publish["if"]
    assert {"settings", "build-utilities", "test-utilities", "deploy-docs"} <= set(publish["needs"])
    assert publish["permissions"]["contents"] == "write"
    release = next(step for step in publish["steps"] if step.get("uses", "").startswith("softprops/action-gh-release@"))
    assert release["with"]["tag_name"] == "zen-api-utils-v${{ needs.settings.outputs.utils_version }}"
    assert release["with"]["make_latest"] is False
    assert "*.whl" in release["with"]["files"] and "*.tar.gz" in release["with"]["files"]
    api_release = next(
        step
        for step in jobs["publish-releases"]["steps"]
        if step.get("uses", "").startswith("softprops/action-gh-release@")
    )
    assert api_release["with"]["tag_name"] == "${{ fromJSON(needs.settings.outputs.release_tags)[matrix.version] }}"


def test_workflow_defaults_match_supported_bundled_sources(builder):
    """Default documentation releases must exist and support the current utility release."""
    repo_root = Path(__file__).resolve().parents[3]
    workflow = repo_root / ".github/workflows/deploy-zen-api-docs.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    defaults = config["on"]["workflow_dispatch"]["inputs"]["versions"]["default"]
    assert defaults == "2026.11.1 2026.7.1 2026.5.1"
    assert defaults in config["env"]["DOC_VERSIONS"]
    readme = (repo_root / "ZEN-API/README.md").read_text(encoding="utf-8")
    for version in defaults.split():
        api_project, utils_project = builder.validate_version(repo_root, version)
        assert api_project["version"] == version
        assert api_project["requires-python"] == ">=3.12,<3.16"
        assert str(Version(utils_project["version"])) == utils_project["version"]
        assert f"https://zeiss-microscopy.github.io/OAD/zenapi/{version}/" in readme


@pytest.mark.parametrize(
    ("relative", "prefix"),
    [("python_packages", "zen_api-"), ("protofiles", "proto_")],
)
def test_bundled_version_folders_use_canonical_names(relative, prefix):
    """Never reintroduce zero-padded release directories during a merge."""
    root = Path(__file__).resolve().parents[3] / "ZEN-API" / relative
    directories = [directory for directory in root.glob(f"{prefix}*") if directory.is_dir()]
    assert directories
    for directory in directories:
        version = directory.name.removeprefix(prefix)
        assert str(Version(version)) == version, f"Noncanonical version directory: {directory}"


def test_workflow_version_matrix_uses_actual_package_metadata(sources):
    """Run CI's version resolver against fixtures, including duplicate handling."""
    workflow = Path(__file__).resolve().parents[2] / "workflows/deploy-zen-api-docs.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    script = config["jobs"]["settings"]["steps"][-1]["run"]
    python_code = "\n".join(script.splitlines()[1:-1])
    output = sources / "outputs.txt"
    environment = {**os.environ, "DOC_VERSIONS": "2026.7.1 2026.7.1", "GITHUB_OUTPUT": str(output)}
    subprocess.run([sys.executable, "-c", python_code], cwd=sources, env=environment, check=True)
    resolved = dict(line.split("=", 1) for line in output.read_text(encoding="utf-8").splitlines())
    assert json.loads(resolved["versions"]) == ["2026.7.1"]
    assert json.loads(resolved["release_tags"]) == {"2026.7.1": "v2026.07.1"}
    assert resolved["utils_version"] == "0.1.0"
    previous = output.read_text(encoding="utf-8")
    for invalid in ("../2026.7.1", "2026.07.1", "2026.11.1", "2025.10.1", ""):
        environment["DOC_VERSIONS"] = invalid
        result = subprocess.run([sys.executable, "-c", python_code], cwd=sources, env=environment, capture_output=True)
        assert result.returncode != 0
        assert output.read_text(encoding="utf-8") == previous


@pytest.mark.parametrize(
    ("api_version", "release_tag"),
    [
        ("2026.5.1", "v2026.05.1"),
        ("2026.7.1", "v2026.07.1"),
        ("2026.11.1", "v2026.11.1"),
    ],
)
def test_release_versions_preserve_legacy_tags_and_independent_utilities(sources, api_version, release_tag):
    """Resolve historical API tags and the utility's own metadata, not an API version."""
    api_root = sources / "ZEN-API"
    if api_version != "2026.7.1":
        package = api_root / "python_packages" / f"zen_api-{api_version}"
        shutil.copytree(api_root / "python_packages/zen_api-2026.7.1", package)
        metadata = package / "pyproject.toml"
        metadata.write_text(metadata.read_text(encoding="utf-8").replace("2026.7.1", api_version), encoding="utf-8")
        shutil.copytree(api_root / "protofiles/proto_2026.7.1", api_root / "protofiles" / f"proto_{api_version}")
    utility_metadata = api_root / "zen_api_utils/pyproject.toml"
    utility_metadata.write_text(
        utility_metadata.read_text(encoding="utf-8").replace('version = "0.1.0"', 'version = "0.2.0"'),
        encoding="utf-8",
    )
    workflow = Path(__file__).resolve().parents[2] / "workflows/deploy-zen-api-docs.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    script = config["jobs"]["settings"]["steps"][-1]["run"]
    python_code = "\n".join(script.splitlines()[1:-1])
    output = sources / "outputs.txt"
    environment = {**os.environ, "DOC_VERSIONS": api_version, "GITHUB_OUTPUT": str(output)}
    subprocess.run([sys.executable, "-c", python_code], cwd=sources, env=environment, check=True)
    resolved = dict(line.split("=", 1) for line in output.read_text(encoding="utf-8").splitlines())
    assert json.loads(resolved["release_tags"]) == {api_version: release_tag}
    assert resolved["utils_version"] == "0.2.0"


@pytest.mark.parametrize("utility_version", ["0.01.0", "invalid/version"])
def test_invalid_utility_version_preserves_settings_output(sources, utility_version):
    """Reject unsafe or noncanonical utility versions before producing release outputs."""
    metadata = sources / "ZEN-API/zen_api_utils/pyproject.toml"
    metadata.write_text(
        metadata.read_text(encoding="utf-8").replace('version = "0.1.0"', f'version = "{utility_version}"'),
        encoding="utf-8",
    )
    workflow = Path(__file__).resolve().parents[2] / "workflows/deploy-zen-api-docs.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    script = config["jobs"]["settings"]["steps"][-1]["run"]
    python_code = "\n".join(script.splitlines()[1:-1])
    output = sources / "outputs.txt"
    output.write_text("previous output\n", encoding="utf-8")
    environment = {**os.environ, "DOC_VERSIONS": "2026.7.1", "GITHUB_OUTPUT": str(output)}
    result = subprocess.run([sys.executable, "-c", python_code], cwd=sources, env=environment, capture_output=True)
    assert result.returncode != 0
    assert output.read_text(encoding="utf-8") == "previous output\n"
