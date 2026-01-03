# karrio.asendia

This package is a Asendia extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.asendia
```

## Usage

```python
import karrio.sdk as karrio
from karrio.mappers.asendia.settings import Settings


# Initialize a carrier gateway
asendia = karrio.gateway["asendia"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
