from typing import List
from karrio.schemas.freightcom.error import ErrorType
from karrio.schemas.freightcom.quote_reply import CarrierErrorMessageType
from karrio.core.models import Message
from karrio.core.utils import Element, XP
from karrio.providers.freightcom.utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    errors = XP.find("Error", response, ErrorType)
    carrier_errors = XP.find("CarrierErrorMessage", response, CarrierErrorMessageType)

    return [
        *[_extract_error(er, settings) for er in errors if er.Message != ""],
        *[
            _extract_carrier_error(er, settings)
            for er in carrier_errors
            if er.errorMessage0 != ""
        ],
    ]


def _extract_carrier_error(
    error: CarrierErrorMessageType, settings: Settings
) -> Message:
    return Message(
        code="CarrierErrorMessage",
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        message=error.errorMessage0,
    )


def _extract_error(error: ErrorType, settings: Settings) -> Message:
    return Message(
        code="Error",
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        message=error.Message,
    )
