"""Build versioned ZEN API MkDocs Material documentation for GitHub Pages."""

from __future__ import annotations

import argparse
import html
import posixpath
import re
import shutil
import subprocess
import sys
import textwrap
import tomllib
from pathlib import Path, PurePosixPath

import yaml
from betterproto.lib.google.protobuf import FileDescriptorSet

ZENAPI_PAGES_PATH = "zenapi"

DOMAIN_LABELS = {
    "acquisition": "Acquisition",
    "application": "Application",
    "common": "Common",
    "em": "Electron Microscopy",
    "hardware": "Hardware",
    "lm": "Light Microscopy",
    "workflows": "Workflows",
}


def run_mkdocs(config_path: Path, *, strict: bool = True) -> None:
    command = [sys.executable, "-m", "mkdocs", "build", "--config-file", str(config_path)]
    if strict:
        command.append("--strict")

    subprocess.run(
        command,
        check=True,
    )


def mkdocs_material_config(site_name: str, site_url: str, docs_dir: Path, site_dir: Path) -> dict:
    return {
        "site_name": site_name,
        "site_url": site_url,
        "site_description": "Python wrappers for the ZEN API (ZEISS microscopy platform)",
        "repo_name": "zeiss-microscopy/OAD",
        "repo_url": "https://github.com/zeiss-microscopy/OAD",
        "use_directory_urls": False,
        "strict": True,
        "validation": {
            "omitted_files": "warn",
            "absolute_links": "warn",
            "unrecognized_links": "warn",
        },
        "docs_dir": str(docs_dir.resolve()),
        "site_dir": str(site_dir.resolve()),
        "theme": {
            "name": "material",
            "icon": {
                "logo": "material/microscope",
                "repo": "fontawesome/brands/github",
            },
            "palette": [
                {
                    "media": "(prefers-color-scheme: light)",
                    "scheme": "default",
                    "primary": "blue",
                    "toggle": {"icon": "material/brightness-7", "name": "Switch to dark mode"},
                },
                {
                    "media": "(prefers-color-scheme: dark)",
                    "scheme": "slate",
                    "primary": "blue grey",
                    "toggle": {"icon": "material/brightness-4", "name": "Switch to light mode"},
                },
            ],
            "features": [
                "search.highlight",
                "search.suggest",
                "content.code.copy",
                "content.code.annotate",
                "navigation.indexes",
                "navigation.footer",
                "navigation.sections",
                "navigation.expand",
                "toc.follow",
            ],
        },
        "markdown_extensions": [
            "admonition",
            "attr_list",
            "pymdownx.details",
            {"pymdownx.highlight": {"pygments_lang_class": True}},
            "pymdownx.inlinehilite",
            "pymdownx.superfences",
            {"pymdownx.tabbed": {"alternate_style": True}},
            {"toc": {"permalink": "#"}},
        ],
        "plugins": ["search"],
    }


def find_leaf_modules(src_dir: Path, package_name: str = "zen_api", *, include_modules: bool = False) -> list[str]:
    zen_api_root = src_dir / package_name
    if not zen_api_root.is_dir():
        raise FileNotFoundError(f"ZEN API Python source directory not found: {zen_api_root}")

    leaf_modules: list[str] = []
    for init_file in sorted(zen_api_root.rglob("__init__.py")):
        package_dir = init_file.parent
        if package_dir == zen_api_root:
            continue

        has_child_packages = any((child / "__init__.py").exists() for child in package_dir.iterdir() if child.is_dir())
        if not has_child_packages:
            leaf_modules.append(".".join(package_dir.relative_to(src_dir).parts))

    if include_modules:
        leaf_modules.extend(
            ".".join(module.relative_to(src_dir).with_suffix("").parts)
            for module in sorted(zen_api_root.rglob("*.py"))
            if module.name != "__init__.py"
        )

    if not leaf_modules:
        raise RuntimeError(f"No leaf modules found in {zen_api_root}")

    return sorted(set(leaf_modules))


