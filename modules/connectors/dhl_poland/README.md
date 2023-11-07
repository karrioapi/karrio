# karrio.dhl_poland

This package is a DHL Parcel Poland extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dhl_poland
```

## Usage

```python
import karrio
from karrio.mappers.dhl_poland.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["dhl_poland"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
