import karrio.schemas.ups.shipping_cancel_response as ups
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.ups.error as provider_error
import karrio.providers.ups.units as provider_units
import karrio.providers.ups.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    result = lib.to_object(
        ups.VoidShipmentResponseType, (response.get("VoidShipmentResponse") or {})
    )
    success = lib.failsafe(lambda: result.Response.ResponseStatus.Code) == "1"

    cancellation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Shipment",
        )
        if success
        else None
    )

    return cancellation, provider_error.parse_error_response(response, settings)


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = dict(shipmentidentificationnumber=payload.shipment_identifier)

    return lib.Serializable(request)
