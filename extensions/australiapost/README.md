# purplship.carrier_name

This package is a Australia Post extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.australiapost
```

## Usage

```python
import purplship
from purplship.mappers.australiapost.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["australiapost"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
