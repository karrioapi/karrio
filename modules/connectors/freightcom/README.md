# karrio.freightcom

This package is a freightcom extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.freightcom
```

## Usage

```python
import karrio
from karrio.mappers.freightcom.settings import Settings


# Initialize a carrier gateway
freightcom = karrio.gateway["freightcom"].create(
    Settings(
        ...
    )
)
```

Check the [karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
