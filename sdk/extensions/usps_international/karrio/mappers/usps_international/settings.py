"""Karrio USPS International client settings."""

import attr
from karrio.providers.usps_international.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """USPS International connection settings."""

    # Carrier specific properties
    username: str
    password: str
    mailer_id: str = None
    customer_registration_id: str = None
    logistics_manager_mailer_id: str = None

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "usps_international"
    account_country_code: str = "US"
