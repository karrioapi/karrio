# karrio.mydhl

This package is a MyDHL extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.mydhl
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.mydhl.settings import Settings


# Initialize a carrier gateway
mydhl = karrio.gateway["mydhl"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
