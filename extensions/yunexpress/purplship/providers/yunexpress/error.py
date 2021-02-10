from typing import List
from yunexpress_lib.tracking import Response
from purplship.core.utils import Element, XP
from purplship.core.models import Message
from purplship.providers.yunexpress import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    response = XP.build(Response, response)

    if response.ResultCode == '0000':
        return []

    return [Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=response.ResultCode,
        message=response.ResultDesc
    )]
