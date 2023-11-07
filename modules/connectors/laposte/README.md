
# karrio.laposte

This package is a La Poste extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.laposte
```

## Usage

```python
import karrio
from karrio.mappers.laposte.settings import Settings


# Initialize a carrier gateway
laposte = karrio.gateway["laposte"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
