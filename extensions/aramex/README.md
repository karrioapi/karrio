# purplship.aramex

This package is a Aramex extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.aramex
```

## Usage

```python
import purplship
from purplship.mappers.aramex.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["aramex"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
