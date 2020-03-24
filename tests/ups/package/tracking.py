import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import TrackingRequest
from tests.ups.package.fixture import gateway
from purplship.package import tracking


class TestUPSTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TrackingRequestPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), [TrackingRequestXml])

    @patch("purplship.package.mappers.ups.proxy.http", return_value="<a></a>")
    def test_get_tracking(self, http_mock):
        tracking.fetch(self.TrackingRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/Track")

    def test_tracking_auth_error_parsing(self):
        with patch("purplship.package.mappers.ups.proxy.http") as mock:
            mock.return_value = AuthError
            parsed_response = (
                tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertEqual(to_dict(parsed_response), to_dict(ParsedAuthError))

    def test_tracking_response_parsing(self):
        with patch("purplship.package.mappers.ups.proxy.http") as mock:
            mock.return_value = TrackingResponseXml
            parsed_response = (
                tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(to_dict(parsed_response), to_dict(ParsedTrackingResponse))

    def test_tracking_unknown_response_parsing(self):
        with patch("purplship.package.mappers.ups.proxy.http") as mock:
            mock.return_value = InvalidTrackingNumberResponseXML
            parsed_response = (
                tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertEqual(
                to_dict(parsed_response), to_dict(ParsedInvalidTrackingNumberResponse)
            )


if __name__ == "__main__":
    unittest.main()


TrackingRequestPayload = ["1Z12345E6205277936"]

ParsedAuthError = [
    [],
    [{"carrier": "UPS", "code": "250003", "message": "Invalid Access License number"}],
]

ParsedTrackingResponse = [
    [
        {
            "carrier": "UPS",
            "events": [
                {
                    "code": "KB",
                    "date": "2010-08-30",
                    "description": "UPS INTERNAL ACTIVITY CODE",
                    "location": "BONN",
                    "time": "10:39",
                },
                {
                    "code": "DJ",
                    "date": "2010-08-30",
                    "description": "ADVERSE WEATHER CONDITIONS CAUSED THIS DELAY",
                    "location": "BONN",
                    "time": "10:32",
                },
                {
                    "code": "X",
                    "date": "2010-09-10",
                    "description": "THE RECEIVER'S LOCATION WAS CLOSED ON THE 2ND DELIVERY ATTEMPT. A 3RD DELIVERY ATTEMPT WILL BE MADE",
                    "location": "ANYTOWN",
                    "time": "18:03",
                },
                {
                    "code": "FS",
                    "date": "2010-09-12",
                    "description": "DELIVERED",
                    "location": "ANYTOWN",
                    "time": "11:57",
                },
                {
                    "code": "PU",
                    "date": "2010-04-04",
                    "description": "PICKUP SCAN",
                    "location": "WEST CHESTER-MALVERN",
                    "time": "14:40",
                },
                {
                    "code": "KB",
                    "date": "2010-08-30",
                    "description": "UPS INTERNAL ACTIVITY CODE",
                    "location": "BONN",
                    "time": "13:13",
                },
            ],
            "tracking_number": "1Z12345E6205277936",
        }
    ],
    [],
]

ParsedInvalidTrackingNumberResponse = [
    [],
    [{"carrier": "UPS", "code": "151018", "message": "Invalid tracking number"}],
]


AuthError = """<wrapper>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header/>
        <soapenv:Body>
            <soapenv:Fault>
                <faultcode>Client</faultcode>
                <faultstring>An exception has been raised as a result of client data.</faultstring>
                <detail>
                    <err:Errors xmlns:err="http://www.ups.com/XMLSchema/XOLTWS/Error/v1.1">
                        <err:ErrorDetail>
                            <err:Severity>Authentication</err:Severity>
                            <err:PrimaryErrorCode>
                                <err:Code>250003</err:Code>
                                <err:Description>Invalid Access License number</err:Description>
                            </err:PrimaryErrorCode>
                            <err:Location>
                                <err:LocationElementName>upss:AccessLicenseNumber</err:LocationElementName>
                                <err:XPathOfElement>/tns:Envelope[1]/tns:Header[1]/upss:UPSSecurity[1]/upss:ServiceAccessToken[1]/upss:AccessLicenseNumber[1]</err:XPathOfElement>
                                <err:OriginalValue>FG09H9G8H09GH8G0</err:OriginalValue>
                            </err:Location>
                        </err:ErrorDetail>
                    </err:Errors>
                </detail>
            </soapenv:Fault>
        </soapenv:Body>
    </soapenv:Envelope>
</wrapper>
"""

TrackingRequestXml = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:trk="http://www.ups.com/XMLSchema/XOLTWS/Track/v2.0" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" >
    <tns:Header>
        <upss:UPSSecurity>
            <UsernameToken>
                <Username>username</Username>
                <Password>password</Password>
            </UsernameToken>
            <ServiceAccessToken>
                <AccessLicenseNumber>FG09H9G8H09GH8G0</AccessLicenseNumber>
            </ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <trk:TrackRequest>
            <common:Request>
                <RequestOption>1</RequestOption>
                <TransactionReference>
                    <TransactionIdentifier>TransactionIdentifier</TransactionIdentifier>
                </TransactionReference>
            </common:Request>
            <InquiryNumber>1Z12345E6205277936</InquiryNumber>
        </trk:TrackRequest>
    </tns:Body>
</tns:Envelope>
"""

TrackingResponseXml = """<wrapper>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header/>
        <soapenv:Body>
            <trk:TrackResponse xmlns:trk="http://www.ups.com/XMLSchema/XOLTWS/Track/v2.0">
                <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                    <common:ResponseStatus>
                        <common:Code>1</common:Code>
                        <common:Description>Success</common:Description>
                    </common:ResponseStatus>
                    <common:TransactionReference>
                        <common:TransactionIdentifier>ciewstt217q879Ddg9vLBK</common:TransactionIdentifier>
                    </common:TransactionReference>
                </common:Response>
                <trk:Shipment>
                    <trk:InquiryNumber>
                        <trk:Code>01</trk:Code>
                        <trk:Description>ShipmentIdentificationNumber</trk:Description>
                        <trk:Value>1Z12345E6205277936</trk:Value>
                    </trk:InquiryNumber>
                    <trk:ShipmentType>
                        <trk:Code>01</trk:Code>
                        <trk:Description>Small Package</trk:Description>
                    </trk:ShipmentType>
                    <trk:ShipperNumber>12345E</trk:ShipperNumber>
                    <trk:Service>
                        <trk:Code>13</trk:Code>
                        <trk:Description>NEXT DAY AIR SAVER</trk:Description>
                    </trk:Service>
                    <trk:Package>
                        <trk:TrackingNumber>1Z12345E6205277936</trk:TrackingNumber>
                        <trk:Activity>
                            <trk:ActivityLocation>
                                <trk:Address>
                                    <trk:City>BONN</trk:City>
                                    <trk:CountryCode>DE</trk:CountryCode>
                                </trk:Address>
                            </trk:ActivityLocation>
                            <trk:Status>
                                <trk:Type>X</trk:Type>
                                <trk:Description>UPS INTERNAL ACTIVITY CODE</trk:Description>
                                <trk:Code>KB</trk:Code>
                            </trk:Status>
                            <trk:Date>20100830</trk:Date>
                            <trk:Time>103900</trk:Time>
                        </trk:Activity>
                        <trk:Activity>
                            <trk:ActivityLocation>
                                <trk:Address>
                                    <trk:City>BONN</trk:City>
                                    <trk:CountryCode>DE</trk:CountryCode>
                                </trk:Address>
                            </trk:ActivityLocation>
                            <trk:Status>
                                <trk:Type>X</trk:Type>
                                <trk:Description>ADVERSE WEATHER CONDITIONS CAUSED THIS DELAY</trk:Description>
                                <trk:Code>DJ</trk:Code>
                            </trk:Status>
                            <trk:Date>20100830</trk:Date>
                            <trk:Time>103200</trk:Time>
                        </trk:Activity>
                        <trk:Activity>
                            <trk:ActivityLocation>
                                <trk:Address>
                                    <trk:City>ANYTOWN</trk:City>
                                    <trk:StateProvinceCode>GA</trk:StateProvinceCode>
                                    <trk:CountryCode>US</trk:CountryCode>
                                </trk:Address>
                            </trk:ActivityLocation>
                            <trk:Status>
                                <trk:Description>THE RECEIVER'S LOCATION WAS CLOSED ON THE 2ND DELIVERY ATTEMPT. A 3RD DELIVERY ATTEMPT WILL BE MADE</trk:Description>
                                <trk:Code>X</trk:Code>
                            </trk:Status>
                            <trk:Date>20100910</trk:Date>
                            <trk:Time>180300</trk:Time>
                        </trk:Activity>
                        <trk:Activity>
                            <trk:ActivityLocation>
                                <trk:Address>
                                    <trk:City>ANYTOWN</trk:City>
                                    <trk:StateProvinceCode>GA</trk:StateProvinceCode>
                                    <trk:PostalCode>30340</trk:PostalCode>
                                    <trk:CountryCode>US</trk:CountryCode>
                                </trk:Address>
                                <trk:Code>MX</trk:Code>
                                <trk:Description>LEFT AT</trk:Description>
                            </trk:ActivityLocation>
                            <trk:Status>
                                <trk:Type>D</trk:Type>
                                <trk:Description>DELIVERED</trk:Description>
                                <trk:Code>FS</trk:Code>
                            </trk:Status>
                            <trk:Date>20100912</trk:Date>
                            <trk:Time>115700</trk:Time>
                        </trk:Activity>
                        <trk:Activity>
                            <trk:ActivityLocation>
                                <trk:Address>
                                    <trk:City>WEST CHESTER-MALVERN</trk:City>
                                    <trk:StateProvinceCode>GA</trk:StateProvinceCode>
                                    <trk:CountryCode>US</trk:CountryCode>
                                </trk:Address>
                            </trk:ActivityLocation>
                            <trk:Status>
                                <trk:Type>P</trk:Type>
                                <trk:Description>PICKUP SCAN</trk:Description>
                                <trk:Code>PU</trk:Code>
                            </trk:Status>
                            <trk:Date>20100404</trk:Date>
                            <trk:Time>144000</trk:Time>
                        </trk:Activity>
                        <trk:Activity>
                            <trk:ActivityLocation>
                                <trk:Address>
                                    <trk:City>BONN</trk:City>
                                    <trk:CountryCode>DE</trk:CountryCode>
                                </trk:Address>
                            </trk:ActivityLocation>
                            <trk:Status>
                                <trk:Type>X</trk:Type>
                                <trk:Description>UPS INTERNAL ACTIVITY CODE</trk:Description>
                                <trk:Code>KB</trk:Code>
                            </trk:Status>
                            <trk:Date>20100830</trk:Date>
                            <trk:Time>131300</trk:Time>
                        </trk:Activity>
                        <trk:PackageWeight>
                            <trk:UnitOfMeasurement>
                                <trk:Code>LBS</trk:Code>
                            </trk:UnitOfMeasurement>
                            <trk:Weight>1.00</trk:Weight>
                        </trk:PackageWeight>
                    </trk:Package>
                </trk:Shipment>
                <trk:Disclaimer>You are using UPS tracking service on customer integration test environment, please switch to UPS production environment once you finish the test. The URL is https://onlinetools.ups.com/webservices/Track</trk:Disclaimer>
            </trk:TrackResponse>
        </soapenv:Body>
    </soapenv:Envelope>
</wrapper>
"""

InvalidTrackingNumberResponseXML = """<wrapper>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header/>
        <soapenv:Body>
            <soapenv:Fault>
                <faultcode>Client</faultcode>
                <faultstring>An exception has been raised as a result of client data.</faultstring>
                <detail>
                    <err:Errors xmlns:err="http://www.ups.com/XMLSchema/XOLTWS/Error/v1.1">
                        <err:ErrorDetail>
                            <err:Severity>Hard</err:Severity>
                            <err:PrimaryErrorCode>
                                <err:Code>151018</err:Code>
                                <err:Description>Invalid tracking number</err:Description>
                            </err:PrimaryErrorCode>
                        </err:ErrorDetail>
                    </err:Errors>
                </detail>
            </soapenv:Fault>
        </soapenv:Body>
    </soapenv:Envelope>
</wrapper>
"""
