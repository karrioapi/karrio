# purplship.dhl_express

This package is a DHL Express extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.6+`

## Installation

```bash
pip install purplship.dhl_express
```

## Usage

```python
import purplship
from purplship.mappers.dhl_express.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["dhl_express"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
