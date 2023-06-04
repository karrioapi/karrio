
# karrio.post_nl

This package is a Post NL extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.post_nl
```

## Usage

```python
import karrio
from karrio.mappers.post_nl.settings import Settings


# Initialize a carrier gateway
post_nl = karrio.gateway["post_nl"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
