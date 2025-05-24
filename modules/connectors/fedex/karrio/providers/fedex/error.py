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
            details=lib.to_dict(
                {
                    **details,
                    "tracking_number": error.get("tracking_number"),
                }
            ),
        )
        for error in errors
    ]
