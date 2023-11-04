
# karrio.geodis

This package is a GEODIS extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.geodis
```

## Usage

```python
import karrio
from karrio.mappers.geodis.settings import Settings


# Initialize a carrier gateway
geodis = karrio.gateway["geodis"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
