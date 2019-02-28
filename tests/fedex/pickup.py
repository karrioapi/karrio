import unittest
from unittest.mock import patch
import time
from gds_helpers import to_xml, jsonify, export
from pyfedex.pickup_service_v15 import CreatePickupRequest, CancelPickupRequest
from purplship.domain.Types import ShipmentRequest
from tests.fedex.fixture import proxy
from tests.utils import strip, get_node_from_xml


class TestFedExPickup(unittest.TestCase):
    def setUp(self):
        self.PickupRequest = CreatePickupRequest()
        self.PickupRequest.build(
            get_node_from_xml(PickupRequestXml, "CreatePickupRequest")
        )

        self.PickupCancellation = CancelPickupRequest()
        self.PickupCancellation.build(
            get_node_from_xml(PickupCancellationRequestXML, "CancelPickupRequest")
        )

    @patch("purplship.mappers.fedex.fedex_proxy.http", return_value="<a></a>")
    def test_request_pickup(self, http_mock):
        proxy.request_pickup(self.PickupRequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(PickupRequestXml))

    @patch("purplship.mappers.fedex.fedex_proxy.http", return_value="<a></a>")
    def test_cancel_pickup(self, http_mock):
        proxy.cancel_pickup(self.PickupCancellation)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(PickupCancellationRequestXML))


if __name__ == "__main__":
    unittest.main()

PickupCancellationRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/pickup/v15">
   <tns:Body>
      <ns:CancelPickupRequest>
         <ns:WebAuthenticationDetail>
            <ns:ParentCredential>
               <ns:Key>INPUT YOUR INFORMATION</ns:Key>
               <ns:Password>INPUT YOUR INFORMATION</ns:Password>
            </ns:ParentCredential>
            <ns:UserCredential>
               <ns:Key>INPUT YOUR INFORMATION</ns:Key>
               <ns:Password>INPUT YOUR INFORMATION</ns:Password>
            </ns:UserCredential>
         </ns:WebAuthenticationDetail>
         <ns:ClientDetail>
            <ns:AccountNumber>INPUT YOUR INFORMATION</ns:AccountNumber>
            <ns:MeterNumber>INPUT YOUR INFORMATION</ns:MeterNumber>
            <ns:Localization>
               <ns:LanguageCode>EN</ns:LanguageCode>
               <ns:LocaleCode>US</ns:LocaleCode>
            </ns:Localization>
         </ns:ClientDetail>
         <ns:TransactionDetail>
            <ns:CustomerTransactionId>CancelPickupRequest_ns</ns:CustomerTransactionId>
            <ns:Localization>
               <ns:LanguageCode>EN</ns:LanguageCode>
               <ns:LocaleCode>US</ns:LocaleCode>
            </ns:Localization>
         </ns:TransactionDetail>
         <ns:Version>
            <ns:ServiceId>disp</ns:ServiceId>
            <ns:Major>15</ns:Major>
            <ns:Intermediate>0</ns:Intermediate>
            <ns:Minor>0</ns:Minor>
         </ns:Version>
         <ns:CarrierCode>FDXE</ns:CarrierCode>
         <ns:PickupConfirmationNumber>INPUT YOUR INFORMATION</ns:PickupConfirmationNumber>
         <ns:ScheduledDate>2016-12-13</ns:ScheduledDate>
         <ns:Location>NQAA</ns:Location>
         <ns:Remarks>Preet</ns:Remarks>
         <ns:ShippingChargesPayment>
            <ns:PaymentType>CASH</ns:PaymentType>
            <ns:Payor>
               <ns:ResponsibleParty>
                  <ns:AccountNumber></ns:AccountNumber>
                  <ns:Tins>
                     <ns:TinType>BUSINESS_NATIONAL</ns:TinType>
                     <ns:Number>123456989012345</ns:Number>
                     <ns:Usage>string</ns:Usage>
                  </ns:Tins>
                  <ns:Contact>
                     <ns:ContactId>INPUT YOUR INFORMATION</ns:ContactId>
                     <ns:PersonName>INPUT YOUR INFORMATION</ns:PersonName>
                     <ns:Title>Mr.</ns:Title>
                     <ns:CompanyName>INPUT YOUR INFORMATION</ns:CompanyName>
                     <ns:PhoneNumber>INPUT YOUR INFORMATION</ns:PhoneNumber>
                     <ns:PhoneExtension>INPUT YOUR INFORMATION</ns:PhoneExtension>
                     <ns:PagerNumber>INPUT YOUR INFORMATION</ns:PagerNumber>
                     <ns:FaxNumber>INPUT YOUR INFORMATION</ns:FaxNumber>
                     <ns:EMailAddress>kaustubha_ramdasi@syntelinc.com</ns:EMailAddress>
                  </ns:Contact>
                  <ns:Address>
                     <ns:StreetLines>INPUT YOUR INFORMATION</ns:StreetLines>
                     <ns:StreetLines>INPUT YOUR INFORMATION</ns:StreetLines>
                     <ns:City>Memphis</ns:City>
                     <ns:StateOrProvinceCode>TN</ns:StateOrProvinceCode>
                     <ns:PostalCode>38125</ns:PostalCode>
                     <ns:CountryCode>US</ns:CountryCode>
                     <ns:GeographicCoordinates>aris imponet</ns:GeographicCoordinates>
                  </ns:Address>
               </ns:ResponsibleParty>
               <ns:AssociatedAccounts>
                  <ns:Type>FEDEX_EXPRESS</ns:Type>
                  <ns:AccountNumber>INPUT YOUR INFORMATION</ns:AccountNumber>
               </ns:AssociatedAccounts>
            </ns:Payor>
            <ns:Amount>
               <ns:Currency>USD</ns:Currency>
               <ns:Amount>220000.</ns:Amount>
            </ns:Amount>
         </ns:ShippingChargesPayment>
         <ns:Reason>TXT</ns:Reason>
         <ns:ContactName>INPUT YOUR INFORMATION</ns:ContactName>
      </ns:CancelPickupRequest>
   </tns:Body>
