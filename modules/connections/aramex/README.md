# karrio.aramex

This package is a Aramex extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.aramex
```

## Usage

```python
import karrio
from karrio.mappers.aramex.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["aramex"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
