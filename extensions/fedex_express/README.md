# purplship.fedex_express

This package is a FedEx Express extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.6+`

## Installation

```bash
pip install purplship.fedex_express
```

## Usage

```python
import purplship
from purplship.mappers.fedex_express.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["fedex_express"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
