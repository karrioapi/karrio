import unittest
from unittest.mock import patch
import time
from gds_helpers import to_xml, jsonify, export
from pydhl.ship_val_global_req_61 import ShipmentRequest
from purplship.domain.entities import Shipment
from tests.dhl.fixture import proxy
from tests.utils import strip


class TestDHLShipment(unittest.TestCase):
    def setUp(self):
        self.ShipmentRequest = ShipmentRequest()
        self.ShipmentRequest.build(to_xml(ShipmentRequestXml))

    def test_create_shipment_request(self):
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
            "state": "Arizona",
            "state_code": "AZ",
            "account_number": "123456789",
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
            "items": [
                {"id": "1", "height": 3, "length": 10, "width": 3, "weight": 4.0, "packaging_type": "EE", "code": "cc", "description": "cn"}
            ],
            "is_document": False,
            "paid_by": "S",
            "payment_account_number": "123456789",
            "duty_paid_by": "S",
            "duty_payment_account": "123456789",
            "declared_value": 200.00,
            "label": {
                "type": "CIN", 
                "format": "PDF", 
                "extra": {
                    "Image": "data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs="
                }
            },
            "service_type": "WY",
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
        ShipmentRequest_ = proxy.mapper.create_shipment_request(payload)

        # remove MessageTime, Date for testing purpose
        ShipmentRequest_.Request.ServiceHeader.MessageTime = None
        ShipmentRequest_.ShipmentDetails.Date = None

        self.assertEqual(export(ShipmentRequest_), export(self.ShipmentRequest))

    @patch("purplship.mappers.dhl.dhl_proxy.http", return_value='<a></a>')
    def test_create_shipment(self, http_mock):
        proxy.create_shipment(self.ShipmentRequest)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(ShipmentRequestXml))
                
    def test_parse_shipment_error(self):
        parsed_response = proxy.mapper.parse_shipment_response(
            to_xml(ShipmentParsingError))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedShipmentParsingError))

    def test_shipment_missing_args_error_parsing(self):
        parsed_response = proxy.mapper.parse_shipment_response(
            to_xml(ShipmentMissingArgsError))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedShipmentMissingArgsError))

    def test_parse_shipment_response(self):
        parsed_response = proxy.mapper.parse_shipment_response(
            to_xml(ShipmentResponseXml))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedShipmentResponse))


if __name__ == '__main__':
    unittest.main()

ParsedShipmentMissingArgsError = [
    None,
    [
        {
            'carrier': 'carrier_name',
            'code': '152',
            'message': 'Shipment Details segment Contents\n                    Conditional Required Error'
        }
    ]
]

ParsedShipmentParsingError = [
    None, 
    [
        {
            'carrier': 'carrier_name', 
            'code': 'PLT006', 
            'message': "Paperless shipment service is not allowed\n                    for one of these reasons: Shipper or receiver\n                    country doesn't support Paperless Service, the\n                    product selected doesn't support Paperless or\n                    the declared value entered is greater than the\n                    allowed limit. Please contact DHL representative for\n                    further information or resubmit as regular shipment."
        }
    ]
]

