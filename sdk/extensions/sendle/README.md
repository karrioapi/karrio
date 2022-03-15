# karrio.sendle

This package is a Sendle extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.sendle
```

## Usage

```python
import karrio
from karrio.mappers.sendle.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["sendle"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.karrio.com) for Shipping API requests
