"""Test fixtures for GLS Group integration."""

import karrio.sdk as karrio
from karrio.core.models import Address

# Create gateway for testing
gateway = karrio.gateway["gls_group"].create(
    {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "test_mode": True,
    }
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
