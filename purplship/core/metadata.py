"""Purplship Extension Metadata definition module."""
import attr
from enum import Enum
from typing import Optional, Type

from purplship.api.proxy import Proxy
from purplship.api.mapper import Mapper
from purplship.core.settings import Settings


@attr.s(auto_attribs=True)
class Metadata:
    """Purplship extension metadata.
    Used to describe and define a purplship compatible extension for a carrier webservice integration.
    """

    label: str

    # Integrations
    Mapper: Type[Mapper]
    Proxy: Type[Proxy]
    Settings: Type[Settings]

    # Data Units
    services: Optional[str] = None
    options: Optional[Type[Enum]] = None
    package_presets: Optional[Type[Enum]] = None
    packaging_types: Optional[Type[Enum]] = None

    def __getitem__(self, item):
        return getattr(self, item)
