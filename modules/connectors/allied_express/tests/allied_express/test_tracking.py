import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAlliedExpressTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/getShipmentsStatus/AOE946862J",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_delivered_tracking_response(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = DeliveredTrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), DeliveredParsedTrackingResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["AOE946862J"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "allied_express",
            "carrier_name": "allied_express",
            "delivered": False,
            "events": [
                {
                    "code": "123456789-001",
                    "date": "2021-05-28",
                    "description": "In Transit",
                    "location": "BANKSTOWN AERODROME",
                    "time": "10:03",
                }
            ],
            "status": "in_transit",
            "tracking_number": "123456789",
        }
    ],
    [],
]

DeliveredParsedTrackingResponse = [
    [
        {
            "carrier_id": "allied_express",
            "carrier_name": "allied_express",
            "delivered": True,
            "events": [
                {
                    "code": "AOE10060817R",
                    "date": "2023-10-26",
                    "description": "Freight has been delivered",
                    "location": "NOWRA",
                    "time": "14:03",
                }
            ],
            "status": "delivered",
            "tracking_number": "AOE10060817R",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "allied_express",
            "carrier_name": "allied_express",
            "code": "400",
            "details": {"tracking_number": "AOE946862J"},
            "message": "No Shipment status found.",
        }
    ],
]


TrackingRequest = [{"shipmentno": "AOE946862J"}]

TrackingResponse = """{
  "soapenv:Body": {
    "ns1:getShipmentsStatusResponse": {
      "@xmlns:ns1": "http://neptune.alliedexpress.com.au/ttws-ejb",
      "result": {
        "statusBarcodesList": {
          "consignmentNote": "123456789",
          "depotLocation": "BANKSTOWN AERODROME",
          "scannedBarcode": "123456789-001",
          "scannnedTimestamp": "2021-05-28T10:03:20.000+10:00"
        }
      }
    }
  }
}
"""

DeliveredTrackingResponse = """{
  "soapenv:Body": {
    "ns1:getShipmentsStatusResponse": {
      "@xmlns:ns1": "http://neptune.alliedexpress.com.au/ttws-ejb",
      "result": {
        "statusBarcodesList": {
          "consignmentNote": "AOE10060817R",
          "depotLocation": "NOWRA",
          "scannedBarcode": "AOE10060817R",
          "scannedStatus": "Freight has been delivered",
          "scannnedTimestamp": "2023-10-26T14:03:55.000+11:00"
        }
      }
    }
  }
}
"""

ErrorResponse = """{
  "soapenv:Body": {
    "ns1:getShipmentsStatusResponse": {
      "@xmlns:ns1": "http://neptune.alliedexpress.com.au/ttws-ejb",
      "result": {
        "statusError": "No Shipment status found."
      }
    }
  }
}
"""
