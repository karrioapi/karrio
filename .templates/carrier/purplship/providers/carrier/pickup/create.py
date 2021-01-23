from typing import Tuple, List
from purplship.core.utils import (
    Serializable,
)
from purplship.core.models import (
    PickupRequest,
    Message,
    PickupDetails,
)
from purplship.providers.carrier.utils import Settings, reformat_time
from purplship.providers.carrier.error import parse_error_response


def parse_pickup_response(response, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    pickup = _extract_detail(response, settings)
    return pickup, parse_error_response(response, settings)


def _extract_detail(response, settings: Settings) -> PickupDetails:
    # return PickupDetails(
    #     carrier_name=settings.carrier_name,
    #     carrier_id=settings.carrier_id,
    #     ...
    # )
    pass


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable['CarrierPickupRequest']:

    # request = CarrierPickupRequest(
    #     ...
    # )
    #
    # return Serializable(request, _request_serializer)
    pass


def _request_serializer(request: 'CarrierPickupRequest') -> str:
    pass
