# karrio.dhl_ecommerce_europe

This package is a DHL eCommerce Europe extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.8+`

## Installation

```bash
pip install karrio.dhl_ecommerce_europe
```

## Usage

```python
import karrio
from karrio.mappers.dhl_ecommerce_europe.settings import Settings


# Initialize a carrier gateway
dhl = karrio.gateway["dhl_ecommerce_europe"].create(
    Settings(
        username="your_username",
        password="your_password",
        account_number="your_account_number",
        test=True,
    )
)
```

Check the [Karrio Multi-carrier SDK docs](https://docs.karrio.io) for Shipping API requests

## API Reference

- [DHL eCommerce Europe API Documentation](https://developer.dhl.com/api-reference/ecommerce-europe)
