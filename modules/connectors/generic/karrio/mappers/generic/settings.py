"""Karrio Generic client settings."""

from typing import List
import attr
from jstruct.types import JList, JStruct
from karrio.core.models import ServiceLevel, LabelTemplate
from karrio.universal.mappers.rating_proxy import RatingMixinSettings
from karrio.universal.mappers.shipping_proxy import ShippingMixinSettings
from karrio.providers.generic.units import DEFAULT_SERVICES
from karrio.providers.generic.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings, RatingMixinSettings, ShippingMixinSettings):
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

    label_template: LabelTemplate = JStruct[LabelTemplate]
    services: List[ServiceLevel] = JList[ServiceLevel, False, dict(default=DEFAULT_SERVICES)]  # type: ignore
