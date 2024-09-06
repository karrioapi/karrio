
# karrio.seko

This package is a SEKO Logistics extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.seko
```

## Usage

```python
import karrio
from karrio.mappers.seko.settings import Settings


# Initialize a carrier gateway
seko = karrio.gateway["seko"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
