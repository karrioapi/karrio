from typing import List, Tuple

from purplship.core.utils import Serializable, Element
from purplship.core.models import RateDetails, Message, ChargeDetails, RateRequest
from purplship.providers.tnt.utils import Settings
from purplship.providers.tnt.error import parse_error_response


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    details = []  # retrieve details from `response`
    tracking_details = [_extract_detail(detail, settings) for detail in details]

    return tracking_details, parse_error_response(response, settings)


def _extract_detail(detail, settings: Settings) -> RateDetails:

    # return RateDetails(
    #     carrier_name=settings.carrier_name,
    #     carrier_id=settings.carrier_id,
    #
    #     ...
    # )
    pass


def rate_request(payload: RateRequest, settings: Settings) -> Serializable['CarrierRateRequest']:

    # request = CarrierRateRequest(
    #     ...
    # )
    #
    # return Serializable(request, _request_serializer)
    pass


def _request_serializer(request: 'CarrierRateRequest') -> str:
    pass
