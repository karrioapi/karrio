import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestLocate2uTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/v1/stops/89108749065090?includeItems=false&includeLines=false",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.locate2u.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["89108749065090"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "locate2u",
            "carrier_name": "locate2u",
            "delivered": False,
            "estimated_delivery": "2023-09-08",
            "events": [
                {
                    "code": "Pending",
                    "date": "2023-09-08",
                    "description": "Pending",
                    "latitude": -33.8706672,
                    "longitude": 151.192487,
                    "time": "13:07 PM",
                }
            ],
            "tracking_number": "164557",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "locate2u",
            "carrier_name": "locate2u",
            "code": "401",
            "details": {"tracking_number": "89108749065090"},
            "message": "Unauthorized",
        }
    ],
]


TrackingRequest = ["89108749065090"]

TrackingResponse = """{
  "assignedTo": {
    "id": "ee59-b174-4698-ac55-81d9d",
    "name": "John Doe"
  },
  "stopId": 164557,
  "status": "Pending",
  "brandId": null,
  "contact": {
    "name": "Matthew Robinson",
    "phone": "0123456789",
    "email": "matt.robinson@email.com"
  },
  "name": "Locate2u",
  "address": "Level 4, Suite 4.11, 55 Miller St, Pyrmont NSW 2009, Australia",
  "location": {
    "latitude": -33.8706672,
    "longitude": 151.192487
  },
  "tripDate": "2023-09-08",
  "appointmentTime": "13:07",
  "timeWindowStart": null,
  "timeWindowEnd": null,
  "durationMinutes": 10,
  "notes": "Please call before you deliver",
  "lastModifiedDate": "2023-09-08T13:07:24.901Z",
  "customFields": {
    "custom1": "value",
    "custom2": "value",
    "custom3": "value"
  },
  "type": null,
  "shipmentId": 0,
  "load": {
    "quantity": 0,
    "volume": 0,
    "weight": 0,
    "length": 0,
    "width": 0,
    "height": 0
  },
  "source": null,
  "sourceReference": null,
  "customerId": 0,
  "runNumber": 0,
  "teamRegionId": 0,
  "teamMemberInvoiceId": 0,
  "customerInvoiceId": 0,
  "arrivalDate": "2023-09-08T13:07:24+00:00",
  "lines": [
    {
      "lineId": 201,
      "itemId": 101,
      "serviceId": null,
      "productVariantId": null,
      "barcode": "1234567890",
      "description": "Item A - Barcode scanning item",
      "quantity": 1,
      "status": "Created",
      "itemStatus": "",
      "unitPriceExTax": 0,
      "priceCurrency": ""
    }
  ],
  "driverInstructions": null,
  "oneTimePin": "0011"
}
"""

ErrorResponse = """{
    "error": "Unauthorized",
    "code": "401"
}
"""
