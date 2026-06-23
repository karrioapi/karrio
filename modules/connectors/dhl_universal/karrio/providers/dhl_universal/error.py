from karrio.core.models import Message
from karrio.providers.dhl_universal.utils import Settings
from karrio.schemas.dhl_universal.tracking import Error


def parse_error_response(response: list[dict], settings: Settings) -> list[Message]:
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
