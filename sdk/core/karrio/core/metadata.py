"""Karrio Extension Metadata definition module."""
import attr
from enum import Enum
from typing import Optional, Type, List, Dict

from karrio.api.proxy import Proxy
from karrio.api.mapper import Mapper
from karrio.core.settings import Settings
from karrio.core.models import ServiceLevel


@attr.s(auto_attribs=True)
class Metadata:
    """Karrio extension metadata.
    Used to describe and define a karrio compatible extension for a carrier webservice integration.
    """

    label: str

    # Integrations
    Mapper: Type[Mapper]
    Proxy: Type[Proxy]
    Settings: Type[Settings]

    # Data Units
    services: Optional[Type[Enum]] = None
    options: Optional[Type[Enum]] = None
    package_presets: Optional[Type[Enum]] = None
    packaging_types: Optional[Type[Enum]] = None
    service_levels: Optional[List[ServiceLevel]] = None

    id: Optional[str] = None
    is_hub: Optional[bool] = False
    hub_carriers: Optional[Dict[str, str]] = None

    def __getitem__(self, item):
        return getattr(self, item)
