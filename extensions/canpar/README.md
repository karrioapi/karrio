# purplship.canpar

This package is a Canpar extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.6+`

## Installation

```bash
pip install purplship.canpar
```

## Usage

```python
import purplship
from purplship.mappers.canpar.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["canpar"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
