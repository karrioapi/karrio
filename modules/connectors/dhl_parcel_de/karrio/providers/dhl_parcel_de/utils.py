import typing
import karrio.lib as lib
import karrio.core as core


class Settings(core.Settings):
    """DHL Germany connection settings."""

    username: str
    password: str
    client_id: str
    client_secret: str

    account_country_code: str = "DE"

    @property
    def carrier_name(self):
        return "dhl_parcel_de"

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
    def tracking_server_url(self):
        return "https://api-eu.dhl.com"

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
        return (
            "https://www.dhl.com/"
            + locale
            + "/home/tracking/tracking-parcel.html?submit=1&tracking-id={}"
        )

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dhl_parcel_de.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    def get_billing_number(self, service_code: str = None) -> typing.Optional[str]:
        """Resolve billing number for a service with fallback to default.

        Args:
            service_code: The karrio service code (e.g., "dhl_parcel_de_paket")

        Returns:
            The billing number for the service, or default if not found
        """
        from karrio.providers.dhl_parcel_de.units import (
            DEFAULT_TEST_BILLING_NUMBERS,
            DEFAULT_TEST_BILLING_NUMBER,
        )

        service_billing_numbers = (
            self.connection_config.service_billing_numbers.state or []
        )

        # Use test defaults if in test mode and no custom config provided
        if self.test_mode and not service_billing_numbers:
            service_billing_numbers = DEFAULT_TEST_BILLING_NUMBERS

        if service_code:
            service_billing = next(
                (
                    item
                    for item in service_billing_numbers
                    if (
                        item.service == service_code
                        if hasattr(item, "service")
                        else item.get("service") == service_code
                    )
                ),
                None,
            )
            if service_billing:
                return (
                    service_billing.billing_number
                    if hasattr(service_billing, "billing_number")
                    else service_billing.get("billing_number")
                )

        # Fallback to configured default or test default
        default_billing = self.connection_config.default_billing_number.state
        if default_billing:
            return default_billing

        # Use test default if in test mode
        if self.test_mode:
            return DEFAULT_TEST_BILLING_NUMBER

        return None

    @property
    def profile(self):
        return self.connection_config.profile.state or "STANDARD_GRUPPENPROFIL"

    @property
    def language(self):
        country = self.account_country_code or "DE"
        language = self.connection_config.language.state or "en"
        return f"{language.lower()}-{country.upper()}"
