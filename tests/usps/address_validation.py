import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import AddressValidationRequest
from purplship.package import Address
from tests.usps.fixture import gateway


class TestUSPSAddressValidation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = AddressValidationRequest(
            **AddressValidationPayload
        )

    def test_create_address_validation_request(self):
        request = gateway.mapper.create_address_validation_request(
            self.AddressValidationRequest
        )
        self.assertEqual(
            request.serialize(),
            AddressValidationRequestXML,
        )

    @patch("purplship.package.mappers.usps.proxy.http", return_value="<a></a>")
    def test_validated_address(self, http_mock):
        Address.validate(self.AddressValidationRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, gateway.settings.server_url)

    def test_parse_address_validation_response(self):
        with patch("purplship.package.mappers.usps.proxy.http") as mock:
            mock.return_value = AddressValidationResponseXML
            parsed_response = (
                Address.validate(self.AddressValidationRequest).from_(gateway).parse()
            )

            self.assertEqual(
                to_dict(parsed_response), to_dict(ParsedAddressValidationResponse)
            )


if __name__ == "__main__":
    unittest.main()


AddressValidationPayload = {}

ParsedAddressValidationResponse = {}


AddressValidationRequestXML = """<ns1:RouteRequest xmlns:ns1="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.comrouting-global-req.xsd" schemaVersion="2.0">
    <Request>
        <ServiceHeader>
            <MessageTime>2013-08-04T11:28:56.000-08:00</MessageTime>
            <MessageReference>Routing_Request_Global_AM_v62__</MessageReference>
            <SiteID>CustomerSiteID</SiteID>
            <Password>CustomerPassword</Password>
        </ServiceHeader>
        <MetaData>
            <SoftwareName>3PV</SoftwareName>
            <SoftwareVersion>1.0</SoftwareVersion>
        </MetaData>
    </Request>
    <RegionCode>AM</RegionCode>
    <RequestType>O</RequestType>
    <Address1>Suit 333</Address1>
    <Address2>333 Twin</Address2>
    <Address3 />
    <PostalCode>94089</PostalCode>
    <City>North Dakhota</City>
    <Division>California</Division>
    <CountryCode>US</CountryCode>
    <CountryName>United States of America</CountryName>
    <OriginCountryCode>US</OriginCountryCode>
</ns1:RouteRequest>
"""

AddressValidationResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<res:RouteResponse xmlns:res="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com routing-res.xsd">
    <Response>
        <ServiceHeader>
            <MessageTime>2018-02-21T04:01:48+01:00</MessageTime>
            <MessageReference>Routing_Request_Global_AM_v62__</MessageReference>
            <SiteID>CustomerSiteID</SiteID>
        </ServiceHeader>
    </Response>
    <Note>
        <ActionNote>Success</ActionNote>
    </Note>
    <GMTNegativeIndicator>Y</GMTNegativeIndicator>
    <GMTOffset>08:00</GMTOffset>
    <RegionCode>AM</RegionCode>
    <ServiceArea>
        <ServiceAreaCode>NUQ</ServiceAreaCode>
        <Description>NUQ|0|GMT-8:00|FREMONT,CA-USA|US</Description>
    </ServiceArea>
</res:RouteResponse>
<!-- ServiceInvocationId:20180221040147_aaa4_7b2d05d1-e388-4018-856c-fd997e4b4721 -->
"""
