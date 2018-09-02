import unittest
from unittest.mock import patch
from gds_helpers import to_xml, jsonify, export
from openship.domain.entities import Shipment
from tests.dhl.fixture import proxy
from tests.utils import strip


class TestDHLShipment(unittest.TestCase):

    @patch("openship.mappers.dhl.dhl_proxy.http", return_value='<a></a>')
    def test_create_quote_request(self, http_mock):
        shipper = {
            "company_name": "shipper company privated limited 12",
            "address_lines": ["238 850925434 Drive"],
            "city": "Scottsdale",
            "postal_code": "85260",
            "country_code": "US",
            "country_name": "United States of America",
            "person_name": "Ms Lucian",
            "phone_number": "1 23 8613402",
            "email_address": "test@email.com",
            "state_or_province": "Arizona",
            "state_or_province_code": "AZ",
            "extra": {
                "ShipperID": "123456789",
                "RegisteredAccount": "123456789",
                "PhoneExtension": "3403",
                "FaxNumber": "1 905 8613411",
                "Telex": "1245"
            }
        }
        recipient = {
            "company_name": "IBM Bruse Pte Ltd",
            "address_lines": ["9 Business Park Central 1", "3th Floor", "The IBM Place"],
            "city": "Brussels",
            "postal_code": "1060",
            "country_code": "BE",
            "country_name": "Belgium",
            "person_name": "Mrs Orlander",
            "phone_number": "506-851-2271",
            "email_address": "c_orlander@gc.ca",
            "extra": {
                "PhoneExtension": "7862",
                "FaxNumber": "506-851-7403",
                "Telex": "506-851-7121"
            }
        }
        shipment = {
            "packages": [{"id": "1", "height": 3, "length": 10, "width": 3, "weight": 4.0, "packaging_type": "EE"}],
            "is_document": False,
            "shipper_account_number": "123456789",
            "paid_by": "S",
            "payment_account_number": "123456789",
            "duty_paid_by": "S",
            "duty_payment_account": "123456789",
            "declared_value": 200.00,
            "label": {"type": "CIN", "format": "PDF", "extra": {"Image": b"SUkqAAgA"}},
            "services": ["WY"],
            "commodities": [{"code": "cc", "description": "cn"}],
            "extra": {"EProcShip": "N", "GlobalProductCode": "P", "LocalProductCode": "P"},
            "customs": {
                "terms_of_trade": "DAP",
                "extra": {
                    "ScheduleB": "3002905110",
                    "ExportLicense": "D123456",
                    "ShipperEIN": "112233445566",
                    "ShipperIDType": "S",
                    "ImportLicense": "ImportLic",
                    "ConsigneeEIN": "ConEIN2123"
                }
            }
        }
        payload = Shipment.create(
            shipper=shipper, recipient=recipient, shipment=shipment)
        quote_req_xml_obj = proxy.mapper.create_shipment_request(payload)

        # remove MessageTime for testing purpose
        quote_req_xml_obj.Request.ServiceHeader.MessageTime = None

        proxy.create_shipment(quote_req_xml_obj)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(ShipmentRequestXml %
                                              quote_req_xml_obj.ShipmentDetails.Date))

    def test_parse_shipment_missing_args_error(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(ShipmentMissingArgsError))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedShipmentMissingArgsError))


if __name__ == '__main__':
    unittest.main()


ParsedShipmentMissingArgsError = [
    [],
    [
        {
            'carrier': 'carrier_name',
            'code': '152',
            'message': 'Shipment Details segment Contents\n                    Conditional Required Error'
        }
    ]
]

ParsedShipmentParsingError = [
]

ParsedShipmentResponse = [
]


ShipmentParsingError = """
"""

ShipmentMissingArgsError = """<?xml version="1.0" encoding="UTF-8"?>
<res:ShipmentValidateErrorResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com ship-val-err-res.xsd'>
    <Response>
        <ServiceHeader>
            <MessageTime>2018-08-31T21:19:52+01:00</MessageTime>
            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>dollarog</SiteID>
        </ServiceHeader>
        <Status>
            <ActionStatus/>
            <Condition>
                <ConditionCode>152</ConditionCode>
                <ConditionData>Shipment Details segment Contents
                    Conditional Required Error</ConditionData>
            </Condition>
        </Status>
    </Response>
</res:ShipmentValidateErrorResponse>
<!-- ServiceInvocationId:20180831211951_7837_4526a967-d468-4741-a69e-88be23f892dc -->
"""

