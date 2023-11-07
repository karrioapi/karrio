# karrio.usps_international

This package is a USPS International extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.usps_international
```

## Usage

```python
import karrio
from karrio.mappers.usps_international.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["usps"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
