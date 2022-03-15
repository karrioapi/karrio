import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio import Tracking
from karrio.core.models import TrackingRequest
from tests.sf_express.fixture import gateway


class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(
            DP.to_dict(request.serialize()), DP.to_dict(TrackingRequestJSON)
        )

    def test_get_tracking(self):
        with patch("karrio.mappers.sf_express.proxy.http") as mock:
            mock.return_value = "{}"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.sf_express.proxy.http") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["444003077898"]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "sf_express",
            "carrier_name": "sf_express",
            "delivered": None,
            "events": [
                {
                    "code": "50",
                    "date": "2019-05-09",
                    "description": "已派件",
                    "location": "深圳",
                    "signatory": None,
                    "time": "10:11",
                },
                {
                    "code": "80",
                    "date": "2019-05-09",
                    "description": "已签收",
                    "location": "深圳",
                    "signatory": None,
                    "time": "18:11",
                },
            ],
            "tracking_number": "SF1011603494291",
        }
    ],
    [],
]


TrackingRequestJSON = """{
    "msgData": {
        "checkPhoneNo": null,
        "language": "1",
        "methodType": "1",
        "trackingNumber": [
            "444003077898"
        ],
        "trackingType": "1"
    },
    "msgDigest": null,
    "partnerID": null,
    "requestID": "EXP_RECE_SEARCH_ROUTES",
    "serviceCode": null,
    "timestamp": null
}
"""

TrackingResponseJSON = """{
    "success": true,
    "errorCode": "S0000",
    "errorMsg": null,
    "msgData": {
        "routeResps": [{
            "mailNo": "SF1011603494291",
            "routes": [{
                    "acceptTime": "2019-05-09 10:11:26",
                    "acceptAddress": "深圳",
                    "opCode": "50",
                    "remark": "已派件"
                },
                {
                    "acceptTime": "2019-05-09 18:11:26",
                    "acceptAddress": "深圳",
                    "opCode": "80",
                    "remark": "已签收"
                }
            ]
        }]
    }
}
"""