ShipmentRequestXml = """<req:ShipmentRequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com ship-val-global-req.xsd" schemaVersion="6.1">
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
    <RequestedPickupTime>Y</RequestedPickupTime>
    <LanguageCode>en</LanguageCode>
    <PiecesEnabled>Y</PiecesEnabled>
    <Billing>
        <ShipperAccountNumber>123456789</ShipperAccountNumber>
        <ShippingPaymentType>S</ShippingPaymentType>
        <BillingAccountNumber>123456789</BillingAccountNumber>
        <DutyPaymentType>S</DutyPaymentType>
        <DutyAccountNumber>123456789</DutyAccountNumber>
    </Billing>
    <Consignee>
        <CompanyName>IBM Bruse Pte Ltd</CompanyName>
        <AddressLine>9 Business Park Central 1</AddressLine>
        <AddressLine>3th Floor</AddressLine>
        <AddressLine>The IBM Place</AddressLine>
        <City>Brussels</City>
        <PostalCode>1060</PostalCode>
        <CountryCode>BE</CountryCode>
        <CountryName>Belgium</CountryName>
        <Contact>
            <PersonName>Mrs Orlander</PersonName>
            <PhoneNumber>506-851-2271</PhoneNumber>
            <PhoneExtension>7862</PhoneExtension>
            <FaxNumber>506-851-7403</FaxNumber>
            <Telex>506-851-7121</Telex>
            <Email>c_orlander@gc.ca</Email>
        </Contact>
    </Consignee>
    <Commodity>
        <CommodityCode>cc</CommodityCode>
        <CommodityName>cn</CommodityName>
    </Commodity>
    <Dutiable>
        <DeclaredValue>200.</DeclaredValue>
        <DeclaredCurrency>USD</DeclaredCurrency>
        <ScheduleB>3002905110</ScheduleB>
        <ExportLicense>D123456</ExportLicense>
        <ShipperEIN>112233445566</ShipperEIN>
        <ShipperIDType>S</ShipperIDType>
        <ImportLicense>ImportLic</ImportLicense>
        <ConsigneeEIN>ConEIN2123</ConsigneeEIN>
        <TermsOfTrade>DAP</TermsOfTrade>
    </Dutiable>
    <ShipmentDetails>
        <NumberOfPieces>1</NumberOfPieces>
        <Pieces>
            <Piece>
                <PieceID>1</PieceID>
                <PackageType>EE</PackageType>
                <Weight>4.</Weight>
                <Width>3</Width>
                <Height>3</Height>
                <Depth>10</Depth>
            </Piece>
        </Pieces>
        <Weight>4.</Weight>
        <WeightUnit>L</WeightUnit>
        <GlobalProductCode>P</GlobalProductCode>
        <LocalProductCode>P</LocalProductCode>
        <Date>%s</Date>
        <Contents></Contents>
        <DimensionUnit>I</DimensionUnit>
        <IsDutiable>Y</IsDutiable>
        <CurrencyCode>USD</CurrencyCode>
    </ShipmentDetails>
    <Shipper>
        <ShipperID>123456789</ShipperID>
        <CompanyName>shipper company privated limited 12</CompanyName>
        <RegisteredAccount>123456789</RegisteredAccount>
        <AddressLine>238 850925434 Drive</AddressLine>
        <City>Scottsdale</City>
        <Division>Arizona</Division>
        <DivisionCode>AZ</DivisionCode>
        <PostalCode>85260</PostalCode>
        <CountryCode>US</CountryCode>
        <CountryName>United States of America</CountryName>
        <Contact>
            <PersonName>Ms Lucian</PersonName>
            <PhoneNumber>1 23 8613402</PhoneNumber>
            <PhoneExtension>3403</PhoneExtension>
            <FaxNumber>1 905 8613411</FaxNumber>
            <Telex>1245</Telex>
            <Email>test@email.com</Email>
        </Contact>
    </Shipper>
    <SpecialService>
        <SpecialServiceType>WY</SpecialServiceType>
    </SpecialService>
    <EProcShip>N</EProcShip>
    <DocImages>
        <DocImage>
            <Type>CIN</Type>
            <Image>b'U1VrcUFBZ0E='</Image>
            <ImageFormat>PDF</ImageFormat>
        </DocImage>
    </DocImages>
</req:ShipmentRequest>
"""

ShipmentResponseXml = """
"""
