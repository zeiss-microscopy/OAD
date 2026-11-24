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

For optional pandas position tables:

```powershell
pip install ".[dataframe]"
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
The two Python distributions and their versions remain separate. By default,
the utility version comes from `pyproject.toml`; an API release does not change it.
Manual CI runs can set the optional `utils_version` input to override that version
for the run. The same version is used for testing, distributions, artifact names
and documentation. This changes only CI checkouts, not committed metadata or the
source revision being built. Tag builds use the utility version committed in TOML.
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

### Offline experiment positions

#### Map stage XY coordinates using an empty carrier experiment

```python
from zen_api_utils.extract_czexp_plan import load_carrier_geometry

carrier = load_carrier_geometry("empty_W96.czexp")
assignments = carrier.assign_positions([(4500.0, 8500.0), (13500.0, 8500.0)])
for assignment in assignments:
    if assignment is not None:
        print(assignment.well_id, assignment.well_row, assignment.well_column)
```

The reference experiment needs a configured carrier, not acquisition positions
or well containers. `carrier_geometry_from_xml(xml)` also accepts a ZEN XML
export. `block_index` selects an ordinal in the active-block list, defaulting to
the first; only its active RegionsSetup is used.

Boundary conditions are documented on `CarrierGeometry` and its methods:

- Absolute XY values must be in micrometers in the reference experiment's
  coordinate frame, with the same origin, calibration and plate placement.
- Mapping considers every physical well in the template, independent of
  acquisition selection. Results preserve input order and duplicates.
- Only regular, centered, unrotated rectangular grids with unswitched and
  noninverted axes and a zero TopLeft reference are supported.
- Rectangle edges are included without snapping or extra tolerance. Points in
  gaps or outside the plate return `None`; non-finite coordinates raise
  `ValueError`. Touching or overlapping wells are rejected as ambiguous.
- Missing/unsupported geometry raises `UnsupportedCarrierGeometryError` (a
  `ValueError`). This differs from automatic plan well inference, which logs
  unsupported geometry and retains positions without inferred wells.
- Assignment describes a point, not containment of an image/tile footprint.
  Z coordinates, stage drift and physical placement accuracy are not evaluated.

The [experiment parser](src/zen_api_utils/extract_czexp_plan.py) defines the
shared index and unit convention for acquisition plans, typed positions, and
tables. No running ZEN instance is required:

```python
from zen_api_utils.extract_czexp_plan import (
    load_experiment_positions,
    load_experiment_positions_dataframe,
    positions_from_plan,
)
from zen_api_utils.experiment_acquisition import ExperimentAcquisition

positions = load_experiment_positions("experiment.czexp")
for position in positions:
    print(position.well_id, position.x, position.y, position.z)
    if position.tile_region is not None:
        print(position.tile_region.width_um, position.tile_region.height_um)

table = load_experiment_positions_dataframe("experiment.czexp")  # dataframe extra
acquisition = ExperimentAcquisition.from_czexp("experiment.czexp")
assert acquisition.positions == tuple(positions)
```

`Position` and `TileRegion` are immutable offline models, distinct from the
meter-based API models in `tiles_positions`. A region position describes the
region center, not each camera tile. Rectangular contour dimensions must be
finite and positive; invalid dimensions raise `ValueError`. Other contours
retain their type without shape-specific geometry. Missing coordinates and
well assignments remain `None`; acquisition code must validate coordinates
before moving hardware. No fields produces an empty list or a typed empty
table. Table columns use pandas nullable dtypes and `pd.NA`.

Use `positions_from_plan(plan)` or `positions_to_dataframe(positions)` to avoid
re-reading an already parsed experiment. `positions_from_plan(..., block_index=n)`
selects the nth active block; each position retains the original XML block
index. `ExperimentAcquisition.from_xml(xml)` uses the same parser for API
exports and exposes positions as typed objects.

**Breaking plan migration:** schema `experimental.czexp-acquisition-plan/0.2`
replaces `0.1`. Re-extract saved plans from their CZEXP source; the typed adapter
and CZMBI exporter reject legacy schemas rather than reinterpret their indices.
CZMBI row/column/field values and OME-Zarr well labels are converted at export
boundaries, so their external conventions are unchanged. Existing consumers of
`ExperimentAcquisition.positions` should use attributes, or `position.to_record()`
for a flat dictionary with `stage_x_um`, `stage_y_um`, and `stage_z_um`.
Rebuild/install the utility wheel before using these APIs from another project.

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

## Utility behavior

- Both streaming writers renew the inactivity timeout after each newly accepted
  frame. Acquisition may run longer than the timeout; foreign and duplicate
  frames do not extend it.
- TCP command runners stop at the first failed or timed-out acknowledgement and
  raise `RuntimeError` with the command and response. Connections are still
  closed on failure; no successful output path is returned.
- `workflow.run_job()` validates all requested resource names and supported value
  types before changing parameters or running the job. Unknown names raise
  `ValueError`; unsupported types raise `TypeError`. Loading the template and
  querying its resource IDs still happen before resource-name validation.
- `stage.PosXYZ` stores coordinates in meters. Its read-only `x_micron`,
  `y_micron`, and `z_micron` properties always reflect the current meter values.
  Update the meter fields to change a position. `stage.move_xyz()` leaves the
  requested position unchanged and returns a new position with the actual
  coordinates.
- `experiment.show_track_info_LM()` returns a `Tracks` dataclass with `info` and
  `number`, not a generated `TrackInfo` message.
- Both changer entry points use the same best-effort movement implementation.
  Their return value is still an ordinary dictionary, now described by
  `changers.ChangerResults` and `changers.ChangerMove` type annotations. Requested
  inventories are queried before movements; failures are reported without
  stopping independent changers, and cancellation propagates.
- Camera helpers preserve service order and exposure settings, and truncate
  floating-point frame coordinates and sizes to integer pixels.
- Streaming uses shared frame-validation, receiver and OME-Zarr helpers.
  `streaming.pipeline.generate_omezarr_pyramids()` remains available and appends
  pyramid levels without rewriting level 0.
