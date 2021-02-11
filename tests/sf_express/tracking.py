import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship import Tracking
from purplship.core.models import TrackingRequest
from tests.sf_express.fixture import gateway


class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize()[0], TrackingRequestXML)

    def test_get_tracking(self):
        with patch("purplship.mappers.sf_express.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("purplship.mappers.sf_express.proxy.http") as mock:
            mock.return_value = TrackingResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse))


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["1Z12345E6205277936"]

ParsedTrackingResponse = [
    [],
    [],
]

TrackingRequestXML = """
"""

TrackingResponseXML = """
"""
