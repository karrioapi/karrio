"""Karrio DHL Parcel Germany client settings."""

import attr
import karrio.providers.dhl_germany.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DHL Parcel Germany connection settings."""

    # required carrier specific properties
    username: str  # type:ignore
    password: str  # type:ignore

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dhl_germany"
    account_country_code: str = None
    metadata: dict = {}
