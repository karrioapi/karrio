import karrio.schemas.canadapost.messages as canadapost

import typing
import karrio.lib as lib
import karrio.core.models as models
from karrio.providers.canadapost import Settings
from urllib.error import HTTPError


def parse_error_response(
    responses: typing.Union[lib.Element, typing.List[lib.Element]],
    settings: Settings,
    **kwargs,
) -> typing.List[models.Message]:
    messages: typing.List[canadapost.messageType] = sum(
        [
            lib.find_element("message", response, canadapost.messageType)
            for response in lib.to_list(responses)
        ],
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
