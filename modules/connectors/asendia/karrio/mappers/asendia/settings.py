"""Karrio Asendia client settings."""

import attr
import jstruct
import karrio.core.models as models
import karrio.providers.asendia.units as provider_units
import karrio.providers.asendia.utils as provider_utils
from karrio.universal.mappers.rating_proxy import RatingMixinSettings


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, RatingMixinSettings):
    """Asendia connection settings."""

    # Asendia API credentials (required)
    username: str
    password: str
    # password: str = attr.ib(metadata={"sensitive": True})

    # Customer ID for API operations
    customer_id: str = None

    # Generic properties
    id: str = None
    test_mode: bool = False
    carrier_id: str = "asendia"
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}

    services: list[models.ServiceLevel] = jstruct.JList[
        models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)
    ]  # type: ignore

    @property
    def shipping_services(self) -> list[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
