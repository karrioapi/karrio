from typing import List
from pyeshipper.error import ErrorType
from purplship.core.models import Message
from purplship.core.utils.xml import Element
from purplship.providers.eshipper.utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    errors = response.xpath(".//*[local-name() = $name]", name="Error")
    return [_extract_error(node, settings) for node in errors]


def _extract_error(error_node: Element, settings: Settings) -> Message:
    error = ErrorType()
    error.build(error_node)
    return Message(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        message=error.Message,
    )
