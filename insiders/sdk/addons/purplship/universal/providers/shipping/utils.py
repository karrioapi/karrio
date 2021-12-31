from typing import List
import attr
from jstruct import JStruct, JList

from purplship.core.settings import Settings as BaseSettings
from purplship.core.models import LabelTemplate
from purplship.core.models import ServiceLevel


@attr.s(auto_attribs=True)
class ShippingMixinSettings(BaseSettings):
    """Universal shipping mixin settings."""

    # Additional properties
    services: List[ServiceLevel] = JList[ServiceLevel]
    label_template: LabelTemplate = JStruct[LabelTemplate]
