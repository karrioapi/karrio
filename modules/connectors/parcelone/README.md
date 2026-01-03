# karrio.parcelone

This package is a ParcelOne extension of the [karrio](https://pypi.org/project/karrio) multi-carrier shipping SDK.

## Requirements

`Python 3.11+`

## Installation

```bash
pip install karrio.parcelone
```

## Usage

```python
import karrio
from karrio.mappers.parcelone.settings import Settings

# Initialize a gateway with your ParcelOne credentials
gateway = karrio.gateway["parcelone"].create(
    Settings(
        username="your-username",
        password="your-password",
        mandator_id="your-mandator-id",
        consigner_id="your-consigner-id",
        test_mode=True,
    )
)
```

Check the [karrio documentation](https://docs.karrio.io) for more details.
