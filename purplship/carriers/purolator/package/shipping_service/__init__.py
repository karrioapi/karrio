from typing import List, Tuple, cast, Union, Type, Dict
from functools import partial
from pypurolator.shipping_service import (
    CreateShipmentRequest, CreateShipmentResponse, PIN, ValidateShipmentRequest, ResponseInformation,
    Error as PurolatorError, ArrayOfError
)
from pypurolator.shipping_documents_service import DocumentDetail
from purplship.core.models import ShipmentRequest, ShipmentDetails, Error
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from purplship.core.utils.helpers import export, to_xml, to_dict
from purplship.carriers.purolator.utils import Settings
from purplship.carriers.purolator.error import parse_error_response
from purplship.carriers.purolator.package.shipping_service.get_documents import get_shipping_documents_request
from purplship.carriers.purolator.package.shipping_service.create_shipping import create_shipping_request

ShipmentRequestType = Type[Union[ValidateShipmentRequest, CreateShipmentRequest]]


def parse_shipment_creation_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Error]]:
    details = next(iter(response.xpath(".//*[local-name() = $name]", name="CreateShipmentResponse")), None)
    shipment = _extract_shipment(response, settings) if details is not None else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(response: Element, settings: Settings) -> ShipmentDetails:
    shipment = CreateShipmentResponse()
    document = DocumentDetail()
    shipment.build(
        next(iter(response.xpath(".//*[local-name() = $name]", name="CreateShipmentResponse")), None)
    )
    document.build(
        next(iter(response.xpath(".//*[local-name() = $name]", name="DocumentDetail")), None)
    )

    label = document.Data if document.Data is not None else None

    return ShipmentDetails(
        carrier=settings.carrier_name,
        tracking_number=cast(PIN, shipment.ShipmentPIN).Value,
        label=label,
    )


def create_shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[Dict]:
    requests = dict(
        validate=partial(_validate_shipment, payload=payload, settings=settings),
        create=partial(_create_shipment, payload=payload, settings=settings),
        document=partial(_get_shipment_label, payload=payload, settings=settings),
    )
    return Serializable(requests)


def _validate_shipment(payload: ShipmentRequest, settings: Settings) -> Dict:
    return dict(
        data=create_shipping_request(payload=payload, settings=settings, validate=True).serialize()
    )


def _create_shipment(validate_response: str, payload: ShipmentRequest, settings: Settings) -> Dict:
    valid = str(to_dict(validate_response)) == str(True)
    return dict(
        data=create_shipping_request(payload, settings).serialize() if valid else None,
        fallback=export(
            ResponseInformation(
                Errors=ArrayOfError(
                    Error=[
                        PurolatorError(
                            Description="Invalid Shipment Request",
                            Code='000000'
                        )
                    ]
                )
            )
        ) if not valid else None
    )


def _get_shipment_label(create_response: str, payload: ShipmentRequest, settings: Settings) -> Dict:
    node = next(
        iter(to_xml(create_response).xpath(".//*[local-name() = $name]", name="ShipmentPIN")),
        None
    )
    pin = PIN()
    if node is not None:
        pin.build(node)
    return dict(
        data=get_shipping_documents_request(pin.Value, payload, settings).serialize() if node is not None else None,
        fallback="",
        service='document'
    )
