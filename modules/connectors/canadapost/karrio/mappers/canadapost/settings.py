"""Karrio Canada post client settings."""

import attr
import karrio.providers.canadapost.utils as utils


@attr.s(auto_attribs=True)
class Settings(utils.Settings):
    """Canada post connection settings."""

    username: str
    password: str = attr.ib(metadata={"sensitive": True})
    customer_number: str = None
    contract_id: str = None
    # contract_id: str = attr.ib(default=None, metadata={"sensitive": True})
    language: utils.LanguageEnum = "en"  # type: ignore

    id: str = None
    test_mode: bool = False
    carrier_id: str = "canadapost"
    account_country_code: str = "CA"
    metadata: dict = {}
    config: dict = {}
