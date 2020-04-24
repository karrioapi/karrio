from functools import partial
from typing import Tuple, List
from purplship.core.utils import Element, to_xml, Serializable
from purplship.core.utils.pipeline import Pipeline, Job
from purplship.core.models import ShipmentRequest, ShipmentDetails, Message
from purplship.carriers.canadapost.utils import Settings
from purplship.carriers.canadapost.shipment.contract_shipment import (
    parse_contract_shipment_response,
    contract_shipment_request,
)
from purplship.carriers.canadapost.shipment.non_contract_shipment import (
    parse_non_contract_shipment_response,
    non_contract_shipment_request,
)


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    if settings.contract_id is None or settings.contract_id == "":
        return parse_non_contract_shipment_response(response, settings)
    return parse_contract_shipment_response(response, settings)


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[Pipeline]:
    requests: Pipeline = Pipeline(
        create_shipment=lambda *_: partial(_create_shipment, payload=payload, settings=settings)(),
        retrieve_label=partial(_get_shipment_label),
    )
    return Serializable(requests)


def _create_shipment(payload: ShipmentRequest, settings: Settings) -> Job:
    no_contract = settings.contract_id is None or settings.contract_id == ""
    create_shipment = (non_contract_shipment_request if no_contract else contract_shipment_request)
    return Job(
        id="non_contract_shipment" if no_contract else "contract_shipment",
        data=create_shipment(payload, settings)
    )


def _get_shipment_label(shipement_response: str) -> Job:
    links = to_xml(shipement_response).xpath(".//*[local-name() = $name]", name="link")
    label_url = next(
        (link.get("href") for link in links if link.get("rel") == "label"),
        None,
    )
    return Job(id="shipment_label", data=label_url, fallback="")