</tns:Envelope>
"""

PickupRequestXml = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://fedex.com/ws/pickup/v15">
   <tns:Body>
      <ns:CreatePickupRequest>
         <ns:WebAuthenticationDetail>
            <ns:ParentCredential>
               <ns:Key>INPUT YOUR INFORMATION</ns:Key>
               <ns:Password>INPUT YOUR INFORMATION</ns:Password>
            </ns:ParentCredential>
            <ns:UserCredential>
               <ns:Key>INPUT YOUR INFORMATION</ns:Key>
               <ns:Password>INPUT YOUR INFORMATION</ns:Password>
            </ns:UserCredential>
         </ns:WebAuthenticationDetail>
         <ns:ClientDetail>
            <ns:AccountNumber>INPUT YOUR INFORMATION</ns:AccountNumber>
            <ns:MeterNumber>INPUT YOUR INFORMATION</ns:MeterNumber>
            <ns:IntegratorId>12345</ns:IntegratorId>
            <ns:Localization>
               <ns:LanguageCode>EN</ns:LanguageCode>
               <ns:LocaleCode>ES</ns:LocaleCode>
            </ns:Localization>
         </ns:ClientDetail>
         <ns:TransactionDetail>
            <ns:CustomerTransactionId>CreatePickupRequest_ns</ns:CustomerTransactionId>
            <ns:Localization>
               <ns:LanguageCode>EN</ns:LanguageCode>
               <ns:LocaleCode>ES</ns:LocaleCode>
            </ns:Localization>
         </ns:TransactionDetail>
         <ns:Version>
            <ns:ServiceId>disp</ns:ServiceId>
            <ns:Major>15</ns:Major>
            <ns:Intermediate>0</ns:Intermediate>
            <ns:Minor>0</ns:Minor>
         </ns:Version>
         <ns:AssociatedAccountNumber>
            <ns:Type>FEDEX_EXPRESS</ns:Type>
            <ns:AccountNumber>INPUT YOUR INFORMATION</ns:AccountNumber>
         </ns:AssociatedAccountNumber>
         <ns:OriginDetail>
            <ns:PickupLocation>
               <ns:Contact>
                  <ns:ContactId>INPUT YOUR INFORMATION</ns:ContactId>
                  <ns:PersonName>INPUT YOUR INFORMATION</ns:PersonName>
                  <ns:Title>Mr.</ns:Title>
                  <ns:CompanyName>INPUT YOUR INFORMATION$</ns:CompanyName>
                  <ns:PhoneNumber>INPUT YOUR INFORMATION</ns:PhoneNumber>
                  <ns:PhoneExtension>02033469</ns:PhoneExtension>
                  <ns:PagerNumber>INPUT YOUR INFORMATION</ns:PagerNumber>
                  <ns:FaxNumber>INPUT YOUR INFORMATION</ns:FaxNumber>
                  <ns:EMailAddress>kaustubha_ramdasi@syntelinc.com</ns:EMailAddress>
               </ns:Contact>
               <ns:Address>
                  <ns:StreetLines>INPUT YOUR INFORMATION</ns:StreetLines>
                  <ns:StreetLines>INPUT YOUR INFORMATION</ns:StreetLines>
                  <ns:City>Memphis</ns:City>
                  <ns:StateOrProvinceCode>TN</ns:StateOrProvinceCode>
                  <ns:PostalCode>38125</ns:PostalCode>
                  <ns:CountryCode>US</ns:CountryCode>
                  <ns:GeographicCoordinates>regina iovisque</ns:GeographicCoordinates>
               </ns:Address>
            </ns:PickupLocation>
            <ns:PackageLocation>FRONT</ns:PackageLocation>
            <ns:BuildingPart>DEPARTMENT</ns:BuildingPart>
            <ns:BuildingPartDescription>BuildingPartDescription</ns:BuildingPartDescription>
            <ns:ReadyTimestamp>2016-12-13T16:16:44-06:00</ns:ReadyTimestamp>
            <ns:CompanyCloseTime>19:00:00</ns:CompanyCloseTime>
            <ns:Location>NQAA</ns:Location>
            <ns:SuppliesRequested>SuppliesRequested</ns:SuppliesRequested>
         </ns:OriginDetail>
         <ns:PackageCount>1</ns:PackageCount>
         <ns:TotalWeight>
            <ns:Units>LB</ns:Units>
            <ns:Value>50.</ns:Value>
         </ns:TotalWeight>
         <ns:CarrierCode>FDXE</ns:CarrierCode>
         <ns:OversizePackageCount>0</ns:OversizePackageCount>
         <ns:Remarks>Remarks</ns:Remarks>
         <ns:CommodityDescription>TEST ENVIRONMENT - PLEASE DO NOT PROCESS PICKUP</ns:CommodityDescription>
         <ns:CountryRelationship>DOMESTIC</ns:CountryRelationship>
      </ns:CreatePickupRequest>
   </tns:Body>
</tns:Envelope>
"""
