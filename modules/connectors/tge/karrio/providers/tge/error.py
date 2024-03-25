import typing
import karrio.core.models as models
import karrio.providers.tge.utils as provider_utils


def parse_error_response(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]

    errors: typing.List[dict] = sum(
        (
            (
                e["TollMessage"]["ErrorMessages"]["ErrorMessage"]
                if any(
                    e.get("TollMessage", {})
                    .get("ErrorMessages", {})
                    .get("ErrorMessage")
                    or []
                )
                else [e]
            )
            for e in responses
            if (
                e.get("message") is not None
                or e.get("Exception") is not None
                or e.get("ExceptionMessage") is not None
                or any(
                    e.get("TollMessage", {})
                    .get("ErrorMessages", {})
                    .get("ErrorMessage")
                    or []
                )
            )
        ),
        [],
    )

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.get("ErrorNumber", {}).get("value") or "400",
            message=(
                error.get("message")
                or error.get("Exception")
                or error.get("ErrorMessage")
                or error.get("ExceptionMessage")
            ),
            details={**kwargs},
        )
        for error in errors
    ]
