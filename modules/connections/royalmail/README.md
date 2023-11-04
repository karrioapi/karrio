# karrio.royalmail

This package is a Royal Mail extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.royalmail
```

## Usage

```python
import karrio
from karrio.mappers.royalmail.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["royalmail"].create(
    Settings(
        ...
    )
)
```

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests
