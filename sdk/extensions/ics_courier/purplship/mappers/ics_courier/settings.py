"""purplship ICS Courier client settings."""

import attr
from purplship.providers.ics_courier import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """ICS Courier connection settings."""

    account_id: str
    password: str

    id: str = None
    test: bool = False
    carrier_id: str = "ics_courier"
    account_country_code: str = "CA"
