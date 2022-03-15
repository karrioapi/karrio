# karrio.yanwen

This package is a Yanwen extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.yanwen
```

## Usage

```python
import karrio
from karrio.mappers.yanwen.settings import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["yanwen"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.karrio.com) for Shipping API requests
