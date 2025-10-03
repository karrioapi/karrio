import karrio.schemas.sendle.cancel_request as sendle
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.sendle.error as error
import karrio.providers.sendle.utils as provider_utils
import karrio.providers.sendle.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    responses = _response.deserialize()
    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
        ],
        start=[],
    )
    success = any([response.get("state") == "Cancelled" for _, response in responses])

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
    order_ids = list(
        set(
            [
                payload.shipment_identifier,
                *((payload.options or {}).get("shipment_identifiers") or []),
            ]
        )
    )

    request = [sendle.CancelRequestType(id=order_id) for order_id in order_ids]

    return lib.Serializable(request, lib.to_dict)
