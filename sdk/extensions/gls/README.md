
# karrio.gls

This package is a GLS extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.gls
```

## Usage

```python
import karrio
from karrio.mappers.gls.settings import Settings


# Initialize a carrier gateway
gls = karrio.gateway["gls"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
