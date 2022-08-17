
# karrio.ups_freight

This package is a UPS Freight extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.ups_freight
```

## Usage

```python
import karrio
from karrio.mappers.ups_freight.settings import Settings


# Initialize a carrier gateway
ups_freight = karrio.gateway["ups_freight"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
