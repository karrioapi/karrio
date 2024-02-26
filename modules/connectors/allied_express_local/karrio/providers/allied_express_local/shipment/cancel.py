import karrio.schemas.allied_express_local.void_request as allied
import karrio.schemas.allied_express_local.void_response as shipping
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.allied_express_local.error as error
import karrio.providers.allied_express_local.utils as provider_utils
import karrio.providers.allied_express_local.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[provider_utils.AlliedResponse],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    success = not response.is_error  # and (response.data.get("result")) == "0"

    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Cancel Shipment",
            success=success,
        )
        if success
        else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = allied.VoidRequestType(
        shipmentno=payload.shipment_identifier,
        postalcode=(payload.options or {}).get("postal_code", ""),
    )

    return lib.Serializable(request, lib.to_dict)
