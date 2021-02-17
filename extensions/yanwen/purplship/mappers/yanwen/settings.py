"""Purplship Yanwen settings."""

import attr
from purplship.providers.yanwen.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Yanwen connection settings."""

    # Carrier specific properties
    customer_number: str
    license_key: str

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "yanwen"
