"""Purplship UPS connection settings."""

import attr
from purplship.providers.purolator_courier.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """UPS connection settings."""

    username: str
    password: str
    account_number: str
    user_token: str
    language: str = "en"
    id: str = None
    test: bool = False
    carrier_id: str = "purolator_courier"
