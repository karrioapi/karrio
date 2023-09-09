"""Karrio DHL Parcel Poland client settings."""

import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.providers.dhl_poland.units as provider_units
import karrio.providers.dhl_poland.utils as provider_utils
from karrio.universal.mappers.rating_proxy import RatingMixinSettings


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, RatingMixinSettings):
    """DHL Parcel Poland connection settings."""

    username: str  # type: ignore
    password: str  # type: ignore
    account_number: str = None

    id: str = None
    test_mode: bool = False
    carrier_id: str = "dhl_poland"
    account_country_code: str = "PL"
    metadata: dict = {}
    config: dict = {}

    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
