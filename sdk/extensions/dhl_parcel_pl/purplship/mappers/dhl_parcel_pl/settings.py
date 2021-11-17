"""Purplship DHL Parcel Poland client settings."""

import attr
from purplship.providers.dhl_parcel_pl import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """DHL Parcel Poland connection settings."""

    username: str
    password: str
    account_number: str = None

    id: str = None
    test: bool = False
    carrier_id: str = "dhl_parcel_pl"
    account_country_code: str = "PL"
