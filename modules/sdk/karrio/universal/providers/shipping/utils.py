import attr
from jstruct import JList, JStruct

from karrio.core.models import LabelTemplate, ServiceLevel
from karrio.core.settings import Settings as BaseSettings


@attr.s(auto_attribs=True)
class ShippingMixinSettings(BaseSettings):
    """Universal shipping mixin settings."""

    display_name: str = "Custom Carrier"
    custom_carrier_name: str = "custom_carrier"

    # Additional properties
    services: list[ServiceLevel] = JList[ServiceLevel]
    label_template: LabelTemplate = JStruct[LabelTemplate]
    metadata: dict = {}
