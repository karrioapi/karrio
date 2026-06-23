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

# Initialize a gateway with your ParcelOne credentials.
# mandator_id / consigner_id (and other carrier defaults) live in `config`
# so they can be left blank when relying on the API's default profile.
gateway = karrio.gateway["parcelone"].create(
    Settings(
        username="your-username",
        password="your-password",
        api_key="your-api-key",
        test_mode=True,
        config=dict(
            mandator_id="your-mandator-id",
            consigner_id="your-consigner-id",
        ),
    )
)
```

Check the [karrio documentation](https://docs.karrio.io) for more details.
