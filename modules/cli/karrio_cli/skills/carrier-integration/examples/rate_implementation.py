"""Example: Rate Implementation Pattern

This example demonstrates the canonical pattern for implementing rate functionality
in a Karrio carrier integration.
"""

# === FILE: karrio/providers/[carrier]/rate.py ===

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.providers.[carrier].units as provider_units
# CRITICAL: Always import generated schema types
import karrio.schemas.[carrier].rate_request as carrier_req
import karrio.schemas.[carrier].rate_response as carrier_res


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    """Parse carrier rate response into Karrio models."""
    response = _response.deserialize()
    
    # Parse errors first
    messages = error.parse_error_response(response, settings)
    
    # Extract rate objects from response (adjust path based on carrier API)
    rate_objects = response.get("rates", []) if isinstance(response, dict) else []
    
    # Functional style: list comprehension to extract rates
    rates = [
        _extract_details(rate_data, settings)
        for rate_data in rate_objects
    ]
    
    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    """Extract rate details from carrier response data.
    
    Always use generated schema types for type-safe access.
    """
    # Convert dict to typed object using generated schema
    rate = lib.to_object(carrier_res.RateType, data)
    
    # Map carrier service code to Karrio service enum
    service = provider_units.ShippingService.map(rate.serviceCode)
    
    # Calculate total from component charges (functional style)
    charges = [
        rate.baseCharge,
        rate.fuelSurcharge,
        rate.insuranceCharge,
    ]
    total_charge = sum(
        lib.to_money(charge) for charge in charges if charge
    )
    
    # Extract currency from first available charge
    currency = next(
        (rate.currency for rate in [rate] if hasattr(rate, 'currency') and rate.currency),
        "USD"
    )
    
    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(total_charge),
        currency=currency,
        transit_days=lib.to_int(rate.transitDays) if hasattr(rate, 'transitDays') else None,
        meta=dict(
            service_name=service.value_or_key,
            quote_id=rate.quoteId if hasattr(rate, 'quoteId') else None,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create carrier-specific rate request.
    
    Use lib utilities for data conversion and generated schema types
    for request building.
    """
    # Convert Karrio models to wrapped address objects with computed fields
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    
    # Parse packages with options
    packages = lib.to_packages(
        payload.parcels,
        options=payload.options,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    
    # Parse requested services
    services = lib.to_services(payload.services, provider_units.ShippingService)
    
    # Parse shipping options
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    
    # Build request using generated schema type (declarative tree structure)
    request = carrier_req.RateRequestType(
        shipper=carrier_req.AddressType(
            name=shipper.person_name,
            company=shipper.company_name,
            addressLine1=shipper.address_line1,
            addressLine2=shipper.address_line2,
            city=shipper.city,
            stateCode=shipper.state_code,
            postalCode=shipper.postal_code,
            countryCode=shipper.country_code,
            phone=shipper.phone_number,
            email=shipper.email,
        ),
        recipient=carrier_req.AddressType(
            name=recipient.person_name,
            company=recipient.company_name,
            addressLine1=recipient.address_line1,
            addressLine2=recipient.address_line2,
            city=recipient.city,
            stateCode=recipient.state_code,
            postalCode=recipient.postal_code,
            countryCode=recipient.country_code,
            phone=recipient.phone_number,
            email=recipient.email,
        ),
        # Functional: list comprehension for packages
        packages=[
            carrier_req.PackageType(
                weight=carrier_req.WeightType(
                    value=package.weight.value,
                    unit=provider_units.WeightUnit[package.weight.unit].value,
                ),
                dimensions=lib.identity(
                    carrier_req.DimensionsType(
                        length=package.length.value,
                        width=package.width.value,
                        height=package.height.value,
                        unit=provider_units.DimensionUnit[package.dimension_unit or "IN"].value,
                    ) if all([package.length, package.width, package.height]) else None
                ),
                packagingType=provider_units.PackagingType.map(
                    package.packaging_type or "your_packaging"
                ).value,
            )
            for package in packages
        ],
        # Optional: filter services if specified
        services=[s.value_or_key for s in services] if services else None,
        # Account configuration
        accountNumber=settings.account_number,
        # Options
        insuranceAmount=options.insurance.state if options.insurance else None,
        signatureRequired=options.signature_required.state if options.signature_required else None,
    )
    
    # Return serializable request - lib.to_dict for JSON APIs
    return lib.Serializable(request, lib.to_dict)


# === FILE: tests/[carrier]/test_rate.py ===
"""
Test file follows the mandatory 4-method pattern.
"""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestCarrierRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rates(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rates"
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


# Test Data Constants
RatePayload = {
    "shipper": {
        "company_name": "Test Company",
        "address_line1": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "person_name": "John Doe",
        "state_code": "NY",
        "phone_number": "555-1234",
    },
    "recipient": {
        "company_name": "Recipient Corp",
        "address_line1": "456 Oak Ave",
        "city": "Los Angeles",
        "postal_code": "90001",
        "country_code": "US",
        "person_name": "Jane Smith",
        "state_code": "CA",
        "phone_number": "555-5678",
    },
    "parcels": [
        {
            "height": 10,
            "length": 12,
            "width": 8,
            "weight": 5.0,
            "dimension_unit": "IN",
            "weight_unit": "LB",
        }
    ],
}

RateRequest = {
    # Expected carrier-specific request format
}

RateResponse = """{
    "rates": [
        {
            "serviceCode": "EXPRESS",
            "baseCharge": 25.99,
            "currency": "USD",
            "transitDays": 2
        }
    ]
}"""

ErrorResponse = """{
    "errors": [
        {
            "code": "INVALID_ADDRESS",
            "message": "Invalid postal code"
        }
    ]
}"""

ParsedRateResponse = [
    [
        {
            "carrier_id": "carrier",
            "carrier_name": "carrier",
            "service": "carrier_express",
            "total_charge": 25.99,
            "currency": "USD",
            "transit_days": 2,
            "meta": {
                "service_name": "EXPRESS",
            },
        }
    ],
    [],  # Empty errors
]

ParsedErrorResponse = [
    [],  # Empty rates
    [
        {
            "carrier_id": "carrier",
            "carrier_name": "carrier",
            "code": "INVALID_ADDRESS",
            "message": "Invalid postal code",
        }
    ],
]
