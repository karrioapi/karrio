
# karrio.australiapost

This package is a Australia Post extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.australiapost
```

## Usage

```python
import karrio
from karrio.mappers.australiapost.settings import Settings


# Initialize a carrier gateway
australiapost = karrio.gateway["australiapost"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
