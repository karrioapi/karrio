# karrio.easypost

This package is a easypost extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.easypost
```

## Usage

```python
import karrio
from karrio.mappers.easypost.settings import Settings


# Initialize a carrier gateway
easypost = karrio.gateway["easypost"].create(
    Settings(
        ...
    )
)
```

Check the [karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
