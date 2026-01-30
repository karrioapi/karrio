"""Karrio DHL Germany client settings."""

import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.providers.dhl_parcel_de.units as provider_units
import karrio.providers.dhl_parcel_de.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """DHL Germany connection settings."""

    # carrier specific properties
    username: str = None
    password: str = None
    client_id: str = None
    client_secret: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dhl_parcel_de"
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
