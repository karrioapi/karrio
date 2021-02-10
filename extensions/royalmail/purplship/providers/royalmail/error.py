from typing import List
from royalmail_lib.error import Error
from purplship.core.models import Message
from purplship.providers.royalmail import Settings


def parse_error_response(response: dict, settings: Settings) -> List[Message]:
    carrier_errors: List[dict] = response.get('errors', [])
    return [_extract_error(Error(**e), settings) for e in carrier_errors]


def _extract_error(carrier_error: Error, settings: Settings) -> Message:
    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=carrier_error.errorCode,
        message=carrier_error.errorDescription,
        details=dict(
            errorCause=carrier_error.errorCause,
            errorResolution=carrier_error.errorResolution
        )
    )
