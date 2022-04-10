from typing import List, Tuple
from karrio.core.utils import Element, Serializable, SF, NF, DP
from karrio.core.models import RateRequest, RateDetails, Message, ChargeDetails
from karrio.core.units import Packages, Options, Services
from karrio.providers.amazon_mws.utils import Settings
from karrio.providers.amazon_mws.units import (
    Service,
    PackagingType,
    Option,
)
from karrio.providers.amazon_mws.error import parse_error_response


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    pass


def _extract_rate(node: Element, settings: Settings) -> RateDetails:
    pass


def rate_request(payload: RateRequest, settings: Settings) -> Serializable:
    pass
