from typing import Tuple, List
from purplship.core.utils import Serializable
from purplship.core.models import (
    ShipmentCancelRequest,
    Message,
    ConfirmationDetails,
)
from purplship.providers.carrier.utils import Settings
from purplship.providers.carrier.error import parse_error_response


def parse_shipment_cancel_response(response, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    successful = True  # retrieve success status from `response`
    cancellation = (
        ConfirmationDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            success=successful,
            operation="Cancel Shipment",
        )
        if successful
        else None
    )

    return cancellation, parse_error_response(response, settings)


def shipment_cancel_request(payload: ShipmentCancelRequest, settings: Settings) -> Serializable['CarrierShipmentCancelRequest']:

    # request = CarrierShipmentCancelRequest(
    #     ...
    # )
    #
    # return Serializable(request, _request_serializer)
    pass


def _request_serializer(request: 'CarrierShipmentCancelRequest') -> str:
    pass
