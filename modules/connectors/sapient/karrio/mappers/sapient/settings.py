"""Karrio SAPIENT client settings."""

import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.providers.sapient.utils as provider_utils
import karrio.providers.sapient.units as provider_units


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """SAPIENT connection settings."""

    # Add carrier specific API connection properties here
    client_id: str
    client_secret: str
    shipping_account_id: str
    sapient_carrier_code: provider_utils.SapientCarrierCode = "RM"  # type: ignore

    # generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "sapient"
    account_country_code: str = "GB"
    metadata: dict = {}
    config: dict = {}

    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
