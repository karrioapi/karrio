
# karrio.allied_express

This package is a Allied Express extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.allied_express
```

## Usage

```python
import karrio
from karrio.mappers.allied_express.settings import Settings


# Initialize a carrier gateway
allied_express = karrio.gateway["allied_express"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
