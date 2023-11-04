import unittest
from unittest.mock import patch
from .fixture import gateway
from karrio.core.utils import DP
from karrio.core.models import TrackingRequest
from karrio import Tracking


class TestUSPSTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(request.serialize(), TRACKING_REQUEST)

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.usps.proxy.http") as mock:
            mock.return_value = TRACKING_RESPONSE
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), PARSED_TRACKING_RESPONSE)


if __name__ == "__main__":
    unittest.main()


TRACKING_PAYLOAD = ["XXXXXXXXXXXX1"]

PARSED_TRACKING_RESPONSE = [
    [
        {
            "carrier_id": "usps",
            "carrier_name": "usps",
            "delivered": False,
            "events": [
                {
                    "code": "10",
                    "date": "2016-01-06",
                    "description": "Arrived at USPS Facility",
                    "location": "COLUMBUS, OH, 43218",
                    "time": "10:45",
                },
                {
                    "code": "03",
                    "date": "2016-01-06",
                    "description": "Acceptance",
                    "location": "LAKE CHARLES, IL, 12345",
                    "time": "09:10",
                },
            ],
            "tracking_number": "XXXXXXXXXX1",
            "info": {
                "carrier_tracking_link": "https://tools.usps.com/go/TrackConfirmAction?tLabels=XXXXXXXXXX1",
                "shipment_destination_postal_code": 12345,
                "shipment_origin_postal_code": "12345",
                "shipment_service": "First-Class Package Service - Retail",
            },
            "status": "in_transit",
        }
    ],
    [],
]


TRACKING_REQUEST = f"""<TrackFieldRequest USERID="username">
    <Revision>1</Revision>
    <ClientIp>127.0.0.1</ClientIp>
    <SourceId>Karrio</SourceId>
    <TrackID ID="XXXXXXXXXXXX1"/>
</TrackFieldRequest>
"""

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
