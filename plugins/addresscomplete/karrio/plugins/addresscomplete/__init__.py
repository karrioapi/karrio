"""
AddressComplete Address Validation Plugin.

This module provides address validation using the Canada Post AddressComplete API.
"""

from karrio.core.metadata import PluginMetadata

from karrio.mappers.addresscomplete.mapper import Mapper
from karrio.mappers.addresscomplete.proxy import Proxy
from karrio.mappers.addresscomplete.settings import Settings


METADATA = PluginMetadata(
    id="addresscomplete",
    label="Canada Post AddressComplete",
    description="Validate addresses using Canada Post AddressComplete API for precision and accuracy.",
    status="production-ready",
    service_type="LSP",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Extra info
    website="https://www.addresscomplete.com/",
    documentation="https://www.addresscomplete.com/api-documentation",
)
