import ups_lib.error_1_1 as ups
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups.utils as provider_utils
from karrio.providers.ups.utils import Settings


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> typing.List[models.Message]:
    errors = lib.find_element("PrimaryErrorCode", response, ups.CodeType)

    return [
        models.Message(
            code=error.Code,
            message=error.Description,
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
        )
        for error in errors
    ]


def parse_rest_error_response(
    responses: typing.List[dict], settings: Settings, details: dict = None
) -> typing.List[models.Message]:
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
            for result in responses
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
