# purplship.boxknight

This package is a BoxKnight extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.boxknight
```

## Usage

```python
import purplship
from purplship.mappers.boxknight.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["boxknight"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
