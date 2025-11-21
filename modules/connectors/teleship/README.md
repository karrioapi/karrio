# karrio.teleship

This package is a Teleship extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.teleship
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.teleship.settings import Settings


# Initialize a carrier gateway
teleship = karrio.gateway["teleship"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
