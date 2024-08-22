"""Karrio Nationex client settings."""

import attr
import karrio.providers.nationex.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Nationex connection settings."""

    # required carrier specific properties
    api_key: str
    customer_id: str
    billing_account: str = None
    language: provider_utils.LanguageEnum = "en"  # type: ignore

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "nationex"
    account_country_code: str = "CA"
    metadata: dict = {}
    config: dict = {}
