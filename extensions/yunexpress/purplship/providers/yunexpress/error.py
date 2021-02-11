from typing import List
from yunexpress_lib.error import Error
from purplship.core.utils import Element, XP
from purplship.core.models import Message
from purplship.providers.yunexpress import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    errors = [XP.build(Error, e) for e in response.xpath(".//*[local-name() = $name]", name="Error")]

    return [
        Message(
            # context info
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,

            # carrier error info
            message=e.Message,
            details=dict(MessageDetail=e.MessageDetail)
        )
        for e in errors
    ]