ParsedShipmentResponse =  [
    {
        'carrier': 'carrier_name', 
        'charges': [
            {'amount': 124.69, 'currency': 'USD', 'name': 'PackageCharge'}
        ], 
        'documents': [
            'iVBORw0KGgoAAAANSUhEUgAAAYwAAABeAQMAAAAKdrGZAAAABlBMVEX///8AAABVwtN+AAAAaklEQVR42mNkYGBIyL8w5a9P7YJXKU8ZgkU2V81cNmWt5IIokaMMX40+N6zsivI+93bZRDMx13vzlRYwMDAxkAxGtYxqGdUyqmVUy6iWUS2jWka1jGoZ1TKqZVTLqJZRLaNaRrWMaiEVAAB3uBe8nSip8QAAAABJRU5ErkJggg==', 
            'iVBORw0KGgoAAAANSUhEUgAAAZYAAABeAQMAAAA6+qC4AAAABlBMVEX///8AAABVwtN+AAAAZ0lEQVR42u3LIRJAUBRA0Ufwk6IY0eqMLBnBS/yi6Gb8XdiBPRBoZE1iDZpwTz+eiJRhNey2qNNZjUZnMMaLmzVR6W5TNfGaNe46Wp3kybfeivjyHYfD4XA4HA6Hw+FwOBwOh/On8wLTGBe8mbtkhgAAAABJRU5ErkJggg==', 
            'iVBORw0KGgoAAAANSUhEUgAAAYwAAABeAQMAAAAKdrGZAAAABlBMVEX///8AAABVwtN+AAAAaklEQVR42mNkYGBIyL8w5a9P7YJXKU8ZgkU2V81cNmWt5IIokaMMX40+N6zsivI+93bZRDMx13vzlRYwMDAxkAxGtYxqGdUyqmVUy6iWUS2jWka1jGoZ1TKqZVTLqJZRLaNaRrWMaiEVAAB3uBe8nSip8QAAAABJRU5ErkJggg==', 
            'iVBORw0KGgoAAAANSUhEUgAAATUAAABeAQMAAAB4lRFqAAAABlBMVEX///8AAABVwtN+AAAAVklEQVR42mNkYGBIyL8whdvO9d6UK0e/3puyeZrrvfkaYnOvlzGm6v4Sjsq/MPECAwMTA3FgVN2oulF1o+pG1Y2qG1U3qm5U3ai6UXWj6kbVjaqjhjoAdiwSvEkaxBcAAAAASUVORK5CYII=', 
            'iVBORw0KGgoAAAANSUhEUgAAARgAAAAkAQMAAABoj7etAAAABlBMVEX///8AAABVwtN+AAAAPElEQVR42mNkYGBIyL8wZcutGwyvUp4yBMtriM295XDlxCm29MRU31ufpRgYmBgIg1E1o2pG1YyqGepqAKFJD0hDGoJfAAAAAElFTkSuQmCC', 
            'iVBORw0KGgoAAAANSUhEUgAAAawAAABeAQMAAABFK7JJAAAABlBMVEX///8AAABVwtN+AAAAaUlEQVR42u3LoRVAUACG0Z/gKLKjOK+YhRlMIOko7xUDSBqSUQyhaFYgsYMkfLdfT1ITdUdcL+PtNpuEqYrJJjZ3g06XXZ7Rs1cKZil2TV+ubW4kX5/QaDQajUaj0Wg0Go1Go9FotH+3F1GxE7xDV+SvAAAAAElFTkSuQmCC'
        ], 
        'reference': {'type': 'St', 'value': 'reference'}, 
        'services': ['EXPRESS WORLDWIDE', 'DUTIES & TAXES PAID ', 'PAPERLESS TRADE ', 'C', 'DTP', 'PLT'], 
        'shipment_date': '2017-11-10', 
        'total_charge': {'amount': '155.160', 'currency': 'USD', 'name': 'Shipment charge'}, 
        'tracking_numbers': ['0044650491']
    }, 
    []
]


ShipmentParsingError = """<?xml version="1.0" encoding="UTF-8"?>
<res:ShipmentValidateErrorResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com ship-val-err-res.xsd'>
    <Response>
        <ServiceHeader>
            <MessageTime>2002-06-25T11:28:56-08:00</MessageTime>
            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>dollarog</SiteID>
            <Password>l7DIbG5N3r</Password>
        </ServiceHeader>
        <Status>
            <ActionStatus/>
            <Condition>
                <ConditionCode>PLT006</ConditionCode>
                <ConditionData>Paperless shipment service is not allowed
                    for one of these reasons: Shipper or receiver
                    country doesn&apos;t support Paperless Service, the
                    product selected doesn&apos;t support Paperless or
                    the declared value entered is greater than the
                    allowed limit. Please contact DHL representative for
                    further information or resubmit as regular shipment.</ConditionData>
            </Condition>
        </Status>
    </Response>
</res:ShipmentValidateErrorResponse>
<!-- ServiceInvocationId:20180902233912_96ab_be7f69b3-f590-42bd-938b-34fb338427ce -->
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

ShipmentRequestXml = f"""<req:ShipmentRequest xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com ship-val-global-req.xsd" schemaVersion="6.1">
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
        <Contents>...</Contents>
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
            <Image>dataimage/gifbase64R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADg==</Image>
            <ImageFormat>PDF</ImageFormat>
        </DocImage>
    </DocImages>
