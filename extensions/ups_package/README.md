# purplship.ups_package

This package is a UPS Package extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.ups_package
```

## Usage

```python
import purplship
from purplship.mappers.ups_package.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["ups_package"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
