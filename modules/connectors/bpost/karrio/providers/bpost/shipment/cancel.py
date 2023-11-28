import karrio.schemas.bpost.shm_deep_integration_v5 as bpost
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.bpost.error as error
import karrio.providers.bpost.utils as provider_utils
import karrio.providers.bpost.units as provider_units


def parse_shipment_cancel_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
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
    request = bpost.OrderUpdateType(status="CANCELLED")

    return lib.Serializable(
        request,
        lambda req: lib.to_xml(
            req,
            namespacedef_=(
                'xmlns="http://schema.post.be/shm/deepintegration/v3/"'
                ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
                ' xsi:schemaLocation="http://schema.post.be/shm/deepintegration/v3/"'
            ),
        ).replace("OrderUpdateType", "orderUpdate"),
        dict(reference=payload.shipment_identifier),
    )
