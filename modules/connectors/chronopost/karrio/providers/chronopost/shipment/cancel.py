import typing
from karrio.schemas.chronopost.trackingservice import cancelSkybill
import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.chronopost.error as provider_error
import karrio.providers.chronopost.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
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
) -> lib.Serializable:
    request = lib.Envelope(
        Body=lib.Body(
            cancelSkybill(
                accountNumber=settings.account_number,
                password=settings.password,
                language=settings.language,
                skybillNumber=payload.shipment_identifier,
            )
        )
    )

    return lib.Serializable(
        request,
        lambda envelope: lib.envelope_serializer(
            envelope,
            namespace=(
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                'xmlns:cxf="http://cxf.tracking.soap.chronopost.fr/"'
            ),
            prefixes=dict(Envelope="soapenv"),
        ),
    )
