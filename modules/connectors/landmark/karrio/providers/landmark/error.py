"""Karrio Landmark Global error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.landmark.utils as provider_utils
import karrio.schemas.landmark.error_response as landmark


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    details: dict = None,
    **kwargs,
) -> typing.List[models.Message]:
    responses = lib.to_list(response)
    errors: typing.List[landmark.ErrorType] = sum(
        [
            [
                *(lib.find_element("Error", resp, landmark.ErrorType)),
                *(lib.find_element("error", resp, landmark.ErrorType)),
            ]
            for resp in responses
        ],
        [],
    )

    return [
        models.Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            code=error.ErrorCode,
            message=error.ErrorMessage,
            details={**kwargs, **(details or {})},
        )
        for error in errors
        if error.ErrorCode or error.ErrorMessage
    ]
