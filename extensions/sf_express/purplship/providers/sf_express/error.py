from typing import List
from purplship.core.models import Message
from purplship.core.utils import Element
from purplship.providers.sf_express import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    if response.get('success', False) is True:
        return []

    return [
        Message(
            # context info
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,

            # carrier error info
            code=response.get('errorCode'),
            message=response.get('errorMsg')
        )
    ]