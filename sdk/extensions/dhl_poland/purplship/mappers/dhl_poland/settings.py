"""Purplship DHL Parcel Poland client settings."""

from typing import List
import attr
from jstruct.types import JList
from purplship.core.models import ServiceLevel
from purplship.universal.mappers import Settings as UniversalSettings
from purplship.providers.dhl_poland.utils import (
    Settings as BaseSettings,
    DEFAULT_SERVICES,
)


@attr.s(auto_attribs=True)
class Settings(BaseSettings, UniversalSettings):
    """DHL Parcel Poland connection settings."""

    username: str
    password: str
    account_number: str = None

    id: str = None
    test: bool = False
    carrier_id: str = "dhl_poland"
    account_country_code: str = "PL"

    services: List[ServiceLevel] = JList[ServiceLevel, False, dict(default=DEFAULT_SERVICES)]  # type: ignore
