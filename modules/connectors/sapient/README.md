
# karrio.sapient

This package is a SAPIENT extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.sapient
```

## Usage

```python
import karrio
from karrio.mappers.sapient.settings import Settings


# Initialize a carrier gateway
sapient = karrio.gateway["sapient"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
