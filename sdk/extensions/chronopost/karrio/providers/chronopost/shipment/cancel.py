import typing
from chronopost_lib.trackingservice import (
    cancelSkybill
)
import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.chronopost.error as provider_error
import karrio.providers.chronopost.utils as provider_utils


def parse_shipment_cancel_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    errors = provider_error.parse_error_response(response, settings)
    success = len(errors) == 0
    confirmation: models.ConfirmationDetails = (
       models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Shipment",
        )
        if success
        else None
    )

    return confirmation, errors


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest, settings: provider_utils.Settings
) -> lib.Serializable[lib.Envelope]:
    request = lib.create_envelope(
        body_content=cancelSkybill(
            accountNumber=settings.account_number,
            password=settings.password,
            language="en_GB",
            skybillNumber=payload.shipment_identifier,
        )
            
    )

    return lib.Serializable(
        request,
        lambda req: settings.serialize(req, "cancelSkybill", settings.server_url),
    )
