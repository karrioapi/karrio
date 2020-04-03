from typing import List
from pyeshipper.quote_reply import CarrierErrorMessageType
from purplship.core.models import Error
from purplship.core.utils.xml import Element
from purplship.extension.carriers.eshipper.utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Error]:
    errors = response.xpath(".//*[local-name() = $name]", name="CarrierErrorMessage")
    return [_extract_error(node, settings) for node in errors]


def _extract_error(error_node: Element, settings: Settings) -> Error:
    error = CarrierErrorMessageType()
    error.build(error_node)
    return Error(
        code="",
        message=error.errorMessage0,
        carrier=settings.carrier_name,
    )
