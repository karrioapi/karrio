import attr
from jstruct import JStruct

from purplship.core.settings import Settings as BaseSettings
from purplship.core.models import LabelTemplate


@attr.s(auto_attribs=True)
class ShippingMixinSettings(BaseSettings):
    """Universal shipping mixin settings."""

    # Additional properties
    label_template: LabelTemplate = JStruct[LabelTemplate]
