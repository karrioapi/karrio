# purplship.fedex

This package is a FedEx extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.fedex
```

## Usage

```python
import purplship
from purplship.mappers.fedex.settings import Settings


# Initialize a carrier gateway
fedex = purplship.gateway["fedex"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
