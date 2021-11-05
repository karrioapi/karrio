# purplship.ups

This package is a UPS extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.ups
```

## Usage

```python
import purplship
from purplship.mappers.ups.settings import Settings


# Initialize a carrier gateway
ups = purplship.gateway["ups"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
