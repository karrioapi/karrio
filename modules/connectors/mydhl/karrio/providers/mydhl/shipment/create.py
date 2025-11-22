"""Karrio MyDHL shipment API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract shipment details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., ShipmentRequestType),
# while XML schema types don't have this suffix (e.g., ShipmentRequest).

import karrio.schemas.mydhl.shipment_request as mydhl_req
import karrio.schemas.mydhl.shipment_response as mydhl_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    shipment_response = lib.to_object(mydhl_res.ShipmentResponseType, response)

    details = _extract_details(shipment_response, settings)

    return details, messages


def _extract_details(
    shipment: mydhl_res.ShipmentResponseType,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """
    Extract shipment details from MyDHL shipment response

    shipment: The MyDHL ShipmentResponseType object
    settings: The carrier connection settings

    Returns a ShipmentDetails object with extracted shipment information
    """
    # Extract tracking number (MyDHL returns as integer)
    tracking_number = str(shipment.shipmentTrackingNumber) if shipment.shipmentTrackingNumber else ""

    # Extract label document from documents array using functional pattern
    label_doc = next(
        (doc for doc in (shipment.documents or []) if doc and doc.content),
        None
    )

    # Get label content and format
    label = label_doc.content if label_doc else ""
    label_format = label_doc.imageFormat if label_doc else "PDF"

    # Extract package tracking numbers for metadata
    package_tracking_numbers = [
        pkg.trackingNumber
        for pkg in (shipment.packages or [])
        if pkg and pkg.trackingNumber
    ]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label_type=label_format,
        docs=models.Documents(label=label),
        meta=dict(
            tracking_url=shipment.trackingUrl if shipment.trackingUrl else "",
            package_tracking_numbers=package_tracking_numbers,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a shipment request for MyDHL API

    payload: The standardized ShipmentRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = lib.to_services(payload.service, provider_units.ShippingService).first
    service_code = service.value_or_key if service else None
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Create the MyDHL shipment request object
    request = mydhl_req.ShipmentRequestType(
        # Map shipper details
        shipper={
            "addressLine1": shipper.address_line1,
            "city": shipper.city,
            "postalCode": shipper.postal_code,
            "countryCode": shipper.country_code,
            "stateCode": shipper.state_code,
            "personName": shipper.person_name,
            "companyName": shipper.company_name,
            "phoneNumber": shipper.phone_number,
            "email": shipper.email,
        },
        # Map recipient details
        recipient={
            "addressLine1": recipient.address_line1,
            "city": recipient.city,
            "postalCode": recipient.postal_code,
            "countryCode": recipient.country_code,
            "stateCode": recipient.state_code,
            "personName": recipient.person_name,
            "companyName": recipient.company_name,
            "phoneNumber": recipient.phone_number,
            "email": recipient.email,
        },
        # Map package details
        packages=[
            {
                "weight": package.weight.value,
                "weightUnit": provider_units.WeightUnit[package.weight.unit].value,
                "length": package.length.value if package.length else None,
                "width": package.width.value if package.width else None,
                "height": package.height.value if package.height else None,
                "dimensionUnit": provider_units.DimensionUnit[package.dimension_unit].value if package.dimension_unit else None,
                "packagingType": provider_units.PackagingType[package.packaging_type or 'your_packaging'].value,
            }
            for package in packages
        ],
        # Add service code
        serviceCode=service_code,
        # Add account information
        customerNumber=settings.account_number,
        # Add label details
        labelFormat=payload.label_type or "PDF",
    )

    return lib.Serializable(request, lib.to_dict)
