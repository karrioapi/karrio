from typing import List
from sendle_lib.validation_error import ValidationError
from purplship.providers.sendle import Settings
from purplship.core.models import Message


def parse_error_response(response: List[dict], settings: Settings) -> List[Message]:
    carrier_errors = [ValidationError(**e) for e in response]
    return [_extract_error(node, settings) for node in carrier_errors]


def _extract_error(carrier_error: ValidationError, settings: Settings) -> Message:
    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=carrier_error.error,
        message=carrier_error.error_description,
        details=carrier_error.messages
    )
