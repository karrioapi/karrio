import karrio.lib as lib
from karrio.core.models import (
    ConfirmationDetails,
    Message,
    ShipmentCancelRequest,
)
from karrio.core.utils import XP, Element, Serializable, create_envelope
from karrio.providers.purolator.error import parse_error_response
from karrio.providers.purolator.utils import Settings, standard_request_serializer
from karrio.schemas.purolator.shipping_service_2_1_3 import (
    PIN,
    RequestContext,
    VoidShipmentRequest,
    VoidShipmentResponse,
)


def parse_shipment_cancel_response(
    _response: lib.Deserializable[Element], settings: Settings
) -> tuple[ConfirmationDetails, list[Message]]:
    response = _response.deserialize()
    void_response = XP.find("VoidShipmentResponse", response, VoidShipmentResponse, first=True)
    voided = void_response is not None and void_response.ShipmentVoided
    cancellation = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=True,
            operation="Cancel Shipment",
        )
        if voided
        else None
    )

    return cancellation, parse_error_response(response, settings)


def shipment_cancel_request(payload: ShipmentCancelRequest, settings: Settings) -> Serializable:
    request = create_envelope(
        header_content=RequestContext(
            Version="2.0",
            Language=settings.language,
            GroupID="",
            RequestReference="",
            UserToken=settings.user_token,
        ),
        body_content=VoidShipmentRequest(PIN=PIN(Value=payload.shipment_identifier)),
    )

    return Serializable(request, standard_request_serializer)
