"""Karrio DTDC client settings."""

import attr
import typing
import jstruct

import karrio.core.models as models
import karrio.providers.dtdc.units as provider_units
import karrio.providers.dtdc.utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """DTDC connection settings."""

    # DTDC specific API connection properties
    api_key: str  # API key for authentication
    customer_code: str  # Customer code for DTDC account
    username: str = None  # Username for token authentication
    password: str = None  # Password for token authentication

    # generic properties (DO NOT MODIFY)
    id: str = None
    test_mode: bool = False
    carrier_id: str = "dtdc"
    account_country_code: str = "IN"
    metadata: dict = {}
    config: dict = {}
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
