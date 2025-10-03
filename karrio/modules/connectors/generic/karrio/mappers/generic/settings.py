"""Karrio Generic client settings."""

import attr
import typing
import jstruct
import karrio.core.models as models
import karrio.providers.generic.units as provider_units
import karrio.providers.generic.utils as provider_utils
import karrio.universal.mappers.rating_proxy as rating_proxy
import karrio.universal.mappers.shipping_proxy as shipping_proxy


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings, rating_proxy.RatingMixinSettings, shipping_proxy.ShippingMixinSettings):
    """Generic connection settings."""

    display_name: str
    custom_carrier_name: str

    test_mode: bool = False
    carrier_id: str = "custom-carrier"
    account_country_code: str = None
    account_number: str = None
    metadata: dict = {}
    config: dict = {}
    id: str = None

    label_template: models.LabelTemplate = jstruct.JStruct[models.LabelTemplate]
    services: typing.List[models.ServiceLevel] = jstruct.JList[models.ServiceLevel, False, dict(default=provider_units.DEFAULT_SERVICES)]  # type: ignore

    @property
    def shipping_services(self) -> typing.List[models.ServiceLevel]:
        if any(self.services or []):
            return self.services

        return provider_units.DEFAULT_SERVICES
