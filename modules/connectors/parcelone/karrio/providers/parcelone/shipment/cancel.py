"""Karrio ParcelOne shipment cancellation implementation."""

import typing
import karrio.schemas.parcelone.shipping_wcf as parcelone
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.parcelone.error as error
import karrio.providers.parcelone.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse shipment cancellation response from ParcelOne API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    action_results: typing.List[parcelone.ShipmentActionResult] = lib.find_element(
        "ShipmentActionResult", response, parcelone.ShipmentActionResult
    )

    successful = any(
        result.Success == 1
        for result in action_results
    )

    confirmation = (
        models.ConfirmationDetails(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            success=successful,
            operation="Cancel Shipment",
        )
        if successful
        else None
    )

    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create ParcelOne shipment cancellation request."""
    # Determine the reference field to use
    # ParcelOne supports: TrackingID, ShipmentID, ShipmentRef
    ref_field = "TrackingID"
    if payload.shipment_identifier.isdigit():
        ref_field = "ShipmentID"

    request = parcelone.identifyShipment(
        ShipmentRefField=ref_field,
        ShipmentRefValue=payload.shipment_identifier,
    )

    return lib.Serializable(
        request,
        lambda req: _request_serializer(req, settings),
    )


def _request_serializer(
    request: parcelone.identifyShipment,
    settings: provider_utils.Settings,
) -> str:
    """Serialize cancellation request to SOAP envelope."""
    identify_xml = lib.to_xml(
        request,
        name_="wcf:identifyShipment",
        namespacedef_='xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF"',
    )

    body = f"""<tns:voidShipments>
            <tns:ShippingData>
                {identify_xml}
            </tns:ShippingData>
        </tns:voidShipments>"""

    return provider_utils.create_envelope(body, settings)
