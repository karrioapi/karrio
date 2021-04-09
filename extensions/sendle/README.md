# purplship.sendle

This package is a Sendle extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.sendle
```

## Usage

```python
import purplship
from purplship.mappers.sendle.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["sendle"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
