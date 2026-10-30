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
python -m pip install build twine
.\zen_api_utils\build_package.ps1
```

The wheel and source distribution are written to
`zen_api_utils\dist`. Build them once per utility release; the same artifacts
support the API range declared in `pyproject.toml`.

The builder only checks that `build` and `twine` are available, builds the
distributions, and validates them with Twine. It does not need a generated API
checkout, select an API version, install packages, run tests, or generate docs.
The former `-Test` and `-ZenApiPackagePath` options are no longer accepted.

Build isolation downloads Hatchling using your pip configuration. If a private
feed returns HTTP 401, either repair its authentication or explicitly use PyPI
for this build, where your package-source policy permits it:

```powershell
.\zen_api_utils\build_package.ps1 -BuildIndexUrl https://pypi.org/simple
```

`-BuildIndexUrl` accepts an HTTPS index URL without embedded credentials. It
temporarily bypasses pip configuration files and any extra index; the original
environment settings are restored even if the build fails. It does not change
pip configuration files or the installed project packages. Without this option,
the builder continues to use your configured package sources.

## Testing

Testing is separate from packaging. With the intended `zen_api` wheel and test
dependencies installed in the active environment, run from the repository root:

```powershell
python -m pytest zen_api_utils/tests
```

CI tests each supported API release separately. These test runs do not require
separate API-specific utility artifacts.

## Documentation

The shared MkDocs generator builds one site with separate `zen_api` and
`zen_api_utils` references, protocol definitions, and both package versions.
The utility guide lives under `mkdocs_docs`. The API build workflow and CI
generate the site under the selected API package's `docs/mkdocs_site`; the
utility builder does not generate documentation. The API output must include
`proto-descriptor.pb` from wrapper generation and have a matching versioned
proto directory. Documentation builds run MkDocs in strict mode and use the
repository's `packaging/requirements.txt`. See `Instructions.md` for standalone
documentation generation with an explicitly selected API release.

CI tests utilities against the matching API wheel before uploading and optionally
publishing the combined `zen_api-<version>-mkdocs-site` artifact to
[the versioned documentation site](https://sebi06.github.io/ZEN_API/).
The two Python distributions and their versions remain separate. Utilities
remain at `0.1.0`; an API release such as `2026.7.1` does not change that version.
The project directory, distribution, and import package are all named
`zen_api_utils`. The import package lives in `zen_api_utils/src/zen_api_utils`.

The dependency `zen_api>=2026.5.1,<=2026.11.1` expresses the supported API range.
CI tests the utilities with API `2026.5.1`, `2026.7.1`, and `2026.11.1`, and with
the API built by the current workflow. API documentation builds and CI reject
selected APIs outside that range before overwriting API output. Extend the range and
the test matrix only after testing another API release. These checks do not
replace hardware integration testing. New API versions and artifact names
use unpadded components, for example `2026.7.1`, never `2026.07.1`.

## Runtime Compatibility Diagnostics

`zen_api_utils.compatibility` provides `api_capabilities`, `api_operation`, and
`ZenApiCompatibilityError`. Generated API import blocks report missing modules
or symbols with the affected feature, installed distribution versions, and a
compatible-wheel installation action. Source checkouts without installed
metadata report the versions as unknown rather than hiding the original error.

`api_capabilities` also checks required message fields or callable client methods
before use. Dataclass fields are checked without reading their values. Required
RPCs that return gRPC `UNIMPLEMENTED` are translated into a compatibility error
with a ZEN server upgrade action; original import and RPC errors are retained
as the exception cause. Other RPC statuses, cancellation, and programming errors
are not reclassified.

For new utility features, guard only the imports or RPC operation that needs the
capability, rather than disabling the entire package:

```python
from zen_api_utils.compatibility import api_capabilities

with api_capabilities("Experiment export", service, methods=("export",)):
    response = await service.export(request)
```

For async function decorators, use `api_operation("Feature name", ...)` instead
of decorating with the synchronous context manager. Both guards preserve errors
deliberately handled by the wrapped operation. For example, the streaming
pipeline still falls back to exported metadata if live status is unavailable;
legacy helpers that return a failure status retain that contract and can include
the compatibility diagnostic in their logs or returned error details.

These are presence and failure diagnostics, not proof of compatible signatures,
wire formats, or server behavior. Keep the dependency bounds and CI matrix, lock
exact tested package versions for deployed microscopes, and test the connected
ZEN version in simulation before hardware use. Rebuild the utility wheel to ship
these changes; existing installed wheels are not modified automatically.

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
