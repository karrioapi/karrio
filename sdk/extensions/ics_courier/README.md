# karrio.ics_courier

This package is a ICS Courier extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.ics_courier
```

## Usage

```python
import karrio
from karrio.mappers.ics_courier.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["ics_courier"].create(
    Settings(
        ...
    )
)
```

Check the [karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
