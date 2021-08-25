# purplship.ics_courier

This package is a ICS Courier extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.ics_courier
```

## Usage

```python
import purplship
from purplship.mappers.ics_courier.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["ics_courier"].create(
    Settings(
        ...
    )
)
```

Check the [purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
