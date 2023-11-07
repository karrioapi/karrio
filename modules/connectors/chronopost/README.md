
# karrio.chronopost

This package is a Chronopost extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.chronopost
```

## Usage

```python
import karrio
from karrio.mappers.chronopost.settings import Settings


# Initialize a carrier gateway
chronopost = karrio.gateway["chronopost"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
