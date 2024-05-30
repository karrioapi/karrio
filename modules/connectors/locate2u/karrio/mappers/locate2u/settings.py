"""Karrio Locate2u client settings."""

import attr
import typing
import jstruct
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.locate2u.utils as provider_utils
import karrio.providers.locate2u.units as provider_units


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Locate2u connection settings."""

    # required carrier specific properties
    client_id: str = None
    client_secret: str = None

    id: str = None
    test_mode: bool = False
    carrier_id: str = "locate2u"
    account_country_code: str = "AU"
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore
    metadata: dict = {}

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
