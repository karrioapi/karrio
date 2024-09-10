import unittest
from unittest.mock import patch
from .fixture import gateway
import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLPolandTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize()[TRACKING_PAYLOAD[0]], TrackingRequestXML)

    def test_get_tracking(self):
        with patch("karrio.mappers.dhl_poland.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )
            self.assertEqual(
                mock.call_args[1]["headers"]["soapaction"],
                f"{gateway.settings.server_url}#getTrackAndTraceInfo",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dhl_poland.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseXML
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dhl_poland.proxy.lib.request") as mock:
            mock.return_value = ErrorResponseXML
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["24333892874"]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dhl_poland",
            "carrier_name": "dhl_poland",
            "delivered": True,
            "events": [
                {
                    "code": "string",
                    "date": "2012-10-12",
                    "description": "string",
                    "location": "string",
                    "time": "07:40 AM",
                },
                {
                    "code": "string",
                    "date": "2012-10-12",
                    "description": "string",
                    "location": "string",
                    "time": "06:40 AM",
                },
            ],
            "tracking_number": "24333892874",
            "info": {
                "carrier_tracking_link": "https://www.dhl.com/pl-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=24333892874"
            },
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "dhl_poland",
            "carrier_name": "dhl_poland",
            "code": "100",
            "details": {"tracking_number": "24333892874"},
            "message": "Nieprawidlowe dane autoryzacyjne",
        }
    ],
]

TrackingRequestXML = """<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/" xmlns="https://dhl24.com.pl/webapi2/provider/service.html?ws=1">
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

TrackingResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<getTrackAndTraceInfoResponse xmlns="https://dhl24.com.pl/webapi2/provider/service.html?ws=1" xsi:schemaLocation="https://dhl24.com.pl/webapi2/provider/service.html?ws=1 schema.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <getTrackAndTraceInfoResult>
    <shipmentId>24333892874</shipmentId>
    <receivedBy>string</receivedBy>
    <events>
      <item>
        <status>string</status>
        <description>string</description>
        <terminal>string</terminal>
        <timestamp>2012-10-12 07:40:31</timestamp>
      </item>
      <item>
        <status>string</status>
        <description>string</description>
        <terminal>string</terminal>
        <timestamp>2012-10-12 06:40:31</timestamp>
      </item>
    </events>
  </getTrackAndTraceInfoResult>
</getTrackAndTraceInfoResponse>
"""

ErrorResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
  xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
  <SOAP-ENV:Body>
    <SOAP-ENV:Fault>
      <faultcode>100</faultcode>
      <faultstring>Nieprawidlowe dane autoryzacyjne</faultstring>
    </SOAP-ENV:Fault>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""
