"""Karrio Deutsche Post Germany client settings."""

import typing
import attr
import karrio.core.models as models
import karrio.providers.deutschepost.units as provider_units
import karrio.providers.deutschepost.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """Deutsche Post Germany connection settings."""

    # required carrier specific properties
    username: str
    password: str
    dhl_api_key: str
    customer_ekp: str = None

    tracking_consumer_key: str = None
    tracking_consumer_secret: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "deutschepost"
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
