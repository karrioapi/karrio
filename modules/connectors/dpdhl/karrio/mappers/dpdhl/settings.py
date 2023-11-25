"""Karrio Deutsche Post DHL client settings."""

import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.providers.dpdhl.utils as provider_utils
import karrio.providers.dpdhl.units as provider_units
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """Deutsche Post DHL connection settings."""

    # required carrier specific properties
    username: str  # type:ignore
    password: str  # type:ignore
    app_id: str = ""
    app_token: str = ""
    zt_id: str = ""
    zt_password: str = ""
    account_number: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpdhl"
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
