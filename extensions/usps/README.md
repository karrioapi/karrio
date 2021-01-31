# purplship.usps

This package is a USPS Express extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.usps
```

## Usage

```python
import purplship
from purplship.mappers.usps.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["usps"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
