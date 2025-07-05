"""Karrio Veho shipment API implementation."""

import karrio.schemas.veho.shipment_request as veho_req
import karrio.schemas.veho.shipment_response as veho_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.veho.error as error
import karrio.providers.veho.utils as provider_utils
import karrio.providers.veho.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    shipment = _extract_details(response, settings) if "errors" not in response else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from carrier response data."""
    shipment = lib.to_object(veho_res.ShipmentResponseType, data)
    
    tracking_number = (
        shipment.trackingNumber 
        if hasattr(shipment, "trackingNumber") and shipment.trackingNumber 
        else ""
    )
    
    label_url = (
        shipment.labelUrl
        if hasattr(shipment, "labelUrl") and shipment.labelUrl
        else None
    )

    shipment_id = (
        shipment.shipmentId
        if hasattr(shipment, "shipmentId") and shipment.shipmentId
        else ""
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_id,
        label_type="PDF",
        docs=models.Documents(
            label=label_url,
        ) if label_url else None,
        meta=dict(
            carrier_tracking_ref=tracking_number,
            shipment_id=shipment_id,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for the carrier API."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(payload.packages).single
    options = lib.to_shipping_options(payload.options)
    service = provider_units.ShippingService.map(payload.service).value_or_key

    request = veho_req.ShipmentRequestType(
        shipFrom={
            "name": shipper.person_name or shipper.company_name,
            "company": shipper.company_name,
            "addressLine1": shipper.address_line1,
            "addressLine2": shipper.address_line2,
            "city": shipper.city,
            "stateProvince": shipper.state_code,
            "postalCode": shipper.postal_code,
            "countryCode": shipper.country_code,
            "phone": shipper.phone_number,
            "email": shipper.email,
        },
        shipTo={
            "name": recipient.person_name or recipient.company_name,
            "company": recipient.company_name,
            "addressLine1": recipient.address_line1,
            "addressLine2": recipient.address_line2,
            "city": recipient.city,
            "stateProvince": recipient.state_code,
            "postalCode": recipient.postal_code,
            "countryCode": recipient.country_code,
            "phone": recipient.phone_number,
            "email": recipient.email,
        },
        packages=[
            {
                "packageCode": provider_units.PackagePresets[package.packaging_type or "PACKAGE"].value,
                "weight": {
                    "value": package.weight.value,
                    "unit": package.weight_unit.value,
                },
                "dimensions": {
                    "length": package.length.value,
                    "width": package.width.value,
                    "height": package.height.value,
                    "unit": package.dimension_unit.value,
                },
                "insuredValue": {
                    "amount": (options.declared_value or 0),
                    "currency": options.currency or "USD",
                } if options.declared_value else None,
            }
        ],
        serviceCode=service,
        shipDate=lib.fdate(options.shipment_date or payload.ship_date),
        carrierServiceOptions={
            "signature_required": options.signature_confirmation,
            "saturday_delivery": options.saturday_delivery,
        },
    )

    return lib.Serializable(request, lib.to_dict) 
