"""Karrio Chronopost client settings."""

from typing import List
import attr
from jstruct.types import JList
from karrio.core.models import ServiceLevel
from karrio.providers.chronopost.units import DEFAULT_SERVICES
from karrio.providers.chronopost.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Chronopost connection settings."""

    account_number: str  # type: ignore
    password: str  # type: ignore
    id_emit: str = "CHRFR"  # type: ignore

    id: str = None
    test: bool = False
    carrier_id: str = "chronopost"
    account_country_code: str = "FR"
