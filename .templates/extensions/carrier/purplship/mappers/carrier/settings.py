"""Purplship [Carrier Name] settings."""

import attr
from purplship.providers.carrier.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """[Carrier Name] connection settings."""

    # Carrier specific properties
    # username: str
    # password: str
    # account_number: str = None

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "[carrier_name]"
