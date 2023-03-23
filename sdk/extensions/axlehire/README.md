
# karrio.axlehire

This package is a AxleHire extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.axlehire
```

## Usage

```python
import karrio
from karrio.mappers.axlehire.settings import Settings


# Initialize a carrier gateway
axlehire = karrio.gateway["axlehire"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
