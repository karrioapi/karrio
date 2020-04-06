import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import TrackingRequest
from purplship.package import Tracking
from tests.purolator.package.fixture import gateway


class TestPurolatorTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(
            tracking_numbers=TRACKING_REQUEST_PAYLOAD
        )

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TRACKING_REQUEST_XML)

    @patch("purplship.package.mappers.purolator.proxy.http", return_value="<a></a>")
    def test_get_tracking(self, http_mock):
        Tracking.fetch(self.TrackingRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url, f"{gateway.settings.server_url}/PWS/V1/Tracking/TrackingService.asmx"
        )

    def test_tracking_response_parsing(self):
        with patch("purplship.package.mappers.purolator.proxy.http") as mock:
            mock.return_value = TRACKING_RESPONSE_XML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                to_dict(parsed_response), to_dict(PARSED_TRACKING_RESPONSE)
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_REQUEST_PAYLOAD = ["m123"]

PARSED_TRACKING_RESPONSE = [
    [
        {
            "carrier": "purolator",
            "carrier_name": "PurolatorCourier",
            "events": [
                {
                    "code": "Other",
                    "date": "2004-01-13",
                    "description": "New Tracking Number Assigned -",
                    "location": "MONTREAL SORT CTR/CTR TRIE, PQ",
                    "time": "23:51",
                },
                {
                    "code": "Other",
                    "date": "2004-01-13",
                    "description": "New Tracking Number Assigned -",
                    "location": "MONTREAL SORT CTR/CTR TRIE, PQ",
                    "time": "23:51",
                },
            ],
            "tracking_number": "M123",
        }
    ],
    [],
]

TRACKING_REQUEST_XML = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://purolator.com/pws/datatypes/v2" xmlns="http://purolator.com/pws/datatypes/v2">
    <soap:Header>
        <v2:RequestContext>
            <Version>1.1</Version>
            <Language>en</Language>
            <GroupID></GroupID>
            <RequestReference></RequestReference>
            <UserToken>token</UserToken>
        </v2:RequestContext>
    </soap:Header>
    <soap:Body>
        <v2:TrackPackagesByPinRequest>
            <PINs>
                <PIN>
                    <Value>m123</Value>
                </PIN>
            </PINs>
        </v2:TrackPackagesByPinRequest>
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
