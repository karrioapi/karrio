from typing import Tuple, List
from purplship.core.utils import (
    Serializable,
)
from purplship.core.models import (
    ShipmentRequest,
    Message,
    ShipmentDetails,
    ChargeDetails,
)
from purplship.providers.carrier.utils import Settings
from purplship.providers.carrier.error import parse_error_response


def parse_shipment_response(response, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    shipment = _extract_detail(response, settings)
    return shipment, parse_error_response(response, settings)


def _extract_detail(response, settings: Settings) -> ShipmentDetails:

    # return ShipmentDetails(
    #     carrier_name=settings.carrier_name,
    #     carrier_id=settings.carrier_id,
    #     ...
    # )
    pass


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable['CarrierShipmentCancelRequest']:

    # request = CarrierShipmentCancelRequest(
    #     ...
    # )
    #
    # return Serializable(request, _request_serializer)
    pass


def _request_serializer(request: 'CarrierShipmentCancelRequest') -> str:
    pass
