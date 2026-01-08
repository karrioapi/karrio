"""Karrio PostAT shipment cancellation API implementation."""

import karrio.schemas.postat.void_types as postat_void

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.postat.error as error
import karrio.providers.postat.utils as provider_utils


def parse_shipment_cancel_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.ConfirmationDetails], typing.List[models.Message]]:
    """Parse shipment cancellation response from PostAT SOAP API."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check for VoidShipmentResult
    result = lib.find_element("VoidShipmentResult", response, first=True)
    success_elem = lib.find_element("Success", result, first=True)
    success = (
        success_elem is not None
        and success_elem.text
        and success_elem.text.lower() == "true"
        and not any(messages)
    )

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
    """Create a shipment cancellation request for the PostAT SOAP API."""
    # Build request using generated schema types
    request = lib.Envelope(
        Body=lib.Body(
            postat_void.VoidShipmentType(
                row=[
                    postat_void.VoidShipmentRowType(
                        TrackingNumber=payload.shipment_identifier,
                        OrgUnitID=settings.org_unit_id,
                        OrgUnitGuid=settings.org_unit_guid,
                    )
                ]
            )
        )
    )

    return lib.Serializable(request, lib.envelope_serializer)
    
