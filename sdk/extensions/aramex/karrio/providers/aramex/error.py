from typing import List
from aramex_lib.tracking import Notification
from karrio.core.utils import Element, XP
from karrio.core.models import Message
from karrio.providers.aramex import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    errors = response.xpath(".//*[local-name() = $name]", name="Notification")
    return [_extract_error(node, settings) for node in errors]


def _extract_error(node: Element, settings: Settings) -> Message:
    notification = XP.to_object(Notification, node)

    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=notification.Code,
        message=notification.Message
    )
