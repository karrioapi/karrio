from typing import List
from pyeshipper.error import ErrorType
from purplship.core.models import Message
from purplship.core.utils import Element, XP
from purplship.providers.eshipper.utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    errors = XP.find("Error", response)
    return [_extract_error(node, settings) for node in errors]


def _extract_error(error_node: Element, settings: Settings) -> Message:
    error = XP.build(ErrorType, error_node)
    return Message(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        message=(error.Message or "Not Detailed"),
    )
