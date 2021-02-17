# purplship.royalmail

This package is a Royal Mail extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.6+`

## Installation

```bash
pip install purplship.royalmail
```

## Usage

```python
import purplship
from purplship.mappers.royalmail.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["royalmail"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
