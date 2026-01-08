"""Karrio PostAT client settings."""

import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.providers.postat.units as provider_units
import karrio.providers.postat.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """PostAT connection settings."""

    # Required credentials (from Austrian Post onboarding)
    client_id: str
    org_unit_id: str
    org_unit_guid: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "postat"
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
    account_country_code: str = "AT"
    metadata: dict = {}
    config: dict = {}

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
