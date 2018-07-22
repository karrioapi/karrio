import unittest
from unittest.mock import patch
from gds_helpers import to_xml, jsonify, export
from openship.domain.entities import Quote
from tests.ups.fixture import proxy
from tests.utils import strip


class TestUPSQuote(unittest.TestCase):

    @patch("openship.mappers.ups.ups_proxy.http", return_value='<a></a>')
    def test_create_quote_request(self, http_mock):
        shipper = {
            "address": {"postal_code":"H3N1S4", "country_code":"CA", "city":"Montreal", "address_lines": ["Rue Fake"]}
        }
        recipient = {"address": {"postal_code":"89109", "city":"Las Vegas", "country_code":"US"}}
        shipment_details = {"packages": [{"id":"1", "height":3, "lenght":10, "width":3,"weight":4.0, "description":"TV"}]}
        payload = Quote.create(shipper=shipper, recipient=recipient, shipment_details=shipment_details)
        quote_req_xml_obj = proxy.mapper.create_quote_request(payload)

        proxy.get_quotes(quote_req_xml_obj)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")

        self.assertEqual(strip(xmlStr), strip(QuoteRequestXml))

    def test_parse_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteResponseXml))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedQuoteResponse))
                
    def test_parse_quote_parsing_error(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteParsingError))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedQuoteParsingError))
                
    def test_parse_quote_missing_args_error(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteMissingArgsError))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedQuoteMissingArgsError))


if __name__ == '__main__':
    unittest.main()




ParsedQuoteParsingError = [
]

ParsedQuoteMissingArgsError = [
]

ParsedQuoteResponse = [
]


QuoteParsingError = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header/>
    <soapenv:Body>
        <soapenv:Fault>
            <faultcode>Client</faultcode>
            <faultstring>An exception has been raised as a result of client data.</faultstring>
            <detail>
                <err:Errors xmlns:err="http://www.ups.com/XMLSchema/XOLTWS/Error/v1.1">
                    <err:ErrorDetail>
                        <err:Severity>Hard</err:Severity>
                        <err:PrimaryErrorCode>
                            <err:Code>9380216</err:Code>
                            <err:Description>Missing or Invalid Handling Unit One Quantity</err:Description>
                        </err:PrimaryErrorCode>
                    </err:ErrorDetail>
                    <err:ErrorDetail>
                        <err:Severity>Hard</err:Severity>
                        <err:PrimaryErrorCode>
                            <err:Code>9360541</err:Code>
                            <err:Description>Missing or Invalid Pickup Date.</err:Description>
                        </err:PrimaryErrorCode>
                    </err:ErrorDetail>
                </err:Errors>
            </detail>
        </soapenv:Fault>
    </soapenv:Body>
</soapenv:Envelope>
"""

QuoteMissingArgsError = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header/>
    <soapenv:Body>
        <soapenv:Fault>
            <faultcode>Client</faultcode>
            <faultstring>An exception has been raised as a result of client data.</faultstring>
            <detail>
                <err:Errors xmlns:err="http://www.ups.com/XMLSchema/XOLTWS/Error/v1.1">
                    <err:ErrorDetail>
                        <err:Severity>Authentication</err:Severity>
                        <err:PrimaryErrorCode>
                            <err:Code>250002</err:Code>
                            <err:Description>Invalid Authentication Information.</err:Description>
                        </err:PrimaryErrorCode>
                        <err:Location>
                            <err:LocationElementName>upss:Password</err:LocationElementName>
                            <err:XPathOfElement>/env:Envelope[1]/env:Header[1]/upss:UPSSecurity[1]/upss:UsernameToken[1]/upss:Password[1]</err:XPathOfElement>
                            <err:OriginalValue/>
                        </err:Location>
                        <err:SubErrorCode>
                            <err:Code>01</err:Code>
                            <err:Description>Missing required element</err:Description>
                        </err:SubErrorCode>
                    </err:ErrorDetail>
                </err:Errors>
            </detail>
        </soapenv:Fault>
    </soapenv:Body>
</soapenv:Envelope>
"""

