
# karrio.allied_express_local

This package is a Allied Express Local extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.allied_express_local
```

## Usage

```python
import karrio
from karrio.mappers.allied_express_local.settings import Settings


# Initialize a carrier gateway
allied_express_local = karrio.gateway["allied_express_local"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
