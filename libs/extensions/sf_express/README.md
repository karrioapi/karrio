# purplship.sf_express

This package is a SF-Express extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.sf_express
```

## Usage

```python
import purplship
from purplship.mappers.sf_express.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["sf_express"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
