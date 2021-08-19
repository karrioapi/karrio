# purplship.asendia_us

This package is a Asendia US extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.asendia_us
```

## Usage

```python
import purplship
from purplship.mappers.asendia_us.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["asendia_us"].create(
    Settings(
        ...
    )
)
```

Check the [Purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests
