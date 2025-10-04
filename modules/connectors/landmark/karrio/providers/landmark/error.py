"""Karrio Landmark Global error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.landmark.utils as provider_utils
import karrio.schemas.landmark.error_response as landmark


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    messages: typing.List[landmark.ErrorType] = sum(
        [
            lib.find_element("Error", response, landmark.ErrorType)
            for response in lib.to_list(response)
        ],
        start=[],
    )

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.ErrorCode,
            message=error.ErrorMessage,
            details={**kwargs},
        )
        for error in messages
    ]
