# karrio.amazon_mws

This package is a amazon_mws extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.amazon_mws
```

## Usage

```python
import karrio
from karrio.mappers.amazon_mws.settings import Settings


# Initialize a carrier gateway
amazon_mws = karrio.gateway["amazon_mws"].create(
    Settings(
        ...
    )
)
```

Check the [karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
