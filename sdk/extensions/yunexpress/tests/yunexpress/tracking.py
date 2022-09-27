import time
import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio import Tracking
from karrio.core.models import TrackingRequest
from .fixture import gateway


class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequestXML)

    def test_get_tracking(self):
        with patch("karrio.mappers.yunexpress.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/WayBill/GetTrackingNumber?trackingNumber=18888800406",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.yunexpress.proxy.http") as mock:
            mock.return_value = TrackingResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.yunexpress.proxy.http") as mock:
            mock.return_value = ErrorResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedErrorResponse)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["18888800406"]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "yunexpress",
            "carrier_name": "yunexpress",
            "events": [{"date": time.strftime('%Y-%m-%d')}],
            "tracking_number": "18888800406",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "yunexpress",
            "carrier_name": "yunexpress",
            "code": None,
            "details": {"MessageDetail": "在控制器“WayBill”上找不到与该请求匹配的操作。"},
            "message": "Error message",
        }
    ],
]


TrackingRequestXML = "18888800406"

TrackingResponseXML = """{
    "ResultCode": "0000",
    "ResultDesc": "提交成功",
     "Items": [
        {
            "OrderNumber": "api3111101111q1",
            "TrackingNumber": "18888800406",
            "WayBillNumber": "YT1432418888800049"
        }
    ]
}
"""

ErrorResponseXML = """{
  "Message": "Error message",
  "MessageDetail": "在控制器“WayBill”上找不到与该请求匹配的操作。"
}
"""
