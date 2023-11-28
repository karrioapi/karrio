
# karrio.nationex

This package is a Nationex extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.nationex
```

## Usage

```python
import karrio
from karrio.mappers.nationex.settings import Settings


# Initialize a carrier gateway
nationex = karrio.gateway["nationex"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
