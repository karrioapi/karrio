import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sapient.error as error
import karrio.providers.sapient.utils as provider_utils
import karrio.providers.sapient.units as provider_units


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = True  # compute address validation success state

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
    options = lib.units.Options(
        payload.options,
        option_type=lib.units.create_enum(
            "PickupOptions",
            # fmt: off
            {
                "sapient_carrier_code": lib.OptionEnum("sapient_carrier_code"),
                "sapient_shipment_id": lib.OptionEnum("sapient_shipment_id"),
            },
            # fmt: on
        ),
    )

    # map data to convert karrio model to sapient specific type
    request = dict(
        shipmentId=options.sapient_shipment_id.state,
        carrier_code=lib.identity(
            options.sapient_carrier_code.state or settings.sapient_carrier_code
        ),
    )

    return lib.Serializable(request, lib.to_dict)
