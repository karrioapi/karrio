"""Karrio MyDHL error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.mydhl.utils as provider_utils
import karrio.schemas.mydhl.error_response as mydhl


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = [
        lib.to_object(mydhl.ErrorResponseType, error)
        for error in responses
        if any(error.get(key) for key in ["detail", "message", "title"])
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=str(error.status) if error.status else None,
            message=error.detail or error.message or error.title or "",
            details=lib.to_dict(
                {
                    **kwargs,
                    "instance": error.instance,
                    "title": error.title,
                }
            ),
        )
        for error in errors
    ]
