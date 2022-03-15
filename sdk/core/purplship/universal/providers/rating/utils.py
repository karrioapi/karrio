import attr
from typing import List, Tuple
from jstruct import JList

from karrio.core.settings import Settings as BaseSettings
from karrio.core.models import ServiceLevel

PackageServices = List[Tuple[str, List[ServiceLevel]]]


@attr.s(auto_attribs=True)
class RatingMixinSettings(BaseSettings):
    """Universal rating settings mixin."""

    # Additional properties
    services: List[ServiceLevel] = JList[ServiceLevel]
