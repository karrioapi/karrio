from typing import List, Optional
from fedex_lib.rate_service_v28 import Notification
from karrio.core.models import Message
from karrio.core.utils import Element, extract_fault, XP
from karrio.providers.fedex.utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    notifications = response.xpath(
        ".//*[local-name() = $name]", name="Notifications"
    ) + response.xpath(".//*[local-name() = $name]", name="Notification")
    errors = [_extract_error(node, settings) for node in notifications] + extract_fault(
        response, settings
    )
    return [error for error in errors if error is not None]


def _extract_error(node: Element, settings: Settings) -> Optional[Message]:
    notification = XP.to_object(Notification, node)
    if notification.Severity not in ("SUCCESS", "NOTE"):
        return Message(
            code=notification.Code,
            message=notification.Message,
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
        )
    return None
