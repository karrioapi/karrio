# purplship.dhl_poland

This package is a DHL Parcel Poland extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.dhl_poland
```

## Usage

```python
import purplship
from purplship.mappers.dhl_poland.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["dhl_poland"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
