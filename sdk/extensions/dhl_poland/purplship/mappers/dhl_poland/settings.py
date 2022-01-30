"""Purplship DHL Parcel Poland client settings."""

from typing import List
import attr
from jstruct.types import JList
from purplship.core.models import ServiceLevel
from purplship.universal.mappers.rating_proxy import RatingMixinSettings
from purplship.providers.dhl_poland.units import DEFAULT_SERVICES
from purplship.providers.dhl_poland.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings, RatingMixinSettings):
    """DHL Parcel Poland connection settings."""

    username: str  # type: ignore
    password: str  # type: ignore
    account_number: str = None

    id: str = None
    test: bool = False
    carrier_id: str = "dhl_poland"
    account_country_code: str = "PL"

    services: List[ServiceLevel] = JList[ServiceLevel, False, dict(default=DEFAULT_SERVICES)]  # type: ignore
