from typing import List
from purplship.providers.dhl_universal import Settings
from purplship.core.models import Message


def parse_error_response(response: dict, settings: Settings) -> List[Message]:
    if 'shipments' in response:
        return []

    return [Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=response.get("status"),
        message=response.get("detail"),
        details=dict(
            title=response.get("title"),
            instance=response.get("instance")
        )
    )]
