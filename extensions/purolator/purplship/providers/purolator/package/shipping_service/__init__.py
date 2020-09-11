from typing import List, Tuple, cast, Union, Type
from functools import partial
from pypurolator.shipping_service_2_1_3 import (
    CreateShipmentRequest,
    CreateShipmentResponse,
    PIN,
    ValidateShipmentRequest,
)
from pypurolator.shipping_documents_service_1_3_0 import DocumentDetail
from purplship.core.models import ShipmentRequest, ShipmentDetails, Message
from purplship.core.utils import Serializable, Element, to_xml
from purplship.core.utils.pipeline import Pipeline, Job
from purplship.providers.purolator.utils import Settings
from purplship.providers.purolator.error import parse_error_response
from purplship.providers.purolator.package.shipping_service.get_documents import (
    get_shipping_documents_request,
)
from purplship.providers.purolator.package.shipping_service.create_shipping import (
    create_shipping_request,
)

ShipmentRequestType = Type[Union[ValidateShipmentRequest, CreateShipmentRequest]]


def parse_shipment_creation_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    details = next(
        iter(
            response.xpath(".//*[local-name() = $name]", name="CreateShipmentResponse")
        ),
        None,
    )
    shipment = _extract_shipment(response, settings) if details is not None else None
    return shipment, parse_error_response(response, settings)


def _extract_shipment(response: Element, settings: Settings) -> ShipmentDetails:
    shipment = CreateShipmentResponse()
    document = DocumentDetail()
    shipment_nodes = response.xpath(".//*[local-name() = $name]", name="CreateShipmentResponse")
    document_nodes = response.xpath(".//*[local-name() = $name]", name="DocumentDetail")

    next((shipment.build(node) for node in shipment_nodes), None)
    next((document.build(node) for node in document_nodes), None)

    label = next(
        (content for content in [document.Data, document.URL] if content is not None),
        "No label returned"
    )

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=cast(PIN, shipment.ShipmentPIN).Value,
        label=label,
    )


def create_shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[Pipeline]:
    requests: Pipeline = Pipeline(
        validate=lambda *_: partial(_validate_shipment, payload=payload, settings=settings)(),
        create=partial(_create_shipment, payload=payload, settings=settings),
        document=partial(_get_shipment_label, payload=payload, settings=settings),
    )
    return Serializable(requests)


def _validate_shipment(payload: ShipmentRequest, settings: Settings) -> Job:
    return Job(
        id="validate",
        data=create_shipping_request(payload=payload, settings=settings, validate=True).serialize(),
    )


def _create_shipment(validate_response: str, payload: ShipmentRequest, settings: Settings) -> Job:
    errors = parse_error_response(to_xml(validate_response), settings)
    valid = len(errors) == 0
    return Job(
        id="create",
        data=create_shipping_request(payload, settings).serialize() if valid else None,
        fallback=(validate_response if not valid else None),
    )


def _get_shipment_label(create_response: str, payload: ShipmentRequest, settings: Settings) -> Job:
    errors = parse_error_response(to_xml(create_response), settings)
    valid = len(errors) == 0
    shipment_pin = None

    if valid:
        node = next(
            iter(
                to_xml(create_response).xpath(
                    ".//*[local-name() = $name]", name="ShipmentPIN"
                )
            ),
            None,
        )
        pin = PIN()
        pin.build(node)
        shipment_pin = pin.Value

    return Job(
        id="document",
        data=(
            get_shipping_documents_request(shipment_pin, payload, settings).serialize() if valid else None
        ),
        fallback="",
    )
