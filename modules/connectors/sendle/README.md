
# karrio.sendle

This package is a Sendle extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.sendle
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.sendle.settings import Settings


# Initialize a carrier gateway
sendle = karrio.gateway["sendle"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
