from typing import List
from purplship.providers.yunexpress import Settings
from purplship.core.models import Message


def parse_error_response(response, settings: Settings) -> List[Message]:
    carrier_errors = []  # retrieve carrier errors from `response`
    return [_extract_error(node, settings) for node in carrier_errors]


def _extract_error(carrier_error, settings: Settings) -> Message:
    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=carrier_error.code,
        message=carrier_error.description,
        details=carrier_error.details
    )
