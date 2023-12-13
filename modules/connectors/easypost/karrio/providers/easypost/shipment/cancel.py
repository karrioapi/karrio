import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.easypost.error as provider_error
import karrio.providers.easypost.units as provider_units
import karrio.providers.easypost.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    status = response.get("status")
    errors = provider_error.parse_error_response(response, settings)

    details = models.ConfirmationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        success=status != "rejected",
        operation="cancel shipment",
    )

    return details, errors


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest, _
) -> lib.Serializable:
    return lib.Serializable(payload.shipment_identifier)
