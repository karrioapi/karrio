from typing import List, Optional
from fedex_lib.rate_service_v26 import Notification
from purplship.core.models import Message
from purplship.core.utils import Element, extract_fault, XP
from purplship.providers.fedex.utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    notifications = response.xpath(
        ".//*[local-name() = $name]", name="Notifications"
    ) + response.xpath(".//*[local-name() = $name]", name="Notification")
    errors = [_extract_error(node, settings) for node in notifications] + extract_fault(
        response, settings
    )
    return [error for error in errors if error is not None]


def _extract_error(node: Element, settings: Settings) -> Optional[Message]:
    notification = XP.build(Notification, node)
    if notification.Severity not in ("SUCCESS", "NOTE"):
        return Message(
            code=notification.Code,
            message=notification.Message,
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
        )
    return None
