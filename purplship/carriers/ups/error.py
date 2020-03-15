from typing import List
from pyups.error_1_1 import CodeType
from purplship.core.models import Error
from purplship.core.utils.xml import Element
from .utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Error]:
    notifications = response.xpath(
        ".//*[local-name() = $name]", name="PrimaryErrorCode"
    )
    return [_extract_error(node, settings) for node in notifications]


def _extract_error(error_node: Element, settings: Settings) -> Error:
    error = CodeType()
    error.build(error_node)
    return Error(
        code=error.Code,
        message=error.Description,
        carrier=settings.carrier_name
    )
