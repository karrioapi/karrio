
# karrio.tnt_it

This package is a TNT Connect Italy extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.tnt_it
```

## Usage

```python
import karrio
from karrio.mappers.tnt_it.settings import Settings


# Initialize a carrier gateway
tnt_it = karrio.gateway["tnt_it"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
