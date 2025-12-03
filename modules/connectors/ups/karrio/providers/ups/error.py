import typing
import karrio.lib as lib
import karrio.core.models as models
from karrio.providers.ups.utils import Settings


def parse_error_response(
    responses: typing.Union[typing.List[dict], dict],
    settings: Settings,
    details: dict = None,
) -> typing.List[models.Message]:
    results = responses if isinstance(responses, list) else [responses]
    # Separate errors from warnings to set appropriate levels
    errors: typing.List[dict] = []
    warnings: typing.List[dict] = []

    for result in results:
        # get errors from the response object returned by UPS
        if "response" in result:
            errors.extend(result["response"].get("errors", []))

        # get warnings from the trackResponse object returned by UPS
        if "trackResponse" in result:
            warnings.extend(
                result["trackResponse"]["shipment"][0].get("warnings", [])
            )

        # get warnings from the UploadResponse object returned by UPS
        if "UploadResponse" in result:
            warnings.extend(
                result["UploadResponse"]["FormsHistoryDocumentID"].get("warnings", [])
            )

        # get errors from the API Fault
        if (
            result.get("Fault", {})
            .get("detail", {})
            .get("Errors", {})
            .get("ErrorDetail", {})
            .get("PrimaryErrorCode")
            is not None
        ):
            errors.append(
                result["Fault"]["detail"]["Errors"]["ErrorDetail"]["PrimaryErrorCode"]
            )

    return [
        *[
            models.Message(
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
                code=error.get("code") or error.get("Code"),
                message=error.get("message") or error.get("Description"),
                level="error",
                details=details,
            )
            for error in errors
        ],
        *[
            models.Message(
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
                code=warning.get("code") or warning.get("Code"),
                message=warning.get("message") or warning.get("Description"),
                level="warning",
                details=details,
            )
            for warning in warnings
        ],
    ]
