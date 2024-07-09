import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestHayPostTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest.get("tracking_numbers"))

    def test_get_tracking(self):
        with patch("karrio.mappers.hay_post.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/Api/Order/Tracking/SPS105759490AM",
            )


if __name__ == "__main__":
    unittest.main()

TrackingPayload = {
    "tracking_numbers": ["SPS105759490AM"],
}

TrackingRequest = {
    "tracking_numbers": ["SPS105759490AM"]
}
