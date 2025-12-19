"""Example: Pickup Implementation Pattern

This example demonstrates the canonical pattern for implementing pickup
(schedule, update, cancel) functionality in a Karrio carrier integration.
"""

# === FILE: karrio/providers/[carrier]/pickup/__init__.py ===

from karrio.providers.[carrier].pickup.create import (
    parse_pickup_response,
    pickup_request,
)
from karrio.providers.[carrier].pickup.update import (
    parse_pickup_update_response,
    pickup_update_request,
)
from karrio.providers.[carrier].pickup.cancel import (
    parse_pickup_cancel_response,
    pickup_cancel_request,
)


# === FILE: karrio/providers/[carrier]/pickup/create.py ===

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.providers.[carrier].units as provider_units
import karrio.schemas.[carrier].pickup_create_request as carrier_req
import karrio.schemas.[carrier].pickup_create_response as carrier_res


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    """Parse pickup scheduling response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    pickup = (
        _extract_details(response, settings)
        if not any(messages)
        else None
    )
    
    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """Extract pickup details from carrier response."""
    pickup = lib.to_object(carrier_res.PickupResponseType, data)
    
    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=pickup.confirmationNumber,
        pickup_date=lib.fdate(pickup.pickupDate),
        pickup_charge=models.ChargeDetails(
            name="Pickup Fee",
            amount=lib.to_money(pickup.pickupCharge) if hasattr(pickup, 'pickupCharge') else None,
            currency=pickup.currency if hasattr(pickup, 'currency') else "USD",
        ) if hasattr(pickup, 'pickupCharge') and pickup.pickupCharge else None,
        ready_time=lib.ftime(pickup.readyTime) if hasattr(pickup, 'readyTime') else None,
        closing_time=lib.ftime(pickup.closingTime) if hasattr(pickup, 'closingTime') else None,
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create pickup scheduling request."""
    address = lib.to_address(payload.address)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    
    request = carrier_req.PickupRequestType(
        # Pickup location
        pickupAddress=carrier_req.AddressType(
            name=address.person_name,
            company=address.company_name,
            addressLine1=address.address_line1,
            addressLine2=address.address_line2,
            city=address.city,
            stateCode=address.state_code,
            postalCode=address.postal_code,
            countryCode=address.country_code,
            phone=address.phone_number,
            email=address.email,
        ),
        # Pickup timing
        pickupDate=lib.fdate(payload.pickup_date),
        readyTime=payload.ready_time,
        closingTime=payload.closing_time,
        # Package information
        packageCount=len(packages),
        totalWeight=carrier_req.WeightType(
            value=packages.weight.value,
            unit=provider_units.WeightUnit[packages.weight.unit].value,
        ),
        # Instructions
        specialInstructions=payload.instruction,
        # Account
        accountNumber=settings.account_number,
    )
    
    return lib.Serializable(request, lib.to_dict)


# === FILE: karrio/providers/[carrier]/pickup/update.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.providers.[carrier].units as provider_units
import karrio.schemas.[carrier].pickup_update_request as carrier_req
import karrio.schemas.[carrier].pickup_update_response as carrier_res


def parse_pickup_update_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.PickupDetails, typing.List[models.Message]]:
    """Parse pickup update response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    pickup = (
        _extract_details(response, settings)
        if not any(messages)
        else None
    )
    
    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    """Extract updated pickup details."""
    pickup = lib.to_object(carrier_res.PickupUpdateResponseType, data)
    
    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=pickup.confirmationNumber,
        pickup_date=lib.fdate(pickup.pickupDate),
    )


def pickup_update_request(
    payload: models.PickupUpdateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create pickup update request."""
    address = lib.to_address(payload.address)
    packages = lib.to_packages(payload.parcels)
    
    request = carrier_req.PickupUpdateRequestType(
        # Existing pickup reference
        confirmationNumber=payload.confirmation_number,
        # Updated pickup location
        pickupAddress=carrier_req.AddressType(
            name=address.person_name,
            company=address.company_name,
            addressLine1=address.address_line1,
            addressLine2=address.address_line2,
            city=address.city,
            stateCode=address.state_code,
            postalCode=address.postal_code,
            countryCode=address.country_code,
            phone=address.phone_number,
            email=address.email,
        ),
        # Updated timing
        pickupDate=lib.fdate(payload.pickup_date),
        readyTime=payload.ready_time,
        closingTime=payload.closing_time,
        # Updated package information
        packageCount=len(packages),
        totalWeight=carrier_req.WeightType(
            value=packages.weight.value,
            unit=provider_units.WeightUnit[packages.weight.unit].value,
        ),
        # Instructions
        specialInstructions=payload.instruction,
        # Account
        accountNumber=settings.account_number,
    )
    
    return lib.Serializable(request, lib.to_dict)


