
# karrio.dpdhl

This package is a Deutsche Post DHL extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dpdhl
```

## Usage

```python
import karrio
from karrio.mappers.dpdhl.settings import Settings


# Initialize a carrier gateway
dpdhl = karrio.gateway["dpdhl"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
