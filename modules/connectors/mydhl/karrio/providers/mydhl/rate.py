"""Karrio MyDHL rate API implementation."""

# IMPLEMENTATION INSTRUCTIONS:
# 1. Uncomment the imports when the schema types are generated
# 2. Import the specific request and response types you need
# 3. Create a request instance with the appropriate request type
# 4. Extract data from the response to populate the RateDetails
#
# NOTE: JSON schema types are generated with "Type" suffix (e.g., RateRequestType),
# while XML schema types don't have this suffix (e.g., RateRequest).

import karrio.schemas.mydhl.rate_request as mydhl_req
import karrio.schemas.mydhl.rate_response as mydhl_res

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.mydhl.error as error
import karrio.providers.mydhl.utils as provider_utils
import karrio.providers.mydhl.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)

    # Extract rate objects from the response - adjust based on carrier API structure
    
    # For JSON APIs, find the path to rate objects
    rate_objects = response.get("rates", []) if hasattr(response, 'get') else []
    rates = [_extract_details(rate, settings) for rate in rate_objects]
    

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """
    Extract rate details from carrier response data

    data: The carrier-specific rate data structure
    settings: The carrier connection settings

    Returns a RateDetails object with extracted rate information
    """
    # Convert the carrier data to a proper object for easy attribute access
    
    # For JSON APIs, convert dict to proper response object
    rate = lib.to_object(mydhl_res.RateResponseType, data)

    # Now access data through the object attributes
    service = rate.serviceCode if hasattr(rate, 'serviceCode') else ""
    service_name = rate.serviceName if hasattr(rate, 'serviceName') else ""
    total = float(rate.totalCharge) if hasattr(rate, 'totalCharge') and rate.totalCharge else 0.0
    currency = rate.currency if hasattr(rate, 'currency') else "USD"
    transit_days = int(rate.transitDays) if hasattr(rate, 'transitDays') and rate.transitDays else 0
    

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service,
        total_charge=lib.to_money(total, currency),
        currency=currency,
        transit_days=transit_days,
        meta=dict(
            service_name=service_name,
            # Add any other useful metadata from the carrier response
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """
    Create a rate request for the carrier API

    payload: The standardized RateRequest from karrio
    settings: The carrier connection settings

    Returns a Serializable object that can be sent to the carrier API
    """
    # Convert karrio models to carrier-specific format
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # Create the carrier-specific request object
    
    # For JSON API request
    request = mydhl_req.RateRequestType(
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
        # Add any other required fields for the carrier API
    )
    

    return lib.Serializable(request, lib.to_dict)
