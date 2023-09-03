
# karrio.dpdhl_international

This package is a Deutsche Post International extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.dpdhl_international
```

## Usage

```python
import karrio
from karrio.mappers.dpdhl_international.settings import Settings


# Initialize a carrier gateway
dpdhl_international = karrio.gateway["dpdhl_international"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
