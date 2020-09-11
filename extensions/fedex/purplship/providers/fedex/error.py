from typing import List, Callable
from functools import reduce
from pyfedex.rate_service_v26 import Notification
from purplship.core.models import Message
from purplship.core.utils.xml import Element
from purplship.core.utils.soap import extract_fault, build
from .utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    notifications = (
            response.xpath(".//*[local-name() = $name]", name="Notifications") +
            response.xpath(".//*[local-name() = $name]", name="Notification")
    )
    return reduce(
        _extract_error(settings), notifications,
        extract_fault(response, settings)
    )


def _extract_error(
    settings: Settings,
) -> Callable[[List[Message], Element], List[Message]]:
    def extract(messages: List[Message], notification_node: Element) -> List[Message]:
        notification = build(Notification, notification_node)
        if notification.Severity not in ("SUCCESS", "NOTE"):
            messages.append(
                Message(
                    code=notification.Code,
                    message=notification.Message,
                    carrier_name=settings.carrier_name,
                    carrier_id=settings.carrier_id,
                )
            )
        return messages

    return extract
