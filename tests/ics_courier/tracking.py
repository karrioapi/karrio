import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship import Tracking
from purplship.core.models import TrackingRequest
from tests.ics_courier.fixture import gateway


class TestICSCourierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize()[0], TrackingRequestXML)

    def test_get_tracking(self):
        with patch("purplship.mappers.ics_courier.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/ICSCourierAddonsService.ICSCourierAddonsServiceHttpSoap12Endpoint/",
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"], "urn:trackByBarcodeV2"
            )

    def test_parse_tracking_response(self):
        with patch("purplship.mappers.ics_courier.proxy.http") as mock:
            mock.return_value = TrackingResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse))


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["1Z12345E6205277936"]

ParsedTrackingResponse = [
]

TrackingRequestXML = """<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <TracePackge xmlns="http://www.icscourier.ca/">
            <TrackNums>
                <string>1Z12345E6205277936</string>
            </TrackNums>
            <DetailInfo>boolean</DetailInfo>
        </TracePackge>
    </soap12:Body>
</soap12:Envelope>
"""

TrackingResponseXML = """
"""

TrackingNotFoundResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <TracePackgeResponse xmlns="http://www.icscourier.ca/">
      <TracePackgeResult>
        <Err>
          <_ErrCode>string</_ErrCode>
          <_ErrDescription>string</_ErrDescription>
        </Err>
        <TrackingInfo>
          <TrackingInfo>
            <TrackingNum>string</TrackingNum>
            <StatusDate>dateTime</StatusDate>
            <Status>string</Status>
            <Signby>string</Signby>
          </TrackingInfo>
          <TrackingInfo>
            <TrackingNum>string</TrackingNum>
            <StatusDate>dateTime</StatusDate>
            <Status>string</Status>
            <Signby>string</Signby>
          </TrackingInfo>
        </TrackingInfo>
      </TracePackgeResult>
    </TracePackgeResponse>
  </soap12:Body>
</soap12:Envelope>
"""
