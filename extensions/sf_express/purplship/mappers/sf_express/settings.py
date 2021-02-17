"""Purplship SF-Express settings."""

import attr
from purplship.providers.sf_express.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """SF-Express connection settings."""

    # Carrier specific properties
    partner_id: str
    check_word: str

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = "sf_express"
