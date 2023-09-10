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
                f"{gateway.settings.server_url}/api/v1/delivery/create",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/v1/delivery/cancel/Z20180101999999",
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
    "service": "zoom2u_VIP",
    "shipper": {
        "person_name": "John Smith",
        "email": "test@test.com",
        "phone_number": "0000 0000",
        "street_number": "123",
        "address_line1": "Main St",
        "city": "North Sydney",
        "state_code": "NSW",
        "postal_code": "2000",
        "country_code": "AU",
    },
    "recipient": {
        "person_name": "Jane Smith",
        "email": "test@test.com",
        "phone_number": "0000 0000",
        "street_number": "123",
        "address_line1": "Main St",
        "city": "North Sydney",
        "state_code": "NSW",
        "postal_code": "2000",
        "country_code": "AU",
    },
    "parcels": [
        {
            "packaging_type": "small_box",
            "description": "1 box with some cakes",
        }
    ],
    "options": {
        "purchase_order_number": "ABCD1234",
        "ready_datetime": "2020-12-24 10:20:00",
        "vehicle_type": "zoom2u_car",
    },
}

ShipmentCancelPayload = {
    "shipment_identifier": "Z20180101999999",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "zoom2u",
        "carrier_name": "zoom2u",
        "docs": {"label": "No label..."},
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://track.zoom2u.com/A1B2C3D4E",
            "trackingCode": "A1B2C3D4E",
        },
        "shipment_identifier": "Z20180101999999",
        "tracking_number": "Z20180101999999",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "zoom2u",
        "carrier_name": "zoom2u",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "PurchaseOrderNumber": "ABCD1234",
    "PackageDescription": "1 box with some cakes",
    "DeliverySpeed": "VIP",
    "ReadyDateTime": "2020-12-24T10:20:00.000000Z",
    "VehicleType": "Car",
    "PackageType": "Box",
    "Pickup": {
        "ContactName": "John Smith",
        "Email": "test@test.com",
        "Phone": "0000 0000",
        "StreetNumber": "123",
        "Street": "Main St",
        "Suburb": "North Sydney",
        "State": "NSW",
        "Postcode": "2000",
        "Country": "Australia",
    },
    "Dropoff": {
        "ContactName": "Jane Smith",
        "Email": "test@test.com",
        "Phone": "0000 0000",
        "StreetNumber": "123",
        "Street": "Main St",
        "Suburb": "North Sydney",
        "State": "NSW",
        "Postcode": "2000",
        "Country": "Australia",
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
