import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship.core.models import TrackingRequest
from tests.ups.fixture import gateway
from purplship import Tracking


class TestUPSTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TrackingRequestPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequestPayload)

    @patch("purplship.mappers.ups.proxy.http", return_value="<a></a>")
    def test_get_tracking(self, http_mock):
        Tracking.fetch(self.TrackingRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}/track/v1/details/{self.TrackingRequest.tracking_numbers[0]}",
        )

    def test_tracking_auth_error_parsing(self):
        with patch("purplship.mappers.ups.proxy.http") as mock:
            mock.return_value = AuthError
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(ParsedAuthError))

    def test_tracking_response_parsing(self):
        with patch("purplship.mappers.ups.proxy.http") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )

    def test_invalid_tracking_number_response_parsing(self):
        with patch("purplship.mappers.ups.proxy.http") as mock:
            mock.return_value = InvalidTrackingNumberResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertEqual(
                DP.to_dict(parsed_response),
                DP.to_dict(ParsedInvalidTrackingNumberResponse),
            )

    def test_tracking_number_not_found_response_parsing(self):
        with patch("purplship.mappers.ups.proxy.http") as mock:
            mock.return_value = TrackingNumberNotFoundResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            print(DP.to_dict(parsed_response))
            self.assertEqual(
                DP.to_dict(parsed_response),
                DP.to_dict(ParsedTrackingNumberNotFound),
            )


if __name__ == "__main__":
    unittest.main()


TrackingRequestPayload = ["1Z12345E6205277936"]

ParsedAuthError = [
    [],
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "code": "250003",
            "details": {"tracking_number": "1Z12345E6205277936"},
            "message": "Invalid Access License number",
        }
    ],
]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "delivered": True,
            "estimated_delivery": "2021-10-21",
            "events": [
                {
                    "code": "FS",
                    "date": "2021-10-21",
                    "description": "Delivered",
                    "location": "ADRIAN, MI, US",
                    "time": "14:33",
                },
                {
                    "code": "OT",
                    "date": "2021-10-21",
                    "description": "Out For Delivery Today",
                    "location": "Adrian, MI, US",
                    "time": "09:22",
                },
                {
                    "code": "YP",
                    "date": "2021-10-21",
                    "description": "Processing at UPS Facility",
                    "location": "Adrian, MI, US",
                    "time": "04:27",
                },
                {
                    "code": "AR",
                    "date": "2021-10-21",
                    "description": "Arrived at Facility",
                    "location": "Adrian, MI, US",
                    "time": "01:15",
                },
                {
                    "code": "DP",
                    "date": "2021-10-21",
                    "description": "Departed from Facility",
                    "location": "Maumee, OH, US",
                    "time": "00:27",
                },
                {
                    "code": "AR",
                    "date": "2021-10-20",
                    "description": "Arrived at Facility",
                    "location": "Maumee, OH, US",
                    "time": "17:57",
                },
                {
                    "code": "DP",
                    "date": "2021-10-20",
                    "description": "Departed from Facility",
                    "location": "Nashville, TN, US",
                    "time": "08:20",
                },
                {
                    "code": "AR",
                    "date": "2021-10-19",
                    "description": "Arrived at Facility",
                    "location": "Nashville, TN, US",
                    "time": "22:24",
                },
                {
                    "code": "DP",
                    "date": "2021-10-19",
                    "description": "Departed from Facility",
                    "location": "Nashville, TN, US",
                    "time": "21:59",
                },
                {
                    "code": "OR",
                    "date": "2021-10-19",
                    "description": "Origin Scan",
                    "location": "Nashville, TN, US",
                    "time": "20:09",
                },
                {
                    "code": "XD",
                    "date": "2021-10-19",
                    "description": "Drop-Off",
                    "location": "Nashville, TN, US",
                    "time": "12:18",
                },
                {
                    "code": "MP",
                    "date": "2021-10-18",
                    "description": "Shipper created a label, UPS has not received the package yet. ",
                    "location": "US",
                    "time": "14:02",
                },
            ],
            "tracking_number": "1ZR760R60332160282",
        }
    ],
    [],
]

ParsedTrackingNumberNotFound = [
    [],
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "code": "TW0001",
            "details": {"tracking_number": "1Z12345E6205277936"},
            "message": "Tracking Information Not Found",
        }
    ],
]

