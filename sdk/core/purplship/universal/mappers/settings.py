"""Purplship Universal client settings."""

import attr
from typing import List
from jstruct import JList
from purplship.core.models import ServiceLevel
from purplship.core.settings import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Universal connection settings."""

    # Additional universal properties
    services: List[ServiceLevel] = JList[ServiceLevel]

    # Base properties
    id: str = None
    test: bool = False
    carrier_id: str = ""
    account_country_code: str = None
