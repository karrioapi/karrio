import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestRoadieTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.roadie.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v1/shipments?ids=152040",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.roadie.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.roadie.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["152040"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "roadie",
            "carrier_name": "roadie",
            "delivered": False,
            "estimated_delivery": "2017-12-26",
            "events": [
                {
                    "code": "at_delivery",
                    "date": "2017-12-25",
                    "description": "at_delivery",
                    "latitude": 36.123456,
                    "longitude": -82.345678,
                    "time": "10:38",
                },
                {
                    "code": "delivery_confirmed",
                    "date": "2017-12-25",
                    "description": "delivery_confirmed",
                    "latitude": 36.123456,
                    "longitude": -82.345678,
                    "time": "12:23",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.roadie.com/id/RETHNKW354W3H438",
                "customer_name": "Destination Contact",
                "package_weight": 1.0,
                "package_weight_unit": "LB",
                "shipment_destination_country": "US",
                "shipment_destination_postal_code": "30308",
                "shipment_origin_country": "US",
                "shipment_origin_postal_code": "30305",
                "shipment_package_count": 1,
            },
            "meta": {"reference": "ABC123", "shipment_id": "45245234"},
            "status": "out_for_delivery",
            "tracking_number": "RETHNKW354W3H438",
        },
        {
            "carrier_id": "roadie",
            "carrier_name": "roadie",
            "delivered": False,
            "estimated_delivery": "2017-12-26",
            "events": [
                {
                    "code": "at_delivery",
                    "date": "2017-12-25",
                    "description": "at_delivery",
                    "latitude": 36.123456,
                    "longitude": -82.345678,
                    "time": "10:38",
                },
                {
                    "code": "delivery_confirmed",
                    "date": "2017-12-25",
                    "description": "delivery_confirmed",
                    "latitude": 36.123456,
                    "longitude": -82.345678,
                    "time": "12:23",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.roadie.com/id/RETHNKW354W3H438",
                "customer_name": "Destination Contact",
                "package_weight": 1.0,
                "package_weight_unit": "LB",
                "shipment_destination_country": "US",
                "shipment_destination_postal_code": "30308",
                "shipment_origin_country": "US",
                "shipment_origin_postal_code": "30305",
                "shipment_package_count": 1,
                "signed_by": "Jane Doe",
            },
            "meta": {"reference": "ABC456", "shipment_id": "152040"},
            "status": "out_for_delivery",
            "tracking_number": "RETHNKW354W3H438",
        },
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "roadie",
            "carrier_name": "roadie",
            "code": 1001,
            "details": {"parameters": "pickup_location"},
            "message": "Pickup location can't be blank.",
        }
    ],
]


TrackingRequest = ["152040"]

TrackingResponse = """[
  {
    "id" : 45245234,
    "reference_id" : "ABC123",
    "description" : "General shipment description.",
    "state" : "assigned",
    "alternate_id_1": "111",
    "alternate_id_2": "222",
    "items" : [
      {
        "description" : "Item description",
        "reference_id" : null,
        "length" : 1.0,
        "width" : 1.0,
        "height" : 1.0,
        "weight" : 1.0,
        "value" : 20.00,
        "quantity" : 1
      }
    ],
    "pickup_location" : {
      "address" : {
        "name" : "Origin Location",
        "store_number" : "12324",
        "street1" : "123 Main Street",
        "street2" : null,
        "city" : "Atlanta",
        "state" : "GA",
        "zip" : "30305",
        "latitude": 33.74903,
        "longitude": -85.38803
      },
      "contact" : {
        "name" : "Origin Contact",
        "phone" : "4049999999"
      },
      "notes" : null
    },
    "delivery_location" : {
      "address" : {
        "name" : "Destination Location",
        "store_number" : null,
        "street1" : "456 Central Ave.",
        "street2" : null,
        "city" : "Atlanta",
        "state" : "GA",
        "zip" : "30308",
        "latitude": 33.04131,
        "longitude": -84.18303
      },
      "contact" : {
        "name" : "Destination Contact",
        "phone" : "4049999999"
      },
      "notes" : null
    },
    "pickup_after" : "2017-12-26T06:00:00.000Z",
    "deliver_between" : {
      "start" : "2017-12-26T06:00:00.000Z",
      "end" : "2017-12-26T20:00:00.000Z"
    },
    "options" : {
      "signature_required" : true,
      "notifications_enabled" : false,
      "over_21_required" : false
    },
    "tracking_number" : "RETHNKW354W3H438",
    "driver" : {
      "name" : "Jeff B.",
      "phone" : "7709999999"
    },
    "price" : 12.00,
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
    "created_at" : "2017-12-25T06:00:00.000Z",
    "updated_at" : "2017-12-25T06:00:00.000Z"
  },
  {
    "id" : 152040,
    "reference_id" : "ABC456",
    "description" : "General shipment description.",
    "state" : "delivered",
    "alternate_id_1": 333,
    "alternate_id_2": 444,
    "items" : [
      {
        "description" : "Item description",
        "reference_id" : null,
        "length" : 1.0,
        "width" : 1.0,
        "height" : 1.0,
        "weight" : 1.0,
        "value" : 20.00,
        "quantity" : 1
      }
    ],
    "pickup_location" : {
      "address" : {
        "name" : "Origin Location",
        "store_number" : "12324",
        "street1" : "123 Main Street",
        "street2" : null,
        "city" : "Atlanta",
        "state" : "GA",
        "zip" : "30305",
        "latitude": 33.74903,
        "longitude": -85.38803
      },
      "contact" : {
        "name" : "Origin Contact",
        "phone" : "4049999999"
      },
      "notes" : null
    },
    "delivery_location" : {
      "address" : {
        "name" : "Destination Location",
        "store_number" : null,
        "street1" : "456 Central Ave.",
        "street2" : null,
        "city" : "Atlanta",
        "state" : "GA",
        "zip" : "30308",
        "latitude": 33.04131,
        "longitude": -84.18303
      },
      "contact" : {
        "name" : "Destination Contact",
        "phone" : "4049999999"
      },
      "notes" : null
    },
    "pickup_after" : "2017-12-26T06:00:00.000Z",
    "deliver_between" : {
      "start" : "2017-12-26T06:00:00.000Z",
      "end" : "2017-12-26T20:00:00.000Z"
    },
    "options" : {
      "signature_required" : true,
      "notifications_enabled" : true,
      "over_21_required" : true
    },
    "tracking_number" : "RETHNKW354W3H438",
    "signatory_name" : "Jane Doe",
    "price" : 12.00,
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
    "created_at" : "2017-12-25T06:00:00.000Z",
    "updated_at" : "2017-12-25T06:00:00.000Z"
  }
]
"""

ErrorResponse = """{
  "errors": [
    {
      "code": 1001,
      "parameter": "pickup_location",
      "message": "Pickup location can't be blank."
    }
  ]
}
"""
