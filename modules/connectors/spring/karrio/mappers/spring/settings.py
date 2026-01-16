"""Karrio Spring client settings."""

import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.providers.spring.units as provider_units
import karrio.providers.spring.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """Spring connection settings."""

    # Carrier-specific credentials
    api_key: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "spring"
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
