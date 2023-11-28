
# karrio.amazon_shipping

This package is a Amazon Shipping extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.amazon_shipping
```

## Usage

```python
import karrio
from karrio.mappers.amazon_shipping.settings import Settings


# Initialize a carrier gateway
amazon_shipping = karrio.gateway["amazon_shipping"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
