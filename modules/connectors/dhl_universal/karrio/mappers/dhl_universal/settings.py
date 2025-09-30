"""Karrio DHL Universal settings."""

import attr
import karrio.providers.dhl_universal.utils as utils


@attr.s(auto_attribs=True)
class Settings(utils.Settings):
    """DHL Universal connection settings."""

    # Carrier specific properties
    consumer_key: str
    consumer_secret: str
    language: utils.LanguageEnum = "en"  # type: ignore

    # Base properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dhl_universal"
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}
