from typing import List
from pypurolator.estimate_service_2_1_2 import Error
from purplship.core.models import Message
from purplship.core.utils.xml import Element
from .utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    errors = response.xpath(".//*[local-name() = $name]", name="Error")
    return [_extract_error(node, settings) for node in errors]


def _extract_error(error_node: Element, settings: Settings) -> Message:
    error = Error()
    error.build(error_node)
    return Message(
        code=error.Code,
        message=error.Description,
        carrier=settings.carrier,
        carrier_name=settings.carrier_name,
        details=dict(AdditionalInformation=error.AdditionalInformation)
        if error.AdditionalInformation is not None
        else None,
    )
