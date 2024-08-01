"""Karrio Colissimo client settings."""

import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.providers.colissimo.utils as provider_utils
import karrio.providers.colissimo.units as provider_units


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Colissimo connection settings."""

    # required carrier specific properties
    password: str
    contract_number: str
    laposte_api_key: str = None

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "colissimo"
    account_country_code: str = "FR"
    metadata: dict = {}
    config: dict = {}

    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
