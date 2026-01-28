import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups.error as error
import karrio.providers.ups.utils as provider_utils
import karrio.schemas.ups.pickup_response as ups_response


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ConfirmationDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if cancellation was successful
    cancel_response = response.get("PickupCancelResponse", {})
    response_status = cancel_response.get("Response", {}).get("ResponseStatus", {})
    success = response_status.get("Code") == "1"

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Pickup",
        )
        if success
        else None
    )

    return confirmation, messages


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    # For UPS, we cancel by PRN (Pickup Request Number)
    # The PRN is the confirmation_number returned when scheduling pickup

    return lib.Serializable(
        dict(
            prn=payload.confirmation_number,
            cancel_by="02",  # 02 = PRN
        ),
        lambda p: p,
    )
