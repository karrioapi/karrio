"""GLS Group carrier tracking tests."""

import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.sdk as karrio

from .fixture import gateway


class TestGLSGroupTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertIsInstance(request.serialize(), list)

    def test_get_tracking(self):
        with patch("karrio.mappers.gls.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            # Verify that the URL uses the T&T API endpoint
            self.assertIn("/track-and-trace-v1/tracking/simple/trackids/", str(mock.call_args))

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.gls.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.gls.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingErrorResponse)


if __name__ == "__main__":
    unittest.main()

# Test data
# `requested` and `unitno` are kept distinct (real-world values) to guard that
# tracking details key by `requested`, not `unitno` — see SPECS.md § Tracking.
TrackingPayload = {
    "tracking_numbers": ["604831862623"],
}

TrackingResponse = """{
  "parcels": [
    {
      "requested": "604831862623",
      "unitno": "60483186262",
      "status": "INTRANSIT",
      "statusDateTime": "2024-10-11T15:24:57+0200",
      "events": [
        {
          "code": "INTIAL.NORMAL",
          "city": "Berlin",
          "postalCode": "10437",
          "country": "DE",
          "description": "The parcel was handed over to GLS.",
          "eventDateTime": "2024-10-07T10:46:14+0200"
        },
        {
          "code": "INTIAL.PREADVICE",
          "city": "",
          "postalCode": "",
          "country": "DE",
          "description": "The parcel data was entered into the GLS IT system.",
          "eventDateTime": "2024-10-07T09:30:00+0200"
        }
      ]
    }
  ]
}"""

ErrorResponse = """{
  "parcels": [
    {
      "requested": "604831862623",
      "errorCode": "E_404_01",
      "errorMessage": "Resource Not Found"
    }
  ]
}"""

# Parsed tracking response
ParsedTrackingResponse = [
    [
        {
            "carrier_id": "gls",
            "carrier_name": "gls",
            "events": [
                {
                    "code": "INTIAL.NORMAL",
                    "date": "2024-10-07",
                    "description": "The parcel was handed over to GLS.",
                    "location": "Berlin, 10437, DE",
                    "time": "10:46",
                },
                {
                    "code": "INTIAL.PREADVICE",
                    "date": "2024-10-07",
                    "description": "The parcel data was entered into the GLS IT system.",
                    "location": "DE",
                    "time": "09:30",
                },
            ],
            "meta": {
                "requested": "604831862623",
                "status_datetime": "2024-10-11T15:24:57+0200",
                "unitno": "60483186262",
            },
            "status": "in_transit",
            "tracking_number": "604831862623",
        }
    ],
    [],
]

# Parsed error response
ParsedTrackingErrorResponse = [
    [],
    [
        {
            "carrier_id": "gls",
            "carrier_name": "gls",
            "code": "E_404_01",
            "details": {"tracking_number": "604831862623"},
            "message": "Resource Not Found",
        }
    ],
]
