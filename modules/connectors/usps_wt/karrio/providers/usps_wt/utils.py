"""Karrio USPS client settings."""

import typing
import karrio.core.settings as settings


class Settings(settings.Settings):
    """USPS connection settings."""

    # Carrier specific properties
    username: str
    password: str
    mailer_id: str = None
    customer_registration_id: str = None
    logistics_manager_mailer_id: str = None

    id: str = None
    account_country_code: str = "US"
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "usps"

    @property
    def server_url(self):
        return "https://secure.shippingapis.com/ShippingAPI.dll"

    @property
    def tracking_url(self):
        return "https://tools.usps.com/go/TrackConfirmAction?tLabels={}"


def parse_phone_number(number: str) -> typing.Optional[str]:
    if number is None:
        return None

    return number.replace(" ", "").replace("-", "").replace("+", "")[-10:]
