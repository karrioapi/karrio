"""DPD France tracking tests (GetShipmentTrace)."""

import unittest
from unittest.mock import patch

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models

from .fixture import gateway


class TestDPDFranceTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(request.serialize(), TrackingRequestXML)

    def test_get_tracking(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = "<r></r>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(mock.call_args[1]["url"], gateway.settings.tracking_url)
            self.assertEqual(
                mock.call_args[1]["headers"]["SOAPAction"],
                "http://www.cargonet.software/GetShipmentTrace",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseXML
            parsed = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd_france.proxy.lib.request") as mock:
            mock.return_value = ErrorResponseXML
            parsed = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {"tracking_numbers": ["250123456789012345"]}

TrackingRequestXML = [
    (
        "250123456789012345",
        """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:imt="http://www.cargonet.software/">
    <soapenv:Header>
        <imt:UserCredentials>
            <imt:userid>test</imt:userid>
            <imt:password>test</imt:password>
        </imt:UserCredentials>
    </soapenv:Header>
    <soapenv:Body>
        <imt:GetShipmentTrace>
            <imt:request>
                <imt:Customer>
                    <imt:centernumber>123</imt:centernumber>
                    <imt:number>456789</imt:number>
                    <imt:countrycode>250</imt:countrycode>
                </imt:Customer>
                <imt:Language>EN</imt:Language>
                <imt:ShipmentNumber>250123456789012345</imt:ShipmentNumber>
                <tns:ExpandContainerMode xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
                <GetPhotos xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
                <GetParsedInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
                <GetServices xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
            </imt:request>
        </imt:GetShipmentTrace>
    </soapenv:Body>
</soapenv:Envelope>
""",
    ),
]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dpd_france",
            "carrier_name": "dpd_france",
            "delivered": False,
            "events": [
                {
                    "code": "10",
                    "date": "2026-04-15",
                    "description": "Picked up by driver",
                    "location": "TOULON",
                    "time": "09:15 AM",
                },
                {
                    "code": "50",
                    "date": "2026-04-16",
                    "description": "Delivered to recipient",
                    "location": "MENTON",
                    "time": "14:32 PM",
                },
            ],
            "tracking_number": "250123456789012345",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "dpd_france",
            "carrier_name": "dpd_france",
            "code": "IpPermissionDenied",
            "details": {"tracking_number": "250123456789012345"},
            "message": "Caller IP not whitelisted",
        }
    ],
]


TrackingResponseXML = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetShipmentTraceResponse xmlns="http://www.cargonet.software/">
      <GetShipmentTraceResult>
        <ShipmentNumber>250123456789012345</ShipmentNumber>
        <DestinationCountry>FR</DestinationCountry>
        <DestinationZipcode>06500</DestinationZipcode>
        <Traces>
          <clsTrace>
            <ScanDate>2026-04-15</ScanDate>
            <ScanTime>09:15:00</ScanTime>
            <StatusNumber>10</StatusNumber>
            <StatusDescription>Picked up by driver</StatusDescription>
            <CenterName>TOULON</CenterName>
          </clsTrace>
          <clsTrace>
            <ScanDate>2026-04-16</ScanDate>
            <ScanTime>14:32:00</ScanTime>
            <StatusNumber>50</StatusNumber>
            <StatusDescription>Delivered to recipient</StatusDescription>
            <CenterName>MENTON</CenterName>
          </clsTrace>
        </Traces>
      </GetShipmentTraceResult>
    </GetShipmentTraceResponse>
  </soap:Body>
</soap:Envelope>"""

ErrorResponseXML = """<?xml version="1.0"?>
<Error><ErrorId>IpPermissionDenied</ErrorId><ErrorMessage>Caller IP not whitelisted</ErrorMessage></Error>"""