</req:ShipmentRequest>
"""

ShipmentResponseXml = """<?xml version="1.0" encoding="UTF-8"?>
<res:ShipmentResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com ship-val-res.xsd'>
    <Response>
        <ServiceHeader>
            <MessageTime>2017-11-08T07:33:26+01:00</MessageTime>
            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>CustomerSiteID</SiteID>
        </ServiceHeader>
    </Response>
    <RegionCode>AM</RegionCode>
    <Note>
        <ActionNote>Success</ActionNote>
    </Note>
    <AirwayBillNumber>0044650491</AirwayBillNumber>
    <BillingCode>DSA</BillingCode>
    <CurrencyCode>USD</CurrencyCode>
    <CourierMessage>Global AM Int PLT shpmt</CourierMessage>
    <DestinationServiceArea>
        <ServiceAreaCode>BRU</ServiceAreaCode>
        <FacilityCode>AND</FacilityCode>
        <InboundSortCode>.</InboundSortCode>
    </DestinationServiceArea>
    <OriginServiceArea>
        <ServiceAreaCode>PHX</ServiceAreaCode>
        <FacilityCode>PHX</FacilityCode>
        <OutboundSortCode>.</OutboundSortCode>
    </OriginServiceArea>
    <PackageCharge>124.690</PackageCharge>
    <Rated>Y</Rated>
    <ShippingCharge>155.160</ShippingCharge>
    <InsuredAmount>120.00</InsuredAmount>
    <WeightUnit>K</WeightUnit>
    <ChargeableWeight>10.0</ChargeableWeight>
    <DimensionalWeight>0.0</DimensionalWeight>
    <ReadyByTime>17:00</ReadyByTime>
    <PickupCharge>0.00</PickupCharge>
    <CallInTime>16:00</CallInTime>
    <DaysAdvanceNotice>0</DaysAdvanceNotice>
    <CountryCode>US</CountryCode>
    <Barcodes>
        <AWBBarCode>iVBORw0KGgoAAAANSUhEUgAAAYwAAABeAQMAAAAKdrGZAAAABlBMVEX///8AAABVwtN+AAAAaklEQVR42mNkYGBIyL8w5a9P7YJXKU8ZgkU2V81cNmWt5IIokaMMX40+N6zsivI+93bZRDMx13vzlRYwMDAxkAxGtYxqGdUyqmVUy6iWUS2jWka1jGoZ1TKqZVTLqJZRLaNaRrWMaiEVAAB3uBe8nSip8QAAAABJRU5ErkJggg==</AWBBarCode>
        <OriginDestnBarcode>iVBORw0KGgoAAAANSUhEUgAAATUAAABeAQMAAAB4lRFqAAAABlBMVEX///8AAABVwtN+AAAAVklEQVR42mNkYGBIyL8whdvO9d6UK0e/3puyeZrrvfkaYnOvlzGm6v4Sjsq/MPECAwMTA3FgVN2oulF1o+pG1Y2qG1U3qm5U3ai6UXWj6kbVjaqjhjoAdiwSvEkaxBcAAAAASUVORK5CYII=</OriginDestnBarcode>
        <ClientIDBarCode>iVBORw0KGgoAAAANSUhEUgAAARgAAAAkAQMAAABoj7etAAAABlBMVEX///8AAABVwtN+AAAAPElEQVR42mNkYGBIyL8wZcutGwyvUp4yBMtriM295XDlxCm29MRU31ufpRgYmBgIg1E1o2pG1YyqGepqAKFJD0hDGoJfAAAAAElFTkSuQmCC</ClientIDBarCode>
        <DHLRoutingBarCode>iVBORw0KGgoAAAANSUhEUgAAAawAAABeAQMAAABFK7JJAAAABlBMVEX///8AAABVwtN+AAAAaUlEQVR42u3LoRVAUACG0Z/gKLKjOK+YhRlMIOko7xUDSBqSUQyhaFYgsYMkfLdfT1ITdUdcL+PtNpuEqYrJJjZ3g06XXZ7Rs1cKZil2TV+ubW4kX5/QaDQajUaj0Wg0Go1Go9FotH+3F1GxE7xDV+SvAAAAAElFTkSuQmCC</DHLRoutingBarCode>
    </Barcodes>
    <Piece>1</Piece>
    <Contents>Global AM Int PLT shpmt</Contents>
    <Reference>
        <ReferenceID>reference</ReferenceID>
        <ReferenceType>St</ReferenceType>
    </Reference>
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
    <CustomerID>300902</CustomerID>
    <ShipmentDate>2017-11-10</ShipmentDate>
    <GlobalProductCode>P</GlobalProductCode>
    <SpecialService>
        <SpecialServiceType>DD</SpecialServiceType>
        <SpecialServiceDesc>DUTIES &amp; TAXES PAID </SpecialServiceDesc>
    </SpecialService>
    <SpecialService>
        <SpecialServiceType>WY</SpecialServiceType>
        <SpecialServiceDesc>PAPERLESS TRADE </SpecialServiceDesc>
    </SpecialService>
    <Billing>
        <ShipperAccountNumber>123456789</ShipperAccountNumber>
        <ShippingPaymentType>S</ShippingPaymentType>
        <BillingAccountNumber>123456789</BillingAccountNumber>
        <DutyPaymentType>S</DutyPaymentType>
        <DutyAccountNumber>123456789</DutyAccountNumber>
    </Billing>
    <Dutiable>
        <DeclaredValue>200.00</DeclaredValue>
        <DeclaredCurrency>USD</DeclaredCurrency>
        <ScheduleB>3002905110</ScheduleB>
        <ExportLicense>D123456</ExportLicense>
        <ShipperEIN>112233445566</ShipperEIN>
        <ShipperIDType>S</ShipperIDType>
        <ImportLicense>ImportLic</ImportLicense>
        <ConsigneeEIN>ConEIN2123</ConsigneeEIN>
        <TermsOfTrade>DAP</TermsOfTrade>
    </Dutiable>
    <NewShipper>Y</NewShipper>
    <DHLRoutingCode>BE1060+48000001</DHLRoutingCode>
    <DHLRoutingDataId>2L</DHLRoutingDataId>
    <ProductContentCode>WPX</ProductContentCode>
    <ProductShortName>EXPRESS WORLDWIDE</ProductShortName>
    <InternalServiceCode>C</InternalServiceCode>
    <InternalServiceCode>DTP</InternalServiceCode>
    <InternalServiceCode>PLT</InternalServiceCode>
    <DeliveryDateCode/>
    <DeliveryTimeCode/>
    <Pieces>
        <Piece>
            <PieceNumber>1</PieceNumber>
            <Depth>3.00</Depth>
            <Width>1.00</Width>
            <Height>2.00</Height>
            <Weight>1.00</Weight>
            <PackageType>EE</PackageType>
            <DimWeight>0.0</DimWeight>
            <DataIdentifier>J</DataIdentifier>
            <LicensePlate>JD013036538168309350</LicensePlate>
            <LicensePlateBarCode>iVBORw0KGgoAAAANSUhEUgAAAZYAAABeAQMAAAA6+qC4AAAABlBMVEX///8AAABVwtN+AAAAZ0lEQVR42u3LIRJAUBRA0Ufwk6IY0eqMLBnBS/yi6Gb8XdiBPRBoZE1iDZpwTz+eiJRhNey2qNNZjUZnMMaLmzVR6W5TNfGaNe46Wp3kybfeivjyHYfD4XA4HA6Hw+FwOBwOh/On8wLTGBe8mbtkhgAAAABJRU5ErkJggg==</LicensePlateBarCode>
        </Piece>
    </Pieces>
    <PLTStatus>A</PLTStatus>
    <QtdSInAdCur>
        <CurrencyCode>USD</CurrencyCode>
        <CurrencyRoleTypeCode>BILLC</CurrencyRoleTypeCode>
        <PackageCharge>124.690</PackageCharge>
        <ShippingCharge>155.160</ShippingCharge>
    </QtdSInAdCur>
    <QtdSInAdCur>
        <CurrencyCode>USD</CurrencyCode>
        <CurrencyRoleTypeCode>PULCL</CurrencyRoleTypeCode>
        <PackageCharge>124.690</PackageCharge>
        <ShippingCharge>155.160</ShippingCharge>
    </QtdSInAdCur>
    <QtdSInAdCur>
        <CurrencyCode>USD</CurrencyCode>
        <CurrencyRoleTypeCode>BASEC</CurrencyRoleTypeCode>
        <PackageCharge>124.690</PackageCharge>
        <ShippingCharge>155.160</ShippingCharge>
    </QtdSInAdCur>
</res:ShipmentResponse>
"""
