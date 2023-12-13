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
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

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
    "tracking_numbers": ["89108749065090"],
}

ParsedTrackingResponse = []

ParsedErrorResponse = []


TrackingRequest = {"shipment_no": "123456789"}

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
