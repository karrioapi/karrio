# purplship.dhl_parcel_pl

This package is a DHL Parcel Poland extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.dhl_parcel_pl
```

## Usage

```python
import purplship
from purplship.mappers.dhl_parcel_pl.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["dhl_parcel_pl"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
