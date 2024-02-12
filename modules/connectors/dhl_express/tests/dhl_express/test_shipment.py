import re
import time
import unittest
from unittest.mock import patch, ANY
import karrio
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from .fixture import gateway


class TestDHLShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)
        self.NonPaperlessShipmentRequest = ShipmentRequest(
            **non_paperless_intl_shipment_data
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        # remove MessageTime, Date for testing purpose
        serialized_request = re.sub(
            "            <MessageTime>[^>]+</MessageTime>",
            "",
            request.serialize(),
        )

        self.assertEqual(serialized_request, ShipmentRequestXml)

    def test_create_non_paperless_shipment_request(self):
        request = gateway.mapper.create_shipment_request(
            self.NonPaperlessShipmentRequest
        )

        # remove MessageTime, Date for testing purpose
        serialized_request = re.sub(
            "            <MessageTime>[^>]+</MessageTime>",
            "",
            request.serialize(),
        )

        self.assertEqual(serialized_request, NonParelessShipmentRequestXml)

    @patch("karrio.mappers.dhl_express.proxy.lib.request", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}/XMLShippingServlet",
        )

    def test_parse_shipment_error(self):
        with patch("karrio.mappers.dhl_express.proxy.lib.request") as mock:
            mock.return_value = ShipmentParsingError
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedShipmentParsingError)
            )

    def test_shipment_missing_args_error_parsing(self):
        with patch("karrio.mappers.dhl_express.proxy.lib.request") as mock:
            mock.return_value = ShipmentMissingArgsError
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedShipmentMissingArgsError)
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.dhl_express.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponseXml
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_not_supported_cancel_shipment(self):
        cancel_request = ShipmentCancelRequest(shipment_identifier="IDENTIFIER")
        response = karrio.Shipment.cancel(cancel_request).from_(gateway).parse()

        self.assertListEqual(
            DP.to_dict(response), ParsedNotSupportedShipmentCancelResponse
        )


if __name__ == "__main__":
    unittest.main()


shipment_data = {
    "shipper": {
        "company_name": "shipper company privated limited 12",
        "address_line1": "238 850925434 Drive",
        "city": "Scottsdale",
        "postal_code": "85260",
        "country_code": "US",
        "person_name": "Ms Lucian",
        "phone_number": "1 23 8613402",
        "email": "test@email.com",
        "state_code": "AZ",
    },
    "recipient": {
        "company_name": "IBM Bruse Pte Ltd",
        "address_line1": "9 Business Park Central 13th Floor The IBM Place",
        "city": "Brussels",
        "postal_code": "1060",
        "country_code": "BE",
        "person_name": "Mrs Orlander",
        "phone_number": "506-851-2271",
        "email": "c_orlander@gc.ca",
    },
    "parcels": [
        {
            "id": "1",
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 4.0,
            "packaging_type": "dhl_parcel",
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "is_document": False,
        }
    ],
    "service": "dhl_express_worldwide_nondoc",
    "options": {"dhl_paperless_trade": True, "insurance": 148.0},
    "payment": {"paid_by": "sender", "account_number": "123456789"},
    "customs": {
        "incoterm": "DAP",
        "invoice": "N/A",
        "invoice_date": "2021-05-03",
        "commodities": [{"description": "cn", "weight": 4.0, "sku": "sku", "hs_code": "hs_code"}],
        "duty": {
            "account_number": "123456789",
            "paid_by": "sender",
            "declared_value": 200.0,
        },
    },
}

non_paperless_intl_shipment_data = {
    "customs": {
        "certify": True,
        "commercial_invoice": True,
        "commodities": [
            {
                "description": "description",
                "hs_code": "hs_code",
                "metadata": {},
                "quantity": 1,
                "sku": "sku",
                "title": "title",
                "value_amount": 928.1,
                "value_currency": "EUR",
                "weight": 0.847,
                "weight_unit": "KG",
            }
        ],
        "content_type": "merchandise",
        "duty": {"currency": "EUR", "declared_value": 928.1, "paid_by": "sender"},
        "incoterm": "DDP",
        "invoice": "36892319",
        "invoice_date": "2023-12-15",
        "options": {},
    },
    "options": {
        "currency": "EUR",
        "declared_value": 928.1,
        "paperless_trade": False,
        "shipment_date": "2023-12-15",
    },
    "parcels": [
        {
            "dimension_unit": "CM",
            "height": 5,
            "is_document": False,
            "items": [
                {
                    "description": "description",
                    "hs_code": "123456",
                    "metadata": {},
                    "quantity": 1,
                    "sku": "sku",
                    "title": "title",
                    "value_amount": 928.1,
                    "value_currency": "EUR",
                    "weight": 0.847,
                    "weight_unit": "KG",
                }
            ],
            "length": 30,
            "packaging_type": "small_box",
            "weight": 0.847,
            "weight_unit": "KG",
            "width": 22,
        }
    ],
    "recipient": {
        "address_line1": "Biryat Hadid 34",
        "city": "Istanbul",
        "country_code": "TR",
        "email": "store@customer.com",
        "person_name": "Store Customer",
        "postal_code": "34020",
    },
    "service": "dhl_express_easy_nondoc",
    "shipper": {
        "address_line1": "address_line_1",
        "city": "city",
        "country_code": "CZ",
        "person_name": "person_name",
    },
}


ParsedShipmentMissingArgsError = [
    None,
    [
        {
            "carrier_name": "dhl_express",
            "carrier_id": "carrier_id",
            "code": "152",
            "message": "Shipment Details segment Contents\n                    Conditional Required Error",
        }
    ],
]

