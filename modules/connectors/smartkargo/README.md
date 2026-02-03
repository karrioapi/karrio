# karrio.smartkargo

This package is a SmartKargo extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.smartkargo
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.smartkargo.settings import Settings


# Initialize a carrier gateway
smartkargo = karrio.gateway["smartkargo"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
