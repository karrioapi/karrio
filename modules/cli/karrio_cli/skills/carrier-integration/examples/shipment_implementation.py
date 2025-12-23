"""Example: Shipment Implementation Pattern

This example demonstrates the canonical pattern for implementing shipment
(create and cancel) functionality in a Karrio carrier integration.
"""

# === FILE: karrio/providers/[carrier]/shipment/__init__.py ===

from karrio.providers.[carrier].shipment.create import (
    parse_shipment_response,
    shipment_request,
)
from karrio.providers.[carrier].shipment.cancel import (
    parse_shipment_cancel_response,
    shipment_cancel_request,
)


# === FILE: karrio/providers/[carrier]/shipment/create.py ===

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.providers.[carrier].units as provider_units
import karrio.schemas.[carrier].shipment_request as carrier_req
import karrio.schemas.[carrier].shipment_response as carrier_res


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    """Parse carrier shipment response into Karrio models."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    # Only extract details if no errors
    shipment = (
        _extract_details(response, settings)
        if not any(m.code for m in messages)  # Check for actual error codes
        else None
    )
    
    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    """Extract shipment details from carrier response."""
    # Convert to typed object
    shipment = lib.to_object(carrier_res.ShipmentResponseType, data)
    
    # Extract label - may be base64 encoded or URL
    label = lib.identity(
        shipment.labelData if hasattr(shipment, 'labelData') else None
    )
    
    # Handle label URL if provided instead of data
    if hasattr(shipment, 'labelUrl') and shipment.labelUrl and not label:
        # Fetch label from URL
        label = lib.request(url=shipment.labelUrl, decoder=lib.encode_base64)
    
    # Extract invoice for international shipments
    invoice = lib.identity(
        shipment.invoiceData if hasattr(shipment, 'invoiceData') else None
    )
    
    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.trackingNumber,
        shipment_identifier=shipment.shipmentId,
        docs=models.Documents(
            label=label,
            invoice=invoice,
        ),
        meta=dict(
            carrier_tracking_link=lib.identity(
                settings.tracking_url.format(shipment.trackingNumber)
                if hasattr(settings, 'tracking_url') else None
            ),
            service_name=shipment.serviceName if hasattr(shipment, 'serviceName') else None,
            label_type=shipment.labelType if hasattr(shipment, 'labelType') else "PDF",
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create carrier-specific shipment request."""
    # Convert Karrio models
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(
        payload.parcels,
        options=payload.options,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    service = lib.to_services(payload.service, provider_units.ShippingService).first
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    
    # Handle customs for international shipments
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=packages.weight_unit,
    )
    
    # Determine if international
    is_international = shipper.country_code != recipient.country_code
    
    # Build request using generated schema type
    request = carrier_req.ShipmentRequestType(
        # Shipper
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
        # Recipient
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
        # Packages
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
                description=package.description,
            )
            for package in packages
        ],
        # Service
        serviceCode=service.value_or_key if service else None,
        # Label configuration
        labelFormat=payload.label_type or "PDF",
        # Options
        signatureRequired=options.signature_required.state,
        insuranceAmount=options.insurance.state,
        saturdayDelivery=options.saturday_delivery.state,
        # References
        reference=payload.reference,
        # Account
        accountNumber=settings.account_number,
        # Customs (for international)
        customs=lib.identity(
            carrier_req.CustomsType(
                contentType=customs.content_type or "merchandise",
                declaredValue=customs.declared_value,
                currency=customs.currency or "USD",
                items=[
                    carrier_req.CustomsItemType(
                        description=item.description,
                        quantity=item.quantity,
                        value=item.value_amount,
                        weight=item.weight,
                        hsCode=item.hs_code,
                        originCountry=item.origin_country,
                    )
                    for item in customs.commodities
                ],
                incoterm=customs.incoterm,
                invoiceNumber=customs.invoice,
            ) if is_international and customs else None
        ),
    )
    
    return lib.Serializable(request, lib.to_dict)


# === FILE: karrio/providers/[carrier]/shipment/cancel.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.schemas.[carrier].shipment_cancel_response as carrier_res


def parse_shipment_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse shipment cancellation response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    # Check if cancellation was successful
    success = response.get("success", False) or response.get("cancelled", False)
    
    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Shipment",
        )
        if success and not any(messages)
        else None
    )
    
    return confirmation, messages


def shipment_cancel_request(
    payload: models.ShipmentCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create shipment cancellation request."""
    # Most carriers just need the shipment identifier
    request = dict(
        shipmentId=payload.shipment_identifier,
        # Some carriers may need additional fields
        trackingNumber=payload.options.get("tracking_number") if payload.options else None,
    )
    
    return lib.Serializable(request, lib.to_dict)


# === FILE: karrio/mappers/[carrier]/proxy.py (shipment portion) ===

def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
    """Create a shipment and generate label."""
    response = lib.request(
        url=f"{self.settings.server_url}/shipments",
        data=lib.to_json(request.serialize()),
        trace=self.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)


def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
    """Cancel a shipment."""
    data = request.serialize()
    shipment_id = data.get("shipmentId")
    
    response = lib.request(
        url=f"{self.settings.server_url}/shipments/{shipment_id}/cancel",
        trace=self.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)


# === FILE: tests/[carrier]/test_shipment.py ===

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestCarrierShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments"
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(self.ShipmentCancelRequest)
        print(f"Generated cancel request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), ShipmentCancelRequest)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertIn("/cancel", mock.call_args[1]["url"])

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed cancel response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentCancelResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


# Test Data Constants
ShipmentPayload = {
    "service": "carrier_express",
    "shipper": {
        "company_name": "Test Company",
        "address_line1": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "person_name": "John Doe",
        "state_code": "NY",
        "phone_number": "555-1234",
        "email": "john@test.com",
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
        "email": "jane@recipient.com",
    },
    "parcels": [
        {
            "height": 10,
            "length": 12,
            "width": 8,
            "weight": 5.0,
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "description": "Test Package",
        }
    ],
    "label_type": "PDF",
    "reference": "ORDER-12345",
}

ShipmentCancelPayload = {
    "shipment_identifier": "SHIP123456",
}

ShipmentRequest = {
    # Expected carrier-specific request format
}

ShipmentCancelRequest = {
    "shipmentId": "SHIP123456",
}

ShipmentResponse = """{
    "shipmentId": "SHIP123456",
    "trackingNumber": "1Z999AA10123456784",
    "labelData": "JVBERi0xLjQK...",
    "labelType": "PDF",
    "serviceName": "Express"
}"""

ShipmentCancelResponse = """{
    "success": true,
    "message": "Shipment cancelled successfully"
}"""

ErrorResponse = """{
    "errors": [
        {
            "code": "INVALID_ADDRESS",
            "message": "Invalid recipient address"
        }
    ]
}"""

ParsedShipmentResponse = [
    {
        "carrier_id": "carrier",
        "carrier_name": "carrier",
        "tracking_number": "1Z999AA10123456784",
        "shipment_identifier": "SHIP123456",
        "docs": {
            "label": "JVBERi0xLjQK...",
        },
        "meta": {
            "service_name": "Express",
            "label_type": "PDF",
        },
    },
    [],  # Empty errors
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "carrier",
        "carrier_name": "carrier",
        "success": True,
        "operation": "Cancel Shipment",
    },
    [],  # Empty errors
]

ParsedErrorResponse = [
    None,  # No shipment details
    [
        {
            "carrier_id": "carrier",
            "carrier_name": "carrier",
            "code": "INVALID_ADDRESS",
            "message": "Invalid recipient address",
        }
    ],
]
