from typing import List
from pysoap.envelope import Fault
from purplship.core.models import Message
from purplship.core.utils import Element, XP
from purplship.providers.dhl_poland.utils import Settings


def parse_error_response(
    response: Element, settings: Settings, details: dict = None
) -> List[Message]:
    errors = XP.find("Fault", response, Fault)
    return [
        Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            message=error.faultstring,
            code=error.faultcode,
            details=details,
        )
        for error in errors
    ]
