from typing import Tuple, List
from purplship.core.utils import (
    Serializable,
)
from purplship.core.models import (
    Message,
    PickupDetails,
    PickupUpdateRequest,
)
from purplship.providers.carrier.utils import Settings
from purplship.providers.carrier.error import parse_error_response


def parse_pickup_update_response(response, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    pickup = _extract_detail(response, settings)
    return pickup, parse_error_response(response, settings)


def _extract_detail(response, settings: Settings) -> PickupDetails:
    # return PickupDetails(
    #     carrier_name=settings.carrier_name,
    #     carrier_id=settings.carrier_id,
    #     ...
    # )
    pass


def pickup_update_request(payload: PickupUpdateRequest, settings: Settings) -> Serializable['CarrierPickupUpdateRequest']:

    # request = CarrierPickupUpdateRequest(
    #     ...
    # )
    #
    # return Serializable(request, _request_serializer)
    pass


def _request_serializer(request: 'CarrierPickupUpdateRequest') -> str:
    pass
