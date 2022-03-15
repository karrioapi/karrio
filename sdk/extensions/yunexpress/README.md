# karrio.yunexpress

This package is a Yunexpress extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.yunexpress
```

## Usage

```python
import karrio
from karrio.mappers.yunexpress .settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["yunexpress"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://sdk.karrio.com) for Shipping API requests
