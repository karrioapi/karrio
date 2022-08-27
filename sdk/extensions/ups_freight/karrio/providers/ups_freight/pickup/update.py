import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups_freight.utils as provider_utils
import karrio.providers.ups_freight.pickup.create as pickup


def parse_pickup_update_response(
    response: dict,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    return pickup.parse_pickup_response(response, settings)


def pickup_update_request(
    payload: models.PickupUpdateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    cancel_request = lib.Serializable(
        dict(PickupRequestConfirmationNumber=payload.confirmation_number)
    )
    create_request = pickup.pickup_request(payload, settings)

    request = dict(
        cancel=cancel_request,
        create=create_request,
    )

    return lib.Serializable(request)
