"""Tests for return shipment interface (address auto-swap and routing)."""

import unittest
from unittest.mock import patch, MagicMock, ANY
import karrio.lib as lib
import karrio.core.models as models
from karrio.api.interface import Shipment

import logging

logging.disable(logging.CRITICAL)


class TestReturnShipmentAddressSwap(unittest.TestCase):
    """Test that the Shipment.create interface auto-swaps addresses for returns."""

    def setUp(self):
        self.maxDiff = None
        self.gateway = MagicMock()
        self.gateway.settings.carrier_name = "test_carrier"
        self.gateway.settings.carrier_id = "test_carrier"

        # Simulate proxy_methods having create_return_shipment
        self.gateway.check.return_value = []

        # Mock mapper and proxy
        self.gateway.mapper.create_return_shipment_request.return_value = (
            lib.Serializable({})
        )
        self.gateway.proxy.create_return_shipment.return_value = (
            lib.Deserializable("{}", lib.to_dict)
        )
        self.gateway.mapper.parse_return_shipment_response.return_value = (
            models.ShipmentDetails(
                carrier_id="test_carrier",
                carrier_name="test_carrier",
                tracking_number="RET123",
                shipment_identifier="RET123",
                docs=dict(label="base64label"),
            ),
            [],
        )

    def test_return_shipment_swaps_addresses(self):
        """When is_return=True, shipper and recipient should be swapped."""
        payload = {
            "shipper": {
                "person_name": "Merchant",
                "address_line1": "100 Warehouse St",
                "city": "Toronto",
                "country_code": "CA",
                "postal_code": "M5V1A1",
                "state_code": "ON",
            },
            "recipient": {
                "person_name": "Customer",
                "address_line1": "200 Home Ave",
                "city": "Ottawa",
                "country_code": "CA",
                "postal_code": "K1A0A1",
                "state_code": "ON",
            },
            "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
            "service": "test_service",
            "is_return": True,
        }

        Shipment.create(payload).from_(self.gateway).parse()

        # Verify create_return_shipment_request was called
        self.gateway.mapper.create_return_shipment_request.assert_called_once()

        # Get the swapped payload that was passed to the mapper
        call_args = self.gateway.mapper.create_return_shipment_request.call_args
        swapped_payload = call_args[0][0]

        # After swap: shipper should be Customer, recipient should be Merchant
        self.assertEqual(swapped_payload.shipper.person_name, "Customer")
        self.assertEqual(swapped_payload.shipper.address_line1, "200 Home Ave")
        self.assertEqual(swapped_payload.recipient.person_name, "Merchant")
        self.assertEqual(swapped_payload.recipient.address_line1, "100 Warehouse St")

    def test_return_shipment_sets_return_address(self):
        """When is_return=True, return_address should be set to original shipper."""
        payload = {
            "shipper": {
                "person_name": "Merchant",
                "address_line1": "100 Warehouse St",
                "city": "Toronto",
                "country_code": "CA",
                "postal_code": "M5V1A1",
                "state_code": "ON",
            },
            "recipient": {
                "person_name": "Customer",
                "address_line1": "200 Home Ave",
                "city": "Ottawa",
                "country_code": "CA",
                "postal_code": "K1A0A1",
                "state_code": "ON",
            },
            "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
            "service": "test_service",
            "is_return": True,
        }

        Shipment.create(payload).from_(self.gateway).parse()

        call_args = self.gateway.mapper.create_return_shipment_request.call_args
        swapped_payload = call_args[0][0]

        # return_address should be the original shipper (Merchant)
        self.assertEqual(swapped_payload.return_address.person_name, "Merchant")
        self.assertEqual(
            swapped_payload.return_address.address_line1, "100 Warehouse St"
        )

    def test_non_return_uses_normal_flow(self):
        """When is_return=False, normal shipment flow should be used."""
        self.gateway.mapper.create_shipment_request.return_value = lib.Serializable({})
        self.gateway.proxy.create_shipment.return_value = lib.Deserializable(
            "{}", lib.to_dict
        )
        self.gateway.mapper.parse_shipment_response.return_value = (
            models.ShipmentDetails(
                carrier_id="test_carrier",
                carrier_name="test_carrier",
                tracking_number="FWD123",
                shipment_identifier="FWD123",
                docs=dict(label="base64label"),
            ),
            [],
        )

        payload = {
            "shipper": {
                "person_name": "Merchant",
                "address_line1": "100 Warehouse St",
                "city": "Toronto",
                "country_code": "CA",
                "postal_code": "M5V1A1",
                "state_code": "ON",
            },
            "recipient": {
                "person_name": "Customer",
                "address_line1": "200 Home Ave",
                "city": "Ottawa",
                "country_code": "CA",
                "postal_code": "K1A0A1",
                "state_code": "ON",
            },
            "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
            "service": "test_service",
            "is_return": False,
        }

        Shipment.create(payload).from_(self.gateway).parse()

        # Should use normal shipment methods
        self.gateway.mapper.create_shipment_request.assert_called_once()
        self.gateway.proxy.create_shipment.assert_called_once()
        # Should NOT use return shipment methods
        self.gateway.mapper.create_return_shipment_request.assert_not_called()
        self.gateway.proxy.create_return_shipment.assert_not_called()

    def test_return_routes_to_return_proxy(self):
        """When is_return=True, proxy.create_return_shipment should be called."""
        payload = {
            "shipper": {
                "person_name": "Merchant",
                "address_line1": "100 Warehouse St",
                "city": "Toronto",
                "country_code": "CA",
                "postal_code": "M5V1A1",
                "state_code": "ON",
            },
            "recipient": {
                "person_name": "Customer",
                "address_line1": "200 Home Ave",
                "city": "Ottawa",
                "country_code": "CA",
                "postal_code": "K1A0A1",
                "state_code": "ON",
            },
            "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
            "service": "test_service",
            "is_return": True,
        }

        Shipment.create(payload).from_(self.gateway).parse()

        # Return shipment methods should be called
        self.gateway.mapper.create_return_shipment_request.assert_called_once()
        self.gateway.proxy.create_return_shipment.assert_called_once()
        self.gateway.mapper.parse_return_shipment_response.assert_called_once()

    def test_is_return_default_is_false(self):
        """When is_return is not specified, it should default to False."""
        self.gateway.mapper.create_shipment_request.return_value = lib.Serializable({})
        self.gateway.proxy.create_shipment.return_value = lib.Deserializable(
            "{}", lib.to_dict
        )
        self.gateway.mapper.parse_shipment_response.return_value = (
            models.ShipmentDetails(
                carrier_id="test_carrier",
                carrier_name="test_carrier",
                tracking_number="FWD123",
                shipment_identifier="FWD123",
                docs=dict(label="base64label"),
            ),
            [],
        )

        payload = {
            "shipper": {
                "person_name": "Merchant",
                "address_line1": "100 Warehouse St",
                "city": "Toronto",
                "country_code": "CA",
                "postal_code": "M5V1A1",
                "state_code": "ON",
            },
            "recipient": {
                "person_name": "Customer",
                "address_line1": "200 Home Ave",
                "city": "Ottawa",
                "country_code": "CA",
                "postal_code": "K1A0A1",
                "state_code": "ON",
            },
            "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
            "service": "test_service",
        }

        Shipment.create(payload).from_(self.gateway).parse()

        # Normal flow should be used
        self.gateway.mapper.create_shipment_request.assert_called_once()
        self.gateway.mapper.create_return_shipment_request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