def generate_reference_pages(
    src_dir: Path, docs_dir: Path, package_name: str = "zen_api", *, include_modules: bool = False
) -> list[dict]:
    domains: dict[str, list[tuple[str, str]]] = {}

    prefix = "reference" if package_name == "zen_api" else f"reference/{package_name}"
    for module in find_leaf_modules(src_dir, package_name, include_modules=include_modules):
        parts = module.split(".")
        domain = parts[1]
        label = ".".join(parts[2:]) if len(parts) > 2 else domain
        md_path = prefix + "/" + "/".join(parts[1:]) + ".md"
        target_path = docs_dir / md_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(f"# {'.'.join(parts[1:])}\n\n::: {module}\n", encoding="utf-8")
        domains.setdefault(domain, []).append((label, md_path))

    nav_items: list[dict] = []
    for domain in sorted(domains):
        entries = sorted(domains[domain])
        display_name = DOMAIN_LABELS.get(domain, domain.title())
        if len(entries) == 1:
            nav_items.append({display_name: entries[0][1]})
        else:
            nav_items.append({display_name: [{label: path} for label, path in entries]})

    return nav_items


def proto_page(name: str) -> str:
    return "proto/" + PurePosixPath(name).with_suffix(".md").as_posix()


def proto_anchor(name: str) -> str:
    return "proto-" + name.lstrip(".").replace(".", "-")


def table_text(text: str) -> str:
    return html.escape(text).replace("|", "\\|").replace("\n", "<br>")


class ProtoRenderer:
    """Render compiled protocol definitions with comments and linked types."""

    def __init__(self, files: dict) -> None:
        self.symbols: dict[str, str] = {}
        self.maps: dict = {}
        self.comments: dict = {}
        for name, descriptor in files.items():
            self.comments[name] = {
                tuple(location.path): "\n\n".join(
                    value.strip() for value in (location.leading_comments, location.trailing_comments) if value.strip()
                )
                for location in descriptor.source_code_info.location
            }
            for message in descriptor.message_type:
                self.index_message(message, descriptor.package, proto_page(name))
            for symbol in [*descriptor.enum_type, *descriptor.service]:
                self.symbols[f"{descriptor.package}.{symbol.name}".lstrip(".")] = proto_page(name)

    def index_message(self, message, parent: str, page: str) -> None:
        name = f"{parent}.{message.name}".lstrip(".")
        if message.options.map_entry:
            self.maps["." + name] = message
            return
        self.symbols[name] = page
        for nested in message.nested_type:
            self.index_message(nested, name, page)
        for enum in message.enum_type:
            self.symbols[f"{name}.{enum.name}"] = page

    def comment(self, file, path: tuple) -> str:
        return self.comments[file.name].get(path, "")

    def type_link(self, name: str, page: str) -> str:
        name = name.lstrip(".")
        if name not in self.symbols:
            return f"`{name}`"
        target = posixpath.relpath(self.symbols[name], posixpath.dirname(page))
        return f"[{name}]({target}#{proto_anchor(name)})"

    def field_type(self, field, page: str) -> str:
        if field.type_name in self.maps:
            key, value = self.maps[field.type_name].field
            return f"map&lt;{self.field_type(key, page)}, {self.field_type(value, page)}&gt;"
        if field.type_name:
            return self.type_link(field.type_name, page)
        return f"`{field.type.name.removeprefix('TYPE_').lower()}`"

    def render_enum(self, enum, parent: str, file, path: tuple, level: int) -> list[str]:
        name = f"{parent}.{enum.name}".lstrip(".")
        lines = [
            f"{'#' * level} Enum `{enum.name}` {{ #{proto_anchor(name)} }}",
            "",
            self.comment(file, path),
            "",
            "| Name | Number | Description |",
            "| --- | --- | --- |",
        ]
        for index, value in enumerate(enum.value):
            lines.append(f"| `{value.name}` | {value.number} | {table_text(self.comment(file, path + (2, index)))} |")
        return [*lines, ""]

    def render_message(self, message, parent: str, file, path: tuple, level: int = 2) -> list[str]:
        if message.options.map_entry:
            return []
        name = f"{parent}.{message.name}".lstrip(".")
        lines = [
            f"{'#' * level} Message `{message.name}` {{ #{proto_anchor(name)} }}",
            "",
            self.comment(file, path),
            "",
        ]
        if message.field:
            lines.extend(["| Field | Number | Type | Presence | Description |", "| --- | --- | --- | --- | --- |"])
            for index, field in enumerate(message.field):
                presence = "repeated" if int(field.label) == 3 else "required" if int(field.label) == 2 else "singular"
                if field.proto3_optional:
                    presence = "optional"
                elif field.is_set("oneof_index"):
                    presence = f"oneof `{message.oneof_decl[field.oneof_index].name}`"
                description = self.comment(file, path + (2, index))
                if field.default_value:
                    description += f"\nDefault: {field.default_value}"
                lines.append(
                    f"| `{field.name}` | {field.number} | {self.field_type(field, proto_page(file.name))} | "
                    f"{presence} | {table_text(description)} |"
                )
            lines.append("")
        for index, enum in enumerate(message.enum_type):
            lines.extend(self.render_enum(enum, name, file, path + (4, index), level + 1))
        for index, nested in enumerate(message.nested_type):
            lines.extend(self.render_message(nested, name, file, path + (3, index), level + 1))
        return lines

    def render(self, file, version: str) -> str:
        source_link = posixpath.relpath("proto/source/" + file.name, posixpath.dirname(proto_page(file.name)))
        lines = [
            f"# {file.name}",
            "",
            f"Version: **{version}**",
            "",
            f"Package: `{file.package}`",
            "",
            f"[Download proto source]({source_link})",
            "",
        ]
        for service_index, service in enumerate(file.service):
            name = f"{file.package}.{service.name}".lstrip(".")
            path = (6, service_index)
            lines.extend([f"## Service `{service.name}` {{ #{proto_anchor(name)} }}", "", self.comment(file, path), ""])
            for index, method in enumerate(service.method):
                input_type = ("stream " if method.client_streaming else "") + method.input_type.lstrip(".")
                output_type = ("stream " if method.server_streaming else "") + method.output_type.lstrip(".")
                lines.extend(
                    [
                        f"### {method.name} {{ #{proto_anchor(name + '.' + method.name)} }}",
                        "",
                        self.comment(file, path + (2, index)),
                        "",
                        "```protobuf",
                        f"rpc {method.name} ({input_type}) returns ({output_type});",
                        "```",
                        "",
                        f"Request: {self.type_link(method.input_type, proto_page(file.name))}",
                        "",
                        f"Response: {self.type_link(method.output_type, proto_page(file.name))}",
                        "",
                    ]
                )
        for index, message in enumerate(file.message_type):
            lines.extend(self.render_message(message, file.package, file, (4, index)))
        for index, enum in enumerate(file.enum_type):
            lines.extend(self.render_enum(enum, file.package, file, (5, index), 2))
        return "\n".join(lines)


