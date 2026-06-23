import karrio.core as core
import karrio.lib as lib


class Settings(core.Settings):
    """DHL Freight connection settings."""

    client_id: str = None
    client_secret: str = None
    account_number: str = None
    consignee_account_number: str = None

    account_country_code: str = "DE"

    @property
    def carrier_name(self):
        return "dhl_freight"

    @property
    def connection_account_number(self) -> str | None:
        """Consignor DHL Freight account number (mandatory ``Parties[Consignor].Id``)."""
        if self.account_number:
            return self.account_number
        return (
            self.connection_system_config.get("DHL_FREIGHT_SANDBOX_ACCOUNT_NUMBER")
            if self.test_mode
            else self.connection_system_config.get("DHL_FREIGHT_ACCOUNT_NUMBER")
        )

    @property
    def connection_consignee_account_number(self) -> str | None:
        """Default consignee DHL Freight account number (``Parties[Consignee].Id``)."""
        return self.consignee_account_number or None

    # Computed credential properties with system config fallback
    @property
    def connection_client_id(self) -> str | None:
        """Return user-provided client_id or fallback to system config."""
        if self.client_id:
            return self.client_id
        return (
            self.connection_system_config.get("DHL_FREIGHT_SANDBOX_CLIENT_ID")
            if self.test_mode
            else self.connection_system_config.get("DHL_FREIGHT_CLIENT_ID")
        )

    @property
    def connection_client_secret(self) -> str | None:
        """Return user-provided client_secret or fallback to system config."""
        if self.client_secret:
            return self.client_secret
        return (
            self.connection_system_config.get("DHL_FREIGHT_SANDBOX_CLIENT_SECRET")
            if self.test_mode
            else self.connection_system_config.get("DHL_FREIGHT_CLIENT_SECRET")
        )

    @property
    def server_url(self):
        return (
            "https://api-sandbox.dhl.com/freight/shipping/orders/v1"
            if self.test_mode
            else "https://api.dhl.com/freight/shipping/orders/v1"
        )

    @property
    def print_server_url(self):
        # DHL Freight Print (Labelling) API — labels/waybill by shipment id.
        return (
            "https://api-sandbox.dhl.com/freight/shipping/labels/v1"
            if self.test_mode
            else "https://api.dhl.com/freight/shipping/labels/v1"
        )

    @property
    def token_server_url(self):
        # Shared DHL Authentication API (client_credentials). See SPECS.md.
        return "https://api-sandbox.dhl.com/auth/v1/token" if self.test_mode else "https://api.dhl.com/auth/v1/token"

    @property
    def tracking_server_url(self):
        # DHL Group Unified Tracking API (UTAPI) — cross-BU /track/shipments.
        # Uses a `DHL-API-Key` header (the client_id), not the OAuth token.
        return "https://api-sandbox.dhl.com/track" if self.test_mode else "https://api-eu.dhl.com/track"

    @property
    def tracking_url(self):
        # Consumer-facing DHL freight-tracking portal.
        return "https://www.dhl.com/global-en/home/tracking/tracking-freight.html?submit=1&tracking-id={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dhl_freight.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def language(self):
        country = self.account_country_code or "DE"
        language = self.connection_config.language.state or "en"
        return f"{language.lower()}-{country.upper()}"
