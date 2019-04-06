import unittest
from unittest.mock import patch
from tests.usps.fixture import proxy
from gds_helpers import to_dict, to_xml, export, jsonify
from purplship.domain.Types import TrackingRequest
from pyusps.trackfieldrequest import TrackFieldRequest
from tests.utils import strip


class TestUSPSTracking(unittest.TestCase):
    def setUp(self):
        self.RateRequest = TrackFieldRequest()
        self.RateRequest.build(to_xml(TRACKING_REQUEST_STR))

    def test_create_tracking_request(self):
        payload = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

        tracking_request = proxy.mapper.create_tracking_request(payload)
        self.assertEqual(strip(export(tracking_request)), strip(TRACKING_REQUEST_STR))

    @patch("purplship.mappers.usps.usps_proxy.http", return_value="<a></a>")
    @patch("urllib.parse.urlencode", return_value="")
    def test_get_tracking(self, encode_mock, http_mock):
        proxy.get_tracking(self.RateRequest)

        data = encode_mock.call_args[0][0]
        self.assertEqual(strip(jsonify(data)), strip(jsonify(TRACKING_REQUEST)))

    def test_parse_tracking_response(self):
        parsed_response = proxy.mapper.parse_tracking_response(
            to_xml(TRACKING_RESPONSE)
        )
        self.assertEqual(to_dict(parsed_response), PARSED_TRACKING_RESPONSE)


if __name__ == "__main__":
    unittest.main()


TRACKING_PAYLOAD = ["XXXXXXXXXXXX1"]

PARSED_TRACKING_RESPONSE = [
    [
        {
            "carrier": "USPS",
            "events": [
                {
                    "code": "03",
                    "date": "January 6, 2016",
                    "location": "LAKE CHARLES, IL, 12345",
                    "time": "9:10 am",
                }
            ],
        }
    ],
    [],
]


TRACKING_REQUEST_STR = f"""<TrackFieldRequest USERID="{proxy.client.username}">
    <Revision>1</Revision>
    <TrackID ID="XXXXXXXXXXXX1"/>
</TrackFieldRequest>
"""

TRACKING_REQUEST = {"API": "TrackV2", "XML": TRACKING_REQUEST_STR}

TRACKING_RESPONSE = """
<TrackResponse>
    <TrackInfo ID="XXXXXXXXXX1">
        <Class>First-Class Package Service - Retail</Class>
        <ClassOfMailCode>BP</ClassOfMailCode>
        <DestinationCity>KBEA</DestinationCity>
        <DestinationState>TX</DestinationState>
        <DestinationZip>12345</DestinationZip>
        <EmailEnabled>true</EmailEnabled>
        <KahalaIndicator>false</KahalaIndicator>
        <MailTypeCode>DM</MailTypeCode>
        <MPDATE>2016-01-08 10:34:04.000000</MPDATE>
        <MPSUFFIX>412725500</MPSUFFIX>
        <OriginCity>LAKE CHARLES</OriginCity>
        <OriginState>IL</OriginState>
        <OriginZip>12345</OriginZip>
        <PodEnabled>false</PodEnabled>
        <RestoreEnabled>false</RestoreEnabled>
        <RramEnabled>false</RramEnabled>
        <RreEnabled>false</RreEnabled>
        <Service>USPS Tracking&lt;SUP&gt;&amp;#174;&lt;/SUP&gt;</Service>
        <ServiceTypeCode>346</ServiceTypeCode>
        <Status>Arrived at facility</Status>
        <StatusCategory>In Transit</StatusCategory>
        <StatusSummary>Your item arrived at our USPS facility in COLUMBUS, OH 43218 on January 6, 2016 at 10:45 pm. The item is currently in transit to the destination.</StatusSummary>
        <TABLECODE>T</TABLECODE>
        <TpodEnabled>true</TpodEnabled>
        <EnabledNotificationRequests>
            <SMS>
                <FD>true</FD>
                <AL>true</AL>
                <TD>true</TD>
                <UP>true</UP>
                <DND>true</DND>
                <FS>true</FS>
                <OA>true</OA>
            </SMS>
            <EMAIL>
                <FD>true</FD>
                <AL>true</AL>
                <TD>true</TD>
                <UP>true</UP>
                <DND>true</DND>
                <FS>true</FS>
                <OA>true</OA>
            </EMAIL>
        </EnabledNotificationRequests>
        <TrackSummary>
            <EventTime>10:45 pm</EventTime>
            <EventDate>January 6, 2016</EventDate>
            <Event>Arrived at USPS Facility</Event>
            <EventCity>COLUMBUS</EventCity>
            <EventState>OH</EventState>
            <EventZIPCode>43218</EventZIPCode>
            <AuthorizedAgent>false</AuthorizedAgent>
            <EventCode>10</EventCode>
        </TrackSummary>
        <TrackDetail>
            <EventTime>9:10 am</EventTime>
            <EventDate>January 6, 2016</EventDate>
            <Event>Acceptance</Event>
            <EventCity>LAKE CHARLES</EventCity>
            <EventState>IL</EventState>
            <EventZIPCode>12345</EventZIPCode>
            <AuthorizedAgent>false</AuthorizedAgent>
            <EventCode>03</EventCode>
        </TrackDetail>
    </TrackInfo>
</TrackResponse>
"""