def generate_proto_pages(proto_dir: Path, docs_dir: Path, version: str, protoc: str) -> list[dict]:
    """Compile the selected source version and publish its reference and originals."""
    sources = sorted(path.relative_to(proto_dir).as_posix() for path in proto_dir.rglob("*.proto"))
    if not sources:
        raise FileNotFoundError(f"No proto sources found in {proto_dir}")
    descriptor_path = docs_dir.parent / "proto-descriptor.pb"
    subprocess.run(
        [
            protoc,
            f"--proto_path={proto_dir.resolve()}",
            f"--descriptor_set_out={descriptor_path.resolve()}",
            "--include_imports",
            "--include_source_info",
            "--experimental_allow_proto3_optional",
            *sources,
        ],
        check=True,
    )
    descriptor_set = FileDescriptorSet().parse(descriptor_path.read_bytes())
    descriptors = {descriptor.name: descriptor for descriptor in descriptor_set.file}
    files = {name: descriptors[name] for name in sources}
    renderer = ProtoRenderer(files)
    domains: dict[str, list[dict]] = {}
    overview = ["# Protocol Buffer Reference", "", f"Protocol definitions for ZEN API **{version}**.", ""]
    for name, descriptor in files.items():
        page = proto_page(name)
        destination = docs_dir / page
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(renderer.render(descriptor, version), encoding="utf-8")
        source = docs_dir / "proto" / "source" / name
        source.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(proto_dir / name, source)
        parts = PurePosixPath(name).with_suffix("").parts
        if parts[0] == "zen_api":
            parts = parts[1:]
        domains.setdefault(parts[0], []).append({".".join(parts[1:]) or parts[0]: page})
        overview.append(f"- [{name}]({posixpath.relpath(page, 'proto')})")
    (docs_dir / "proto" / "index.md").write_text("\n".join(overview) + "\n", encoding="utf-8")
    return [{"Overview": "proto/index.md"}] + [
        {DOMAIN_LABELS.get(domain, domain.title()): entries} for domain, entries in sorted(domains.items())
    ]


