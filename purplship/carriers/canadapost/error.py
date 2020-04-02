from typing import List, Callable
from functools import reduce
from purplship.core.utils.xml import Element
from purplship.carriers.canadapost import Settings
from purplship.core.models import Message
from pycanadapost.messages import messageType


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    messages = response.xpath(".//*[local-name() = $name]", name="message")
    return reduce(_extract_error(settings), messages, [])


def _extract_error(settings: Settings) -> Callable[[List[Message], Element], List[Message]]:
    def extract(errors: List[Message], message_node: Element) -> List[Message]:
        message = messageType()
        message.build(message_node)
        return errors + [
            Message(
                code=message.code,
                message=message.description,
                carrier=settings.carrier,
                carrier_name=settings.carrier_name,
            )
        ]

    return extract
