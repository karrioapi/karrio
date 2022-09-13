import dpdhl_lib.business_interface as dpdhl
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpdhl.error as error
import karrio.providers.dpdhl.utils as provider_utils
import karrio.providers.dpdhl.units as provider_units


def parse_shipment_cancel_response(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    messages = error.parse_error_response(response, settings)
    deletion: dpdhl.DeletionState = lib.find_element(
        "DeletionState",
        response,
        dpdhl.DeletionState,
        first=True,
    )
    success = deletion is not None and deletion.Status.statusCode == 0

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

    request = lib.Envelope(
        Header=lib.Header(
            settings.AuthentificationType,
        ),
        Body=lib.Body(
            dpdhl.DeleteShipmentOrderRequest(
                Version=dpdhl.Version(
                    majorRelease=3,
                    minorRelease=1,
                ),
                shipmentNumber=[payload.shipment_identifier],
            )
        ),
    )

    return lib.Serializable(
        request,
        lambda _: lib.envelope_serializer(
            _,
            namespace=(
                'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"'
                ' xmlns:cis="http://dhl.de/webservice/cisbase"'
                ' xmlns:ns="http://dhl.de/webservices/businesscustomershipping/3.0"'
            ),
            prefixes=dict(
                Envelope="soapenv",
                shipmentNumber="cis",
                AuthentificationType="cis",
                DeleteShipmentOrderRequest="ns",
            ),
        ),
    )
