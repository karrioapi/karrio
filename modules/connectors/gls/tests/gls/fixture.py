"""Test fixtures for GLS Group integration."""

import karrio.sdk as karrio
import karrio.lib as lib
import datetime
from karrio.core.models import Address

# Pre-populate OAuth cache to avoid real API calls during tests
expiry = datetime.datetime.now() + datetime.timedelta(days=1)
client_id = "test_client_id"
client_secret = "test_client_secret"
cached_auth = {
    f"gls|{client_id}|{client_secret}": dict(
        access_token="fake_access_token_for_testing",
        token_type="Bearer",
        expires_in="3600",
        expiry=expiry.strftime("%Y-%m-%d %H:%M:%S"),
    )
}

# Create gateway for testing
gateway = karrio.gateway["gls"].create(
    {
        "client_id": client_id,
        "client_secret": client_secret,
        "test_mode": True,
    },
    cache=lib.Cache(**cached_auth),
)

# Sample addresses
shipper_address = Address(
    company_name="Test Shipper Company",
    address_line1="Main Street",
    address_line2="123",
    city="Berlin",
    postal_code="12345",
    country_code="DE",
    person_name="John Doe",
    phone_number="+49301234567",
    email="shipper@example.com",
)

recipient_address = Address(
    company_name="Test Recipient Company",
    address_line1="Market Street",
    address_line2="456",
    city="Munich",
    postal_code="54321",
    country_code="DE",
    person_name="Jane Smith",
    phone_number="+49891234567",
    email="recipient@example.com",
)
