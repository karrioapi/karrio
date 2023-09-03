
# karrio.asendia_us

This package is a Asendia US extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.asendia_us
```

## Usage

```python
import karrio
from karrio.mappers.asendia_us.settings import Settings


# Initialize a carrier gateway
asendia_us = karrio.gateway["asendia_us"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
