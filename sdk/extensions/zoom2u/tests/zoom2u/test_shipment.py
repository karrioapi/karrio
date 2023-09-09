import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestZoom2uShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "locate2u_local_delivery",
    "shipper": {
        "company_name": "Shipper Name",
        "person_name": "Shipper Attn Name",
        "federal_tax_id": "123456",
        "phone_number": "1234567890",
        "address_line1": "Address Line",
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
    },
    "recipient": {
        "company_name": "Locate2u",
        "person_name": "Matthew Robinson",
        "phone_number": "0123456789",
        "address_line1": "Level 4, Suite 4.11, 55 Miller St",
        "city": "Pyrmont",
        "state_code": "2009",
        "postal_code": "NSW",
        "country_code": "AU",
        "email": "matt.robinson@email.com",
    },
    "parcels": [
        {
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "length": 7,
            "width": 5,
            "height": 2,
            "weight": 10,
            "items": [
                {
                    "sku": "1234567890",
                    "description": "Item A - Barcode scanning item",
                    "quantity": 1,
                    "metadata": {"currentLocation": "Warehouse"},
                }
            ],
        }
    ],
    "options": {
        "notes": "Please call before you deliver",
        "shipment_date": "2023-09-08",
        "appointment_time": "12:00",
        "duration_minutes": 10,
        "longitude": 151.192487,
        "latitude": -33.8706672,
    },
}

ShipmentCancelPayload = {
    "shipment_identifier": "Z20180101999999",
}

ParsedShipmentResponse = []

ParsedCancelShipmentResponse = []


ShipmentRequest = {
    "PurchaseOrderNumber": "ABCD1234",
    "PackageDescription": "1 box with some cakes",
    "DeliverySpeed": "VIP",
    "ReadyDateTime": "2020-12-24T10:20:00.06Z",
    "VehicleType": "Car",
    "PackageType": "Box",
    "Pickup": {
        "ContactName": "John Smith",
        "Email": "test@test.com",
        "Phone": "0000 0000",
        "UnitNumber": "",
        "StreetNumber": "123",
        "Street": "Main St",
        "Suburb": "North Sydney",
        "State": "NSW",
        "Postcode": "2000",
        "Country": "Australia",
        "Notes": "",
    },
    "Dropoff": {
        "ContactName": "Jane Smith",
        "Email": "test@test.com",
        "Phone": "0000 0000",
        "UnitNumber": "ACME Co.",
        "StreetNumber": "123",
        "Street": "Main St",
        "Suburb": "North Sydney",
        "State": "NSW",
        "Postcode": "2000",
        "Country": "Australia",
        "Notes": "",
    },
}


ShipmentCancelRequest = {"reference": "Z20180101999999"}

ShipmentResponse = """{
  "reference": "Z20180101999999",
  "price": 42.0,
  "tracking-link": "https://track.zoom2u.com/A1B2C3D4E",
  "trackingCode": "A1B2C3D4E"
}
"""

ShipmentCancelResponse = """{"ok": true }"""

ShipmentErrorResponse = """{
  "message": "The request is invalid.",
  "modelState": {
    "getQuoteRequest.Pickup.Suburb":   [ "The Suburb field is required." ],
    "getQuoteRequest.Pickup.Postcode": [ "The Postcode field is required." ],
  }
}
"""

ShipmentCancelErrorResponse = """{
    "error-code": "TOOLATE",
    "message": "The booking cannot be modified after its status has passed On Route to Pickup"
}
"""
