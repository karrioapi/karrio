from purplship.providers.canpar.shipment.process import process_shipment_request, parse_shipment_response
from purplship.providers.canpar.shipment.void import void_shipment_request, parse_void_shipment_response
from purplship.providers.canpar.shipment.label import get_label_request, LabelRequest
from functools import partial
from pycanpar.CanshipBusinessService import Shipment
from purplship.core.models import ShipmentRequest
from purplship.core.utils import (
    Serializable,
    Pipeline,
    Job,
    to_xml,
    build
)
from purplship.providers.canpar.utils import Settings


def create_shipment_pipeline(payload: ShipmentRequest, settings: Settings) -> Serializable[Pipeline]:

    request: Pipeline = Pipeline(
        process=lambda *_: _process_shipment(payload, settings),
        get_label=partial(_get_label, settings=settings)
    )

    return Serializable(request)


def _process_shipment(payload: ShipmentRequest, settings: Settings) -> Job:

    return Job(id="process", data=process_shipment_request(payload, settings))


def _get_label(shipment_response: str, settings: Settings) -> Job:
    response = to_xml(shipment_response)
    shipment = build(
        Shipment, next(iter(response.xpath(".//*[local-name() = $name]", name="shipment")), None)
    )
    success = (shipment is not None and shipment.id is not None)
    data = (
        get_label_request(LabelRequest(shipment_id=shipment.id), settings)
        if success else
        None
    )

    return Job(id="get_label", data=data, fallback=("" if not success else None))
