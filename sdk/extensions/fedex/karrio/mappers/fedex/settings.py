
"""Karrio FedEx client settings."""

import attr
import karrio.providers.fedex.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """FedEx connection settings."""

    # required carrier specific properties

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "fedex"
    account_country_code: str = None
    metadata: dict = {}
