import unittest
from unittest.mock import patch
import time
from gds_helpers import to_xml, jsonify, export
from pyups.freight_ship import FreightShipRequest
from pyups.package_ship import ShipmentRequest
from purplship.domain.entities import Shipment
from tests.ups.fixture import proxy
from tests.utils import strip, get_node_from_xml


class TestUPSShipment(unittest.TestCase):
    def setUp(self):
        self.FreightShipRequest = FreightShipRequest()
        self.FreightShipRequest.build(get_node_from_xml(FreightShipmentRequestXML, 'FreightShipRequest'))

        self.ShipmentRequest = ShipmentRequest()
        self.ShipmentRequest.build(get_node_from_xml(ShipmentRequestXML, 'ShipmentRequest'))

    @patch("purplship.mappers.ups.ups_proxy.http", return_value='<a></a>')
    def test_create_freight_shipment(self, http_mock):
        proxy.create_shipment(self.FreightShipRequest)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(FreightShipmentRequestXML))

    @patch("purplship.mappers.ups.ups_proxy.http", return_value='<a></a>')
    def test_create_shipment(self, http_mock):
        proxy.create_shipment(self.ShipmentRequest)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(ShipmentRequestXml))


if __name__ == '__main__':
    unittest.main()


ParsedFreightShipmentResponse = []


FreightShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
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

FreightShipmentRequestXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:fsp="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0" xmlns:IF="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0" >
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
      <fsp:FreightShipRequest>
         <common:Request>
            <common:RequestOption>1</common:RequestOption>
            <common:SubVersion>SubVersion</common:SubVersion>
            <common:TransactionReference>
               <common:CustomerContext>Your Customer Context</common:CustomerContext>
            </common:TransactionReference>
         </common:Request>
         <fsp:Shipment>
            <fsp:ShipFrom>
               <fsp:Name>Ship From Name</fsp:Name>
               <fsp:Address>
                  <fsp:AddressLine>Address Line</fsp:AddressLine>
                  <fsp:City>City</fsp:City>
                  <fsp:StateProvinceCode>StateProvinceCode</fsp:StateProvinceCode>
                  <fsp:PostalCode>PostalCode</fsp:PostalCode>
                  <fsp:CountryCode>CountryCode</fsp:CountryCode>
               </fsp:Address>
               <fsp:AttentionName>Attention Name</fsp:AttentionName>
               <fsp:Phone>
                  <fsp:Number>Shipper Phone number</fsp:Number>
               </fsp:Phone>
            </fsp:ShipFrom>
            <fsp:ShipperNumber>Your Shipper Number</fsp:ShipperNumber>
            <fsp:ShipTo>
               <fsp:Name>Ship To Name</fsp:Name>
               <fsp:Address>
                  <fsp:AddressLine>Address Line</fsp:AddressLine>
                  <fsp:City>City</fsp:City>
                  <fsp:StateProvinceCode>StateProvinceCode</fsp:StateProvinceCode>
                  <fsp:PostalCode>PostalCode</fsp:PostalCode>
                  <fsp:CountryCode>CountryCode</fsp:CountryCode>
               </fsp:Address>
               <fsp:AttentionName>Attention Name</fsp:AttentionName>
            </fsp:ShipTo>
            <fsp:PaymentInformation>
               <fsp:Payer>
                  <fsp:Name>Payer Name</fsp:Name>
                  <fsp:Address>
                     <fsp:AddressLine>Address Line</fsp:AddressLine>
                     <fsp:City>City</fsp:City>
                     <fsp:StateProvinceCode>StateProvinceCode</fsp:StateProvinceCode>
                     <fsp:PostalCode>PostalCode</fsp:PostalCode>
                     <fsp:CountryCode>CountryCode</fsp:CountryCode>
                  </fsp:Address>
                  <fsp:ShipperNumber>Payer Shipper Number</fsp:ShipperNumber>
                  <fsp:AttentionName>Attention Name</fsp:AttentionName>
                  <fsp:Phone>
                     <fsp:Number>Phone Number</fsp:Number>
                  </fsp:Phone>
               </fsp:Payer>
               <fsp:ShipmentBillingOption>
                  <fsp:Code>ShipmentBillingOption</fsp:Code>
               </fsp:ShipmentBillingOption>
            </fsp:PaymentInformation>
            <fsp:Service>
               <fsp:Code>Service code</fsp:Code>
            </fsp:Service>
            <fsp:HandlingUnitOne>
               <fsp:Quantity>HandlingUnitOne quantity</fsp:Quantity>
               <fsp:Type>
                  <fsp:Code>HandlingUnitOne type</fsp:Code>
               </fsp:Type>
            </fsp:HandlingUnitOne>
            <fsp:Commodity>
               <fsp:Description>Commodity Description</fsp:Description>
               <fsp:Weight>
                  <fsp:UnitOfMeasurement>
                     <fsp:Code>UnitOfMeasurement code</fsp:Code>
                  </fsp:UnitOfMeasurement>
                  <fsp:Value>Weight</fsp:Value>
               </fsp:Weight>
               <fsp:NumberOfPieces>NumberOfPieces</fsp:NumberOfPieces>
               <fsp:PackagingType>
                  <fsp:Code>PackagingType code</fsp:Code>
               </fsp:PackagingType>
               <fsp:FreightClass>FreightClass</fsp:FreightClass>
            </fsp:Commodity>
            <fsp:TimeInTransitIndicator></fsp:TimeInTransitIndicator>
            <fsp:DensityEligibleIndicator></fsp:DensityEligibleIndicator>
         </fsp:Shipment>
      </fsp:FreightShipRequest>
   </tns:Body>
