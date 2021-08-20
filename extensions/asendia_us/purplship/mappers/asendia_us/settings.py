"""Purplship Asendia US settings."""

import attr
from purplship.providers.asendia_us.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Asendia US connection settings."""

    # Carrier specific properties
    username: str
    password: str
    x_asendia_one_api_key: str
    account_number: str = None

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "asendia_us"
    account_country_code: str = "US"
