
# karrio.dhl_parcel_de

This package is a DHL Parcel DE extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dhl_parcel_de
```

## Usage

```python
import karrio
from karrio.mappers.dhl_parcel_de.settings import Settings


# Initialize a carrier gateway
dhl_parcel_de = karrio.gateway["dhl_parcel_de"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
