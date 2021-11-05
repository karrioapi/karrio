# purplship.freightcom

This package is a freightcom extension of the [purplship](https://pypi.org/project/purplship) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install purplship.freightcom
```

## Usage

```python
import purplship
from purplship.mappers.freightcom.settings import Settings


# Initialize a carrier gateway
freightcom = purplship.gateway["freightcom"].create(
    Settings(
        ...
    )
)
```

Check the [purplship Mutli-carrier SDK docs](https://sdk.purplship.com) for Shipping API requests

