# karrio.generic

This package is a Generic extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.generic
```

## Usage

```python
import karrio
from karrio.mappers.generic.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["generic"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