QuoteRequestXml = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <env:Header>
      <upss:UPSSecurity>
         <upss:UsernameToken>
            <upss:Username>D@nielk91</upss:Username>
            <upss:Password>Shikamaru91</upss:Password>
         </upss:UsernameToken>
         <upss:ServiceAccessToken>
            <upss:AccessLicenseNumber>3D2AE545EC0E43FE</upss:AccessLicenseNumber>
         </upss:ServiceAccessToken>
      </upss:UPSSecurity>
   </env:Header>
   <env:Body>
      <XOLTWS:FreightRateRequest xmlns:XOLTWS="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0">
         <common:Request>
            <common:RequestOption>1</common:RequestOption>
            <common:TransactionReference>
               <common:TransactionIdentifier>TransactionIdentifier</common:TransactionIdentifier>
            </common:TransactionReference>
         </common:Request>
         <XOLTWS:ShipFrom>
            <XOLTWS:Name>ShipFrom Name</XOLTWS:Name>
            <XOLTWS:Address>
               <XOLTWS:PostalCode>H8Z2Z3</XOLTWS:PostalCode>
               <XOLTWS:CountryCode>CA</XOLTWS:CountryCode>
            </XOLTWS:Address>
            <XOLTWS:AttentionName>Contact</XOLTWS:AttentionName>
            <XOLTWS:Phone>
               <XOLTWS:Number>4389856072</XOLTWS:Number>
               <XOLTWS:Extension>333</XOLTWS:Extension>
            </XOLTWS:Phone>
            <XOLTWS:EMailAddress>daniel@gmail.com</XOLTWS:EMailAddress>
         </XOLTWS:ShipFrom>
         <XOLTWS:ShipperNumber>002R48</XOLTWS:ShipperNumber>
         <XOLTWS:ShipTo>
            <XOLTWS:Name>ShipTo name</XOLTWS:Name>
            <XOLTWS:Address>
               <XOLTWS:AddressLine>3150 Paradise, Rd</XOLTWS:AddressLine>
               <XOLTWS:City>Las Cegas</XOLTWS:City>
               <XOLTWS:PostalCode>89109</XOLTWS:PostalCode>
               <XOLTWS:CountryCode>US</XOLTWS:CountryCode>
            </XOLTWS:Address>
            <XOLTWS:AttentionName>Blah</XOLTWS:AttentionName>
            <XOLTWS:Phone>
               <XOLTWS:Number>+22648484858</XOLTWS:Number>
               <XOLTWS:Extension>555</XOLTWS:Extension>
            </XOLTWS:Phone>
         </XOLTWS:ShipTo>
         <XOLTWS:PaymentInformation>
            <XOLTWS:Payer>
               <XOLTWS:Name>Payer Name</XOLTWS:Name>
               <XOLTWS:Address>
                  <XOLTWS:AddressLine>AddressLine</XOLTWS:AddressLine>
                  <XOLTWS:City>City</XOLTWS:City>
                  <XOLTWS:StateProvinceCode>QC</XOLTWS:StateProvinceCode>
                  <XOLTWS:PostalCode>H8Z2Z3</XOLTWS:PostalCode>
                  <XOLTWS:CountryCode>CA</XOLTWS:CountryCode>
               </XOLTWS:Address>
               <XOLTWS:ShipperNumber>002R48</XOLTWS:ShipperNumber>
               <XOLTWS:AccountType>AccountType</XOLTWS:AccountType>
               <XOLTWS:AttentionName>AttentionName</XOLTWS:AttentionName>
               <XOLTWS:Phone>
                  <XOLTWS:Number>Phone number</XOLTWS:Number>
                  <XOLTWS:Extension>Extension number</XOLTWS:Extension>
               </XOLTWS:Phone>
               <XOLTWS:EMailAddress>EMailAddress</XOLTWS:EMailAddress>
            </XOLTWS:Payer>
            <XOLTWS:ShipmentBillingOption>
               <XOLTWS:Code>10</XOLTWS:Code>
            </XOLTWS:ShipmentBillingOption>
         </XOLTWS:PaymentInformation>
         <XOLTWS:Service>
            <XOLTWS:Code>309</XOLTWS:Code>
            <XOLTWS:Description>UPS Ground Freight</XOLTWS:Description>
         </XOLTWS:Service>
         <XOLTWS:HandlingUnitOne>
            <XOLTWS:Quantity>1</XOLTWS:Quantity>
            <XOLTWS:Type>
               <XOLTWS:Code>SKD</XOLTWS:Code>
            </XOLTWS:Type>
         </XOLTWS:HandlingUnitOne>
         <XOLTWS:Commodity>
            <XOLTWS:Description>Commodity description</XOLTWS:Description>
            <XOLTWS:Weight>
               <XOLTWS:UnitOfMeasurement>
                  <XOLTWS:Code>LBS</XOLTWS:Code>
               </XOLTWS:UnitOfMeasurement>
               <XOLTWS:Value>1.5</XOLTWS:Value>
            </XOLTWS:Weight>
            <XOLTWS:Dimensions>
               <XOLTWS:UnitOfMeasurement>
                  <XOLTWS:Code>IN</XOLTWS:Code>
               </XOLTWS:UnitOfMeasurement>
               <XOLTWS:Width>1.5</XOLTWS:Width>
               <XOLTWS:Height>1.5</XOLTWS:Height>
               <XOLTWS:Length>1.5</XOLTWS:Length>
            </XOLTWS:Dimensions>
            <XOLTWS:NumberOfPieces>1</XOLTWS:NumberOfPieces>
            <XOLTWS:PackagingType>
               <XOLTWS:Code>BAG</XOLTWS:Code>
               <XOLTWS:Description>BAG</XOLTWS:Description>
            </XOLTWS:PackagingType>
            <XOLTWS:FreightClass>50</XOLTWS:FreightClass>
         </XOLTWS:Commodity>
         <XOLTWS:ShipmentServiceOption>
            <XOLTWS:WeekendPickupIndicator />
         </XOLTWS:ShipmentServiceOption>
         <XOLTWS:DensityEligibleIndicator />
         <XOLTWS:AdjustedWeightIndicator />
         <XOLTWS:HandlingUnitWeight>
            <XOLTWS:Value>1</XOLTWS:Value>
            <XOLTWS:UnitOfMeasurement>
               <XOLTWS:Code>LB</XOLTWS:Code>
            </XOLTWS:UnitOfMeasurement>
         </XOLTWS:HandlingUnitWeight>
         <XOLTWS:PickupRequest> 
        	<XOLTWS:PickupDate>20180721</XOLTWS:PickupDate> 
    	 </XOLTWS:PickupRequest>
         <XOLTWS:TimeInTransitIndicator />
         <XOLTWS:GFPOptions>
            <XOLTWS:OnCallInformation>
               <XOLTWS:OnCallPickupIndicator />
            </XOLTWS:OnCallInformation>
         </XOLTWS:GFPOptions>
      </XOLTWS:FreightRateRequest>
   </env:Body>
