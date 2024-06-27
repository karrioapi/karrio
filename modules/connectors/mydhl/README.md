
# karrio.mydhl

This package is a DHL Express extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.mydhl
```

## Usage

```python
import karrio
from karrio.mappers.mydhl.settings import Settings


# Initialize a carrier gateway
mydhl = karrio.gateway["mydhl"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
