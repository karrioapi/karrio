"""
Karrio Plugin Metadata Module.

This module provides the PluginMetadata class and related functionality
for defining and working with Karrio plugin metadata.
"""

import attr
from enum import Enum
from typing import Optional, Type, List, Dict, Any, Literal

from karrio.api.proxy import Proxy
from karrio.api.mapper import Mapper
from karrio.core.settings import Settings
from karrio.core.models import ServiceLevel


@attr.s(auto_attribs=True)
class PluginMetadata:
    """
    Metadata for a Karrio plugin.

    This class defines the metadata for a Karrio plugin, including its ID,
    label, description, capabilities, and other attributes.
    """
    id: str
    label: str
    description: Optional[str] = ""
    status: Optional[str] = "beta"

    # Components that will be registered if present
    Proxy: Any = None
    Mapper: Any = None
    Validator: Any = None
    Settings: Any = None

    # Optional metadata
    options: Any = None
    services: Any = None
    countries: Any = None
    packaging_types: Any = None
    package_presets: Any = None
    service_levels: Any = None
    connection_configs: Any = None

    # Extra metadata
    website: Optional[str] = None
    documentation: Optional[str] = None
    readme: Optional[str] = None
    is_hub: bool = False
    hub_carriers: Optional[Dict[str, str]] = None
    has_intl_accounts: Optional[bool] = False

    def is_carrier_integration(self) -> bool:
        """Check if this plugin is a carrier integration based on registered components."""
        return bool(self.Mapper) and bool(self.Proxy) and bool(self.Settings)

    def is_address_validator(self) -> bool:
        """Check if this plugin is an address validator based on registered components."""
        return bool(self.Validator)

    def is_dual_purpose(self) -> bool:
        """Check if this plugin serves both as a carrier integration and address validator."""
        return self.is_carrier_integration() and self.is_address_validator()

    @property
    def plugin_types(self) -> List[str]:
        """
        Get a list of all functionality types provided by this plugin.

        Returns:
            List[str]: List of plugin types, e.g. ["carrier_integration", "address_validator"]
        """
        types = []
        if self.is_carrier_integration():
            types.append("carrier_integration")
        if self.is_address_validator():
            types.append("address_validator")
        if not types:
            types.append("unknown")
        return types

    @property
    def plugin_type(self) -> str:
        """
        Determine the primary type of plugin based on registered components.
        For dual-purpose plugins, returns "dual_purpose".

        Returns:
            str: "carrier_integration", "address_validator", "dual_purpose", or "unknown"
        """
        if self.is_carrier_integration() and self.is_address_validator():
            return "dual_purpose"
        elif self.is_carrier_integration():
            return "carrier_integration"
        elif self.is_address_validator():
            return "address_validator"
        else:
            return "unknown"

    @property
    def supports_carrier_integration(self) -> bool:
        """Check if this plugin provides carrier integration functionality."""
        return self.is_carrier_integration()

    @property
    def supports_address_validation(self) -> bool:
        """Check if this plugin provides address validation functionality."""
        return self.is_address_validator()

    # Dictionary-like access methods for backward compatibility
    def __getitem__(self, item):
        return getattr(self, item)

    def get(self, key, default=None):
        """
        Dictionary-like get method for backward compatibility.

        Args:
            key: Attribute name to retrieve
            default: Default value if attribute doesn't exist

        Returns:
            The attribute value or default if not found
        """
        return getattr(self, key, default)


# Legacy compatibility aliases
Metadata = PluginMetadata
AddressValidatorMetadata = PluginMetadata
