
# karrio.deutschepost

This package is a Deutsche Post Germany extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.deutschepost
```

## Usage

```python
import karrio
from karrio.mappers.deutschepost.settings import Settings


# Initialize a carrier gateway
deutschepost = karrio.gateway["deutschepost"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
