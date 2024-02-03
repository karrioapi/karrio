
# karrio.deutschepost_international

This package is a Deutsche Post International extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.deutschepost_international
```

## Usage

```python
import karrio
from karrio.mappers.deutschepost_international.settings import Settings


# Initialize a carrier gateway
deutschepost_international = karrio.gateway["deutschepost_international"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
