"""Karrio Spring shipment API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract shipment details from the response
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., ShipmentRequestType),
# while XML schema types don't have this suffix (e.g., ShipmentRequest).

import karrio.schemas.spring.shipment_request as spring_req
import karrio.schemas.spring.shipment_response as spring_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.spring.error as error
import karrio.providers.spring.utils as provider_utils
import karrio.providers.spring.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    # Check if we have valid shipment data
    
    has_shipment = "shipment" in response if hasattr(response, 'get') else False
    

    shipment = _extract_details(response, settings) if has_shipment else None

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """
    Extract shipment details from carrier response data

    data: The carrier-specific shipment data structure
    settings: The carrier connection settings

    Returns a ShipmentDetails object with extracted shipment information
    """
    # Convert the carrier data to a proper object for easy attribute access
    
    # For JSON APIs, convert dict to proper response object
    response_obj = lib.to_object(spring_res.ShipmentResponseType, data)

    # Access the shipment data
    shipment = response_obj.shipment if hasattr(response_obj, 'shipment') else None

    if shipment:
        # Extract tracking info
        tracking_number = shipment.trackingNumber if hasattr(shipment, 'trackingNumber') else ""
        shipment_id = shipment.shipmentId if hasattr(shipment, 'shipmentId') else ""

        # Extract label info
        label_data = shipment.labelData if hasattr(shipment, 'labelData') else None
        label_format = label_data.format if label_data and hasattr(label_data, 'format') else "PDF"
        label_base64 = label_data.image if label_data and hasattr(label_data, 'image') else ""

        # Extract optional invoice
        invoice_base64 = shipment.invoiceImage if hasattr(shipment, 'invoiceImage') else ""

        # Extract service code for metadata
        service_code = shipment.serviceCode if hasattr(shipment, 'serviceCode') else ""
    else:
        tracking_number = ""
        shipment_id = ""
        label_format = "PDF"
        label_base64 = ""
        invoice_base64 = ""
        service_code = ""
    

    documents = models.Documents(
        label=label_base64,
    )

    # Add invoice if present
    if invoice_base64:
        documents.invoice = invoice_base64

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_id,
        label_type=label_format,
        docs=documents,
        meta=dict(
            service_code=service_code,
            # Add any other relevant metadata from the carrier's response
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a shipment request for the carrier API

    payload: The standardized ShipmentRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Create the carrier-specific request object
    
    # For JSON API request
    request = spring_req.ShipmentRequestType(
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
        serviceCode=service,
        # Add account information
        customerNumber=settings.customer_number,
        # Add label details
        labelFormat=payload.label_type or "PDF",
        # Add any other required fields for this carrier's API
    )
    

    return lib.Serializable(request, lib.to_dict)
