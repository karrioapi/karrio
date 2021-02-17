# purplship.yunexpress 

This package is a Yunexpress extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.6+`

## Installation

```bash
pip install purplship.yunexpress
```

## Usage

```python
import purplship
from purplship.mappers.yunexpress .settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["yunexpress"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
