from typing import List, Callable
from functools import reduce
from purplship.core.utils.xml import Element
from purplship.core.settings import Settings
from purplship.core.models import Error
from pycaps.messages import messageType


def parse_error_response(response: Element, settings: Settings) -> List[Error]:
    messages = response.xpath(".//*[local-name() = $name]", name="message")
    return reduce(_extract_error(settings), messages, [])


def _extract_error(settings: Settings) -> Callable[[List[Error], Element], List[Error]]:
    def extract(errors: List[Error], message_node: Element) -> List[Error]:
        message = messageType()
        message.build(message_node)
        return errors + [
            Error(
                code=message.code,
                message=message.description,
                carrier=settings.carrier_name,
            )
        ]
    return extract
