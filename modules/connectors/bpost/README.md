
# karrio.bpost

This package is a Belgian Post extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.bpost
```

## Usage

```python
import karrio
from karrio.mappers.bpost.settings import Settings


# Initialize a carrier gateway
bpost = karrio.gateway["bpost"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
