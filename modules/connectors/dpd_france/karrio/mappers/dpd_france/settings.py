"""Karrio DPD France client settings."""

import attr
import jstruct
import karrio.core.models as models
import karrio.providers.dpd_france.units as provider_units
import karrio.providers.dpd_france.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings):
    """DPD France connection settings."""

    userid: str  # type: ignore
    password: str = attr.ib(metadata={"sensitive": True})  # type: ignore
    customer_center_number: str = None  # type: ignore
    customer_number: str = None  # type: ignore
    language: str = "EN"  # type: ignore
    customer_country_code: str = "250"  # type: ignore

    id: str = None
    test_mode: bool = False
    carrier_id: str = "dpd_france"
    account_country_code: str = "FR"
    services: list[models.ServiceLevel] = jstruct.JList[
        models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)
    ]  # type: ignore
    metadata: dict = {}
    config: dict = {}

    @property
    def shipping_services(self) -> list[models.ServiceLevel]:
        if any(self.services or []):
            return self.services
        return provider_units.DEFAULT_SERVICES
