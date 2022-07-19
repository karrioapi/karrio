"""Karrio USPS International client settings."""

from karrio.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """USPS International connection settings."""

    # Carrier specific properties
    username: str
    password: str
    mailer_id: str = None
    customer_registration_id: str = None
    logistics_manager_mailer_id: str = None

    id: str = None
    account_country_code: str = "US"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "usps_international"

    @property
    def server_url(self):
        return "https://secure.shippingapis.com/ShippingAPI.dll"
