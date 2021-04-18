from typing import Tuple, List, Optional
from tnt_lib.shipment_response import document
from purplship.core.models import (
    ShipmentRequest,
    Message,
    ShipmentDetails,
)
from purplship.core.utils import (
    Serializable,
    Pipeline,
    Element,
    Job,
    XP,
)
from purplship.providers.tnt.shipment.label import create_label_request, parse_label_response
from purplship.providers.tnt.shipment.request import create_shipment_request
from purplship.providers.tnt.error import parse_error_response
from purplship.providers.tnt.utils import Settings


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    shipment = _extract_detail(response, settings)

    return shipment, parse_error_response(response, settings)


def _extract_detail(response: Element, settings: Settings) -> Optional[ShipmentDetails]:
    activity: document = XP.find("document", response, element_type=document, first=True)

    if activity is None or activity.CREATE.SUCCESS != 'Y':
        return None

    label = parse_label_response(response)

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        label=label,
        tracking_number=activity.CREATE.CONNUMBER,
        shipment_identifier=activity.CREATE.CONREF,
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[Pipeline]:

    def _create_shipment_request(_) -> Job:
        return Job(id='create', data=create_shipment_request(payload, settings))

    def _create_label_request(shipment_response: str) -> Job:
        activity = XP.build(document, XP.to_xml(shipment_response))
        fallback = shipment_response if activity is None else None
        data = (create_label_request(activity, payload, settings) if activity is None else None)

        return Job(id='create', data=data, fallback=fallback)

    request: Pipeline = Pipeline(
        create=_create_shipment_request,
        get_label=_create_label_request
    )

    return Serializable(request)
