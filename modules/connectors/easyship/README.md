
# karrio.easyship

This package is a Easyship extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.easyship
```

## Usage

```python
import karrio
from karrio.mappers.easyship.settings import Settings


# Initialize a carrier gateway
easyship = karrio.gateway["easyship"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
