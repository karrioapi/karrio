# karrio.canadapost

This package is a Canada Post extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.canadapost
```

## Usage

```python
import karrio
from karrio.mappers.canadapost.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["canadapost"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
