"""Tests for the recipient contact-data suppression interface (GDPR toggles).

`suppress_recipient_email` / `suppress_recipient_phone` are generic core
ShippingOptions. They are enforced once in `Shipment.create`, before any carrier
mapper runs, so every connector honours them uniformly. These tests exercise the
interface seam with a mocked gateway and assert what reaches the mapper.
"""

import logging
import unittest
from unittest.mock import MagicMock

import karrio.core.models as models
import karrio.lib as lib
from karrio.api.interface import Rating, Shipment

logging.disable(logging.CRITICAL)


SHIPPER = {
    "person_name": "Merchant",
    "address_line1": "100 Warehouse St",
    "city": "Toronto",
    "country_code": "CA",
    "postal_code": "M5V1A1",
    "state_code": "ON",
    "email": "merchant@example.com",
    "phone_number": "111 111 1111",
}
RECIPIENT = {
    "person_name": "Customer",
    "address_line1": "200 Home Ave",
    "city": "Ottawa",
    "country_code": "CA",
    "postal_code": "K1A0A1",
    "state_code": "ON",
    "email": "customer@example.com",
    "phone_number": "999 999 9999",
}


def _payload(**overrides) -> dict:
    return {
        "shipper": dict(SHIPPER),
        "recipient": dict(RECIPIENT),
        "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
        "service": "test_service",
        **overrides,
    }


class TestSuppressRecipientContact(unittest.TestCase):
    """The interface strips recipient contact data before the mapper runs."""

    def setUp(self):
        self.maxDiff = None
        self.gateway = MagicMock()
        self.gateway.settings.carrier_name = "test_carrier"
        self.gateway.settings.carrier_id = "test_carrier"
        self.gateway.check.return_value = []
        self.gateway.mapper.create_shipment_request.return_value = lib.Serializable({})
        self.gateway.proxy.create_shipment.return_value = lib.Deserializable("{}", lib.to_dict)
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
        self.gateway.mapper.create_return_shipment_request.return_value = lib.Serializable({})
        self.gateway.proxy.create_return_shipment.return_value = lib.Deserializable("{}", lib.to_dict)
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

    def _mapper_recipient(self):
        return self.gateway.mapper.create_shipment_request.call_args[0][0].recipient

    def test_suppress_both_strips_email_and_phone(self):
        Shipment.create(_payload(options={"suppress_recipient_email": True, "suppress_recipient_phone": True})).from_(
            self.gateway
        ).parse()

        recipient = self._mapper_recipient()
        self.assertIsNone(recipient.email)
        self.assertIsNone(recipient.phone_number)
        # other recipient fields remain intact
        self.assertEqual(recipient.person_name, "Customer")
        self.assertEqual(recipient.postal_code, "K1A0A1")

    def test_suppress_email_only_keeps_phone(self):
        Shipment.create(_payload(options={"suppress_recipient_email": True})).from_(self.gateway).parse()

        recipient = self._mapper_recipient()
        self.assertIsNone(recipient.email)
        self.assertEqual(recipient.phone_number, "999 999 9999")

    def test_suppress_phone_only_keeps_email(self):
        Shipment.create(_payload(options={"suppress_recipient_phone": True})).from_(self.gateway).parse()

        recipient = self._mapper_recipient()
        self.assertEqual(recipient.email, "customer@example.com")
        self.assertIsNone(recipient.phone_number)

    def test_default_off_transmits_both(self):
        Shipment.create(_payload()).from_(self.gateway).parse()

        recipient = self._mapper_recipient()
        self.assertEqual(recipient.email, "customer@example.com")
        self.assertEqual(recipient.phone_number, "999 999 9999")

    def test_explicit_false_transmits_both(self):
        Shipment.create(_payload(options={"suppress_recipient_email": False, "suppress_recipient_phone": False})).from_(
            self.gateway
        ).parse()

        recipient = self._mapper_recipient()
        self.assertEqual(recipient.email, "customer@example.com")
        self.assertEqual(recipient.phone_number, "999 999 9999")

    def test_shipper_contact_never_suppressed(self):
        Shipment.create(_payload(options={"suppress_recipient_email": True, "suppress_recipient_phone": True})).from_(
            self.gateway
        ).parse()

        shipper = self.gateway.mapper.create_shipment_request.call_args[0][0].shipper
        self.assertEqual(shipper.email, "merchant@example.com")
        self.assertEqual(shipper.phone_number, "111 111 1111")

    def test_return_shipment_suppresses_customer_contact(self):
        """On a return the customer becomes the swapped shipper — their PII stays
        suppressed regardless of shipment direction."""
        Shipment.create(
            _payload(
                is_return=True,
                options={"suppress_recipient_email": True, "suppress_recipient_phone": True},
            )
        ).from_(self.gateway).parse()

        swapped = self.gateway.mapper.create_return_shipment_request.call_args[0][0]
        # customer (original recipient) is now the shipper, with contact stripped
        self.assertEqual(swapped.shipper.person_name, "Customer")
        self.assertIsNone(swapped.shipper.email)
        self.assertIsNone(swapped.shipper.phone_number)


class TestSuppressRecipientContactOnRating(unittest.TestCase):
    """The same suppression applies to the live-rate leg (Rating.fetch), since a
    label purchase fetches carrier rates before buying and several rate mappers
    transmit recipient contact data."""

    def setUp(self):
        self.maxDiff = None
        self.gateway = MagicMock()
        self.gateway.settings.carrier_name = "test_carrier"
        self.gateway.settings.carrier_id = "test_carrier"
        self.gateway.check.return_value = []
        self.gateway.mapper.create_rate_request.return_value = lib.Serializable({})
        self.gateway.proxy.get_rates.return_value = lib.Deserializable("{}", lib.to_dict)
        self.gateway.mapper.parse_rate_response.return_value = ([], [])

    def _mapper_recipient(self):
        return self.gateway.mapper.create_rate_request.call_args[0][0].recipient

    def test_rate_request_strips_recipient_contact(self):
        Rating.fetch(_payload(options={"suppress_recipient_email": True, "suppress_recipient_phone": True})).from_(
            self.gateway
        ).parse()

        recipient = self._mapper_recipient()
        self.assertIsNone(recipient.email)
        self.assertIsNone(recipient.phone_number)
        self.assertEqual(recipient.postal_code, "K1A0A1")

    def test_rate_request_default_off_transmits_both(self):
        Rating.fetch(_payload()).from_(self.gateway).parse()

        recipient = self._mapper_recipient()
        self.assertEqual(recipient.email, "customer@example.com")
        self.assertEqual(recipient.phone_number, "999 999 9999")

    def test_rate_shipper_contact_never_suppressed(self):
        Rating.fetch(_payload(options={"suppress_recipient_email": True, "suppress_recipient_phone": True})).from_(
            self.gateway
        ).parse()

        shipper = self.gateway.mapper.create_rate_request.call_args[0][0].shipper
        self.assertEqual(shipper.email, "merchant@example.com")
        self.assertEqual(shipper.phone_number, "111 111 1111")


if __name__ == "__main__":
    unittest.main()
