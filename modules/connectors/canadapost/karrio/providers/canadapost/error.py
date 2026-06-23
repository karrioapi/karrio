import typing
from urllib.error import HTTPError

import karrio.core.models as models
import karrio.lib as lib
import karrio.schemas.canadapost.messages as canadapost
from karrio.providers.canadapost.utils import Settings


def parse_error_response(
    responses: lib.Element | list[lib.Element],
    settings: Settings,
    **kwargs,
) -> list[models.Message]:
    messages: list[canadapost.messageType] = sum(
        [lib.find_element("message", response, canadapost.messageType) for response in lib.to_list(responses)],
        start=[],
    )

    return [
        models.Message(
            code=message.code,
            message=message.description,
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            details={**kwargs},
        )
        for message in messages
    ]


def process_error(error: HTTPError) -> str:
    return f"""<messages xmlns="http://www.canadapost.ca/ws/messages">
        <message>
            <code>{error.code}</code>
            <description>{typing.cast(typing.Any, error).msg}</description>
        </message>
    </messages>
    """