</tns:Envelope>
"""

ShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header />
    <soapenv:Body>
        <freightShip:FreightShipResponse xmlns:freightShip="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0">
            <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                <common:ResponseStatus>
                    <common:Code>1</common:Code>
                    <common:Description>Success</common:Description>
                </common:ResponseStatus>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Response>
            <freightShip:ShipmentResults>
                <freightShip:OriginServiceCenterCode>OriginServiceCenterCode</freightShip:OriginServiceCenterCode>
                <freightShip:ShipmentNumber>Shipment Number</freightShip:ShipmentNumber>
                <freightShip:BOLID>BOLID</freightShip:BOLID>
                <freightShip:GuaranteedIndicator />
                <freightShip:Rate>
                    <freightShip:Type>
                        <freightShip:Code>DSCNT</freightShip:Code>
                        <freightShip:Description>DSCNT</freightShip:Description>
                    </freightShip:Type>
                    <freightShip:Factor>
                        <freightShip:Value>Value</freightShip:Value>
                        <freightShip:UnitOfMeasurement>
                            <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                        </freightShip:UnitOfMeasurement>
                    </freightShip:Factor>
                </freightShip:Rate>
                <freightShip:Rate>
                    <freightShip:Type>
                        <freightShip:Code>DSCNT_RATE</freightShip:Code>
                        <freightShip:Description>DSCNT_RATE</freightShip:Description>
                    </freightShip:Type>
                    <freightShip:Factor>
                        <freightShip:Value>Value</freightShip:Value>
                        <freightShip:UnitOfMeasurement>
                            <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                        </freightShip:UnitOfMeasurement>
                    </freightShip:Factor>
                </freightShip:Rate>
                <freightShip:Rate>
                    <freightShip:Type>
                        <freightShip:Code>2</freightShip:Code>
                        <freightShip:Description>2</freightShip:Description>
                    </freightShip:Type>
                    <freightShip:Factor>
                        <freightShip:Value>Value</freightShip:Value>
                        <freightShip:UnitOfMeasurement>
                            <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                        </freightShip:UnitOfMeasurement>
                    </freightShip:Factor>
                </freightShip:Rate>
                <freightShip:Rate>
                    <freightShip:Type>
                        <freightShip:Code>LND_GROSS</freightShip:Code>
                        <freightShip:Description>LND_GROSS</freightShip:Description>
                    </freightShip:Type>
                    <freightShip:Factor>
                        <freightShip:Value>Value</freightShip:Value>
                        <freightShip:UnitOfMeasurement>
                            <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                        </freightShip:UnitOfMeasurement>
                    </freightShip:Factor>
                </freightShip:Rate>
                <freightShip:Rate>
                    <freightShip:Type>
                        <freightShip:Code>AFTR_DSCNT</freightShip:Code>
                        <freightShip:Description>AFTR_DSCNT</freightShip:Description>
                    </freightShip:Type>
                    <freightShip:Factor>
                        <freightShip:Value>Value</freightShip:Value>
                        <freightShip:UnitOfMeasurement>
                            <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                        </freightShip:UnitOfMeasurement>
                    </freightShip:Factor>
                </freightShip:Rate>
                <freightShip:TotalShipmentCharge>
                    <freightShip:CurrencyCode>CurrencyCode</freightShip:CurrencyCode>
                    <freightShip:MonetaryValue>MonetaryValue</freightShip:MonetaryValue>
                </freightShip:TotalShipmentCharge>
                <freightShip:BillableShipmentWeight>
                    <freightShip:UnitOfMeasurement>
                        <freightShip:Code>UnitOfMeasurement code</freightShip:Code>
                    </freightShip:UnitOfMeasurement>
                    <freightShip:Value>BillableShipmentWeight</freightShip:Value>
                </freightShip:BillableShipmentWeight>
                <freightShip:Service>
                    <freightShip:Code>Service code</freightShip:Code>
                </freightShip:Service>
                <freightShip:TimeInTransit>
                    <freightShip:DaysInTransit>DaysInTransit</freightShip:DaysInTransit>
                </freightShip:TimeInTransit>
            </freightShip:ShipmentResults>
        </freightShip:FreightShipResponse>
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
                    <ship:Description>Express</ship:Description>
                </ship:Service>
                <ship:Package>
                    <ship:Description>Description</ship:Description>
                    <ship:Packaging>
                        <ship:Code>02</ship:Code>
                        <ship:Description>Description</ship:Description>
                    </ship:Packaging>
                    <ship:Dimensions>
                        <ship:UnitOfMeasurement>
                            <ship:Code>IN</ship:Code>
                            <ship:Description>Inches</ship:Description>
                        </ship:UnitOfMeasurement>
                        <ship:Length>7</ship:Length>
                        <ship:Width>5</ship:Width>
                        <ship:Height>2</ship:Height>
                    </ship:Dimensions>
                    <ship:PackageWeight>
                        <ship:UnitOfMeasurement>
                            <ship:Code>LBS</ship:Code>
                            <ship:Description>Pounds</ship:Description>
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