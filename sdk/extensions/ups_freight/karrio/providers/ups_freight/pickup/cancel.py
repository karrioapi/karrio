import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups_freight.error as error
import karrio.providers.ups_freight.utils as provider_utils


def parse_pickup_cancel_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    cancel_response = response.get("FreightCancelPickupResponse") or {}
    response_messages = [
        *response.get("response", {}).get("errors", []),
        *cancel_response.get("Response", {}).get("Alert", []),
    ]
    messages = error.parse_error_response(response_messages, settings)
    success = cancel_response.get("FreightCancelStatus") == "1"

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Pickup",
            success=success,
        )
        if success
        else None
    )

    return confirmation, messages


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    request = dict(PickupRequestConfirmationNumber=payload.confirmation_number)

    return lib.Serializable(request)
