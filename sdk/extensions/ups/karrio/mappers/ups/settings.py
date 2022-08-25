"""Karrio UPS connection settings."""

import attr
from karrio.providers.ups.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """UPS connection settings."""

    username: str  # type:ignore
    password: str  # type:ignore
    access_license_number: str  # type:ignore
    account_number: str = None
    account_country_code: str = None
    metadata: dict = {}

    id: str = None
    test_mode: bool = False
    carrier_id: str = "ups"
