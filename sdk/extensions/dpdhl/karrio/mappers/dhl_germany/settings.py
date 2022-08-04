"""Karrio Deutsche Post DHL client settings."""

import attr
import karrio.providers.dpdhl.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """Deutsche Post DHL connection settings."""

    # required carrier specific properties
    username: str  # type:ignore
    password: str  # type:ignore
    customer_number: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpdhl"
    account_country_code: str = None
    metadata: dict = {}
