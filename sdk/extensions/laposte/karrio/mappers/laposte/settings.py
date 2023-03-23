
"""Karrio La Poste client settings."""

import attr
import karrio.providers.laposte.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """La Poste connection settings."""

    # required carrier specific properties

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "laposte"
    account_country_code: str = None
    metadata: dict = {}
