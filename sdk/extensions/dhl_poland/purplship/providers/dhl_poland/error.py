from typing import List
from pysoap.envelope import Fault
from karrio.core.models import Message
from karrio.core.utils import Element, XP
from karrio.providers.dhl_poland.utils import Settings


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
