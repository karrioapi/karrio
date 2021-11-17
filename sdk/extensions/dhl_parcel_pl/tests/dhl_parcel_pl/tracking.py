import unittest
import logging
from unittest.mock import patch
from purplship.core.utils import DP
from purplship import Tracking
from purplship.core.models import TrackingRequest
from tests.dhl_parcel_pl.fixture import gateway


class TestCanparTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize()[0], TrackingRequestXML)

    def test_get_tracking(self):
        with patch("purplship.mappers.dhl_parcel_pl.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    # def test_parse_tracking_response(self):
    #     with patch("purplship.mappers.dhl_parcel_pl.proxy.http") as mock:
    #         mock.return_value = TrackingResponseXML
    #         parsed_response = (
    #             Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
    #         )

    #         self.assertEqual(
    #             DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
    #         )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["24333892874"]

ParsedTrackingResponse = []

TrackingRequestXML = """<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns="https://sandbox.dhl24.com.pl/webapi2/provider/service.html?ws=1">
    <soap-env:Body>
        <getTrackAndTraceInfo>
            <authData>
                <username>username</username>
                <password>password</password>
            </authData>
            <shipmentId>24333892874</shipmentId>
        </getTrackAndTraceInfo>
    </soap-env:Body>
</soap-env:Envelope>
"""

TrackingResponseXML = """<SOAP-ENV:Envelope
  xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:ns1="https://sandbox.dhl24.com.pl/webapi2/provider/service.html?ws=1">
  <SOAP-ENV:Body>
    <ns1:getTrackAndTraceInfoResponse>
      <getTrackAndTraceInfoResult>
        <shipmentId>24333892874</shipmentId>
        <receivedBy></receivedBy>
        <events/>
      </getTrackAndTraceInfoResult>
    </ns1:getTrackAndTraceInfoResponse>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""
