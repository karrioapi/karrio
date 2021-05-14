import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship.core.models import TrackingRequest
from purplship import Tracking
from tests.purolator_courier.fixture import gateway


class TestPurolatorTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(
            tracking_numbers=TRACKING_REQUEST_PAYLOAD
        )

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TRACKING_REQUEST_XML)

    @patch("purplship.mappers.purolator_courier.proxy.http", return_value="<a></a>")
    def test_get_tracking(self, http_mock):
        Tracking.fetch(self.TrackingRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url, f"{gateway.settings.server_url}/PWS/V1/Tracking/TrackingService.asmx"
        )

    def test_tracking_response_parsing(self):
        with patch("purplship.mappers.purolator_courier.proxy.http") as mock:
            mock.return_value = TRACKING_RESPONSE_XML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(PARSED_TRACKING_RESPONSE)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_REQUEST_PAYLOAD = ["m123"]

PARSED_TRACKING_RESPONSE = [
    [
        {
            "carrier_name": "purolator_courier",
            "carrier_id": "purolator_courier",
            "events": [
                {
                    "code": "Other",
                    "date": "2004-01-13",
                    "description": "New Tracking Number Assigned -",
                    "location": "MONTREAL SORT CTR/CTR TRIE, PQ",
                    "time": "17:23",
                },
                {
                    "code": "Other",
                    "date": "2004-01-13",
                    "description": "New Tracking Number Assigned -",
                    "location": "MONTREAL SORT CTR/CTR TRIE, PQ",
                    "time": "17:23",
                },
            ],
            "tracking_number": "M123",
            "delivered": False
        }
    ],
    [],
]

TRACKING_REQUEST_XML = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://purolator.com/pws/datatypes/v1">
    <soap:Header>
        <v1:RequestContext>
            <v1:Version>1.2</v1:Version>
            <v1:Language>en</v1:Language>
            <v1:GroupID></v1:GroupID>
            <v1:RequestReference></v1:RequestReference>
            <v1:UserToken>token</v1:UserToken>
        </v1:RequestContext>
    </soap:Header>
    <soap:Body>
        <v1:TrackPackagesByPinRequest>
            <v1:PINs>
                <v1:PIN>
                    <v1:Value>m123</v1:Value>
                </v1:PIN>
            </v1:PINs>
        </v1:TrackPackagesByPinRequest>
    </soap:Body>
</soap:Envelope>
"""

TRACKING_RESPONSE_XML = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Header>
        <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1" 
            xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <h:ResponseReference>Rating Example</h:ResponseReference>
        </h:ResponseContext>
    </s:Header>
    <s:Body>
        <TrackPackagesByPinResponse xmlns="http://purolator.com/pws/datatypes/v1" 
            xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <ResponseInformation>
                <Errors/>
                <InformationalMessages i:nil="true"/>
            </ResponseInformation>
            <TrackingInformationList>
                <TrackingInformation>
                    <PIN>
                        <Value>M123</Value>
                    </PIN>
                    <Scans>
                        <Scan>
                            <ScanType>Other</ScanType>
                            <PIN>
                                <Value>M123</Value>
                            </PIN>
                            <Depot>
                                <Name>MONTREAL SORT CTR/CTR TRIE, PQ</Name>
                            </Depot>
                            <ScanDate>2004-01-13</ScanDate>
                            <ScanTime>172300</ScanTime>
                            <Description>New Tracking Number Assigned -</Description>
                            <Comment/>
                            <SummaryScanIndicator>false</SummaryScanIndicator>
                        </Scan>
                        <Scan>
                            <ScanType>Other</ScanType>
                            <PIN>
                                <Value>M123</Value>
                            </PIN>
                            <Depot>
                                <Name>MONTREAL SORT CTR/CTR TRIE, PQ</Name>
                            </Depot>
                            <ScanDate>2004-01-13</ScanDate>
                            <ScanTime>172300</ScanTime>
                            <Description>New Tracking Number Assigned -</Description>
                            <Comment/>
                            <SummaryScanIndicator>false</SummaryScanIndicator>
                        </Scan>
                    </Scans>
                    <ResponseInformation i:nil="true"/>
                </TrackingInformation>
            </TrackingInformationList>
        </TrackPackagesByPinResponse>
    </s:Body>
</s:Envelope>
"""
