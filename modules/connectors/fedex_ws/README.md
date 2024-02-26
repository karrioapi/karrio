# karrio.fedex

This package is a FedEx extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.fedex
```

## Usage

```python
import karrio
from karrio.mappers.fedex.settings import Settings


# Initialize a carrier gateway
fedex = karrio.gateway["fedex"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
