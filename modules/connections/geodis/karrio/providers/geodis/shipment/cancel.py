import karrio.schemas.geodis.cancel_request as geodis
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.geodis.error as error
import karrio.providers.geodis.utils as provider_utils
import karrio.providers.geodis.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    success = response.get("ok") is True

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
    request = geodis.CancelRequestType(listNosSuivis=[payload.shipment_identifier])

    return lib.Serializable(request, lib.to_dict)
