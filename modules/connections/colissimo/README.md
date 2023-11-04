
# karrio.colissimo

This package is a Colissimo extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.colissimo
```

## Usage

```python
import karrio
from karrio.mappers.colissimo.settings import Settings


# Initialize a carrier gateway
colissimo = karrio.gateway["colissimo"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
