import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.usps_international.error as error
import karrio.providers.usps_international.utils as provider_utils


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.ConfirmationDetails, list[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = response.get("ok") is True

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

    # map data to convert karrio model to usps specific type
    request = dict(confirmationNumber=payload.confirmation_number)

    return lib.Serializable(request, lib.to_dict)
