"""
Karrio Plugin Metadata Module.

This module provides the PluginMetadata class and related functionality
for defining and working with Karrio plugin metadata.
"""

import attr
from typing import Optional, List, Dict, Any, Literal


# Service type constants
SERVICE_TYPE_CARRIER: Literal["carrier", "LSP"] = "carrier"  # Shipping carrier with full shipping capabilities
SERVICE_TYPE_LSP: Literal["carrier", "LSP"] = (
    "LSP"  # Logistics Service Provider (address validation, geocoding, etc.)
)


@attr.s(auto_attribs=True)
class PluginMetadata:
    """
    Metadata for a Karrio plugin.

    This class defines the metadata for a Karrio plugin, including its ID,
    label, description, capabilities, and other attributes.

    service_type: Distinguishes plugin types:
        - "carrier": Full shipping carriers with rating, shipping, tracking capabilities
        - "LSP": Logistics Service Providers (address validation, geocoding, duties calculation, etc.)
    """

    id: str
    label: str
    description: Optional[str] = ""
    status: Optional[str] = "beta"

    # Service type: "carrier" (default) or "LSP"
    service_type: Literal["carrier", "LSP"] = SERVICE_TYPE_CARRIER

    # Components that will be registered if present
    Proxy: Any = None
    Mapper: Any = None
    Hooks: Any = None
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

    # System configuration for runtime settings (e.g., OAuth credentials)
    # Format: Dict[str, Tuple[default_value, description, type]]
    # Example: {"CARRIER_OAUTH_CLIENT_ID": ("", "OAuth client ID", str)}
    system_config: Optional[Dict[str, Any]] = None

    def is_carrier(self) -> bool:
        """Check if this plugin is a shipping carrier."""
        return self.service_type == SERVICE_TYPE_CARRIER and self.is_integration()

    def is_lsp(self) -> bool:
        """Check if this plugin is a Logistics Service Provider."""
        return self.service_type == SERVICE_TYPE_LSP and self.is_integration()

    def is_integration(self) -> bool:
        """Check if this plugin has valid integration components (Mapper + Proxy + Settings)."""
        return bool(self.Mapper) and bool(self.Proxy) and bool(self.Settings)

    def has_hooks(self) -> bool:
        """Check if this plugin has hooks/webhook processing capability."""
        return bool(self.Hooks)

    # Keep for backward compatibility
    def is_carrier_integration(self) -> bool:
        """Check if this plugin is a carrier integration based on registered components."""
        return self.is_carrier()

    def is_address_validator(self) -> bool:
        """Check if this plugin provides address validation (LSP with validate_address proxy method)."""
        if not self.is_lsp():
            return False
        # Check if proxy has validate_address method
        if self.Proxy:
            return hasattr(self.Proxy, "validate_address") and callable(
                getattr(self.Proxy, "validate_address", None)
            )
        return False

    @property
    def plugin_types(self) -> List[str]:
        """
        Get a list of all functionality types provided by this plugin.

        Returns:
            List[str]: List of plugin types, e.g. ["carrier", "LSP"]
        """
        types = []
        if self.is_carrier():
            types.append("carrier")
        if self.is_lsp():
            types.append("LSP")
        if not types:
            types.append("unknown")
        return types

    @property
    def plugin_type(self) -> str:
        """
        Determine the primary type of plugin based on service_type.

        Returns:
            str: "carrier", "LSP", or "unknown"
        """
        if self.is_carrier():
            return "carrier"
        elif self.is_lsp():
            return "LSP"
        else:
            return "unknown"

    @property
    def supports_carrier_integration(self) -> bool:
        """Check if this plugin provides carrier integration functionality."""
        return self.is_carrier()

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