</env:Envelope>
"""

QuoteResponseXml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header/>
    <soapenv:Body>
        <freightRate:FreightRateResponse xmlns:freightRate="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0">
            <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                <common:ResponseStatus>
                    <common:Code>1</common:Code>
                    <common:Description>Success</common:Description>
                </common:ResponseStatus>
                <common:Alert>
                    <common:Code>9369054</common:Code>
                    <common:Description>User is not registered with UPS Ground Freight.</common:Description>
                </common:Alert>
                <common:Alert>
                    <common:Code>9369055</common:Code>
                    <common:Description>User is not eligible for contract rates.</common:Description>
                </common:Alert>
                <common:TransactionReference>
                    <common:TransactionIdentifier>ciewgst217pclkyNcmvNq6</common:TransactionIdentifier>
                </common:TransactionReference>
            </common:Response>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>DSCNT</freightRate:Code>
                    <freightRate:Description>DSCNT</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>776.36</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>USD</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>DSCNT_RATE</freightRate:Code>
                    <freightRate:Description>DSCNT_RATE</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>70.00</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>%</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>2</freightRate:Code>
                    <freightRate:Description>2</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>66.54</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>USD</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>CA_BORDER</freightRate:Code>
                    <freightRate:Description>CA_BORDER</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>30.00</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>USD</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>LND_GROSS</freightRate:Code>
                    <freightRate:Description>LND_GROSS</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>1109.08</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>USD</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>AFTR_DSCNT</freightRate:Code>
                    <freightRate:Description>AFTR_DSCNT</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>332.72</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>USD</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Commodity>
                <freightRate:Description>Commodity description</freightRate:Description>
                <freightRate:Weight>
                    <freightRate:Value>1.5</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>LBS</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Weight>
                <freightRate:AdjustedWeight>
                    <freightRate:Value>1.5</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>LBS</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:AdjustedWeight>
            </freightRate:Commodity>
            <freightRate:TotalShipmentCharge>
                <freightRate:CurrencyCode>USD</freightRate:CurrencyCode>
                <freightRate:MonetaryValue>429.26</freightRate:MonetaryValue>
            </freightRate:TotalShipmentCharge>
            <freightRate:BillableShipmentWeight>
                <freightRate:Value>1</freightRate:Value>
                <freightRate:UnitOfMeasurement>
                    <freightRate:Code>LBS</freightRate:Code>
                </freightRate:UnitOfMeasurement>
            </freightRate:BillableShipmentWeight>
            <freightRate:DimensionalWeight>
                <freightRate:Value>0</freightRate:Value>
                <freightRate:UnitOfMeasurement>
                    <freightRate:Code>LBS</freightRate:Code>
                </freightRate:UnitOfMeasurement>
            </freightRate:DimensionalWeight>
            <freightRate:Service>
                <freightRate:Code>309</freightRate:Code>
            </freightRate:Service>
            <freightRate:GuaranteedIndicator/>
            <freightRate:MinimumChargeAppliedIndicator/>
            <freightRate:RatingSchedule>
                <freightRate:Code>02</freightRate:Code>
                <freightRate:Description>Published Rates</freightRate:Description>
            </freightRate:RatingSchedule>
            <freightRate:TimeInTransit>
                <freightRate:DaysInTransit>5</freightRate:DaysInTransit>
            </freightRate:TimeInTransit>
        </freightRate:FreightRateResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""