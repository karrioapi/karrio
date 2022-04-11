from easypost_lib.errors_response import ReponseError
from karrio.core.utils import DP
from karrio.core.models import Message
from karrio.providers.easypost.utils import Settings


def parse_error_response(response: dict, settings: Settings) -> Message:
    error = DP.to_object(ReponseError, response)

    return Message(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        code=error.code,
        message=error.message,
        details=error.errors,
    )
