from typing import List
from purplship.providers.sendle import Settings
from purplship.core.models import Message


def parse_error_response(response: List[dict], settings: Settings) -> List[Message]:
    return [_extract_error(e, settings) for e in response]


def _extract_error(carrier_error: dict, settings: Settings) -> Message:
    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=carrier_error.get('Code'),
        message=carrier_error.get('Message')
    )
