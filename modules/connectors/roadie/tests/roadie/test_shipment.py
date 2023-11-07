import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestRoadieShipping(unittest.TestCase):
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
        with patch("karrio.mappers.roadie.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v1/shipments",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.roadie.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v1/shipments/152040",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.roadie.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.roadie.proxy.lib.request") as mock:
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
    "service": "roadie_local_delivery",
    "shipper": {
        "street_number": "123",
        "address_line1": "Main Street",
        "city": "Atlanta",
        "state_code": "GA",
        "postal_code": "30305",
        "company_name": "Origin Location",
        "person_name": "Origin Contact",
        "phone_number": "4049999999",
    },
    "recipient": {
        "address_line1": "456 Central Ave.",
        "city": "Atlanta",
        "state_code": "GA",
        "postal_code": "30308",
        "company_name": "Destination Location",
        "person_name": "Destination Contact",
        "phone_number": "4049999999",
    },
    "parcels": [
        {
            "length": 1.0,
            "width": 1.0,
            "height": 1.0,
            "weight": 1.0,
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "description": "Item description",
        }
    ],
    "options": {
        "pickup_after": "2017-12-26 06:00:00",
        "deliver_start": "2017-12-26 06:00:00",
        "deliver_end": "2017-12-26 20:00:00",
        "declared_value": 20.0,
        "roadie_extra_compensation": 5.0,
        "signature_required": True,
        "email_notification": False,
        "roadie_over_21_required": False,
        "roadie_trailer_required": False,
    },
    "reference": "ABCDEFG12345",
}

ShipmentCancelPayload = {
    "shipment_identifier": "152040",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "roadie",
        "carrier_name": "roadie",
        "docs": {},
        "meta": {
            "service_name": "Roadie Local Delivery",
            "tracking_number": "RETHNKW354W3H438",
        },
        "shipment_identifier": "152040",
        "tracking_number": 152040,
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "roadie",
        "carrier_name": "roadie",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "reference_id": "ABCDEFG12345",
    "description": "Item description",
    "items": [
        {
            "description": "Item description",
            "length": 1.0,
            "width": 1.0,
            "height": 1.0,
            "weight": 1.0,
            "value": 20.00,
            "quantity": 1,
        }
    ],
    "pickup_location": {
        "address": {
            "name": "Origin Location",
            "street1": "123 Main Street",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30305",
        },
        "contact": {"name": "Origin Contact", "phone": "4049999999"},
    },
    "delivery_location": {
        "address": {
            "name": "Destination Location",
            "street1": "456 Central Ave.",
            "city": "Atlanta",
            "state": "GA",
            "zip": "30308",
        },
        "contact": {"name": "Destination Contact", "phone": "4049999999"},
    },
    "pickup_after": "2017-12-26T06:00:00Z",
    "deliver_between": {
        "start": "2017-12-26T06:00:00Z",
        "end": "2017-12-26T20:00:00Z",
    },
    "options": {
        "signature_required": True,
        "notifications_enabled": False,
        "over_21_required": False,
        "extra_compensation": 5.0,
        "trailer_required": False,
    },
}


ShipmentCancelRequest = {"shipment_id": "152040"}

ShipmentResponse = """{
  "id": 152040,
  "reference_id": "ABCDEFG12345",
  "description": "General shipment description.",
  "state": "scheduled",
  "alternate_id_1": "111",
  "alternate_id_2": "222",
  "items": [
    {
      "description": "Item description",
      "reference_id": null,
      "length": 1.0,
      "width": 1.0,
      "height": 1.0,
      "weight": 1.0,
      "value": 20.00,
      "quantity": 1
    }
  ],
  "pickup_location": {
    "address": {
      "name": "Origin Location",
      "store_number": "12324",
      "street1": "123 Main Street",
      "street2": null,
      "city": "Atlanta",
      "state": "GA",
      "zip": "30305",
      "latitude": 33.74903,
      "longitude": -85.38803
    },
    "contact": {
      "name": "Origin Contact",
      "phone": "4049999999"
    },
    "notes": null
  },
  "delivery_location": {
    "address": {
      "name": "Destination Location",
      "store_number": null,
      "street1": "456 Central Ave.",
      "street2": null,
      "city": "Atlanta",
      "state": "GA",
      "zip": "30308",
      "latitude": 33.04131,
      "longitude": -84.18303
    },
    "contact": {
      "name": "Destination Contact",
      "phone": "4049999999"
    },
    "notes": null
  },
  "pickup_after": "2017-12-26T06:00:00.000Z",
  "deliver_between": {
    "start": "2017-12-26T06:00:00.000Z",
    "end": "2017-12-26T20:00:00.000Z"
  },
  "options": {
    "signature_required": true,
    "notifications_enabled": false,
    "over_21_required": false,
    "extra_compensation": 5.0,
    "trailer_required": false,
    "decline_insurance": true
  },
  "tracking_number": "RETHNKW354W3H438",
  "price": 12.00,
  "estimated_distance": 3.456,
  "events": [
    {
      "name": "at_delivery",
      "occurred_at": "2017-12-25T10:38:43.467Z",
      "location": {
        "latitude": 36.123456,
        "longitude": -82.345678
      }
    },
    {
      "name": "delivery_confirmed",
      "occurred_at": "2017-12-25T12:23:54.325Z",
      "location": {
        "latitude": 36.123456,
        "longitude": -82.345678
      }
    }
  ],
  "created_at": "2017-12-25T06:00:00.000Z",
  "updated_at": "2017-12-25T06:00:00.000Z"
}
"""

ShipmentCancelResponse = """{
    "cancellation_code": "item_not_ready",
    "cancellation_comment": "item was not ready for pickup"
}
"""
