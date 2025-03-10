from typing import List
from karrio.schemas.royalmail.errors import Errors
from karrio.providers.royalmail import Settings
from karrio.core.models import Message


def parse_error_response(response: List[dict], settings: Settings) -> List[Message]:
    errors = [Errors(**e) for e in response]

    return [
        Message(
            # context info
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            # carrier error info
            code=str(error.httpCode),
            message=error.httpMessage,
            details=dict(information=error.moreInformation, errors=error.errors),
        )
        for error in errors
    ]
