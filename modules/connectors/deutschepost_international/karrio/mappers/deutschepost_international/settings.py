"""Karrio Deutsche Post International client settings."""

import attr
import typing
import jstruct
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.deutschepost_international.units as provider_units
import karrio.providers.deutschepost_international.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """Deutsche Post International connection settings."""

    # required carrier specific properties
    consumer_key: str
    consumenr_secret: str
    customer_ekp: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "deutschepost_international"
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
    cache: lib.Cache = jstruct.JStruct[lib.Cache, False, dict(default=lib.Cache())]
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
