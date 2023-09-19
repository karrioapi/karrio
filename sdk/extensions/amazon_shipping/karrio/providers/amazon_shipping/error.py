import karrio.schemas.amazon_shipping.error_response as amazon
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.amazon_shipping.utils as provider_utils


def parse_error_response(
    response: dict, settings: provider_utils.Settings, details: dict = None
) -> typing.List[models.Message]:
    errors = (
        lib.to_object(amazon.ErrorResponse, response)
        if response.get("errors") is not None
        else amazon.ErrorResponse(errors=[])
    )

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.code,
            message=error.message,
            details={
                **(details or {}),
                **({} if error.details is None else {"note": error.details}),
            },
        )
        for error in errors.errors
    ]
