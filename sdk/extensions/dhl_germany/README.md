
# karrio.dhl_germany

This package is a DHL Parcel Germany extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dhl_germany
```

## Usage

```python
import karrio
from karrio.mappers.dhl_germany.settings import Settings


# Initialize a carrier gateway
dhl_germany = karrio.gateway["dhl_germany"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
