# karrio.tnt

This package is a TNT extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.tnt
```

## Usage

```python
import karrio
from karrio.mappers.tnt.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["tnt"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
