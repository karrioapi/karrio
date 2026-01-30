import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_parcel_de.utils as provider_utils


TRACKING_ERROR_CODES = {
    "5": "Login failed",
    "6": "Too many invalid logins",
    "41": "Invalid tracking number format",
    "45": "No tracking number supplied",
    "62": "Authorization error",
    "100": "No data found",
    "200": "No electronic shipment data available",
}


def parse_error_response(
    responses: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    results = responses if isinstance(responses, list) else [responses]
    errors: typing.List[dict] = sum(
        [
            [result.get("status")]
            if isinstance(result.get("status"), dict)
            and result.get("status", {}).get("title", "").lower() != "ok"
            else [result] if result.get("title") and result.get("title") != "ok" else []
            for result in results
        ],
        [],
    )
    validations: typing.List[dict] = sum(
        [
            [
                {**msg, "shipmentNo": item.get("shipmentNo")}
                for item in result.get("items", [])
                for msg in item.get("validationMessages", [])
                if msg.get("validationState", "").lower() in ["error", "warning"]
            ]
            for result in results
        ],
        [],
    )

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=str(error.get("status") or error.get("statusCode")),
            message=error.get("detail") or error.get("title"),
            details=lib.to_dict(
                dict(title=error.get("title"), instance=error.get("instance"))
            ),
        )
        for error in errors
    ] + [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=msg.get("validationMessageCode") or msg.get("validationState"),
            message=lib.text(
                msg.get("property"), msg.get("validationMessage"), separator=": "
            ),
            details=lib.to_dict(
                dict(
                    property=msg.get("property"),
                    shipmentNo=msg.get("shipmentNo"),
                    validationState=msg.get("validationState"),
                )
            ),
        )
        for msg in validations
    ]


def parse_tracking_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    code = response.get("code")
    error_status = response.get("error-status")
    messages = []

    if code and code != "0":
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=code,
                message=response.get("error") or TRACKING_ERROR_CODES.get(code, "Tracking error"),
                details=dict(
                    request_id=response.get("request-id"),
                    response_name=response.get("name"),
                ),
            )
        )

    if error_status and error_status != "0":
        piece_code = response.get("searched-piece-code") or response.get("piece-code")
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=error_status,
                message=f"Tracking error for {piece_code}",
                details=dict(piece_code=piece_code),
            )
        )

    return messages
