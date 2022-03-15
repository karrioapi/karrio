# karrio.purolator

This package is a Purolator extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.purolator
```

## Usage

```python
import karrio
from karrio.mappers.purolator.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["purolator"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
