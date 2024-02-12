import re
import unittest
import logging
from unittest.mock import patch
import karrio
from karrio.core.utils import DP
from karrio.core.models import AddressValidationRequest
from .fixture import gateway


class TestDHLAddressValidation(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.AddressValidationRequest = AddressValidationRequest(
            **address_validation_data
        )

    def test_create_AddressValidation_request(self):
        request = gateway.mapper.create_address_validation_request(
            self.AddressValidationRequest
        )

        # remove MessageTime, Date and ReadyTime for testing purpose
        self.assertEqual(
            re.sub(
                "            <MessageTime>[^>]+</MessageTime>", "", request.serialize()
            ),
            AddressValidationRequestXML,
        )

    def test_validate_address(self):
        with patch("karrio.mappers.dhl_express.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Address.validate(self.AddressValidationRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/XMLShippingServlet",
            )

    def test_parse_address_validation_response(self):
        with patch("karrio.mappers.dhl_express.proxy.lib.request") as mock:
            mock.return_value = AddressValidationResponseXML
            parsed_response = (
                karrio.Address.validate(self.AddressValidationRequest)
                .from_(gateway)
                .parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedAddressValidationResponse)
            )


if __name__ == "__main__":
    unittest.main()

address_validation_data = {
    "address": {
        "address_line1": "333 Twin",
        "address_line2": "Suit 333",
        "postal_code": "94089",
        "city": "North Dakhota",
        "country_code": "US",
        "state_code": "CA",
    }
}

ParsedAddressValidationResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "dhl_express",
        "success": True,
    },
    [],
]


AddressValidationRequestXML = """<RouteRequest xmlns:ns1="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com routing-global-req.xsd" schemaVersion="2">
    <Request>
        <ServiceHeader>

            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>site_id</SiteID>
            <Password>password</Password>
        </ServiceHeader>
        <MetaData>
            <SoftwareName>3PV</SoftwareName>
            <SoftwareVersion>1.0</SoftwareVersion>
        </MetaData>
    </Request>
    <RegionCode>AM</RegionCode>
    <RequestType>D</RequestType>
    <Address1>333 Twin</Address1>
    <Address2>Suit 333</Address2>
    <PostalCode>94089</PostalCode>
    <City>North Dakhota</City>
    <Division>California</Division>
    <CountryCode>US</CountryCode>
    <CountryName>United States</CountryName>
    <OriginCountryCode>US</OriginCountryCode>
</RouteRequest>
"""

AddressValidationResponseXML = """<res:RouteResponse xmlns:res="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com routing-res.xsd">
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
