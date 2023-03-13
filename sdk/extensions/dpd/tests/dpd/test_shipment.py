import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDPDShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.IntlShipmentRequest = models.ShipmentRequest(**IntlShipmentPayload)
        self.MultiPieceShipmentRequest = models.ShipmentRequest(
            **MultiPieceShipmentPayload
        )

   #  def test_create_shipment_request(self):
   #      request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

   #      self.assertEqual(request.serialize(), ShipmentRequest)

   #  def test_create_intl_shipment_request(self):
   #      request = gateway.mapper.create_shipment_request(self.IntlShipmentRequest)

   #      self.assertEqual(request.serialize(), IntlShipmentRequest)

   #  def test_create_multi_piece_shipment_request(self):
   #      request = gateway.mapper.create_shipment_request(self.MultiPieceShipmentRequest)

   #      self.assertEqual(request.serialize(), MultiPieceShipmentRequest)

   #  def test_create_shipment(self):
   #      with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
   #          mock.return_value = "<a></a>"
   #          karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

   #          self.assertEqual(
   #              mock.call_args[1]["url"],
   #              f"{gateway.settings.server_url}",
   #          )

   #  def test_parse_shipment_response(self):
   #      with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
   #          mock.return_value = ShipmentResponse
   #          parsed_response = (
   #              karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
   #          )

   #          self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "person_name": "Senders NV",
        "company_name": "Jan Janssens",
        "city": "Mechelen",
        "country_code": "BE",
        "postal_code": "2800",
        "address_line1": "Egide Walschaertsstraat 20",
        "residential": False,
    },
    "recipient": {
        "person_name": "Receivers NV",
        "city": "Mechelen",
        "country_code": "BE",
        "postal_code": "2800",
        "address_line1": "Teststraat 5",
        "residential": False,
    },
    "parcels": [
        {
            "weight": 340,
            "weight_unit": "LB",
            "reference_number": "Box 1234",
        }
    ],
    "service": "purolator_express",
    "label_type": "PDF",
    "options": {"shipment_date": "2021-02-04"},
}

IntlShipmentPayload = {}

MultiPieceShipmentPayload = {}

ParsedShipmentResponse = [
    {
        "carrier_name": "dpd",
        "carrier_id": "dpd",
        "tracking_number": "05308801410058",
        "shipment_identifier": "MPS0530880141005820190701",
        "docs": {"label": ANY},
    },
    [],
]


ShipmentRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0" xmlns:ns1="http://dpd.com/common/service/types/ShipmentService/3.3">
   <soapenv:Header>
      <ns:authentication>
         <delisId>KD*****</delisId>
         <authToken>****</authToken>
         <messageLanguage>en_EN</messageLanguage> 
      </ns:authentication>
   </soapenv:Header>
   <soapenv:Body>
      <ns1:storeOrders>
         <printOptions>
            <printerLanguage>PDF</printerLanguage>
            <paperFormat>A6</paperFormat>
         </printOptions>
         <order>
            <generalShipmentData>
               <sendingDepot>0530</sendingDepot>
               <product>CL</product> 
               <sender> 
                  <name1>Senders NV</name1>
                  <name2>Jan Janssens</name2>
                  <street>Egide Walschaertsstraat 20</street>
                  <country>BE</country>
                  <zipCode>2800</zipCode>
                  <city>Mechelen</city>
                  <type>B</type>
               </sender>
               <recipient> 
                  <name1>Receivers NV</name1>
                  <street>Teststraat 5</street>
                  <country>BE</country>
                  <zipCode>2800</zipCode>
                  <city>Mechelen</city>
                  <type>B</type> 
               </recipient>
            </generalShipmentData>            
            <parcels>
               <customerReferenceNumber1>Box 1234</customerReferenceNumber1> 
               <weight>340</weight> 
            </parcels>
            <productAndServiceData>
               <orderType>consignment</orderType> 
            </productAndServiceData>
         </order>
       </ns1:storeOrders>
   </soapenv:Body>
</soapenv:Envelope>
"""

MultiPieceShipmentRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0" xmlns:ns1="http://dpd.com/common/service/types/ShipmentService/3.3">
   <soapenv:Header><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0" xmlns:ns1="http://dpd.com/common/service/types/ShipmentService/3.3">
   <soapenv:Header>
      <ns:authentication>
         <delisId>KD*****</delisId>
         <authToken>****</authToken>
         <messageLanguage>en_EN</messageLanguage> 
      </ns:authentication>
   </soapenv:Header>
   <soapenv:Body>
      <ns1:storeOrders>
         <printOptions>
            <printerLanguage>PDF</printerLanguage>
            <paperFormat>A6</paperFormat>
         </printOptions>
         <order>
            <generalShipmentData>
               <sendingDepot>0530</sendingDepot>
               <product>CL</product> 
               <sender> 
                  <name1>Senders NV</name1>
                  <name2>Jan Janssens</name2>
                  <street>Egide Walschaertsstraat 20</street>
                  <country>BE</country>
                  <zipCode>2800</zipCode>
                  <city>Mechelen</city>
                  <type>B</type>
               </sender>
               <recipient> 
                  <name1>Receivers NV</name1>
                  <street>Teststraat 5</street>
                  <country>BE</country>
                  <zipCode>2800</zipCode>
                  <city>Mechelen</city>
                  <type>B</type> 
               </recipient>
            </generalShipmentData>            
            <parcels>
               <customerReferenceNumber1>Box 1</customerReferenceNumber1> 
               <weight>340</weight> 
            </parcels>
            <parcels>
               <customerReferenceNumber1>Box 2</customerReferenceNumber1> 
               <weight>500</weight> 
            </parcels>
            <productAndServiceData>
               <orderType>consignment</orderType> 
            </productAndServiceData>
         </order>
       </ns1:storeOrders>
   </soapenv:Body>
</soapenv:Envelope>
"""

IntlShipmentRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0" xmlns:ns1="http://dpd.com/common/service/types/ShipmentService/3.3">
   <soapenv:Header>
      <ns:authentication>
         <delisId>KD*****</delisId>
         <authToken>****</authToken>
         <messageLanguage>en_En</messageLanguage>
      </ns:authentication>
   </soapenv:Header>
   <soapenv:Body>
      <ns1:storeOrders>
         <printOptions>
            <printerLanguage>PDF</printerLanguage>
            <paperFormat>A6</paperFormat>
         </printOptions>
         <order>
            <generalShipmentData>
               <sendingDepot>0530</sendingDepot>
               <product>CL</product>
               <sender>
                  <name1>Sender NV</name1>
                  <name2>Jan Jansens</name2>
                  <street>Egide Walschaertsstraat</street>
                  <houseNo>20</houseNo>
                  <country>BE</country>
                  <zipCode>2800</zipCode>
                  <city>Mechelen</city>
                <phone>+3215124578</phone>
              <email>sender@sendercompany.com</email>
                  <eoriNumber>1133113311</eoriNumber>
              <vatNumber>BE123456</vatNumber>
              <destinationCountryRegistration>QQ123456C</destinationCountryRegistration>
               </sender>
               <recipient>
                  <name1>British Test</name1>
                  <street>Receiverstraat</street>
                   <houseNo>5</houseNo>
                  <country>GB</country>
                  <zipCode>LS101AB</zipCode>
                  <city>Leeds</city>
             <phone>+442012345678</phone>
              <email>receiver@receivercompany.com</email>
                  <eoriNumber>7788778877</eoriNumber>
              <vatNumber>GB654321</vatNumber> 
               </recipient>
            </generalShipmentData>
            <parcels>
               <customerReferenceNumber1>Box 1234</customerReferenceNumber1>
               <weight>123</weight>
                <international>
                  <parcelType>false</parcelType> 
                  <customsAmount>1400</customsAmount> 
                  <customsCurrency>EUR</customsCurrency>
                  <customsAmountEx>1400</customsAmountEx> 
                  <customsCurrencyEx>EUR</customsCurrencyEx>
                  <clearanceCleared>N</clearanceCleared> 
                  <prealertStatus>S03</prealertStatus>
                  <exportReason>01</exportReason>
                  <customsTerms>06</customsTerms>
                  <customsContent>Paperclips</customsContent>                 
                  <customsInvoice>12345</customsInvoice>
                  <customsInvoiceDate>20190624</customsInvoiceDate>
                  <comment2>QQ123456C</comment2>
                  <commercialInvoiceConsigneeVatNumber>GB654321</commercialInvoiceConsigneeVatNumber>                    
                  <commercialInvoiceConsignee>
                       <name1>British Test</name1>
                       <street>Receiverstraat</street>
                       <houseNo>5</houseNo>
                       <country>GB</country>
                       <zipCode>LS101AB</zipCode>
                       <city>Leeds</city>
                       <phone>+442012345678</phone>
                       <email>receiver@receivercompany.com</email>
                       <eoriNumber>7788778877</eoriNumber>
                       <vatNumber>GB654321</vatNumber>               
                  </commercialInvoiceConsignee>
                  <commercialInvoiceConsignor>
                       <name1>Sender NV</name1>
                       <name2>Jan Jansens</name2>
                       <street>Egide Walschaertsstraat</street>
                       <houseNo>20</houseNo>
                       <country>BE</country>
                       <zipCode>2800</zipCode>
                       <city>Mechelen</city>
                       <phone>+3215124578</phone>
                       <email>sender@sendercompany.com</email> 
                       <eoriNumber>1133113311</eoriNumber>
                       <vatNumber>BE123456</vatNumber>    
                  </commercialInvoiceConsignor>
                 <commercialInvoiceLine>
                     <customsTarif>2225522</customsTarif>
                     <receiverCustomsTarif>5552255</receiverCustomsTarif>
                     <productCode>88776655</productCode>
                     <content>Paperclips</content>
                     <grossWeight>123</grossWeight>                  
                     <itemsNumber>1</itemsNumber>
                     <amountLine>1515</amountLine>
                     <customsOrigin>BE</customsOrigin>
                     <invoicePosition>5151</invoicePosition>
                  </commercialInvoiceLine>   
               </international>
               <!-- CUSTOMS SEGMENT FOR NON-EU ENDS HERE -->
            </parcels>
            <productAndServiceData>
               <orderType>consignment</orderType>
            </productAndServiceData>
         </order>
      </ns1:storeOrders>
   </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
        <orderResult xmlns= ”http:// dpd.com/ common/ service/ types/ ShipmentService/ 3.3“>
            <parcellabelsPDF>****</parcellabelsPDF>
            <shipmentResponses>
                <identificationNumber />
                <mpsId>MPS0530880141005820190701</mpsId>
                <parcelInformation>
                    <parcelLabelNumber>05308801410058</parcelLabelNumber>
                </parcelInformation>
            </shipmentResponses>
        </orderResult>
    </soap:Body>
</soap:Envelope>
"""
