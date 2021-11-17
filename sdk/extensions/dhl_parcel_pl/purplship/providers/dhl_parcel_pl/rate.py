import time
from functools import partial
from typing import List, Tuple, Optional
from purplship.core.models import RateRequest, RateDetails, Message, ChargeDetails
from purplship.core.units import Packages, Services, Options
from purplship.core.utils import (
    Serializable,
    Envelope,
    create_envelope,
    Element,
    NF,
    XP,
    DF,
)
from purplship.providers.dhl_parcel_pl.error import parse_error_response
from purplship.providers.dhl_parcel_pl.utils import Settings
from purplship.providers.dhl_parcel_pl.units import (
    WeightUnit,
    DimensionUnit,
    Option,
    Service,
    Charges,
)


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    pass


def _extract_rate_details(node: Element, settings: Settings) -> RateDetails:
    pass


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[Envelope]:
    pass
