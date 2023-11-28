# karrio.dhl_express

This package is a DHL Express extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dhl_express
```

## Usage

```python
import karrio
from karrio.mappers.dhl_express.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["dhl_express"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
