# karrio.canpar

This package is a Canpar extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.canpar
```

## Usage

```python
import karrio
from karrio.mappers.canpar.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["canpar"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
