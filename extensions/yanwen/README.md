# purplship.yanwen

This package is a Yanwen extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.6+`

## Installation

```bash
pip install purplship.yanwen
```

## Usage

```python
import purplship
from purplship.mappers.yanwen.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["yanwen"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