ParsedShipmentParsingError = [
    None,
    [
        {
            "carrier_name": "dhl_express",
            "carrier_id": "carrier_id",
            "code": "PLT006",
            "message": "Paperless shipment service is not allowed\n                    for one of these reasons: Shipper or receiver\n                    country doesn't support Paperless Service, the\n                    product selected doesn't support Paperless or\n                    the declared value entered is greater than the\n                    allowed limit. Please contact DHL representative for\n                    further information or resubmit as regular shipment.",
        }
    ],
]

ParsedShipmentResponse = [
    {
        "carrier_id": "carrier_id",
        "carrier_name": "dhl_express",
        "shipment_identifier": "0057714403",
        "tracking_number": "0057714403",
        "docs": {"label": ANY, "invoice": ANY},
        "meta": {
            "carrier_tracking_link": "https://www.dhl.com/ca-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=0057714403"
        },
    },
    [],
]

ParsedNotSupportedShipmentCancelResponse = [
    None,
    [
        {
            "carrier_id": "carrier_id",
            "carrier_name": "dhl_express",
            "code": "SHIPPING_SDK_NON_SUPPORTED_ERROR",
            "message": "this operation is not supported.",
        }
    ],
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

ShipmentRequestXml = f"""<req:ShipmentRequest xsi:schemaLocation="http://www.dhl.com ship-val-global-req.xsd" xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" schemaVersion="10.0">
    <Request>
        <ServiceHeader>

            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>site_id</SiteID>
            <Password>password</Password>
        </ServiceHeader>
        <MetaData>
            <SoftwareName>3PV</SoftwareName>
            <SoftwareVersion>10.0</SoftwareVersion>
        </MetaData>
    </Request>
    <RegionCode>AM</RegionCode>
    <LanguageCode>en</LanguageCode>
    <Billing>
        <ShipperAccountNumber>123456789</ShipperAccountNumber>
        <ShippingPaymentType>S</ShippingPaymentType>
        <BillingAccountNumber>123456789</BillingAccountNumber>
        <DutyAccountNumber>123456789</DutyAccountNumber>
    </Billing>
    <Consignee>
        <CompanyName>IBM Bruse Pte Ltd</CompanyName>
        <AddressLine1>9 Business Park Central 13th Floor The IBM Place</AddressLine1>
        <City>Brussels</City>
        <PostalCode>1060</PostalCode>
        <CountryCode>BE</CountryCode>
        <CountryName>Belgium</CountryName>
        <Contact>
            <PersonName>Mrs Orlander</PersonName>
            <PhoneNumber>506-851-2271</PhoneNumber>
            <Email>c_orlander@gc.ca</Email>
        </Contact>
        <StreetName>Business Park Central 13th Floor The IBM Place</StreetName>
        <StreetNumber>9</StreetNumber>
    </Consignee>
    <Commodity>
        <CommodityCode>hs_code</CommodityCode>
        <CommodityName>cn</CommodityName>
    </Commodity>
    <Dutiable>
        <DeclaredValue>200</DeclaredValue>
        <DeclaredCurrency>USD</DeclaredCurrency>
        <TermsOfTrade>DAP</TermsOfTrade>
    </Dutiable>
    <UseDHLInvoice>Y</UseDHLInvoice>
    <DHLInvoiceType>PFI</DHLInvoiceType>
    <ExportDeclaration>
        <InvoiceNumber>N/A</InvoiceNumber>
        <InvoiceDate>2021-05-03</InvoiceDate>
        <ExportLineItem>
            <LineNumber>1</LineNumber>
            <Quantity>1</Quantity>
            <QuantityUnit>PCS</QuantityUnit>
            <Description>cn</Description>
            <Value>0</Value>
            <CommodityCode>hs_code</CommodityCode>
            <Weight>
                <Weight>4</Weight>
                <WeightUnit>K</WeightUnit>
            </Weight>
            <GrossWeight>
                <Weight>4</Weight>
                <WeightUnit>K</WeightUnit>
            </GrossWeight>
            <ManufactureCountryCode>US</ManufactureCountryCode>
            <ManufactureCountryName>United States</ManufactureCountryName>
            <ImportCommodityCode>hs_code</ImportCommodityCode>
        </ExportLineItem>
        <PlaceOfIncoterm>N/A</PlaceOfIncoterm>
        <ShipmentPurpose>PERSONAL</ShipmentPurpose>
    </ExportDeclaration>
    <ShipmentDetails>
        <Pieces>
            <Piece>
                <PieceID>1</PieceID>
                <PackageType>PA</PackageType>
                <Weight>4</Weight>
                <Width>3</Width>
                <Height>3</Height>
                <Depth>10</Depth>
                <PieceReference>
                    <ReferenceID>1</ReferenceID>
                </PieceReference>
            </Piece>
        </Pieces>
        <WeightUnit>K</WeightUnit>
        <GlobalProductCode>P</GlobalProductCode>
        <LocalProductCode>P</LocalProductCode>
        <Date>{time.strftime('%Y-%m-%d')}</Date>
        <Contents>N/A</Contents>
        <DimensionUnit>C</DimensionUnit>
        <PackageType>PA</PackageType>
        <IsDutiable>Y</IsDutiable>
        <CurrencyCode>USD</CurrencyCode>
    </ShipmentDetails>
    <Shipper>
        <ShipperID>123456789</ShipperID>
        <CompanyName>shipper company privated limited 12</CompanyName>
        <RegisteredAccount>123456789</RegisteredAccount>
        <AddressLine1>238 850925434 Drive</AddressLine1>
        <City>Scottsdale</City>
        <DivisionCode>AZ</DivisionCode>
        <PostalCode>85260</PostalCode>
        <CountryCode>US</CountryCode>
        <CountryName>United States</CountryName>
        <Contact>
            <PersonName>Ms Lucian</PersonName>
            <PhoneNumber>1 23 8613402</PhoneNumber>
            <Email>test@email.com</Email>
        </Contact>
        <StreetName>850925434 Drive</StreetName>
        <StreetNumber>238</StreetNumber>
    </Shipper>
    <SpecialService>
        <SpecialServiceType>WY</SpecialServiceType>
    </SpecialService>
    <SpecialService>
        <SpecialServiceType>II</SpecialServiceType>
        <ChargeValue>148</ChargeValue>
        <CurrencyCode>USD</CurrencyCode>
    </SpecialService>
    <Notification>
        <EmailAddress>c_orlander@gc.ca</EmailAddress>
    </Notification>
    <LabelImageFormat>PDF</LabelImageFormat>
    <Label>
        <LabelTemplate>6X4_PDF</LabelTemplate>
    </Label>
</req:ShipmentRequest>
"""

NonParelessShipmentRequestXml = """<req:ShipmentRequest xsi:schemaLocation="http://www.dhl.com ship-val-global-req.xsd" xmlns:req="http://www.dhl.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" schemaVersion="10.0">
    <Request>
        <ServiceHeader>

            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID>site_id</SiteID>
            <Password>password</Password>
        </ServiceHeader>
        <MetaData>
            <SoftwareName>3PV</SoftwareName>
            <SoftwareVersion>10.0</SoftwareVersion>
        </MetaData>
    </Request>
    <RegionCode>EU</RegionCode>
    <LanguageCode>en</LanguageCode>
    <Billing>
        <ShipperAccountNumber>123456789</ShipperAccountNumber>
        <ShippingPaymentType>S</ShippingPaymentType>
        <BillingAccountNumber>123456789</BillingAccountNumber>
    </Billing>
    <Consignee>
        <CompanyName>N/A</CompanyName>
        <AddressLine1>34 Biryat Hadid</AddressLine1>
        <City>Istanbul</City>
        <PostalCode>34020</PostalCode>
        <CountryCode>TR</CountryCode>
        <CountryName>Turkey</CountryName>
        <Contact>
            <PersonName>Store Customer</PersonName>
            <PhoneNumber>0000</PhoneNumber>
            <Email>store@customer.com</Email>
        </Contact>
        <StreetName>Biryat Hadid</StreetName>
        <StreetNumber>34</StreetNumber>
    </Consignee>
    <Commodity>
        <CommodityCode>hs_code</CommodityCode>
        <CommodityName>title</CommodityName>
    </Commodity>
    <Dutiable>
        <DeclaredValue>928.1</DeclaredValue>
        <DeclaredCurrency>EUR</DeclaredCurrency>
        <TermsOfTrade>DDP</TermsOfTrade>
    </Dutiable>
    <UseDHLInvoice>Y</UseDHLInvoice>
    <ExportDeclaration>
        <ExportReason>merchandise</ExportReason>
        <ExportReasonCode>C</ExportReasonCode>
        <InvoiceNumber>36892319</InvoiceNumber>
        <InvoiceDate>2023-12-15</InvoiceDate>
        <ExportLineItem>
            <LineNumber>1</LineNumber>
            <Quantity>1</Quantity>
            <QuantityUnit>PCS</QuantityUnit>
            <Description>title</Description>
            <Value>928.1</Value>
            <CommodityCode>hs_code</CommodityCode>
            <Weight>
                <Weight>0.85</Weight>
                <WeightUnit>K</WeightUnit>
            </Weight>
            <GrossWeight>
                <Weight>0.85</Weight>
                <WeightUnit>K</WeightUnit>
            </GrossWeight>
            <ManufactureCountryCode>CZ</ManufactureCountryCode>
            <ManufactureCountryName>Czech Republic</ManufactureCountryName>
            <ImportCommodityCode>hs_code</ImportCommodityCode>
        </ExportLineItem>
        <PlaceOfIncoterm>N/A</PlaceOfIncoterm>
        <ShipmentPurpose>COMMERCIAL</ShipmentPurpose>
    </ExportDeclaration>
    <ShipmentDetails>
        <Pieces>
            <Piece>
                <PieceID>1</PieceID>
                <PackageType>JJ</PackageType>
                <Weight>0.85</Weight>
                <Width>22</Width>
                <Height>5</Height>
                <Depth>30</Depth>
            </Piece>
        </Pieces>
        <WeightUnit>K</WeightUnit>
        <GlobalProductCode>8</GlobalProductCode>
        <LocalProductCode>8</LocalProductCode>
        <Date>2023-12-15</Date>
        <Contents>N/A</Contents>
        <DimensionUnit>C</DimensionUnit>
        <PackageType>JJ</PackageType>
        <IsDutiable>Y</IsDutiable>
        <CurrencyCode>EUR</CurrencyCode>
    </ShipmentDetails>
    <Shipper>
        <ShipperID>123456789</ShipperID>
        <CompanyName>N/A</CompanyName>
        <RegisteredAccount>123456789</RegisteredAccount>
        <AddressLine1>address_line_1</AddressLine1>
        <City>city</City>
        <CountryCode>CZ</CountryCode>
        <CountryName>Czech Republic</CountryName>
        <Contact>
            <PersonName>person_name</PersonName>
            <PhoneNumber>0000</PhoneNumber>
        </Contact>
        <StreetNumber>address_line_1</StreetNumber>
    </Shipper>
    <Notification>
        <EmailAddress>store@customer.com</EmailAddress>
    </Notification>
    <LabelImageFormat>PDF</LabelImageFormat>
    <Label>
        <LabelTemplate>6X4_PDF</LabelTemplate>
    </Label>
</req:ShipmentRequest>
"""

ShipmentResponseXml = """<?xml version="1.0" encoding="UTF-8"?><res:ShipmentResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com ship-val-res.xsd'>
    <Response>
        <ServiceHeader>
            <MessageTime>2018-02-27T08:08:49+01:00</MessageTime>
            <MessageReference>Shipmnt_AM_US_lblimg_62_sch_PLT</MessageReference>
            <SiteID>CustomerSiteID</SiteID>
        </ServiceHeader>
    </Response>
    <RegionCode>AM</RegionCode>
    <Note>
        <ActionNote>Success</ActionNote>
    </Note>
    <AirwayBillNumber>0057714403</AirwayBillNumber>
    <DHLInvoiceLanguageCode>en</DHLInvoiceLanguageCode>
    <DHLInvoiceType>CMI</DHLInvoiceType>
    <BillingCode>DSA</BillingCode>
    <CurrencyCode>GBP</CurrencyCode>
    <CourierMessage>For testing only. Please do not ship</CourierMessage>
    <DestinationServiceArea>
        <ServiceAreaCode>BRU</ServiceAreaCode>
        <FacilityCode>AND</FacilityCode>
        <InboundSortCode>.</InboundSortCode>
    </DestinationServiceArea>
    <OriginServiceArea>
        <ServiceAreaCode>NWK</ServiceAreaCode>
        <FacilityCode>NWK</FacilityCode>
        <OutboundSortCode>CVG</OutboundSortCode>
    </OriginServiceArea>
    <PackageCharge>144.980</PackageCharge>
    <Rated>Y</Rated>
    <ShippingCharge>151.140</ShippingCharge>
    <WeightUnit>K</WeightUnit>
    <ChargeableWeight>20</ChargeableWeight>
    <DimensionalWeight>0.0</DimensionalWeight>
    <CountryCode>US</CountryCode>
    <Barcodes>
        <AWBBarCode>iVBORw0KGgoAAAANSUhEUgAAAYwAAABeAQMAAAAKdrGZAAAABlBMVEX///8AAABVwtN+AAAAaElEQVR42mNkYGBIyL8w5a9P7YJXKU91u5IbfgG5l8tqfwknpn418tZY2RVl61O7bP65A1/vzVdawMDAxEAyGNUyqmVUy6iWUS2jWka1jGoZ1TKqZVTLqJZRLaNaRrWMahnVMqqFVAAAs94ZvNoc2F4AAAAASUVORK5CYII=</AWBBarCode>
        <OriginDestnBarcode>iVBORw0KGgoAAAANSUhEUgAAATUAAABeAQMAAAB4lRFqAAAABlBMVEX///8AAABVwtN+AAAAVklEQVR42mNkYGBIyL8whWGz5oSMowy6C14lT3O9N19DbO71MsZU3V/CUfkXJl5gYGBiIA6MqhtVN6puVN2oulF1o+pG1Y2qG1U3qm5U3ai6UXXUUAcAMkEQvBnQSdMAAAAASUVORK5CYII=</OriginDestnBarcode>
        <ClientIDBarCode>iVBORw0KGgoAAAANSUhEUgAAARgAAAAkAQMAAABoj7etAAAABlBMVEX///8AAABVwtN+AAAAPElEQVR42mNkYGBIyL8wZcutGwyvUp4yBMtriM295XDlxCm29MRU31ufpRgYmBgIg1E1o2pG1YyqGepqAKFJD0hDGoJfAAAAAElFTkSuQmCC</ClientIDBarCode>
        <DHLRoutingBarCode>iVBORw0KGgoAAAANSUhEUgAAAawAAABeAQMAAABFK7JJAAAABlBMVEX///8AAABVwtN+AAAAaUlEQVR42u3LoRVAUACG0Z/gKLKjOK+YhRlMIOko7xUDSBqSUQyhaFYgsYMkfLdfT1ITdUdcL+PtNpuEqYrJJjZ3g06XXZ7Rs1cKZil2TV+ubW4kX5/QaDQajUaj0Wg0Go1Go9FotH+3F1GxE7xDV+SvAAAAAElFTkSuQmCC</DHLRoutingBarCode>
    </Barcodes>
    <Piece>1</Piece>
    <Contents>For testing only. Please do not ship</Contents>
    <Reference>
        <ReferenceID>ReferenceID</ReferenceID>
    </Reference>
    <Consignee>
        <CompanyName>IBM Bruse Private Limited Company Name</CompanyName>
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
        <CompanyName>IBM Corporation</CompanyName>
        <RegisteredAccount>123456789</RegisteredAccount>
        <AddressLine>1 New Orchard Road</AddressLine>
        <AddressLine>Armonk</AddressLine>
        <City>New York</City>
        <Division>New York</Division>
        <DivisionCode>NY</DivisionCode>
        <PostalCode>10504</PostalCode>
        <CountryCode>US</CountryCode>
        <CountryName>United States Of America</CountryName>
        <Contact>
            <PersonName>Mr peter</PersonName>
            <PhoneNumber>1 905 8613402</PhoneNumber>
            <PhoneExtension>3403</PhoneExtension>
            <FaxNumber>1 905 8613411</FaxNumber>
            <Telex>1245</Telex>
            <Email>test@email.com</Email>
        </Contact>
    </Shipper>
    <CustomerID>300902</CustomerID>
    <ShipmentDate>2018-03-06</ShipmentDate>
    <GlobalProductCode>P</GlobalProductCode>
    <SpecialService>
        <SpecialServiceType>WY</SpecialServiceType>
        <SpecialServiceDesc>PAPERLESS TRADE </SpecialServiceDesc>
    </SpecialService>
    <Billing>
        <ShipperAccountNumber>123456789</ShipperAccountNumber>
        <ShippingPaymentType>S</ShippingPaymentType>
        <BillingAccountNumber>123456789</BillingAccountNumber>
        <DutyPaymentType>R</DutyPaymentType>
    </Billing>
    <Dutiable>
        <DeclaredValue>100.00</DeclaredValue>
        <DeclaredCurrency>USD</DeclaredCurrency>
        <ScheduleB>3002905110</ScheduleB>
        <ExportLicense>D123456</ExportLicense>
        <ShipperEIN>112233445566</ShipperEIN>
        <ShipperIDType>S</ShipperIDType>
        <ImportLicense>ImportLic</ImportLicense>
        <ConsigneeEIN>ConEIN2123</ConsigneeEIN>
        <TermsOfTrade>DAP</TermsOfTrade>
    </Dutiable>
    <ExportDeclaration>
        <SignatureName>SignatureName</SignatureName>
        <SignatureTitle>SignatureTitle</SignatureTitle>
        <ExportReason>ExportReason</ExportReason>
        <ExportReasonCode>P</ExportReasonCode>
        <InvoiceNumber>12345</InvoiceNumber>
        <InvoiceDate>2017-08-09</InvoiceDate>
        <BillToCompanyName>BillToCompanyName</BillToCompanyName>
        <BillToContanctName>BillToContanctName</BillToContanctName>
        <BillToAddressLine>BillToAddressLine</BillToAddressLine>
        <BillToCity>BillToCity</BillToCity>
        <BillToPostcode>BillToPostcode</BillToPostcode>
        <BillToSuburb>BillToSuburb</BillToSuburb>
        <BillToState>BillToState</BillToState>
        <BillToCountryName>BillToCountryName</BillToCountryName>
        <BillToPhoneNumber>BillToPhoneNumber</BillToPhoneNumber>
        <BillToPhoneNumberExtn>BillToPhoneNumberExtn</BillToPhoneNumberExtn>
        <BillToFaxNumber>BillToFaxNumber</BillToFaxNumber>
        <BillToFederalTaxID>12345</BillToFederalTaxID>
        <Remarks>Successfully processed</Remarks>
        <OtherCharges1>13.0</OtherCharges1>
        <OtherCharges2>13.0</OtherCharges2>
        <OtherCharges3>14.0</OtherCharges3>
        <DestinationPort>4444</DestinationPort>
        <TermsOfPayment>credit card</TermsOfPayment>
        <PayerGSTVAT>yes</PayerGSTVAT>
        <ReceiverReference>ReceiverReference</ReceiverReference>
        <ExporterCode>ExporterCode</ExporterCode>
        <RUBankINN>RUBankINN</RUBankINN>
        <RUBankKPP>RUBankKPP</RUBankKPP>
        <RUBankOKPO>RUBankOKPO</RUBankOKPO>
        <RUBankOGRN>RUBankOKPO</RUBankOGRN>
        <RUBankSettlementAcctNumUSDEUR>RUBankSettl</RUBankSettlementAcctNumUSDEUR>
        <RUBankSettlementAcctNumRUR>RUBankSettl</RUBankSettlementAcctNumRUR>
        <RUBankName>RUBankName</RUBankName>
        <ExportLineItem>
            <LineNumber>1</LineNumber>
            <Quantity>4</Quantity>
            <QuantityUnit>PCS</QuantityUnit>
            <Description>ExportLineItem Goods Description-1</Description>
            <Value>5.0</Value>
            <IsDomestic>Y</IsDomestic>
            <CommodityCode>4455</CommodityCode>
            <ScheduleB>ScheduleB</ScheduleB>
            <ECCN>0</ECCN>
            <Weight>
                <Weight>20.0</Weight>
                <WeightUnit>K</WeightUnit>
            </Weight>
            <GrossWeight>
                <Weight>400.0</Weight>
                <WeightUnit>K</WeightUnit>
            </GrossWeight>
            <License>
                <LicenseNumber>123</LicenseNumber>
                <ExpiryDate>2017-12-10</ExpiryDate>
            </License>
            <LicenseSymbol>LICENSE</LicenseSymbol>
            <ManufactureCountryCode>RU</ManufactureCountryCode>
        </ExportLineItem>
        <ExportLineItem>
            <LineNumber>2</LineNumber>
            <Quantity>5</Quantity>
            <QuantityUnit>PCS</QuantityUnit>
            <Description>ExportLineItem Goods Description-2</Description>
            <Value>4.0</Value>
            <IsDomestic>Y</IsDomestic>
            <CommodityCode>2233</CommodityCode>
            <ScheduleB>ScheduleB</ScheduleB>
            <ECCN>0</ECCN>
            <Weight>
                <Weight>20.0</Weight>
                <WeightUnit>K</WeightUnit>
            </Weight>
            <GrossWeight>
                <Weight>400.0</Weight>
                <WeightUnit>K</WeightUnit>
            </GrossWeight>
            <License>
                <LicenseNumber>123</LicenseNumber>
                <ExpiryDate>2017-12-10</ExpiryDate>
            </License>
            <LicenseSymbol>LICENSE</LicenseSymbol>
            <ManufactureCountryCode>RU</ManufactureCountryCode>
        </ExportLineItem>
        <ExportLineItem>
            <LineNumber>3</LineNumber>
            <Quantity>5</Quantity>
            <QuantityUnit>PCS</QuantityUnit>
            <Description>ExportLineItem Goods Description-3</Description>
            <Value>4.0</Value>
            <IsDomestic>Y</IsDomestic>
            <CommodityCode>4455</CommodityCode>
            <ScheduleB>ScheduleB</ScheduleB>
            <ECCN>0</ECCN>
            <Weight>
                <Weight>20.0</Weight>
                <WeightUnit>K</WeightUnit>
            </Weight>
            <GrossWeight>
                <Weight>400.0</Weight>
                <WeightUnit>K</WeightUnit>
            </GrossWeight>
            <License>
                <LicenseNumber>123</LicenseNumber>
                <ExpiryDate>2017-12-10</ExpiryDate>
            </License>
            <LicenseSymbol>LICENSE</LicenseSymbol>
            <ManufactureCountryCode>RU</ManufactureCountryCode>
        </ExportLineItem>
        <ExportLineItem>
            <LineNumber>4</LineNumber>
            <Quantity>5</Quantity>
            <QuantityUnit>PCS</QuantityUnit>
            <Description>ExportLineItem Goods Description-4</Description>
            <Value>4.0</Value>
            <IsDomestic>Y</IsDomestic>
            <CommodityCode>2233</CommodityCode>
            <ScheduleB>ScheduleB</ScheduleB>
            <ECCN>0</ECCN>
            <Weight>
                <Weight>20.0</Weight>
                <WeightUnit>K</WeightUnit>
            </Weight>
            <GrossWeight>
                <Weight>400.0</Weight>
                <WeightUnit>K</WeightUnit>
            </GrossWeight>
            <License>
                <LicenseNumber>123</LicenseNumber>
                <ExpiryDate>2017-12-10</ExpiryDate>
            </License>
            <LicenseSymbol>LICENSE</LicenseSymbol>
            <ManufactureCountryCode>RU</ManufactureCountryCode>
        </ExportLineItem>
        <ExportLineItem>
            <LineNumber>5</LineNumber>
            <Quantity>5</Quantity>
            <QuantityUnit>PCS</QuantityUnit>
            <Description>ExportLineItem Goods Description-5</Description>
            <Value>4.0</Value>
            <IsDomestic>Y</IsDomestic>
            <CommodityCode>2233</CommodityCode>
            <ScheduleB>ScheduleB</ScheduleB>
            <ECCN>0</ECCN>
            <Weight>
                <Weight>20.0</Weight>
                <WeightUnit>K</WeightUnit>
            </Weight>
            <GrossWeight>
                <Weight>400.0</Weight>
                <WeightUnit>K</WeightUnit>
            </GrossWeight>
            <License>
                <LicenseNumber>123</LicenseNumber>
                <ExpiryDate>2017-12-10</ExpiryDate>
            </License>
            <LicenseSymbol>LICENSE</LicenseSymbol>
            <ManufactureCountryCode>RU</ManufactureCountryCode>
        </ExportLineItem>
    </ExportDeclaration>
    <NewShipper>Y</NewShipper>
    <DHLRoutingCode>BE1060+48000001</DHLRoutingCode>
    <DHLRoutingDataId>2L</DHLRoutingDataId>
    <ProductContentCode>WPX</ProductContentCode>
    <ProductShortName>EXPRESS WORLDWIDE</ProductShortName>
    <InternalServiceCode>C</InternalServiceCode>
    <InternalServiceCode>PLT</InternalServiceCode>
    <DeliveryDateCode/>
    <DeliveryTimeCode/>
    <Pieces>
        <Piece>
            <PieceNumber>1</PieceNumber>
            <Depth>2.00</Depth>
            <Width>2.00</Width>
            <Height>2.00</Height>
            <Weight>2.00</Weight>
            <PackageType>EE</PackageType>
            <DimWeight>0.0</DimWeight>
            <DataIdentifier>J</DataIdentifier>
            <LicensePlate>JD013036538172296379</LicensePlate>
            <LicensePlateBarCode>iVBORw0KGgoAAAANSUhEUgAAAZYAAABeAQMAAAA6+qC4AAAABlBMVEX///8AAABVwtN+AAAAaElEQVR42u3LIRJAUBRA0fcFkqIgGbsjS8YYL/6iSArDLuzAHhRmFFuQWIMm3NOPEZHSr4bDFk26qqfB5U7hNq8aq7S315/j9RzLqXUWmSTfOyviyHccDofD4XA4HA6Hw+FwOBzOn84L4/kXvJ1yubEAAAAASUVORK5CYII=</LicensePlateBarCode>
        </Piece>
    </Pieces>
    <PLTStatus>A</PLTStatus>
    <QtdSInAdCur>
        <CurrencyCode>USD</CurrencyCode>
        <CurrencyRoleTypeCode>BILLC</CurrencyRoleTypeCode>
        <PackageCharge>144.980</PackageCharge>
        <ShippingCharge>151.140</ShippingCharge>
    </QtdSInAdCur>
    <QtdSInAdCur>
        <CurrencyCode>USD</CurrencyCode>
        <CurrencyRoleTypeCode>PULCL</CurrencyRoleTypeCode>
        <PackageCharge>144.980</PackageCharge>
        <ShippingCharge>151.140</ShippingCharge>
    </QtdSInAdCur>
    <QtdSInAdCur>
        <CurrencyCode>EUR</CurrencyCode>
        <CurrencyRoleTypeCode>BASEC</CurrencyRoleTypeCode>
        <PackageCharge>122.390</PackageCharge>
        <ShippingCharge>127.590</ShippingCharge>
    </QtdSInAdCur>
    <LabelImage>
        <OutputFormat>PDF</OutputFormat>
        <OutputImage>JVBERi0xLjQKJfbk/N8KMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovVmVyc2lvbiAvMS40Ci9QYWdlcyAyIDAgUgo+PgplbmRvYmoKMyAwIG9iago8PAovUHJvZHVjZXIgKGlUZXh0IDIuMS43IGJ5IDFUM1hUKQovTW9kRGF0ZSAoRDoyMDE4MDIyNzA4MDg0OSswMScwMCcpCi9DcmVhdGlvbkRhdGUgKEQ6MjAxODAyMjcwODA4NDkrMDEnMDAnKQo+PgplbmRvYmoKMiAwIG9iago8PAovVHlwZSAvUGFnZXMKL0tpZHMgWzQgMCBSIDUgMCBSXQovQ291bnQgMgo+PgplbmRvYmoKNCAwIG9iago8PAovUGFyZW50IDIgMCBSCi9Db250ZW50cyA2IDAgUgovVHlwZSAvUGFnZQovUmVzb3VyY2VzIDcgMCBSCi9NZWRpYUJveCBbMC4wIDAuMCA4NDEuODkgNTk1LjI4XQovQ3JvcEJveCBbMC4wIDAuMCA4NDEuODkgNTk1LjI4XQovUm90YXRlIDAKPj4KZW5kb2JqCjUgMCBvYmoKPDwKL1BhcmVudCAyIDAgUgovQ29udGVudHMgOCAwIFIKL1R5cGUgL1BhZ2UKL1Jlc291cmNlcyA5IDAgUgovTWVkaWFCb3ggWzAuMCAwLjAgODQxLjg5IDU5NS4yOF0KL0Nyb3BCb3ggWzAuMCAwLjAgODQxLjg5IDU5NS4yOF0KL1JvdGF0ZSAwCj4+CmVuZG9iago2IDAgb2JqCjw8Ci9MZW5ndGggNTEKL0ZpbHRlciAvRmxhdGVEZWNvZGUKPj4Kc3RyZWFtDQp4nCvkcgrhMlAwtTTVM7JQCEnhcg3hCuQqVDBUMABCCJmcq6AfkWao4JKvEMgFAP2hClYNCmVuZHN0cmVhbQplbmRvYmoKNyAwIG9iago8PAovWE9iamVjdCA8PAovWGYxIDEwIDAgUgo+PgovUHJvY1NldCBbL1BERiAvVGV4dCAvSW1hZ2VCIC9JbWFnZUMgL0ltYWdlSV0KPj4KZW5kb2JqCjggMCBvYmoKPDwKL0xlbmd0aCA1MQovRmlsdGVyIC9GbGF0ZURlY29kZQo+PgpzdHJlYW0NCnicK+RyCuEyUDC1NNUzslAISeFyDeEK5CpUMFQwAEIImZyroB+RZqjgkq8Q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74WUwoWAXyykecYrIv7HHFQlq+3XXSON0ttX+3a12ft0+DUQ/lcEdnj18OVLyduuF5t2vZmvbkW3Wux/brP7cPjNvjznKO9VfhP80oizRTtdt+K6E6vuBaODPJTi8EXSxvw+vxHru/n904cP5ROOavvwUfQ/PGTml13lzfa7J+Sd8t3z/XzWrvCr2YI+03Y34p5ewsR8Rf3ja92zH4/x0laWxcSQ8oPO9ycSrvXGOxPhgqKTN+E5D9xY5EByhmRlyg6wMbjsuANxP71twQiGq8QBp/0If/4PWx5djw0KZW5kc3RyZWFtCmVuZG9iagoxMiAwIG9iago8PAovTGVuZ3RoIDcxNTUKL1R5cGUgL1hPYmplY3QKL1N1YnR5cGUgL0ltYWdlCi9Db2xvclNwYWNlIFsvSW5kZXhlZCAvRGV2aWNlUkdCIDI1NSA8RDJFNTlDQkNENzZCRTlGMkNFRkFGQ0YzQUJDRDQ1QzdERTg0RERFQkI1RjRGOUU3QjZENDVFQjBEMTUyRUVGNURCRDhFOEE5Q0RFMTkwRTNFRkMyQzFEQjc3QkJENzZBQUFDRDQ1RThGMUNERjlGQkYyQzZERDgzQjVEMzVFRjNGOEU2RUVGNUQ5RDJFNDlDRERFQkI0QzFEQTc2RDdFN0E4QjBEMDUxQ0NFMThGRTJFRUMxQTVDQTM5RkZGRkZGMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAw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q3/orhbLw28n393sXfKHKtar1X7xYr9ajbjIbrW6fX0Ri9VK+gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQ2v8B4fNgUg0KZW5kc3RyZWFtCmVuZG9iagoxMyAwIG9iago8PAovRjEgMTYgMCBSCi9GMiAxNyAwIFIKPj4KZW5kb2JqCjE0IDAgb2JqCjw8Ci9MZW5ndGggNzE1NQovVHlwZSAvWE9iamVjdAovU3VidHlwZSAvSW1hZ2UKL0NvbG9yU3BhY2UgWy9JbmRleGVkIC9EZXZpY2VSR0IgMjU1IDxEMkU1OUNCQ0Q3NkJFOUYyQ0VGQUZDRjNBQkNENDVDN0RFODREREVCQjVGNEY5RTdCNkQ0NUVCMEQxNTJFRUY1REJEOEU4QTlDREUxOTBFM0VGQzJDMURCNzdCQkQ3NkFBQUNENDVFOEYxQ0RGOUZCRjJDNkREODNCNUQzNUVGM0Y4RTZFRUY1RDlEMkU0OUNEREVCQjRDMURBNzZEN0U3QThCMEQwNTFDQ0UxOEZFMkVFQzFBNUNBMzlGRkZGRkYwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA+XQov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</OutputImage>
        <MultiLabels>
            <MultiLabel>
                <DocName>CustomInvoiceImage</DocName>
                <DocFormat>PDF</DocFormat>
                <DocImageVal>JVBERi0xLjQKJfbk/N8KMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovVmVyc2lvbiAvMS40Ci9QYWdlcyAyIDAgUgo+PgplbmRvYmoKMyAwIG9iago8PAovUHJvZHVjZXIgKGlUZXh0IDIuMS43IGJ5IDFUM1hUKQovTW9kRGF0ZSAoRDoyMDE4MDIyNzA4MDg0OSswMScwMCcpCi9DcmVhdGlvbkRhdGUgKEQ6MjAxODAyMjcwODA4NDkrMDEnMDAnKQo+PgplbmRvYmoKMiAwIG9iago8PAovVHlwZSAvUGFnZXMKL0tpZHMgWzQgMCBSXQovQ291bnQgMQo+PgplbmRvYmoKNCAwIG9iago8PAovUGFyZW50IDIgMCBSCi9Db250ZW50cyA1IDAgUgovVHlwZSAvUGFnZQovUmVzb3VyY2VzIDYgMCBSCi9NZWRpYUJveCBbMC4wIDAuMCA1MzguNTggNzc5LjUzXQovQ3JvcEJveCBbMC4wIDAuMCA1MzguNTggNzc5LjUzXQovUm90YXRlIDAKPj4KZW5kb2JqCjUgMCBvYmoKPDwKL0xlbmd0aCA1MQovRmlsdGVyIC9GbGF0ZURlY29kZQo+PgpzdHJlYW0NCnicK+RyCuEyUDA3t9QzNVYISeFyDeEK5CpUMFQwAEIImZyroB+RZqjgkq8QyAUA/fwKWA0KZW5kc3RyZWFtCmVuZG9iago2IDAgb2JqCjw8Ci9YT2JqZWN0IDw8Ci9YZjEgNyAwIFIKPj4KL1Byb2NTZXQgWy9QREYgL1RleHQgL0ltYWdlQiAvSW1hZ2VDIC9JbWFnZUldCj4+CmVuZG9iago3IDAgb2JqCjw8Ci9MZW5ndGggMzI5OQovVHlwZSAvWE9iamVjdAovUmVzb3VyY2VzIDw8Ci9YT2JqZWN0IDw8Ci9pbWcwIDggMCBSCj4+Ci9Qcm9jU2V0IFsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXQovRm9udCA5IDAgUgo+PgovU3VidHlwZSAvRm9ybQovQkJveCBbMCAwIDUzOC41OCA3NzkuNTNdCi9NYXRyaXggWzEgMCAwIDEgMCAwXQovRm9ybVR5cGUgMQovRmlsdGVyIC9GbGF0ZURlY29kZQo+PgpzdHJlYW0NCnicpVtdc9s2Fn3Xr8Bj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MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAw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83QTVd7NgBfxGPUiNq7+wxXCjr0H3XffBb0Ii3/gKkEHAH1v/r8Jug/p4x+uE3QAMHDZXcwBgI9/uFLIAcCQs/9XId9E8vEP11oHfAlgM/i2e8QtABf/4WoBV9+Hr7rbDt8LDbsEATM1+LM3orzBlwCHH4PAHK0HXn2LOe8eeh3iMeJFwPwMfARXzFfu18O+i/AQ8iJghgYdfEdddht0CcDJP/Q24HtAQ2/9/XDffwdw59Yf9Nf77Dsu/wE7APnDID2fwheZf+8dgPxhoF7XAKJX3PbaAcgfBnu8ur1N/Iq77fV3AWIPQWCm7q9s767nA//PWl95JaLAPgjm6aqLAA+FDruvOg4psg+CeVpdfAiwK/dDG5cfAmx84xci3V706Vs4vNVlvwl2Y8k/xFovvtwDbBbFr7hfsAdQP5Rwe/Ys4K7OFbfV2bOA3UL9UMh2f2IXcPdQr7v17YlvJm9ufNkPilo/Phwdgy8fbqt/6K4Wy8NvJ9/d7F3yhyrWq9V+8WK/Wo24yG61un19EYvVSvoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkNr/AeHzYFINCmVuZHN0cmVhbQplbmRvYmoKOSAwIG9iago8PAovRjEgMTAgMCBSCi9GMiAxMSAwIFIKPj4KZW5kb2JqCjEwIDAgb2JqCjw8Ci9CYXNlRm9udCAvSGVsdmV0aWNhLUJvbGQKL1R5cGUgL0ZvbnQKL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcKL1N1YnR5cGUgL1R5cGUxCj4+CmVuZG9iagoxMSAwIG9iago8PAovQmFzZUZvbnQgL0hlbHZldGljYQovVHlwZSAvRm9udAovRW5jb2RpbmcgL1dpbkFuc2lFbmNvZGluZwovU3VidHlwZSAvVHlwZTEKPj4KZW5kb2JqCnhyZWYKMCAxMgowMDAwMDAwMDAwIDY1NTM1IGYNCjAwMDAwMDAwMTUgMDAwMDAgbg0KMDAwMDAwMDIwNyAwMDAwMCBuDQowMDAwMDAwMDc4IDAwMDAwIG4NCjAwMDAwMDAyNjQgMDAwMDAgbg0KMDAwMDAwMDQyMSAwMDAwMCBuDQowMDAwMDAwNTQ1IDAwMDAwIG4NCjAwMDAwMDA2MzggMDAwMDAgbg0KMDAwMDAwNDIwNCAwMDAwMCBuDQowMDAwMDEzMDg2IDAwMDAwIG4NCjAwMDAwMTMxMjkgMDAwMDAgbg0KMDAwMDAxMzIzMiAwMDAwMCBuDQp0cmFpbGVyCjw8Ci9Sb290IDEgMCBSCi9JbmZvIDMgMCBSCi9JRCBbPDVBOEEyRkExQjJDNjQzNzYxRjM2RDk3ODc3NjU4MEZEPiA8NUE4QTJGQTFCMkM2NDM3NjFGMzZEOTc4Nzc2NTgwRkQ+XQovU2l6ZSAxMgo+PgpzdGFydHhyZWYKMTMzMzAKJSVFT0YK</DocImageVal>
            </MultiLabel>
        </MultiLabels>
    </LabelImage>
    <Label>
        <LabelTemplate>8X4_A4_PDF</LabelTemplate>
    </Label>
</res:ShipmentResponse>
"""
