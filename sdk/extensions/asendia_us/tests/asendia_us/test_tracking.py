import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAsendiaUSTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.asendia_us.proxy.lib.request") as mock:
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

ParsedTrackingResponse = [[], []]

ParsedErrorResponse = [[], []]


TrackingRequest = ["89108749065090"]

TrackingResponse = """{
  "data": [
    {
      "trackingNumberVendor": "RL924104146CH",
      "customerReferenceNumber": "9400109205568727179826",
      "trackingDetailEvents": [
        {
          "eventCode": "DELIVERY",
          "eventDescription": "Delivered",
          "eventLocationDetails": {
            "addressLine1": "",
            "city": "",
            "province": "",
            "postalCode": "",
            "countryIso2": "TH",
            "countryName": "Thailand"
          },
          "eventOn": "2021-08-09T11:13:00+00:00"
        },
        {
          "eventCode": "OUTDELIVCENTER",
          "eventDescription": "Out for delivery",
          "eventLocationDetails": {
            "addressLine1": "",
            "city": "string",
            "province": "string",
            "postalCode": "string",
            "countryIso2": "string",
            "countryName": "string"
          },
          "eventOn": "2021-08-09T09:07:00+00:00"
        },
        {
          "eventCode": "INDELIVCENTER",
          "eventDescription": "Arrived at delivery centre",
          "eventLocationDetails": {
            "addressLine1": "",
            "city": "string",
            "province": "string",
            "postalCode": "string",
            "countryIso2": "string",
            "countryName": "string"
          },
          "eventOn": "2021-08-09T08:37:00+00:00"
        },
        {
          "eventCode": "LEAVHUB",
          "eventDescription": "Handled by local carrier",
          "eventLocationDetails": {
            "addressLine1": "",
            "city": "string",
            "province": "string",
            "postalCode": "string",
            "countryIso2": "string",
            "countryName": "string"
          },
          "eventOn": "2021-08-07T13:47:00+00:00"
        },
        {
          "eventCode": "IMPCUSTOUT",
          "eventDescription": "Out customs authorities",
          "eventLocationDetails": {
            "addressLine1": "",
            "city": "string",
            "province": "string",
            "postalCode": "string",
            "countryIso2": "string",
            "countryName": "string"
          },
          "eventOn": "2021-08-07T13:17:00+00:00"
        },
        {
          "eventCode": "ARRDEST",
          "eventDescription": "Arrived at Destination Country",
          "eventLocationDetails": {
            "addressLine1": "LAKSI MAIL CENTER",
            "city": "Lak Si",
            "province": "Bangkok",
            "postalCode": "10210",
            "countryIso2": "TH",
            "countryName": "Thailand"
          },
          "eventOn": "2021-08-07T09:43:00+00:00"
        },
        {
          "eventCode": "2.2",
          "eventDescription": "Dispatched by Asendia USA",
          "eventLocationDetails": {
            "addressLine1": "string",
            "city": "FOLCROFT",
            "province": "PA",
            "postalCode": "19032",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-30T10:10:51.867423+00:00"
        },
        {
          "eventCode": "DEPSUB",
          "eventDescription": "Departed Asendia facility",
          "eventLocationDetails": {
            "addressLine1": "string",
            "city": "string",
            "province": "string",
            "postalCode": "string",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-30T10:10:49+00:00"
        },
        {
          "eventCode": "2.1",
          "eventDescription": "Sorted by Asendia USA",
          "eventLocationDetails": {
            "addressLine1": "string",
            "city": "FOLCROFT",
            "province": "PA",
            "postalCode": "19032",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-29T16:33:14.998765+00:00"
        },
        {
          "eventCode": "2",
          "eventDescription": "Processed by Asendia USA",
          "eventLocationDetails": {
            "addressLine1": "string",
            "city": "FOLCROFT",
            "province": "PA",
            "postalCode": "19032",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-29T01:44:44.983094+00:00"
        },
        {
          "eventCode": "10",
          "eventDescription": "Departed USPS Regional Destination Facility",
          "eventLocationDetails": {
            "addressLine1": "PHILADELPHIA PA DISTRIBUTION CENTER",
            "city": "PHILADELPHIA",
            "province": "PA ",
            "postalCode": "19176",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-27T18:14:00+00:00"
        },
        {
          "eventCode": "U1",
          "eventDescription": "Arrived at USPS Regional Facility",
          "eventLocationDetails": {
            "addressLine1": "PHILADELPHIA PA DISTRIBUTION CENTER",
            "city": "PHILADELPHIA",
            "province": "PA ",
            "postalCode": "19176",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-27T14:17:00+00:00"
        },
        {
          "eventCode": "T1",
          "eventDescription": "Departed USPS Regional Facility",
          "eventLocationDetails": {
            "addressLine1": "PHILADELPHIA PA NETWORK DISTRIBUTION CENTER",
            "city": "PHILADELPHIA",
            "province": "PA ",
            "postalCode": "19176",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-27T12:07:00+00:00"
        },
        {
          "eventCode": "U1",
          "eventDescription": "Arrived at USPS Regional Facility",
          "eventLocationDetails": {
            "addressLine1": "PHILADELPHIA PA NETWORK DISTRIBUTION CENTER",
            "city": "PHILADELPHIA",
            "province": "PA ",
            "postalCode": "19176",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-27T10:33:00+00:00"
        },
        {
          "eventCode": "NT",
          "eventDescription": "In Transit to Next Facility",
          "eventLocationDetails": {
            "addressLine1": "",
            "city": "string",
            "province": "string",
            "postalCode": "string",
            "countryIso2": "string",
            "countryName": "string"
          },
          "eventOn": "2021-07-26T00:00:00+00:00"
        },
        {
          "eventCode": "L1",
          "eventDescription": "Departed USPS Regional Facility",
          "eventLocationDetails": {
            "addressLine1": "CLEVELAND OH DISTRIBUTION CENTER ANNEX",
            "city": "CLEVELAND",
            "province": "OH",
            "postalCode": "44101",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-25T01:43:00+00:00"
        },
        {
          "eventCode": "10",
          "eventDescription": "Departed USPS Regional Origin Facility",
          "eventLocationDetails": {
            "addressLine1": "CLEVELAND OH DISTRIBUTION CENTER ANNEX",
            "city": "CLEVELAND",
            "province": "OH",
            "postalCode": "44101",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-24T22:36:00+00:00"
        },
        {
          "eventCode": "10",
          "eventDescription": "Arrived at USPS Regional Origin Facility",
          "eventLocationDetails": {
            "addressLine1": "CLEVELAND OH DISTRIBUTION CENTER ANNEX",
            "city": "CLEVELAND",
            "province": "OH",
            "postalCode": "44101",
            "countryIso2": "US",
            "countryName": "United States"
          },
          "eventOn": "2021-07-24T22:35:00+00:00"
        },
        {
          "eventCode": "OA",
          "eventDescription": "Accepted at USPS Origin Facility",
          "eventLocationDetails": {
            "addressLine1": "WICKLIFFE, OH 44092",
            "city": "string",
            "province": "string",
            "postalCode": "string",
            "countryIso2": "string",
            "countryName": "string"
          },
          "eventOn": "2021-07-24T21:20:00+00:00"
        },
        {
          "eventCode": "TM",
          "eventDescription": "Shipment Received, Package Acceptance Pending",
          "eventLocationDetails": {
            "addressLine1": "WICKLIFFE, OH 44092",
            "city": "string",
            "province": "string",
            "postalCode": "string",
            "countryIso2": "string",
            "countryName": "string"
          },
          "eventOn": "2021-07-24T15:51:00+00:00"
        },
        {
          "eventCode": "1",
          "eventDescription": "Shipment Information Received",
          "eventLocationDetails": {
            "addressLine1": "",
            "city": "string",
            "province": "string",
            "postalCode": "string",
            "countryIso2": "string",
            "countryName": "string"
          },
          "eventOn": "2021-07-24T13:00:15.85088+00:00"
        }
      ]
    }
  ],
  "responseStatus": {
    "responseStatusCode": 200,
    "responseStatusMessage": ""
  }
}
"""

ErrorResponse = """{
	"responseStatusCode": 401,
	"responseStatusMessage": "Authentication to the resource has been denied: incorrect username or password."
}
"""
