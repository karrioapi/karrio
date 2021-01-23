from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import (
    PickupCancelRequest,
    Message,
    ConfirmationDetails,
)
from purplship.providers.carrier.utils import Settings, reformat_time
from purplship.providers.carrier.error import parse_error_response


def parse_pickup_cancel_response(response, settings) -> Tuple[ConfirmationDetails, List[Message]]:
    successful = True  # retrieve success status from `response`
    cancellation = (
        ConfirmationDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            success=successful,
            operation="Cancel Pickup",
        )
        if successful
        else None
    )

    return cancellation, parse_error_response(response, settings)


def pickup_cancel_request(payload: PickupCancelRequest, settings: Settings) -> Serializable['CarrierPickupCancelRequest']:

    # request = CarrierPickupCancelRequest(
    #     ...
    # )
    #
    # return Serializable(request, _request_serializer)
    pass


def _request_serializer(request: 'CarrierPickupCancelRequest') -> str:
    pass
