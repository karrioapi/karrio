from typing import List
from eshipper_lib.error import ErrorType
from karrio.core.models import Message
from karrio.core.utils import Element, XP
from karrio.providers.eshipper.utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    errors = XP.find("Error", response, ErrorType)
    return [_extract_error(node, settings) for node in errors]


def _extract_error(error: ErrorType, settings: Settings) -> Message:
    return Message(
        code="Error",
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        message=error.Message,
    )
