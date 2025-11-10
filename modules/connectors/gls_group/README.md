# Karrio - GLS Group Shipping Extension

This extension adds support for GLS Group shipping services to the Karrio platform.

## Features

- Shipment creation with label generation
- Tracking information retrieval
- OAuth2 authentication
- Support for multiple parcel types and services

## Installation

```bash
pip install karrio-gls-group
```

## Configuration

```python
import karrio
from karrio.mappers.gls_group.settings import Settings

settings = Settings(
    client_id="your_client_id",
    client_secret="your_client_secret",
    test_mode=True
)

gateway = karrio.gateway["gls_group"].create(settings)
```

## API Documentation

- Production: https://api.gls-group.net
- Sandbox: https://api-sandbox.gls-group.net
- Developer Portal: https://dev-portal.gls-group.net
