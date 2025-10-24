"""
AddressComplete Address Validator Plugin.

This module provides address validation using the AddressComplete API.
"""

from karrio.core.metadata import PluginMetadata
from karrio.validators.addresscomplete import Validator

# Export the metadata for this validator
METADATA = PluginMetadata(
    label="Canada Post AddressComplete",
    Validator=Validator,
    id="addresscomplete",
    status="production-ready",
    website="https://www.addresscomplete.com/",
    documentation="https://www.addresscomplete.com/api-documentation",
    description="Validate addresses using AddressComplete API for precision and accuracy.",
    readme=""
)
