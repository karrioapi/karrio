
# karrio.locate2u

This package is a Locate2u extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.locate2u
```

## Usage

```python
import karrio
from karrio.mappers.locate2u.settings import Settings


# Initialize a carrier gateway
locate2u = karrio.gateway["locate2u"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
