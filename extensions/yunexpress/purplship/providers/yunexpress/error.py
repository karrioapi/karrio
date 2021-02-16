from typing import List
from yunexpress_lib.error import ErrorResponse
from purplship.core.models import Message
from purplship.providers.yunexpress import Settings


def parse_error_response(response: dict, settings: Settings) -> List[Message]:
    if 'Message' not in response and str(response.get('ResultCode')) == "0000":
        return []

    error = ErrorResponse(**response)

    return [
        Message(
            # context info
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,

            # carrier error info
            code=str(error.ResultCode) if error.ResultCode is not None else None,
            message=error.Message or error.ResultDesc,
            details=dict(MessageDetail=error.MessageDetail)
        )
    ]
