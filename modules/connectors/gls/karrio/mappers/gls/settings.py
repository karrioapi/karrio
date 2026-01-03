"""Karrio GLS Group client settings."""

import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.providers.gls.units as provider_units
import karrio.providers.gls.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """GLS Group connection settings."""

    # OAuth2 credentials
    client_id: str
    client_secret: str

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "gls"
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
