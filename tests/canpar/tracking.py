import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship import Tracking
from purplship.core.models import TrackingRequest
from tests.canpar.fixture import gateway


class TestCanparTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    # def test_create_tracking_request(self):
    #     request = gateway.mapper.create_tracking_request(self.TrackingRequest)
    #
    #     self.assertEqual(request.serialize(), TRACKING_PAYLOAD)


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["1Z12345E6205277936"]

ParsedTrackingResponse = []

TrackingResponseXml = """<wrapper>
</wrapper>
"""