def write_yaml(path: Path, config: dict) -> None:
    path.write_text(
        yaml.dump(config, default_flow_style=False, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def build_landing_page(build_dir: Path, site_dir: Path, versions: list[str]) -> None:
    docs_dir = build_dir / "landing" / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    version_links = "\n".join(f"- [ZEN API {version}]({ZENAPI_PAGES_PATH}/{version}/)" for version in versions)
    (docs_dir / "index.md").write_text(
        f"# ZEN API Documentation\n\nSelect one of the published ZEN API documentation versions:\n\n{version_links}\n",
        encoding="utf-8",
    )

    config = mkdocs_material_config(
        site_name="ZEN API Documentation",
        site_url="https://zeiss-microscopy.github.io/OAD/",
        docs_dir=docs_dir,
        site_dir=site_dir,
    )
    # The version folders are generated by separate MkDocs builds after the
    # landing page build, so strict link validation would fail here.
    config["strict"] = False
    config["nav"] = [{"Home": "index.md"}]

    config_path = build_dir / "landing" / "mkdocs.yml"
    write_yaml(config_path, config)
    run_mkdocs(config_path, strict=False)


def build_version_page(repo_root: Path, build_dir: Path, site_dir: Path, version: str, protoc: str = "protoc") -> None:
    package_dir = repo_root / "ZEN-API" / "python_packages" / f"zen_api-{version}"
    if not package_dir.is_dir():
        raise FileNotFoundError(f"Package directory not found: {package_dir}")

    src_dir = package_dir / "src"
    version_build_dir = build_dir / version
    docs_dir = version_build_dir / "docs"
    version_site_dir = site_dir / ZENAPI_PAGES_PATH / version
    docs_dir.mkdir(parents=True, exist_ok=True)

    utils_dir = repo_root / "ZEN-API" / "zen_api_utils_package"
    with (utils_dir / "pyproject.toml").open("rb") as metadata:
        utils_project = tomllib.load(metadata)["project"]
    with (package_dir / "pyproject.toml").open("rb") as metadata:
        api_project = tomllib.load(metadata)["project"]
    utils_version = utils_project["version"]
    shutil.copytree(utils_dir / "mkdocs_docs", docs_dir / "guides" / "zen_api_utils", dirs_exist_ok=True)

    (docs_dir / "index.md").write_text(
        textwrap.dedent(f"""
            # ZEN API

            Python wrappers for the ZEN API, enabling programmatic control of ZEISS microscopy software via gRPC.

            | Package | Documented version |
            | --- | --- |
            | `zen_api` | `{version}` |
            | `zen_api_utils` | `{utils_version}` |

            This site pairs the selected API sources with the utility sources from this repository checkout.
            The packages are independently versioned.

            See the [utilities guide](guides/zen_api_utils/index.md), Python API references,
            and [protocol definitions](proto/index.md).

            ## Installation

            This package is not available on PyPI. Install from the wheel file:

            ```bash
            pip install zen_api-{version}-py3-none-any.whl
            pip install zen_api_utils-{utils_version}-py3-none-any.whl
            ```

            ## Requirements

            - API Python requirement: `{api_project['requires-python']}`
            - Utilities Python requirement: `{utils_project['requires-python']}`
            - betterproto == 2.0.0b7

            ## API Domains

            The ZEN API is organized into several domains:

            | Domain          | Description                                                                |
            | --------------- | -------------------------------------------------------------------------- |
            | **acquisition** | Experiment and image acquisition services                                  |
            | **application** | Application-level composition services                                     |
            | **common**      | Shared data types and enumerations                                         |
            | **em**          | Electron microscopy hardware and workflow services                         |
            | **hardware**    | Microscope hardware control (stages, axes)                                 |
            | **lm**          | Light microscopy acquisition, hardware, live scan, and slide scan services |
            | **workflows**   | Automated workflow and job management services                             |

            ## Quick Start

            ```python
            from zen_api.acquisition.v1beta import ExperimentServiceStub

            # Connect to ZEN API server
            # (requires ZEN software running with API server enabled)
            ```

            ## License

            Apache License 2.0 — see [LICENSE](https://github.com/zeiss-microscopy/OAD/blob/master/LICENSE) for details.

            Copyright © Carl Zeiss Microscopy GmbH.
            """).lstrip(),
        encoding="utf-8",
    )

    nav_items = generate_reference_pages(src_dir, docs_dir)
    utils_src = utils_dir / "src"
    utils_nav = generate_reference_pages(utils_src, docs_dir, "zen_api_utils", include_modules=True)
    proto_nav = generate_proto_pages(
        repo_root / "ZEN-API" / "protofiles" / f"proto_{version}", docs_dir, version, protoc
    )
    config = mkdocs_material_config(
        site_name=f"ZEN API {version}",
        site_url=f"https://zeiss-microscopy.github.io/OAD/{ZENAPI_PAGES_PATH}/{version}/",
        docs_dir=docs_dir,
        site_dir=version_site_dir,
    )
    config["plugins"] = [
        "search",
        {"autorefs": {"resolve_closest": True}},
        {
            "mkdocstrings": {
                "handlers": {
                    "python": {
                        "paths": [str(src_dir.resolve()), str(utils_src.resolve())],
                        "options": {
                            "docstring_style": "google",
                            "docstring_section_style": "list",
                            "show_root_heading": True,
                            "show_symbol_type_heading": True,
                            "show_symbol_type_toc": True,
                            "show_signature_annotations": True,
                            "separate_signature": True,
                            "merge_init_into_class": True,
                            "members_order": "source",
                            "filters": ["!^_"],
                            "show_source": False,
                            "heading_level": 2,
                            "summary": True,
                        },
                    }
                }
            }
        },
    ]
    config["site_description"] = "ZEN API services, protocol definitions, and workflow utilities"
    config["extra"] = {"documented_versions": {"zen_api": version, "zen_api_utils": utils_version}}
    config["nav"] = [
        {"Home": "index.md"},
        {"Utilities Guide": "guides/zen_api_utils/index.md"},
        {"Python API Reference": [{"zen_api": nav_items}, {"zen_api_utils": utils_nav}]},
        {"Protocol Buffer Reference": proto_nav},
    ]

    config_path = version_build_dir / "mkdocs.yml"
    write_yaml(config_path, config)
    run_mkdocs(config_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build versioned ZEN API docs for GitHub Pages.")
    parser.add_argument("--versions", nargs="+", required=True, help="ZEN API package versions to publish.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Repository root.")
    parser.add_argument("--build-dir", type=Path, default=Path("_zen_api_pages"), help="Temporary build directory.")
    parser.add_argument("--site-dir", type=Path, default=Path("site"), help="GitHub Pages output directory.")
    parser.add_argument("--protoc", default="protoc", help="Protocol Buffers compiler executable.")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    build_dir = (repo_root / args.build_dir).resolve()
    site_dir = (repo_root / args.site_dir).resolve()

    for version in args.versions:
        if not re.fullmatch(r"[0-9]{4}\.[0-9]{2}\.[0-9]+", version):
            parser.error(f"Invalid API version: {version!r}; expected YYYY.MM.PATCH")
        api_root = repo_root / "ZEN-API"
        for required in (
            api_root / "python_packages" / f"zen_api-{version}" / "src" / "zen_api",
            api_root / "protofiles" / f"proto_{version}",
        ):
            if not required.is_dir():
                parser.error(f"Required documentation input not found: {required}")
    if shutil.which(args.protoc) is None:
        parser.error(f"Protocol Buffers compiler not found: {args.protoc}")

    if build_dir.exists():
        shutil.rmtree(build_dir)
    if site_dir.exists():
        shutil.rmtree(site_dir)

    build_dir.mkdir(parents=True, exist_ok=True)
    site_dir.mkdir(parents=True, exist_ok=True)

    build_landing_page(build_dir, site_dir, args.versions)
    for version in args.versions:
        build_version_page(repo_root, build_dir, site_dir, version, args.protoc)


if __name__ == "__main__":
    main()
