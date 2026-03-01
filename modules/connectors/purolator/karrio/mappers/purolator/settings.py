"""Karrio Purolator connection settings."""

import attr
import karrio.providers.purolator.utils as utils


@attr.s(auto_attribs=True)
class Settings(utils.Settings):
    """Purolator connection settings."""

    username: str
    password: str
    # password: str = attr.ib(metadata={"sensitive": True})
    account_number: str
    user_token: str = None
    # user_token: str = attr.ib(default=None, metadata={"sensitive": True})
    language: utils.LanguageEnum = "en"  # type: ignore

    id: str = None
    test_mode: bool = False
    carrier_id: str = "purolator"
    account_country_code: str = "CA"
    metadata: dict = {}
    config: dict = {}
