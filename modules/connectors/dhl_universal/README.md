# karrio.dhl_universal

This package is a DHL Universal Tracking extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dhl_universal
```

## Usage

```python
import karrio
from karrio.mappers.dhl_universal.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["dhl_universal"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