ParsedInvalidTrackingNumberResponse = [
    [],
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "code": "TV1002",
            "details": {"tracking_number": "1Z12345E6205277936"},
            "message": "Invalid inquiry number",
        }
    ],
]


AuthError = """{
  "response": {
    "errors": [
      {
        "code": "250003",
        "message": "Invalid Access License number"
      }
    ]
  }
}
"""

TrackingResponseJSON = """{
  "trackResponse": {
    "shipment": [
      {
        "package": [
          {
            "trackingNumber": "1ZR760R60332160282",
            "deliveryDate": [
              {
                "type": "DEL",
                "date": "20211021"
              }
            ],
            "deliveryTime": {
              "startTime": "",
              "endTime": "143316",
              "type": "DEL"
            },
            "activity": [
              {
                "location": {
                  "address": {
                    "city": "ADRIAN",
                    "stateProvince": "MI",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "D",
                  "description": "Delivered",
                  "code": "FS"
                },
                "date": "20211021",
                "time": "143316"
              },
              {
                "location": {
                  "address": {
                    "city": "Adrian",
                    "stateProvince": "MI",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "I",
                  "description": "Out For Delivery Today",
                  "code": "OT"
                },
                "date": "20211021",
                "time": "092215"
              },
              {
                "location": {
                  "address": {
                    "city": "Adrian",
                    "stateProvince": "MI",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "I",
                  "description": "Processing at UPS Facility",
                  "code": "YP"
                },
                "date": "20211021",
                "time": "042712"
              },
              {
                "location": {
                  "address": {
                    "city": "Adrian",
                    "stateProvince": "MI",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "I",
                  "description": "Arrived at Facility",
                  "code": "AR"
                },
                "date": "20211021",
                "time": "011500"
              },
              {
                "location": {
                  "address": {
                    "city": "Maumee",
                    "stateProvince": "OH",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "I",
                  "description": "Departed from Facility",
                  "code": "DP"
                },
                "date": "20211021",
                "time": "002700"
              },
              {
                "location": {
                  "address": {
                    "city": "Maumee",
                    "stateProvince": "OH",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "I",
                  "description": "Arrived at Facility",
                  "code": "AR"
                },
                "date": "20211020",
                "time": "175700"
              },
              {
                "location": {
                  "address": {
                    "city": "Nashville",
                    "stateProvince": "TN",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "I",
                  "description": "Departed from Facility",
                  "code": "DP"
                },
                "date": "20211020",
                "time": "082000"
              },
              {
                "location": {
                  "address": {
                    "city": "Nashville",
                    "stateProvince": "TN",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "I",
                  "description": "Arrived at Facility",
                  "code": "AR"
                },
                "date": "20211019",
                "time": "222400"
              },
              {
                "location": {
                  "address": {
                    "city": "Nashville",
                    "stateProvince": "TN",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "I",
                  "description": "Departed from Facility",
                  "code": "DP"
                },
                "date": "20211019",
                "time": "215900"
              },
              {
                "location": {
                  "address": {
                    "city": "Nashville",
                    "stateProvince": "TN",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "I",
                  "description": "Origin Scan",
                  "code": "OR"
                },
                "date": "20211019",
                "time": "200952"
              },
              {
                "location": {
                  "address": {
                    "city": "Nashville",
                    "stateProvince": "TN",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "I",
                  "description": "Drop-Off",
                  "code": "XD"
                },
                "date": "20211019",
                "time": "121800"
              },
              {
                "location": {
                  "address": {
                    "city": "",
                    "stateProvince": "",
                    "postalCode": "",
                    "country": "US"
                  }
                },
                "status": {
                  "type": "M",
                  "description": "Shipper created a label, UPS has not received the package yet. ",
                  "code": "MP"
                },
                "date": "20211018",
                "time": "140229"
              }
            ]
          }
        ]
      }
    ]
  }
}
"""

InvalidTrackingNumberResponseJSON = """{
  "response": {
    "errors": [
      {
        "code": "TV1002",
        "message": "Invalid inquiry number"
      }
    ]
  }
}
"""

TrackingNumberNotFoundResponseJSON = """{
    "trackResponse": {
        "shipment": [
            {
                "warnings": [
                    {"code": "TW0001", "message": "Tracking Information Not Found"}
                ]
            }
        ]
    }
}"""
