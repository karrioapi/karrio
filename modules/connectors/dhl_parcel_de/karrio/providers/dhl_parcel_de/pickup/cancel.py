"""Karrio DHL Germany pickup cancel implementation."""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.dhl_parcel_de.error as error
import karrio.providers.dhl_parcel_de.utils as provider_utils


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.ConfirmationDetails | None, list[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check for successful cancellations
    confirmed = response.get("confirmedCancellations") or []
    failed = response.get("failedCancellations") or []

    success = len(confirmed) > 0 and len(failed) == 0

    # Add failed cancellation messages
    for fail in failed:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=fail.get("orderState"),
                message=fail.get("message"),
            )
        )

    confirmation = lib.identity(
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Pickup",
            success=success,
        )
        if success or len(confirmed) > 0
        else None
    )

    return confirmation, messages


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    # The DHL Germany API uses query parameters for cancellation
    # DELETE /orders?orderID={orderID}
    request = dict(
        orderID=payload.confirmation_number,
    )

    return lib.Serializable(request, lib.to_dict)
