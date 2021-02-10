from typing import List
from aramex_lib.tracking import Notification
from purplship.core.utils import Element, XP
from purplship.core.models import Message
from purplship.providers.aramex import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    errors = response.xpath(".//*[local-name() = $name]", name="Notification")
    return [_extract_error(node, settings) for node in errors]


def _extract_error(node: Element, settings: Settings) -> Message:
    notification = XP.build(Notification, node)

    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=notification.Code,
        message=notification.Message
    )
