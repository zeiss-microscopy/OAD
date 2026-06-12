"""Build versioned ZEN API MkDocs Material documentation for GitHub Pages."""

from __future__ import annotations

import argparse
import subprocess
import sys
import textwrap
from pathlib import Path

import yaml

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


def find_leaf_modules(src_dir: Path) -> list[str]:
    zen_api_root = src_dir / "zen_api"
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

    if not leaf_modules:
        raise RuntimeError(f"No leaf modules found in {zen_api_root}")

    return leaf_modules


def generate_reference_pages(src_dir: Path, docs_dir: Path) -> list[dict]:
    domains: dict[str, list[tuple[str, str]]] = {}

    for module in find_leaf_modules(src_dir):
        parts = module.split(".")
        domain = parts[1]
        label = ".".join(parts[2:]) if len(parts) > 2 else domain
        md_path = "reference/" + "/".join(parts[1:]) + ".md"
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


def build_version_page(repo_root: Path, build_dir: Path, site_dir: Path, version: str) -> None:
    package_dir = repo_root / "ZEN-API" / "python_package" / f"zen_api-{version}"
    if not package_dir.is_dir():
        raise FileNotFoundError(f"Package directory not found: {package_dir}")

    src_dir = package_dir / "src"
    version_build_dir = build_dir / version
    docs_dir = version_build_dir / "docs"
    version_site_dir = site_dir / ZENAPI_PAGES_PATH / version
    docs_dir.mkdir(parents=True, exist_ok=True)

    (docs_dir / "index.md").write_text(
        textwrap.dedent(f"""
            # ZEN API

            Python wrappers for the ZEN API, enabling programmatic control of ZEISS microscopy software via gRPC.

            ## Installation

            This package is not available on PyPI. Install from the wheel file:

            ```bash
            pip install zen_api-{version}-py3-none-any.whl
            ```

            ## Requirements

            - Python >= 3.10
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
                        "paths": [str(src_dir.resolve())],
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
    config["extra"] = {"version": {"provider": "mike"}}
    config["nav"] = [{"Home": "index.md"}, {"API Reference": nav_items}]

    config_path = version_build_dir / "mkdocs.yml"
    write_yaml(config_path, config)
    run_mkdocs(config_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build versioned ZEN API docs for GitHub Pages.")
    parser.add_argument("--versions", nargs="+", required=True, help="ZEN API package versions to publish.")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Repository root.")
    parser.add_argument("--build-dir", type=Path, default=Path("_zen_api_pages"), help="Temporary build directory.")
    parser.add_argument("--site-dir", type=Path, default=Path("site"), help="GitHub Pages output directory.")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    build_dir = (repo_root / args.build_dir).resolve()
    site_dir = (repo_root / args.site_dir).resolve()

    if build_dir.exists():
        import shutil

        shutil.rmtree(build_dir)
    if site_dir.exists():
        import shutil

        shutil.rmtree(site_dir)

    build_dir.mkdir(parents=True, exist_ok=True)
    site_dir.mkdir(parents=True, exist_ok=True)

    build_landing_page(build_dir, site_dir, args.versions)
    for version in args.versions:
        build_version_page(repo_root, build_dir, site_dir, version)


if __name__ == "__main__":
    main()
