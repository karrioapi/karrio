import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.zoom2u.error as error
import karrio.providers.zoom2u.utils as provider_utils
import karrio.providers.zoom2u.units as provider_units


def parse_shipment_cancel_response(
    response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response_messages: list = []  # extract carrier response errors and messages
    messages = error.parse_error_response(response_messages, settings)
    success = len(messages) == 0

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
    request = dict(reference=payload.shipment_identifier)

    return lib.Serializable(request)
