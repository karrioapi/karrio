from karrio.core.models import Message
from karrio.core.utils import XP, Element
from karrio.providers.dhl_poland.utils import Settings
from pysoap.envelope import Fault


def parse_error_response(response: Element, settings: Settings, details: dict = None) -> list[Message]:
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
