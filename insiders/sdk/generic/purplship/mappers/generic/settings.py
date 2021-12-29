"""Purplship Generic client settings."""

from typing import List
import attr
from jstruct.types import JList, REQUIRED, JStruct
from purplship.core.models import ServiceLevel, LabelTemplate
from purplship.universal.mappers.rating_proxy import RatingMixinSettings
from purplship.universal.mappers.shipping_proxy import ShippingMixinSettings
from purplship.providers.generic.units import DEFAULT_SERVICES
from purplship.providers.generic.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class _Settings:
    """Generic connection settings."""

    name: str  # noqa

    id: str = None
    test: bool = False
    carrier_id: str = "generic"
    account_country_code: str = None

    label_template: LabelTemplate = JStruct[LabelTemplate]
    services: List[ServiceLevel] = JList[ServiceLevel, not REQUIRED, dict(default=DEFAULT_SERVICES)]  # type: ignore


@attr.s(auto_attribs=True)
class Settings(BaseSettings, RatingMixinSettings, ShippingMixinSettings, _Settings):
    """Generic connection settings."""

    pass
