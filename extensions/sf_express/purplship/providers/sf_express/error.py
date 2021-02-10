from typing import List
from sf_express_lib.route_response import ERRORType
from purplship.core.models import Message
from purplship.core.utils import XP, Element
from purplship.providers.sf_express import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    carrier_errors = response.xpath(".//*[local-name() = $name]", name="ERROR")
    return [_extract_error(node, settings) for node in carrier_errors]


def _extract_error(node: Element, settings: Settings) -> Message:
    error = XP.build(ERRORType, node)
    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=error.code,
        message=error.valueOf_
    )
