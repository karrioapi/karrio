from typing import List
from pypurolator.estimate_service import Error as PurolatorError
from purplship.core.models import Error
from purplship.core.utils.xml import Element
from .utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Error]:
    errors = response.xpath(".//*[local-name() = $name]", name="Error")
    return [_extract_error(node, settings) for node in errors]


def _extract_error(error_node: Element, settings: Settings) -> Error:
    error = PurolatorError()
    error.build(error_node)
    return Error(
        code=error.Code,
        message=error.Description,
        carrier=settings.carrier_name,
        details=dict(
            AdditionalInformation=error.AdditionalInformation
        ) if error.AdditionalInformation is not None else None
    )
