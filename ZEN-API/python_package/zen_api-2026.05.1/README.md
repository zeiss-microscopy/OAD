# ZEN API

This package provides Python wrappers for various ZEN API services, enabling programmatic control of ZEISS microscopy software.

## Installation

This package is not available on PyPI. Install it from the wheel file:

```bash
pip install zen_api-<version>-py3-none-any.whl
```

Or install directly from the wheel path:

```bash
pip install "/path/to/zen_api-<version>-py3-none-any.whl"
```

## Requirements

- Python >= 3.9
- betterproto == 2.0.0b7

## Usage

The ZEN API package provides gRPC-based Python classes for interacting with ZEN microscopy software. The API is organized into several domains:

- **acquisition**: Experiment and image acquisition services
- **hardware**: Microscope hardware control (stages, axes)
- **workflows**: Automated workflow services
- **application**: Application-level services
- **common**: Shared data types
- **lm**: Light microscopy specific services
- **em**: Electron microscopy specific services

### Example

```python
from zen_api.acquisition.v1beta import ExperimentServiceStub

# Connect to ZEN API server
# (requires ZEN software running with API server enabled)
```

## Documentation

For detailed API documentation, please refer to the ZEN software documentation or contact Carl Zeiss Microscopy GmbH.

## License

Copyright 2025 Carl Zeiss Microscopy GmbH

Licensed under the Apache License, Version 2.0. See [LICENSE.txt](LICENSE.txt) for details.

## Contact

For more information about ZEN microscopy software, visit [https://www.zeiss.com/microscopy](https://www.zeiss.com/microscopy)