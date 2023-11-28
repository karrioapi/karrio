import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.nationex.error as error
import karrio.providers.nationex.utils as provider_utils
import karrio.providers.nationex.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[typing.Union[bool, dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    response_data = response if isinstance(response, dict) else {}
    messages = error.parse_error_response(response_data, settings)
    success = any(messages) is False

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
    request = dict(shipment_id=payload.shipment_identifier)

    return lib.Serializable(request)
