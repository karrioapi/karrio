"""
Google Geocoding Address Validation Plugin.

This module provides address validation using the Google Geocoding API.
"""

from karrio.core.metadata import PluginMetadata

from karrio.mappers.googlegeocoding.mapper import Mapper
from karrio.mappers.googlegeocoding.proxy import Proxy
from karrio.mappers.googlegeocoding.settings import Settings


METADATA = PluginMetadata(
    id="googlegeocoding",
    label="Google Geocode",
    description="Validate addresses using Google Geocode API for precision and accuracy.",
    status="production-ready",
    service_type="LSP",
    # Integrations
    Mapper=Mapper,
    Proxy=Proxy,
    Settings=Settings,
    # Extra info
    website="https://cloud.google.com/maps-platform/",
    documentation="https://developers.google.com/maps/documentation/geocoding/overview",
)
