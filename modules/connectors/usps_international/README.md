
# karrio.usps

This package is a USPS extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.usps
```

## Usage

```python
import karrio
from karrio.mappers.usps_international.settings import Settings


# Initialize a carrier gateway
usps = karrio.gateway["usps"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
