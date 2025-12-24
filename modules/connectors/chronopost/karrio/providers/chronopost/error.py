import typing
from karrio.core.models import Message
from karrio.providers.chronopost.utils import Settings
import karrio.schemas.chronopost.shippingservice as chronopost
import karrio.lib as lib

ReturnType = chronopost.resultMultiParcelExpeditionValue


def parse_error_response(
    response: lib.Element, settings: Settings
) -> typing.List[Message]:
    errors = lib.find_element("return", response, ReturnType)
    return [
        Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            message=error.errorMessage,
            code=error.errorCode,
        )
        for error in errors
        if error.errorCode != 0
    ]
