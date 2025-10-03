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
    errors: typing.List[dict] = sum(
        [
            [
                *(  # get errors from the response object returned by UPS
                    result["response"].get("errors", []) if "response" in result else []
                ),
                *(  # get warnings from the trackResponse object returned by UPS
                    result["trackResponse"]["shipment"][0].get("warnings", [])
                    if "trackResponse" in result
                    else []
                ),
                *(  # get warnings from the trackResponse object returned by UPS
                    result["UploadResponse"]["FormsHistoryDocumentID"].get(
                        "warnings", []
                    )
                    if "UploadResponse" in result
                    else []
                ),
                *(  # get errors from the API Fault
                    [
                        result["Fault"]["detail"]["Errors"]["ErrorDetail"][
                            "PrimaryErrorCode"
                        ]
                    ]
                    if result.get("Fault", {})
                    .get("detail", {})
                    .get("Errors", {})
                    .get("ErrorDetail", {})
                    .get("PrimaryErrorCode")
                    is not None
                    else []
                ),
            ]
            for result in results
        ],
        [],
    )

    return [
        models.Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            code=error.get("code") or error.get("Code"),
            message=error.get("message") or error.get("Description"),
            details=details,
        )
        for error in errors
    ]
