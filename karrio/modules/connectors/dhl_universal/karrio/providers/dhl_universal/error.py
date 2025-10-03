from typing import List
from karrio.schemas.dhl_universal.tracking import Error
from karrio.providers.dhl_universal import Settings
from karrio.core.models import Message


def parse_error_response(response: List[dict], settings: Settings) -> List[Message]:
    errors = [Error(**e) for e in response]
    return [
        Message(
            # context info
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            # carrier error info
            code=str(error.status),
            message=error.detail,
            details=dict(title=error.title, instance=error.instance),
        )
        for error in errors
    ]
