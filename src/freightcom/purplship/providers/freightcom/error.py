from typing import List
from pyfreightcom.error import ErrorType
from pyfreightcom.quote_reply import CarrierErrorMessageType
from purplship.core.models import Message
from purplship.core.utils.xml import Element
from purplship.providers.freightcom.utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    carrier_errors = response.xpath(
        ".//*[local-name() = $name]", name="CarrierErrorMessage"
    )
    errors = response.xpath(".//*[local-name() = $name]", name="Error")
    return [_extract_error(node, settings) for node in errors] + [
        _extract_carrier_error(node, settings) for node in carrier_errors
    ]


def _extract_carrier_error(error_node: Element, settings: Settings) -> Message:
    error = CarrierErrorMessageType()
    error.build(error_node)
    return Message(
        code="",
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        message=error.errorMessage0,
    )


def _extract_error(error_node: Element, settings: Settings) -> Message:
    error = ErrorType()
    error.build(error_node)
    return Message(
        code="",
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        message=error.Message,
    )
