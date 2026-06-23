"""Karrio Amazon Shipping connection settings."""

import karrio.core as core
import karrio.lib as lib


class Settings(core.Settings):
    """Amazon Shipping SP-API connection settings. See SPECS.md."""

    # LWA SP-API credentials
    client_id: str
    client_secret: str
    refresh_token: str

    # Optional settings
    aws_region: str = "us-east-1"
    shipping_business_id: str = None

    @property
    def carrier_name(self):
        return "amazon_shipping"

    @property
    def server_url(self):
        """Get the SP-API endpoint based on AWS region."""
        region_mapping = {
            # North America
            "us-east-1": "https://sellingpartnerapi-na.amazon.com",
            # Europe
            "eu-west-1": "https://sellingpartnerapi-eu.amazon.com",
            # Far East
            "us-west-2": "https://sellingpartnerapi-fe.amazon.com",
        }
        base_url = region_mapping.get(self.aws_region, region_mapping["us-east-1"])

        if self.test_mode:
            return base_url.replace("sellingpartnerapi", "sandbox.sellingpartnerapi")

        return base_url

    @property
    def token_url(self):
        """LWA token endpoint."""
        return "https://api.amazon.com/auth/o2/token"

    @property
    def connection_config(self) -> lib.units.Options:
        """Additional connection configuration."""
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


class ConnectionConfig(lib.Enum):
    """Amazon Shipping connection configuration options."""

    shipping_business_id = lib.OptionEnum("shipping_business_id")
    label_format = lib.OptionEnum("label_format", str)
    label_size_width = lib.OptionEnum("label_size_width", float)
    label_size_length = lib.OptionEnum("label_size_length", float)
    label_size_unit = lib.OptionEnum("label_size_unit", str)
