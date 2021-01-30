from typing import Tuple, List
from functools import partial
from purolator_lib.shipping_service_2_1_3 import (
    VoidShipmentRequest,
    VoidShipmentResponse,
    RequestContext,
    PIN,
)
from purplship.core.models import (
    ShipmentCancelRequest,
    ConfirmationDetails,
    Message,
)
from purplship.core.utils import Serializable, create_envelope, Envelope, Element, XP
from purplship.providers.purolator_courier.error import parse_error_response
from purplship.providers.purolator_courier.utils import Settings, standard_request_serializer


def parse_shipment_cancel_response(
    response: Element, settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    void_response = XP.build(VoidShipmentResponse, next(
        iter(response.xpath(".//*[local-name() = $name]", name="VoidShipmentResponse")),
        None
    ))
    voided = void_response is not None and void_response.ShipmentVoided
    cancellation = ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=True,
        operation="Cancel Shipment",
    ) if voided else None

    return cancellation, parse_error_response(response, settings)


def shipment_cancel_request(
    payload: ShipmentCancelRequest, settings: Settings
) -> Serializable[Envelope]:

    request = create_envelope(
        header_content=RequestContext(
            Version="2.0",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=VoidShipmentRequest(
            PIN=PIN(Value=payload.shipment_identifier)
        ),
    )

    return Serializable(request, standard_request_serializer)
