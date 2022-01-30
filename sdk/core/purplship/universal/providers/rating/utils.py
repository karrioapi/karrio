import attr
from typing import List, Tuple
from jstruct import JList

from purplship.core.settings import Settings as BaseSettings
from purplship.core.models import ServiceLevel

PackageServices = List[Tuple[str, List[ServiceLevel]]]


@attr.s(auto_attribs=True)
class RatingMixinSettings(BaseSettings):
    """Universal rating settings mixin."""

    # Additional properties
    services: List[ServiceLevel] = JList[ServiceLevel]
