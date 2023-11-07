import typing
import karrio.lib as lib
import karrio.core.models as models
from karrio.providers.fedex.utils import Settings


def parse_error_response(
    responses: typing.Union[typing.List[dict], dict],
    settings: Settings,
    details: dict = None,
) -> typing.List[models.Message]:
    results = responses if isinstance(responses, list) else [responses]
    errors: typing.List[dict] = sum(
        [
            [
                *(result["errors"] if "errors" in result else []),
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
            for result in results
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
