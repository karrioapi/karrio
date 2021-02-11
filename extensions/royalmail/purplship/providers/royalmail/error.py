from typing import List
from royalmail_lib.error import ErrorResponse
from purplship.core.models import Message
from purplship.providers.royalmail import Settings


def parse_error_response(response: List[dict], settings: Settings) -> List[Message]:
    errors = [ErrorResponse(**e) for e in response]

    return [
        Message(
            # context info
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,

            # carrier error info
            code=str(error.httpCode),
            message=error.httpMessage,
            details=dict(
                information=error.moreInformation,
                errors=error.errors
            )
        )
        for error in errors
    ]
