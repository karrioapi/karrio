"""
Google Geocode Address Validator Plugin.

This module provides address validation using the Google Geocode API.
"""

from karrio.core.metadata import PluginMetadata
from karrio.validators.googlegeocoding import Validator

# Export the metadata for this validator
METADATA = PluginMetadata(
    label="Google Geocode",
    Validator=Validator,
    id="googlegeocoding",
    status="production-ready",
    website="https://cloud.google.com/maps-platform/",
    documentation="https://developers.google.com/maps/documentation/geocoding/overview",
    description="Validate addresses using Google Geocode API for precision and accuracy.",
    readme=""
)
