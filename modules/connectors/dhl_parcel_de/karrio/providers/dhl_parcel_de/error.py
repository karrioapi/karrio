import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_parcel_de.utils as provider_utils


def parse_error_response(
    response: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = [
        response.get("status") if isinstance(response.get("status"), dict) else response
        for response in responses
        if (
            ("title" in response and (response.get("title") or "") != "ok")
            or (
                isinstance(response.get("status"), dict)
                and "title" in response.get("status", {})
                and (response.get("status", {}).get("title") or "").lower() != "ok"
            )
        )
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=str(error.get("status") or error.get("statusCode")),
            message=error.get("detail") or error.get("title"),
            details={
                "title": error.get("title"),
                "instance": error.get("instance"),
                **kwargs,
            },
        )
        for error in errors
    ]