# === FILE: karrio/providers/[carrier]/pickup/cancel.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.schemas.[carrier].pickup_cancel_request as carrier_req
import karrio.schemas.[carrier].pickup_cancel_response as carrier_res


def parse_pickup_cancel_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    """Parse pickup cancellation response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    success = response.get("success", False) or response.get("cancelled", False)
    
    confirmation = (
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="Cancel Pickup",
        )
        if success and not any(messages)
        else None
    )
    
    return confirmation, messages


def pickup_cancel_request(
    payload: models.PickupCancelRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create pickup cancellation request."""
    request = carrier_req.PickupCancelRequestType(
        confirmationNumber=payload.confirmation_number,
        pickupDate=lib.fdate(payload.pickup_date) if payload.pickup_date else None,
        reason=payload.reason,
        accountNumber=settings.account_number,
    )
    
    return lib.Serializable(request, lib.to_dict)


# === FILE: karrio/mappers/[carrier]/proxy.py (pickup portion) ===

def schedule_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
    """Schedule a pickup."""
    response = lib.request(
        url=f"{self.settings.server_url}/pickups",
        data=lib.to_json(request.serialize()),
        trace=self.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)


def modify_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
    """Update an existing pickup."""
    data = request.serialize()
    confirmation_number = data.get("confirmationNumber")
    
    response = lib.request(
        url=f"{self.settings.server_url}/pickups/{confirmation_number}",
        data=lib.to_json(data),
        trace=self.trace_as("json"),
        method="PUT",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)


def cancel_pickup(self, request: lib.Serializable) -> lib.Deserializable[str]:
    """Cancel a pickup."""
    data = request.serialize()
    confirmation_number = data.get("confirmationNumber")
    
    response = lib.request(
        url=f"{self.settings.server_url}/pickups/{confirmation_number}/cancel",
        data=lib.to_json(data),
        trace=self.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)


# === FILE: tests/[carrier]/test_pickup.py ===

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestCarrierPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupUpdateRequest = models.PickupUpdateRequest(**PickupUpdatePayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), PickupRequest)

    def test_schedule_pickup(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickups"
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_create_pickup_update_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)
        print(f"Generated update request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), PickupUpdateRequest)

    def test_update_pickup(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertIn("/pickups/", mock.call_args[1]["url"])

    def test_create_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)
        print(f"Generated cancel request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), PickupCancelRequest)

    def test_cancel_pickup(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)
            print(f"Called URL: {mock.call_args[1]['url']}")
            self.assertIn("/cancel", mock.call_args[1]["url"])

    def test_parse_error_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest)
                .from_(gateway)
                .parse()
            )
            print(f"Error response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


# Test Data Constants
PickupPayload = {
    "pickup_date": "2024-01-20",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "instruction": "Ring doorbell",
    "address": {
        "company_name": "Test Company",
        "address_line1": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "person_name": "John Doe",
        "state_code": "NY",
        "phone_number": "555-1234",
    },
    "parcels": [
        {
            "weight": 5.0,
            "weight_unit": "LB",
        }
    ],
}

PickupUpdatePayload = {
    "confirmation_number": "PICKUP123",
    "pickup_date": "2024-01-21",
    "ready_time": "10:00",
    "closing_time": "18:00",
    "instruction": "Use side entrance",
    "address": {
        "company_name": "Test Company",
        "address_line1": "123 Main St",
        "city": "New York",
        "postal_code": "10001",
        "country_code": "US",
        "person_name": "John Doe",
        "state_code": "NY",
        "phone_number": "555-1234",
    },
    "parcels": [
        {
            "weight": 5.0,
            "weight_unit": "LB",
        }
    ],
}

PickupCancelPayload = {
    "confirmation_number": "PICKUP123",
    "pickup_date": "2024-01-20",
    "reason": "No longer needed",
}

PickupRequest = {
    # Expected carrier-specific request format
}

PickupUpdateRequest = {
    # Expected carrier-specific update request format
}

PickupCancelRequest = {
    # Expected carrier-specific cancel request format
}

PickupResponse = """{
    "confirmationNumber": "PICKUP123",
    "pickupDate": "2024-01-20",
    "readyTime": "09:00",
    "closingTime": "17:00"
}"""

ParsedPickupResponse = [
    {
        "carrier_id": "carrier",
        "carrier_name": "carrier",
        "confirmation_number": "PICKUP123",
        "pickup_date": "2024-01-20",
    },
    [],
]

ErrorResponse = """{
    "errors": [
        {
            "code": "INVALID_DATE",
            "message": "Pickup date must be in the future"
        }
    ]
}"""

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "carrier",
            "carrier_name": "carrier",
            "code": "INVALID_DATE",
            "message": "Pickup date must be in the future",
        }
    ],
]
