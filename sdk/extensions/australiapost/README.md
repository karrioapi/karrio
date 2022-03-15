# karrio.carrier_name

This package is a Australia Post extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.australiapost
```

## Usage

```python
import karrio
from karrio.mappers.australiapost.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["australiapost"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://sdk.karrio.com) for Shipping API requests
