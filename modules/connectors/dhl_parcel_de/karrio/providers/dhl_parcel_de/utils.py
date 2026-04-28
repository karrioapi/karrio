import karrio.core as core
import karrio.lib as lib


class Settings(core.Settings):
    """DHL Germany connection settings."""

    username: str = None
    password: str = None
    client_id: str = None
    client_secret: str = None

    account_country_code: str = "DE"

    @property
    def carrier_name(self):
        return "dhl_parcel_de"

    # Computed credential properties with system config fallback
    @property
    def connection_username(self) -> str | None:
        """Return user-provided username (no system config fallback)."""
        return self.username or None

    @property
    def connection_password(self) -> str | None:
        """Return user-provided password (no system config fallback)."""
        return self.password or None

    @property
    def connection_client_id(self) -> str | None:
        """Return user-provided client_id or fallback to system config."""
        if self.client_id:
            return self.client_id
        return (
            self.connection_system_config.get("DHL_PARCEL_DE_SANDBOX_CLIENT_ID")
            if self.test_mode
            else self.connection_system_config.get("DHL_PARCEL_DE_CLIENT_ID")
        )

    @property
    def connection_client_secret(self) -> str | None:
        """Return user-provided client_secret or fallback to system config."""
        if self.client_secret:
            return self.client_secret
        return (
            self.connection_system_config.get("DHL_PARCEL_DE_SANDBOX_CLIENT_SECRET")
            if self.test_mode
            else self.connection_system_config.get("DHL_PARCEL_DE_CLIENT_SECRET")
        )

    @property
    def server_url(self):
        return (
            "https://api-sandbox.dhl.com/parcel/de/shipping"
            if self.test_mode
            else "https://api-eu.dhl.com/parcel/de/shipping"
        )

    @property
    def token_server_url(self):
        return (
            "https://api-sandbox.dhl.com/parcel/de/account/auth/ropc/v1"
            if self.test_mode
            else "https://api-eu.dhl.com/parcel/de/account/auth/ropc/v1"
        )

    @property
    def returns_server_url(self):
        return (
            "https://api-sandbox.dhl.com/parcel/de/shipping/returns/v1"
            if self.test_mode
            else "https://api-eu.dhl.com/parcel/de/shipping/returns/v1"
        )

    @property
    def tracking_server_url(self):
        """Dedicated DHL Parcel DE Tracking API endpoint.

        Uses XML request in query parameter and returns XML response.
        Requires HTTP Basic Auth (API key:secret) + XML credentials (appname:password).
        """
        return (
            "https://api-sandbox.dhl.com/parcel/de/tracking/v0/shipments"
            if self.test_mode
            else "https://api-eu.dhl.com/parcel/de/tracking/v0/shipments"
        )

    @property
    def tracking_appname(self) -> str:
        """Return tracking service appname (username).

        In sandbox mode, uses hardcoded credentials as per DHL documentation.
        In production, uses the connection username.
        """
        if self.test_mode:
            return "zt12345"  # Sandbox hardcoded credential
        return self.connection_username or ""

    @property
    def tracking_password(self) -> str:
        """Return tracking service password.

        In sandbox mode, uses hardcoded credentials as per DHL documentation.
        In production, uses the connection password.
        """
        if self.test_mode:
            return "geheim"  # Sandbox hardcoded credential
        return self.connection_password or ""

    @property
    def pickup_server_url(self):
        return (
            "https://api-sandbox.dhl.com/parcel/de/transportation/pickup/v3"
            if self.test_mode
            else "https://api-eu.dhl.com/parcel/de/transportation/pickup/v3"
        )

    @property
    def tracking_url(self):
        country = self.account_country_code or "DE"
        language = self.connection_config.language.state or "en"
        locale = f"{country}-{language}".lower()
        return "https://www.dhl.com/" + locale + "/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dhl_parcel_de.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    def get_billing_number(
        self,
        service_code: str = None,
        billing_id: str | None = None,
    ) -> str | None:
        """Resolve billing number with optional unique-id selection.

        Lookup order:
            1. billing_id - exact match on the configured `id` field
               (used when the merchant picked one of multiple entries that
               share the same service_code).
            2. service_code - first exact match on `service`.
            3. config.default_billing_number.
            4. test default (test mode only).
        """
        from karrio.providers.dhl_parcel_de.units import (
            DEFAULT_TEST_BILLING_NUMBER,
            DEFAULT_TEST_BILLING_NUMBERS,
        )

        service_billing_numbers = self.connection_config.service_billing_numbers.state or []

        # Use test defaults if in test mode and no custom config provided
        if self.test_mode and not service_billing_numbers:
            service_billing_numbers = DEFAULT_TEST_BILLING_NUMBERS

        def _field(item, key):
            return (
                getattr(item, key, None) if hasattr(item, key) else (item.get(key) if isinstance(item, dict) else None)
            )

        # 1. Prefer exact id match when provided.
        if billing_id:
            match = next(
                (i for i in service_billing_numbers if _field(i, "id") == billing_id),
                None,
            )
            if match:
                bn = _field(match, "billing_number")
                if bn:
                    return bn

        # 2. Match by service_code. When duplicates exist, first row wins.
        if service_code:
            match = next((i for i in service_billing_numbers if _field(i, "service") == service_code), None)
            if match:
                bn = _field(match, "billing_number")
                if bn:
                    return bn

        # 3. Fallback to configured default or test default
        default_billing = self.connection_config.default_billing_number.state
        if default_billing:
            return default_billing

        # 4. Use test default if in test mode
        if self.test_mode:
            return DEFAULT_TEST_BILLING_NUMBER

        return None

    def get_return_billing_number(self, service_code_override: str | None = None) -> str | None:
        """Resolve return billing number with fallback chain:
        1. service_code_override (from shipping method option) -> lookup in service_billing_numbers map
        2. return_billing_number config (single default)
        3. test default for retoure
        """
        return_service = service_code_override
        if return_service:
            billing = self.get_billing_number(return_service)
            if billing:
                return billing

        return_billing = self.connection_config.return_billing_number.state
        if return_billing:
            return return_billing

        if self.test_mode:
            return "33333333330701"

        return None

    @property
    def language(self):
        country = self.account_country_code or "DE"
        language = self.connection_config.language.state or "en"
        return f"{language.lower()}-{country.upper()}"
