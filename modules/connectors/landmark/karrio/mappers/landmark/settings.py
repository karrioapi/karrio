"""Karrio Landmark Global client settings."""

import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.universal.mappers.rating_proxy as rating_proxy
import karrio.providers.landmark.units as provider_units
import karrio.providers.landmark.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """Landmark Global connection settings."""

    # Add carrier specific API connection properties here
    username: str
    password: str
    client_id: str
    account_number: str = None
    region: str = "Landmark CMH"  # Default BE region

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "landmark"
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
    account_country_code: str = None  # Default to BE region
    metadata: dict = {}
    config: dict = {}

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
