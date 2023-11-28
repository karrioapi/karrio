
# karrio.boxknight

This package is a BoxKnight extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.boxknight
```

## Usage

```python
import karrio
from karrio.mappers.boxknight.settings import Settings


# Initialize a carrier gateway
boxknight = karrio.gateway["boxknight"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
