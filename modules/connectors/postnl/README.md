# karrio.postnl

This package is a Post NL extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.postnl
```

## Usage

```python
import karrio
from karrio.mappers.postnl.settings import Settings


# Initialize a carrier gateway
postnl = karrio.gateway["postnl"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
