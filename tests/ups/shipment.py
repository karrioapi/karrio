import unittest
from unittest.mock import patch
import time
from gds_helpers import to_xml, jsonify, export
from pyups.freight_ship import FreightShipRequest
from purplship.domain.entities import Shipment
from tests.ups.fixture import proxy
from tests.utils import strip, get_node_from_xml


class TestUPSShipment(unittest.TestCase):
    def setUp(self):
        self.ShipmentRequest = FreightShipRequest()
        self.ShipmentRequest.build(get_node_from_xml(ShipmentRequestXml, 'FreightShipRequest'))

    @patch("purplship.mappers.ups.ups_proxy.http", return_value='<a></a>')
    def test_create_shipment(self, http_mock):
        proxy.create_shipment(self.ShipmentRequest)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(ShipmentRequestXml))


if __name__ == '__main__':
    unittest.main()

ShipmentRequestXml = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:fsp="http://www.ups.com/XMLSchema/XOLTWS/FreightShip/v1.0" xmlns:IF="http://www.ups.com/XMLSchema/XOLTWS/IF/v1.0" >
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
