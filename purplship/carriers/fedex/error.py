from typing import List, Callable
from functools import reduce
from pyfedex.rate_v22 import Notification
from purplship.core.models import Error
from purplship.core.utils.xml import Element
from .utils import Settings


def parse_error_response(response: Element, settings: Settings) -> List[Error]:
    notifications = (
        response.xpath(".//*[local-name() = $name]", name="Notifications") +
        response.xpath(".//*[local-name() = $name]", name="Notification")
    )
    return reduce(_extract_error(settings), notifications, [])


def _extract_error(settings: Settings) -> Callable[[List[Error], Element], List[Error]]:

    def extract(errors: List[Error], notification_node: Element) -> List[Error]:
        notification = Notification()
        notification.build(notification_node)
        if notification.Severity not in ("SUCCESS", "NOTE"):
            errors.append(
                Error(
                    code=notification.Code,
                    message=notification.Message,
                    carrier=settings.carrier_name,
                )
            )
        return errors

    return extract
