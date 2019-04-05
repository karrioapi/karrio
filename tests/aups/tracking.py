import unittest
from unittest.mock import patch
from tests.aups.fixture import proxy
from gds_helpers import to_dict
from purplship.domain.Types import TrackingRequest


class TestAustraliaPostTracking(unittest.TestCase):
    def test_create_quote_request(self):
        payload = TrackingRequest(tracking_numbers=TRACKING_REQUEST)

        tracking_request = proxy.mapper.create_tracking_request(payload)
        self.assertEqual(to_dict(tracking_request), to_dict(TRACKING_REQUEST))

    @patch("purplship.mappers.aups.aups_proxy.http", return_value="{}")
    def test_get_quotes(self, http_mock):
        proxy.get_tracking(TRACKING_REQUEST)

        reqUrl = http_mock.call_args[1]["url"]
        self.assertEqual(
            reqUrl,
            f'{proxy.client.server_url}/shipping/v1/track?tracking_ids={",".join(TRACKING_REQUEST)}',
        )

    def test_parse_quote_response(self):
        parsed_response = proxy.mapper.parse_tracking_response(TRACKING_RESPONSE)
        self.assertEqual(to_dict(parsed_response), to_dict(PARSED_TRACKING_RESPONSE))

    def test_parse_quote_response_with_errors(self):
        parsed_response = proxy.mapper.parse_tracking_response(TRACKING_ERROR)
        self.assertEqual(to_dict(parsed_response), to_dict(PARSED_TRACKING_ERROR))

    def test_parse_quote_response_errors(self):
        parsed_response = proxy.mapper.parse_tracking_response(ERRORS)
        self.assertEqual(to_dict(parsed_response), to_dict(PARSED_ERRORS))


if __name__ == "__main__":
    unittest.main()


TRACKING_REQUEST = ["7XX1000", "7XX1000634011427"]

PARSED_TRACKING_RESPONSE = [
    [
        {
            "carrier": "AustraliaPost",
            "events": [
                {
                    "date": "2017-09-18T14:35:07+10:00",
                    "description": "Item Delivered",
                    "location": "MEL",
                },
                {
                    "date": "2017-09-18T09:50:05+10:00",
                    "description": "On Board for Delivery",
                    "location": "MEL",
                },
            ],
            "tracking_number": "7XX1000634011427",
        }
    ],
    [{"carrier": "AustraliaPost", "code": "ESB-10001"}],
]

PARSED_TRACKING_ERROR = [[], [{"carrier": "AustraliaPost", "code": "ESB-10001"}]]

PARSED_ERRORS = [
    [],
    [
        {
            "carrier": "AustraliaPost",
            "code": "51101",
            "message": "The request must contain 10 or less AP article ids, consignment ids, or barcode ids.",
        }
    ],
]


TRACKING_RESPONSE = {
    "tracking_results": [
        {
            "tracking_id": "7XX1000",
            "errors": [{"code": "ESB-10001", "name": "Invalid tracking ID"}],
        },
        {
            "tracking_id": "7XX1000634011427",
            "status": "Delivered",
            "consignment": {
                "events": [
                    {
                        "location": "MEL",
                        "description": "Item Delivered",
                        "date": "2017-09-18T14:35:07+10:00",
                    },
                    {
                        "location": "MEL",
                        "description": "On Board for Delivery",
                        "date": "2017-09-18T09:50:05+10:00",
                    },
                ],
                "status": "Delivered in Full",
            },
            "trackable_items": [
                {
                    "article_id": "7XX1000634011427",
                    "product_type": "eParcel",
                    "events": [
                        {
                            "location": "ALEXANDRIA NSW",
                            "description": "Delivered",
                            "date": "2014-05-30T14:43:09+10:00",
                        },
                        {
                            "location": "ALEXANDRIA NSW",
                            "description": "With Australia Post for delivery today",
                            "date": "2014-05-30T06:08:51+10:00",
                        },
                        {
                            "location": "CHULLORA NSW",
                            "description": "Processed through Australia Post facility",
                            "date": "2014-05-29T19:40:19+10:00",
                        },
                        {
                            "location": "SYDNEY (AU)",
                            "description": "Arrived at facility in destination country",
                            "date": "2014-05-29T10:16:00+10:00",
                        },
                        {
                            "location": "JOHN F. KENNEDY APT\/NEW YORK (US)",
                            "description": "Departed facility",
                            "date": "2014-05-26T05:00:00+10:00",
                        },
                        {
                            "location": "JOHN F. KENNEDY APT\/NEW YORK (US)",
                            "description": "Departed facility",
                            "date": "2014-05-26T05:00:00+10:00",
                        },
                        {
                            "description": "Shipping information approved by Australia Post",
                            "date": "2014-05-23T14:27:15+10:00",
                        },
                    ],
                }
            ],
        },
    ]
}

TRACKING_ERROR = {
    "tracking_results": [
        {
            "tracking_id": "7XX1000",
            "errors": [{"code": "ESB-10001", "name": "Invalid tracking ID"}],
        }
    ]
}

ERRORS = {
    "errors": [
        {
            "code": "51101",
            "name": "TOO_MANY_AP_TRACKING_IDS",
            "message": "The request must contain 10 or less AP article ids, consignment ids, or barcode ids.",
        }
    ]
}
