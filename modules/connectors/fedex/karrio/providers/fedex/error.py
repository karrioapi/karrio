import typing
import karrio.lib as lib
import karrio.core.models as models
from karrio.providers.fedex.utils import Settings


def parse_error_response(
    response: typing.Union[typing.List[dict], dict],
    settings: Settings,
    **details,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors: typing.List[dict] = sum(
        [
            [
                *(result["errors"] if "errors" in result else []),
                *(
                    result["output"]["alerts"]
                    if "output" in result
                    and not isinstance(result["output"], str)
                    and "alerts" in result.get("output", {})
                    and not isinstance(result["output"]["alerts"], str)
                    else []
                ),
                *(
                    [{"message": result["output"]["message"]}]
                    if "output" in result
                    and not isinstance(result["output"], str)
                    and "message" in result.get("output", {})
                    and isinstance(result["output"]["message"], str)
                    and not result["output"].get("alertType") != "NOTE"
                    else []
                ),
                *(
                    [
                        {
                            **result["error"],
                            "tracking_number": result.get("trackingNumberInfo", {}).get(
                                "trackingNumber"
                            ),
                        }
                    ]
                    if "error" in result
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
            code=error.get("code"),
            message=error.get("message"),
            level=_get_level(error.get("alertType")),
            details=lib.to_dict(
                {
                    **details,
                    "tracking_number": error.get("tracking_number"),
                }
            ),
        )
        for error in errors
    ]


def _get_level(alert_type: typing.Optional[str]) -> typing.Optional[str]:
    """Map FedEx alertType to standardized level.

    For actual errors (no alertType), defaults to "error".
    For alerts with alertType, maps: NOTE -> info, WARNING -> warning, ERROR -> error.
    """
    if alert_type is None:
        return "error"  # Default to error for actual errors without alertType
    alert_type_lower = alert_type.lower()
    if alert_type_lower == "note":
        return "info"
    elif alert_type_lower == "warning":
        return "warning"
    elif alert_type_lower == "error":
        return "error"
    return alert_type_lower
