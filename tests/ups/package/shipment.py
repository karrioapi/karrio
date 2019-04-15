import unittest
from unittest.mock import patch
from gds_helpers import to_xml, to_dict, export
from pyups.package_ship import ShipmentRequest
from purplship.domain import Types as T
from tests.ups.package.fixture import proxy
from tests.utils import strip, get_node_from_xml


class TestUPSShipment(unittest.TestCase):
    def setUp(self):
        self.ShipmentRequest = ShipmentRequest()
        self.ShipmentRequest.build(
            get_node_from_xml(ShipmentRequestXML, "ShipmentRequest")
        )

    def test_create_package_shipment_request(self):
        payload = T.ShipmentRequest(**package_shipment_data)
        Shipment_ = proxy.mapper.create_shipment_request(payload)
        self.assertEqual(export(Shipment_), export(self.ShipmentRequest))

    @patch("purplship.mappers.ups.ups_proxy.http", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        proxy.create_shipment(self.ShipmentRequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(ShipmentRequestXML))

    def test_parse_shipment_response(self):
        parsed_response = proxy.mapper.parse_shipment_response(
            to_xml(NegotiatedShipmentResponseXML)
        )
        self.assertEqual(
            to_dict(parsed_response), to_dict(NegotiatedParsedShipmentResponse)
        )

    def test_parse_publish_rate_shipment_response(self):
        parsed_response = proxy.mapper.parse_shipment_response(
            to_xml(ShipmentResponseXML)
        )
        self.assertEqual(to_dict(parsed_response), to_dict(ParsedShipmentResponse))


if __name__ == "__main__":
    unittest.main()


package_shipment_data = {
    "shipper": {
        "company_name": "Shipper Name",
        "person_name": "Shipper Attn Name",
        "tax_id": "123456",
        "phone_number": "1234567890",
        "account_number": "Your Shipper Number",
        "address_lines": ["Address Line"],
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
        "extra": {"Extension": "1", "FaxNumber": "1234567890"},
    },
    "recipient": {
        "company_name": "Ship To Name",
        "person_name": "Ship To Attn Name",
        "phone_number": "1234567890",
        "address_lines": ["Address Line"],
        "city": "City",
        "state_code": "StateProvinceCode",
        "postal_code": "PostalCode",
        "country_code": "CountryCode",
    },
    "shipment": {
        "references": ["Your Customer Context"],
        "services": ["UPS_Express"],
        "dimension_unit": "IN",
        "weight_unit": "LB",
        "paid_by": "SENDER",
        "payment_account_number": "Your Account Number",
        "items": [
            {
                "description": "Description",
                "packaging_type": "Customer_Supplied_Package",
                "length": 7,
                "width": 5,
                "height": 2,
                "weight": 10,
            }
        ],
        "label": {"format": "GIF", "extra": {"HTTPUserAgent": "Mozilla/4.5"}},
        "extra": {
            "Description": "Description",
            "ShipFrom": {
                "company_name": "Ship From Name",
                "person_name": "Ship From Attn Name",
                "phone_number": "1234567890",
                "address_lines": ["Address Line"],
                "city": "City",
                "state_code": "StateProvinceCode",
                "postal_code": "PostalCode",
                "country_code": "CountryCode",
                "extra": {"FaxNumber": "1234567890"},
            },
            "ShipmentCharge": {"Type": "01"},
        },
    },
}


NegotiatedParsedShipmentResponse = [
    {
        "carrier": "UPS",
        "charges": [
            {"amount": "88.12", "currency": "USD", "name": None},
            {"amount": "0.00", "currency": "USD", "name": None},
        ],
        "documents": ["R0lGODdheAUgA+cAAAAAAAEBAQIC (Truncated)"],
        "reference": {"type": "CustomerContext", "value": "Your Customer Context"},
        "services": None,
        "shipment_date": None,
        "total_charge": {
            "amount": "70.00",
            "currency": "USD",
            "name": "Shipment charge",
        },
        "tracking_numbers": ["1ZWA82900191640782"],
    },
    [],
]

ParsedShipmentResponse = [
    {
        "carrier": "UPS",
        "charges": [
            {"amount": "88.12", "currency": "USD", "name": None},
            {"amount": "0.00", "currency": "USD", "name": None},
        ],
        "documents": ["R0lGODdheAUgA+c(Truncated)"],
        "reference": {"type": "CustomerContext", "value": "Your Customer Context"},
        "services": None,
        "shipment_date": None,
        "total_charge": {
            "amount": "88.12",
            "currency": "USD",
            "name": "Shipment charge",
        },
        "tracking_numbers": ["1ZWA82900191640782"],
    },
    [],
]


NegotiatedShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header />
    <soapenv:Body>
        <ship:ShipmentResponse xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0">
            <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                <common:ResponseStatus>
                    <common:Code>1</common:Code>
                    <common:Description>Success</common:Description>
                </common:ResponseStatus>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Response>
            <ship:ShipmentResults>
                <ship:ShipmentCharges>
                    <ship:TransportationCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>88.12</ship:MonetaryValue>
                    </ship:TransportationCharges>
                    <ship:ServiceOptionsCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>0.00</ship:MonetaryValue>
                    </ship:ServiceOptionsCharges>
                    <ship:TotalCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>88.12</ship:MonetaryValue>
                    </ship:TotalCharges>
                </ship:ShipmentCharges>
                <ship:NegotiatedRateCharges>
                    <ship:TotalCharge>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>70.00</ship:MonetaryValue>
                    </ship:TotalCharge>
                </ship:NegotiatedRateCharges>
                <ship:BillingWeight>
                    <ship:UnitOfMeasurement>
                        <ship:Code>LBS</ship:Code>
                        <ship:Description>Pounds</ship:Description>
                    </ship:UnitOfMeasurement>
                    <ship:Weight>10.0</ship:Weight>
                </ship:BillingWeight>
                <ship:ShipmentIdentificationNumber>1ZWA82900191640782</ship:ShipmentIdentificationNumber>
                <ship:PackageResults>
                    <ship:TrackingNumber>1ZWA82900191640782</ship:TrackingNumber>
                    <ship:ServiceOptionsCharges>
                        <ship:CurrencyCode>USD</ship:CurrencyCode>
                        <ship:MonetaryValue>0.00</ship:MonetaryValue>
                    </ship:ServiceOptionsCharges>
                    <ship:ShippingLabel>
                        <ship:ImageFormat>
                            <ship:Code>GIF</ship:Code>
                            <ship:Description>GIF</ship:Description>
                        </ship:ImageFormat>
                        <ship:GraphicImage>R0lGODdheAUgA+cAAAAAAAEBAQIC (Truncated)</ship:GraphicImage>
                        <ship:HTMLImage>PCFET0NUWVBFIEhUTUwgUFVCTElD(Truncated)</ship:HTMLImage>
                    </ship:ShippingLabel>
                </ship:PackageResults>
            </ship:ShipmentResults>
        </ship:ShipmentResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Header />
   <soapenv:Body>
      <ship:ShipmentResponse xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0">
         <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
            <common:ResponseStatus>
               <common:Code>1</common:Code>
               <common:Description>Success</common:Description>
            </common:ResponseStatus>
            <common:TransactionReference>
               <common:CustomerContext>Your Customer Context</common:CustomerContext>
            </common:TransactionReference>
         </common:Response>
         <ship:ShipmentResults>
            <ship:ShipmentCharges>
               <ship:TransportationCharges>
                  <ship:CurrencyCode>USD</ship:CurrencyCode>
                  <ship:MonetaryValue>88.12</ship:MonetaryValue>
               </ship:TransportationCharges>
               <ship:ServiceOptionsCharges>
                  <ship:CurrencyCode>USD</ship:CurrencyCode>
                  <ship:MonetaryValue>0.00</ship:MonetaryValue>
               </ship:ServiceOptionsCharges>
               <ship:TotalCharges>
                  <ship:CurrencyCode>USD</ship:CurrencyCode>
                  <ship:MonetaryValue>88.12</ship:MonetaryValue>
               </ship:TotalCharges>
            </ship:ShipmentCharges>
            <ship:BillingWeight>
               <ship:UnitOfMeasurement>
                  <ship:Code>LBS</ship:Code>
                  <ship:Description>Pounds</ship:Description>
               </ship:UnitOfMeasurement>
               <ship:Weight>10.0</ship:Weight>
            </ship:BillingWeight>
            <ship:ShipmentIdentificationNumber>1ZWA82900191640782</ship:ShipmentIdentificationNumber>
            <ship:PackageResults>
               <ship:TrackingNumber>1ZWA82900191640782</ship:TrackingNumber>
               <ship:ServiceOptionsCharges>
                  <ship:CurrencyCode>USD</ship:CurrencyCode>
                  <ship:MonetaryValue>0.00</ship:MonetaryValue>
               </ship:ServiceOptionsCharges>
               <ship:ShippingLabel>
                  <ship:ImageFormat>
                     <ship:Code>GIF</ship:Code>
                     <ship:Description>GIF</ship:Description>
                  </ship:ImageFormat>
                  <ship:GraphicImage>R0lGODdheAUgA+c(Truncated)</ship:GraphicImage>
                  <ship:HTMLImage>PCFET0NUWVBFIEhUTUwgUFVCTElDICI(Truncated)</ship:HTMLImage>
               </ship:ShippingLabel>
            </ship:PackageResults>
         </ship:ShipmentResults>
      </ship:ShipmentResponse>
   </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentRequestXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ship="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0" xmlns:ifs="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0" xsi:schemaLocation="http://www.ups.com/XMLSchema/XOLTWS/Ship/v1.0" >
    <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <ship:ShipmentRequest>
            <common:Request>
                <common:RequestOption>validate</common:RequestOption>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Request>
            <ship:Shipment>
                <ship:Description>Description</ship:Description>
                <ship:Shipper>
                    <ship:Name>Shipper Name</ship:Name>
                    <ship:AttentionName>Shipper Attn Name</ship:AttentionName>
                    <ship:TaxIdentificationNumber>123456</ship:TaxIdentificationNumber>
                    <ship:Phone>
                        <ship:Number>1234567890</ship:Number>
                        <ship:Extension>1</ship:Extension>
                    </ship:Phone>
                    <ship:ShipperNumber>Your Shipper Number</ship:ShipperNumber>
                    <ship:FaxNumber>1234567890</ship:FaxNumber>
                    <ship:Address>
                        <ship:AddressLine>Address Line</ship:AddressLine>
                        <ship:City>City</ship:City>
                        <ship:StateProvinceCode>StateProvinceCode</ship:StateProvinceCode>
                        <ship:PostalCode>PostalCode</ship:PostalCode>
                        <ship:CountryCode>CountryCode</ship:CountryCode>
                    </ship:Address>
                </ship:Shipper>
                <ship:ShipTo>
                    <ship:Name>Ship To Name</ship:Name>
                    <ship:AttentionName>Ship To Attn Name</ship:AttentionName>
                    <ship:Phone>
                        <ship:Number>1234567890</ship:Number>
                    </ship:Phone>
                    <ship:Address>
                        <ship:AddressLine>Address Line</ship:AddressLine>
                        <ship:City>City</ship:City>
                        <ship:StateProvinceCode>StateProvinceCode</ship:StateProvinceCode>
                        <ship:PostalCode>PostalCode</ship:PostalCode>
                        <ship:CountryCode>CountryCode</ship:CountryCode>
                    </ship:Address>
                </ship:ShipTo>
                <ship:ShipFrom>
                    <ship:Name>Ship From Name</ship:Name>
                    <ship:AttentionName>Ship From Attn Name</ship:AttentionName>
                    <ship:Phone>
                        <ship:Number>1234567890</ship:Number>
                    </ship:Phone>
                    <ship:FaxNumber>1234567890</ship:FaxNumber>
                    <ship:Address>
                        <ship:AddressLine>Address Line</ship:AddressLine>
                        <ship:City>City</ship:City>
                        <ship:StateProvinceCode>StateProvinceCode</ship:StateProvinceCode>
                        <ship:PostalCode>PostalCode</ship:PostalCode>
                        <ship:CountryCode>CountryCode</ship:CountryCode>
                    </ship:Address>
                </ship:ShipFrom>
                <ship:PaymentInformation>
                    <ship:ShipmentCharge>
                        <ship:Type>01</ship:Type>
                        <ship:BillShipper>
                            <ship:AccountNumber>Your Account Number</ship:AccountNumber>
                        </ship:BillShipper>
                    </ship:ShipmentCharge>
                </ship:PaymentInformation>
                <ship:Service>
                    <ship:Code>01</ship:Code>
                </ship:Service>
                <ship:Package>
                    <ship:Description>Description</ship:Description>
                    <ship:Packaging>
                        <ship:Code>02</ship:Code>
                    </ship:Packaging>
                    <ship:Dimensions>
                        <ship:UnitOfMeasurement>
                            <ship:Code>IN</ship:Code>
                        </ship:UnitOfMeasurement>
                        <ship:Length>7</ship:Length>
                        <ship:Width>5</ship:Width>
                        <ship:Height>2</ship:Height>
                    </ship:Dimensions>
                    <ship:PackageWeight>
                        <ship:UnitOfMeasurement>
                            <ship:Code>LBS</ship:Code>
                        </ship:UnitOfMeasurement>
                        <ship:Weight>10</ship:Weight>
                    </ship:PackageWeight>
                </ship:Package>
            </ship:Shipment>
            <ship:LabelSpecification>
                <ship:LabelImageFormat>
                    <ship:Code>GIF</ship:Code>
                    <ship:Description>GIF</ship:Description>
                </ship:LabelImageFormat>
                <ship:HTTPUserAgent>Mozilla/4.5</ship:HTTPUserAgent>
            </ship:LabelSpecification>
        </ship:ShipmentRequest>
    </tns:Body>
</tns:Envelope>
"""
