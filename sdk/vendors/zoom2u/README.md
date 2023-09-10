
# karrio.zoom2u

This package is a Zoom2u extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.zoom2u
```

## Usage

```python
import karrio
from karrio.mappers.zoom2u.settings import Settings


# Initialize a carrier gateway
zoom2u = karrio.gateway["zoom2u"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
