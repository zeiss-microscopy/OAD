# ZEN API Utilities

Reusable, headless helpers for applications built on the generated `zen_api`
protobuf and gRPC package.

## Documentation Versions

This site's version dropdown selects `zen_api_utils` releases independently of
the [ZEN API documentation](https://zeiss-microscopy.github.io/OAD/).
The **Documented Version** page identifies the current utility snapshot.
Install an API version within the utility package's declared dependency range;
the two package version numbers do not need to match.

## Contents

The API reference includes connection and logging helpers, experiment and
acquisition-plan parsing, hardware helpers, stage and sample-carrier models,
workflow helpers, TCP/IP control helpers, and streaming utilities.

## Installation

Install a matching local `zen_api` wheel first, then install this package:

```powershell
pip install zen_api-<version>-py3-none-any.whl
pip install zen_api_utils-<version>-py3-none-any.whl
```

OME-Zarr support is optional:

```powershell
pip install "zen_api_utils[omezarr]"
```