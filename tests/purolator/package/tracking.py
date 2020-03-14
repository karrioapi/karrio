import re
import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import TrackingRequest
from purplship.package import tracking
from tests.dhl.package.fixture import gateway


class TestDHLTracking(unittest.TestCase):
    def setUp(self):
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_REQUEST_PAYLOAD)


if __name__ == "__main__":
    unittest.main()

TRACKING_REQUEST_PAYLOAD = ["8346088391"]

TRACKING_REQUEST_XML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:ns1="http://purolator.com/pws/datatypes/v1">
    <SOAP-ENV:Header>
        <ns1:RequestContext>
            <ns1:Version>1.0</ns1:Version>
            <ns1:Language>en</ns1:Language>
            <ns1:GroupID>xxx</ns1:GroupID>
            <ns1:RequestReference>Rating Example</ns1:RequestReference>
        </ns1:RequestContext>
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
        <ns1:TrackPackagesByPinRequest>
            <ns1:PINs>
                <ns1:PIN>
                    <ns1:Value>m123</ns1:Value>
                </ns1:PIN>
            </ns1:PINs>
        </ns1:TrackPackagesByPinRequest>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

TRACKING_RESPONSE_XML ="""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
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
