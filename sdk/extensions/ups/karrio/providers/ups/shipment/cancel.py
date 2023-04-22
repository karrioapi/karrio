from typing import List, Tuple
from ups_lib import common
from ups_lib.void_web_service_schema import (
    VoidShipmentRequest,
    CodeDescriptionType,
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
import karrio.lib as lib


def parse_shipment_cancel_response(
    _response: lib.Deserializable[Element], settings: Settings
) -> Tuple[ConfirmationDetails, List[Message]]:
    response = _response.deserialize()
    status = XP.to_object(
        CodeDescriptionType,
        lib.find_element("ResponseStatus", response, first=True),
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
) -> Serializable:
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

    return lib.Serializable(
        request,
        lambda envelope: lib.envelope_serializer(
            envelope,
            namespace=(
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"'
                ' xmlns:xsd="http://www.w3.org/2001/XMLSchema"'
                ' xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"'
                ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
                ' xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"'
                ' xmlns:void="http://www.ups.com/XMLSchema/XOLTWS/Void/v1.1"'
            ),
            prefixes=dict(
                Request="common",
                Envelope="soapenv",
                UPSSecurity="upss",
                VoidShipmentRequest="void",
            ),
        ),
    )
