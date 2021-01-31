from typing import Tuple, List
from boxknight_lib.rates import (
    RateRequest as BoxKnightRateRequest,
)
from purplship.core.utils import Serializable
from purplship.core.models import (
    RateRequest,
    RateDetails,
    Message
)

from purplship.providers.boxknight.error import parse_error_response
from purplship.providers.boxknight.utils import Settings


def parse_rate_response(response: dict, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    errors = parse_error_response(response, settings)
    details: List[RateDetails] = []

    return details, errors


def rate_request(payload: RateRequest, _) -> Serializable:

    request = BoxKnightRateRequest(
        postalCode=payload.recipient.postal_code,
        originPostalCode=payload.shipper.postal_code
    )

    return Serializable(request)
