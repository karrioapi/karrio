import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship import Tracking
from purplship.core.models import TrackingRequest
from tests.canadapost.fixture import gateway


class TestCanadaPostTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TRACKING_PAYLOAD)

    @patch("purplship.mappers.canadapost.proxy.http", return_value="<a></a>")
    def test_get_tracking(self, http_mock):
        Tracking.fetch(self.TrackingRequest).from_(gateway)

        reqUrl = http_mock.call_args[1]["url"]
        self.assertEqual(reqUrl, TrackingRequestURL)

    def test_tracking_auth_error_parsing(self):
        with patch("purplship.mappers.canadapost.proxy.http") as mock:
            mock.return_value = AuthError
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertEqual(to_dict(parsed_response), to_dict(ParsedAuthError))

    def test_parse_tracking_response(self):
        with patch("purplship.mappers.canadapost.proxy.http") as mock:
            mock.return_value = TrackingResponseXml
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(to_dict(parsed_response), to_dict(ParsedTrackingResponse))

    def test_tracking_unknown_response_parsing(self):
        with patch("purplship.mappers.canadapost.proxy.http") as mock:
            mock.return_value = UnknownTrackingNumberResponse
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertEqual(
                to_dict(parsed_response), to_dict(ParsedUnknownTrackingNumberResponse)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["1Z12345E6205277936"]

ParsedAuthError = [
    [],
    [
        {
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "code": "E002",
            "message": "AAA Authentication Failure",
        }
    ],
]

ParsedTrackingResponse = [
    [
        {
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "events": [
                {
                    "code": "INDUCTION",
                    "date": "2011-04-04",
                    "description": "Order information received by Canada Post",
                    "time": "13:34",
                }
            ],
            "tracking_number": "7023210039414604",
        }
    ],
    [],
]

ParsedUnknownTrackingNumberResponse = [
    [],
    [
        {
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "code": "004",
            "message": "No Pin History",
        }
    ],
]


AuthError = """<wrapper>
    <messages xmlns="http://www.canadapost.ca/ws/messages">
        <message>
            <code>E002</code>
            <description>AAA Authentication Failure</description>
        </message>
    </messages>
</wrapper>
"""

TrackingRequestURL = (
    f"""{gateway.settings.server_url}/vis/track/pin/1Z12345E6205277936/summary"""
)

TrackingResponseXml = """<wrapper>
    <tracking-summary>
        <pin-summary>
            <pin>7023210039414604</pin>
            <origin-postal-id>K1G</origin-postal-id>
            <destination-postal-id>K0J</destination-postal-id>
            <destination-province>ON</destination-province>
            <service-name>Expedited Parcels</service-name>
            <mailed-on-date>2011-04-04</mailed-on-date>
            <expected-delivery-date>2011-04-05</expected-delivery-date>
            <actual-delivery-date />
            <delivery-option-completed-ind>2</delivery-option-completed-ind>
            <event-date-time>20110404:133457</event-date-time>
            <event-description>Order information received by Canada Post</event-description>
            <attempted-date />
            <customer-ref-1>APRIL1REF1A</customer-ref-1>
            <customer-ref-2>APRIL1REF1C</customer-ref-2>
            <return-pin />
            <event-type>INDUCTION</event-type>
            <event-location />
            <signatory-name />
        </pin-summary>
    </tracking-summary>
</wrapper>
"""

UnknownTrackingNumberResponse = """<wrapper>
    <messages xmlns="http://www.canadapost.ca/ws/track">
        <message>
            <code>004</code>
            <description>No Pin History</description>
        </message>
    </messages>
</wrapper>
"""
