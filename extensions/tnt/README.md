# purplship.tnt

This package is a TNT extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.6+`

## Installation

```bash
pip install purplship.tnt
```

## Usage

```python
import purplship
from purplship.mappers.tnt.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["tnt"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
