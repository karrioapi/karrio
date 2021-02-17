# purplship.dhl_universal

This package is a DHL Universal Tracking extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.6+`

## Installation

```bash
pip install purplship.dhl_universal
```

## Usage

```python
import purplship
from purplship.mappers.dhl_universal.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["dhl_universal"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
