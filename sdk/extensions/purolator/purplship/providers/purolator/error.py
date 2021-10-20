from typing import List
from purolator_lib.estimate_service_2_1_2 import Error
from purplship.core.models import Message
from purplship.core.utils.xml import Element
from purplship.core.utils.soap import extract_fault
from .utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    errors = response.xpath(".//*[local-name() = $name]", name="Error")
    return [_extract_error(node, settings) for node in errors] + extract_fault(
        response, settings
    )


def _extract_error(error_node: Element, settings: Settings) -> Message:
    error = Error()
    error.build(error_node)
    return Message(
        code=error.Code,
        message=error.Description,
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        details=dict(AdditionalInformation=error.AdditionalInformation)
        if error.AdditionalInformation is not None
        else None,
    )
