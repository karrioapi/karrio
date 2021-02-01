# purplship.purolator_courier

This package is a Purolator Courier extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.6+`

## Installation

```bash
pip install purplship.purolator_courier
```

## Usage

```python
import purplship
from purplship.mappers.purolator_courier.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["purolator_courier"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
