from functools import partial
from typing import Tuple, List

from purplship.core.utils import Element, XP, Serializable
from purplship.core.utils.pipeline import Pipeline, Job
from purplship.core.models import ShipmentRequest, ShipmentDetails, Message

from purplship.providers.canadapost.utils import Settings
import purplship.providers.canadapost.shipment.contract as contract
import purplship.providers.canadapost.shipment.non_contract as non_contract


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Message]]:
    if settings.contract_id is None or settings.contract_id == "":
        return non_contract.parse_shipment_response(response, settings)
    return contract.parse_shipment_response(response, settings)


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[Pipeline]:
    requests: Pipeline = Pipeline(
        create_shipment=lambda *_: _create_shipment(payload, settings),
        retrieve_label=partial(_get_shipment_label),
    )
    return Serializable(requests)


def _create_shipment(payload: ShipmentRequest, settings: Settings) -> Job:
    no_contract = settings.contract_id is None or settings.contract_id == ""
    create_shipment = (
        non_contract.shipment_request if no_contract else contract.shipment_request
    )
    return Job(
        id="non_contract_shipment" if no_contract else "contract_shipment",
        data=create_shipment(payload, settings),
    )


def _get_shipment_label(shipement_response: str) -> Job:
    response = XP.to_xml(shipement_response)
    has_errors = len(response.xpath(".//*[local-name() = $name]", name="message")) > 0
    links = response.xpath(".//*[local-name() = $name]", name="link")
    href, media = next(
        ((link.get("href"), link.get("media-type")) for link in links if link.get("rel") == "label"),
        (None, None),
    )
    data = None if has_errors else dict(href=href, media=media)

    return Job(id="shipment_label", data=data, fallback="")
