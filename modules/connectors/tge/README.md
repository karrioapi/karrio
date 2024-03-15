
# karrio.tge

This package is a TGE extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.tge
```

## Usage

```python
import karrio
from karrio.mappers.tge.settings import Settings


# Initialize a carrier gateway
tge = karrio.gateway["tge"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
