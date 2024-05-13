<<<<<<< HEAD:modules/connectors/eshipper/karrio/providers/eshipper/error.py
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.eshipper.utils as provider_utils
=======
from typing import List
from karrio.schemas.eshipper_xml.error import ErrorType
from karrio.core.models import Message
from karrio.core.utils import Element, XP
from karrio.providers.eshipper_xml.utils import Settings
>>>>>>> 3ccfd84c0 (feat: Rename legacy eshipper integration eshipper_xml):modules/connectors/eshipper_xml/karrio/providers/eshipper_xml/error.py


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = [
        *[_ for _ in responses if _.get("code")],
        *sum(
            [
                [dict(code="warning", message=__) for __ in _.get("warnings")]
                for _ in responses
                if _.get("warnings")
            ],
            [],
        ),
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("code"),
            message=error.get("message"),
            details={
                **kwargs,
                "type": error.get("type"),
                "fieldErrors": error.get("fieldErrors"),
                "thirdPartyMessage": error.get("thirdPartyMessage"),
            },
        )
        for error in errors
    ]
