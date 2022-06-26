from typing import List, Tuple
from ups_lib import common
from ups_lib.void_web_service_schema import (
    VoidShipmentRequest,
    CodeDescriptionType,
    RequestType,
    VoidShipmentType,
)
from karrio.core.utils import Envelope, Element, create_envelope, Serializable, XP
from karrio.core.models import (
    ShipmentCancelRequest,
    ConfirmationDetails,
    Message,
)
from karrio.providers.ups.utils import Settings, default_request_serializer
from karrio.providers.ups.error import parse_error_response


def parse_shipment_cancel_response(
    response: Element, settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    status = XP.to_object(
        CodeDescriptionType,
        next(
            iter(response.xpath(".//*[local-name() = $name]", name="ResponseStatus")),
            None,
        ),
    )
    success = status is not None and status.Code == "1"
    cancellation = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Shipment",
        )
        if success
        else None
    )

    return cancellation, parse_error_response(response, settings)


def shipment_cancel_request(
    payload: ShipmentCancelRequest, settings: Settings
) -> Serializable[Envelope]:

    request = create_envelope(
        header_content=settings.Security,
        body_content=VoidShipmentRequest(
            Request=common.RequestType(
                TransactionReference=common.TransactionReferenceType(
                    CustomerContext=payload.shipment_identifier,
                ),
            ),
            VoidShipment=VoidShipmentType(
                ShipmentIdentificationNumber=payload.shipment_identifier,
                TrackingNumber=None,
            ),
        ),
    )

    return Serializable(
        request,
        default_request_serializer(
            "void", 'xmlns:void="http://www.ups.com/XMLSchema/XOLTWS/Void/v1.1"'
        ),
    )
