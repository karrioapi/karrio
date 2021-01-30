from typing import List, Callable, cast, Any
from functools import reduce
from urllib.error import HTTPError
from purplship.core.utils.xml import Element
from purplship.providers.canadapost import Settings
from purplship.core.models import Message
from canadapost_lib.messages import messageType


def parse_error_response(response: Element, settings: Settings) -> List[Message]:
    messages = response.xpath(".//*[local-name() = $name]", name="message")
    return reduce(_extract_error(settings), messages, [])


def _extract_error(
    settings: Settings,
) -> Callable[[List[Message], Element], List[Message]]:
    def extract(errors: List[Message], message_node: Element) -> List[Message]:
        message = messageType()
        message.build(message_node)
        return errors + [
            Message(
                code=message.code,
                message=message.description,
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
            )
        ]

    return extract


def process_error(error: HTTPError) -> str:
    return f"""<messages xmlns="http://www.canadapost.ca/ws/messages">
        <message>
            <code>{error.code}</code>
            <description>{cast(Any, error).msg}</description>
        </message>
    </messages>
    """
