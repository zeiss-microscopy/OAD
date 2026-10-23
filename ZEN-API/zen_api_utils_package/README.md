# zen_api_utils

Reusable, headless helpers for applications built on the generated `zen_api`
protobuf and gRPC package.

## Scope

- ZEN API connection and logging helpers
- Experiment metadata and CZEXP acquisition-plan parsing
- Camera, changer, filter, objective, and stage helpers
- Sample-carrier and tile-position models
- Workflow service helpers
- Legacy TCP/IP control helpers
- Headless scene geometry primitives

This package contains application-side utilities and is separate from the
generated `zen_api` package. OME-Zarr support is included under
`zen_api_utils.streaming.pipeline` and `zen_api_utils.streaming.omezarr` and is
optional.

## Installation

Both `zen_api` and `zen_api_utils` support Python 3.12-3.15
(`>=3.12,<3.16`). Python versions below 3.12 are not supported.

Install a generated `zen_api` wheel first, then install this package:

```powershell
pip install .
```

For OME-Zarr output and post-processing:

```powershell
pip install ".[omezarr]"
```

For development:

```powershell
pip install ".[dev]"
```

## Build distributions

From the repository root, run:

```powershell
.\zen_api_utils_package\build_package.ps1
```

The wheel and source distribution are written to
`zen_api_utils_package\dist`.

To build the local generated `zen_api` package, install it, and run the
utility package tests as well:

```powershell
.\zen_api_utils_package\build_package.ps1 -Test
```

Both builds and documentation default to the stable package directory
`python_packages/zen_api-2026.11.1`; a newer development folder is not selected
automatically. The test mode does not require `zen_api` to be published on PyPI.
Pass `-ZenApiPackagePath <directory>` to intentionally select another local
package for both its dependency build and documentation imports.

## Documentation

The shared MkDocs generator builds one site with separate `zen_api` and
`zen_api_utils` references, protocol definitions, and both package versions.
The utility guide lives under `mkdocs_docs`; both local builders write the site
under the selected API package's `docs/mkdocs_site`. The API output must include
`proto-descriptor.pb` from wrapper generation and have a matching versioned
proto directory. The build script runs MkDocs in strict mode. Install the repository's
`packaging/requirements.txt` and `twine` before running the full builder.

CI tests utilities against the matching API wheel before uploading and optionally
publishing the combined `zen_api-<version>-mkdocs-site` artifact to
[the versioned documentation site](https://sebi06.github.io/ZEN_API/).
The two Python distributions and their versions remain separate.

To install all optional dependencies:

```powershell
pip install ".[all]"
```

## Migration

The examples now use this package directly, while the established root module
names remain available for the general-purpose utilities:

```python
from zen_api_utils.experiment_acquisition import ExperimentAcquisition
from zen_api_utils.misc import initialize_zenapi
from zen_api_utils.streaming import decode_pixel_payload
from zen_api_utils.streaming.pipeline import stream_to_omezarr_with_config
```

Streaming and OME-Zarr helpers live under the `streaming` subpackage so they
share the same acquisition and connection utilities without requiring a
second distribution.

The reusable streaming pipeline is also available as a console command after
installation:

```powershell
zenapi-stream2omezarr --help
```

## Acquisition integrity

Both writers load and export the selected experiment before sending channel
subscriptions. Exported dimensions replace INI dimension hints; live status is
queried for the pinned experiment, never for an arbitrary active experiment.
If live and exported channel counts disagree, acquisition fails rather than
silently producing a subset of channels.

Monitoring requests are sent before a script-started acquisition begins, and
only frames with its experiment ID are accepted. For manually started runs,
the first nonempty frame experiment ID pins the run. Other experiments cannot
extend its inactivity timeout or contribute to completion.

Both entry points raise
`zen_api_utils.streaming.pipeline.IncompleteAcquisitionError` on incomplete
acquisitions, including runs that receive no frames. Partial stores retain
their source tiles and include `acquisition_status.json` with expected and
received counts and missing T/S/M/C/Z coordinates. When no store was created,
the report is a sibling named `<store>.acquisition_status.json`. The exception
provides `zarr_path`, `report_path`, `received_frames`, and `expected_frames`.
Missing planes are zero-filled only to preserve the partial array layout;
they are explicitly marked as missing in the report. Failed acquisitions
must not be opened automatically or used for pyramid generation.

Library imports do not configure or remove application logging handlers.
`set_logging()` returns the shared Loguru logger without changing its sinks.
The legacy TCP acquisition example runs only when explicitly launched as
`python -m zen_api_utils.zen_tcpip_interface`, never on import.
