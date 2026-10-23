"""Regression checks for combined ZEN API documentation and CI artifacts."""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


@pytest.fixture
def builder():
    path = Path(__file__).resolve().parents[1] / "build_zen_api_docs.py"
    spec = importlib.util.spec_from_file_location("build_zen_api_docs", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def sources(tmp_path):
    api_root = tmp_path / "ZEN-API"
    package = api_root / "python_packages" / "zen_api-2026.07.1"
    module = package / "src" / "zen_api" / "common" / "v1"
    module.mkdir(parents=True)
    (module / "__init__.py").write_text('"""API definitions."""\n', encoding="utf-8")
    (package / "pyproject.toml").write_text(
        '[project]\nname = "zen_api"\nversion = "2026.07.1"\nrequires-python = ">=3.12,<3.16"\n',
        encoding="utf-8",
    )
    utils = api_root / "zen_api_utils_package"
    utils_source = utils / "src" / "zen_api_utils"
    utils_source.mkdir(parents=True)
    (utils_source / "__init__.py").write_text("", encoding="utf-8")
    (utils_source / "misc.py").write_text('"""Utility helpers."""\n', encoding="utf-8")
    (utils / "pyproject.toml").write_text(
        '[project]\nname = "zen_api_utils"\nversion = "0.1.0"\nrequires-python = ">=3.12,<3.16"\n',
        encoding="utf-8",
    )
    guide = utils / "mkdocs_docs"
    guide.mkdir()
    (guide / "index.md").write_text("# Utilities\n", encoding="utf-8")
    proto = api_root / "protofiles" / "proto_2026.07.1" / "zen_api" / "common" / "v1"
    proto.mkdir(parents=True)
    (proto / "sample.proto").write_text(
        'syntax = "proto3";\npackage zen_api.common.v1;\n'
        '// Request documentation.\nmessage Request {\n'
        '  // Value description.\n  string value = 1;\n'
        '  optional int32 count = 2;\n'
        '  map<string, string> labels = 3;\n'
        '  oneof choice { string text = 4; int32 number = 5; }\n'
        '  enum State { UNKNOWN = 0; READY = 1; }\n'
        '  State state = 6;\n}\n'
        'service SampleService {\n  // Streaming documentation.\n'
        '  rpc Watch (stream Request) returns (stream Request);\n}\n',
        encoding="utf-8",
    )
    return tmp_path


def test_combined_navigation_and_versions(builder, sources, monkeypatch):
    """Keep API URLs while adding utility references and exact source versions."""
    configs = []
    monkeypatch.setattr(builder, "run_mkdocs", lambda path, **kwargs: configs.append(path))
    monkeypatch.setattr(builder, "generate_proto_pages", lambda *args: [{"Overview": "proto/index.md"}])
    builder.build_version_page(sources, sources / "build", sources / "site", "2026.07.1")
    config = yaml.safe_load(configs[0].read_text(encoding="utf-8"))
    docs = Path(config["docs_dir"])
    assert config["extra"]["documented_versions"] == {"zen_api": "2026.07.1", "zen_api_utils": "0.1.0"}
    assert (docs / "reference/common/v1.md").is_file()
    assert "::: zen_api_utils.misc" in (docs / "reference/zen_api_utils/misc.md").read_text(encoding="utf-8")
    assert (docs / "guides/zen_api_utils/index.md").is_file()
    assert config["nav"][-1] == {"Protocol Buffer Reference": [{"Overview": "proto/index.md"}]}
    handler = config["plugins"][-1]["mkdocstrings"]["handlers"]["python"]
    assert len(handler["paths"]) == 2
    assert config["strict"] is True
    assert ">=3.12,<3.16" in (docs / "index.md").read_text(encoding="utf-8")


def test_proto_reference_and_original_sources(builder, sources):
    """Compile real descriptors and preserve comments, maps, presence and RPCs."""
    protoc = shutil.which("protoc")
    if protoc is None:
        pytest.skip("Protocol Buffers compiler unavailable")
    docs = sources / "build" / "docs"
    docs.mkdir(parents=True)
    proto_root = sources / "ZEN-API/protofiles/proto_2026.07.1"
    nav = builder.generate_proto_pages(proto_root, docs, "2026.07.1", protoc)
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


@pytest.mark.parametrize("version", ["../2026.07.1", "2026.07.1;echo", "2026.11.1"])
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
    assert "inputs.publish_releases" in jobs["publish-releases"]["if"]
    assert "deploy-docs" in jobs["publish-releases"]["needs"]


def test_workflow_version_matrix_uses_actual_package_metadata(sources):
    """Run CI's version resolver against fixtures, including duplicate handling."""
    workflow = Path(__file__).resolve().parents[2] / "workflows/deploy-zen-api-docs.yml"
    config = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    script = config["jobs"]["settings"]["steps"][-1]["run"]
    python_code = "\n".join(script.splitlines()[1:-1])
    output = sources / "outputs.txt"
    environment = {**os.environ, "DOC_VERSIONS": "2026.07.1 2026.07.1", "GITHUB_OUTPUT": str(output)}
    subprocess.run([sys.executable, "-c", python_code], cwd=sources, env=environment, check=True)
    assert json.loads(output.read_text(encoding="utf-8").split("=", 1)[1]) == ["2026.07.1"]
    environment["DOC_VERSIONS"] = "../2026.07.1"
    result = subprocess.run([sys.executable, "-c", python_code], cwd=sources, env=environment, capture_output=True)
    assert result.returncode != 0