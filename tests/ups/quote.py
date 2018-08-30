import unittest
from unittest.mock import patch
from gds_helpers import to_xml, jsonify, export
from openship.domain.entities import Quote
from tests.ups.fixture import proxy
from tests.utils import strip
import time


class TestUPSQuote(unittest.TestCase):

    @patch("openship.mappers.ups.ups_proxy.http", return_value='<a></a>')
    def test_create_quote_request(self, http_mock):
        shipper = {
            "postal_code":"H3N1S4", "country_code":"CA", "city":"Montreal", "address_lines": ["Rue Fake"]
        }
        recipient = {"postal_code":"89109", "city":"Las Vegas", "country_code":"US"}
        shipment = {"packages": [{"id":"1", "height":3, "length":10, "width":3,"weight":4.0, "description":"TV"}]}
        payload = Quote.create(shipper=shipper, recipient=recipient, shipment=shipment)
        quote_req_xml_obj = proxy.mapper.create_quote_request(payload)

        proxy.get_quotes(quote_req_xml_obj)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        
        self.assertEqual(strip(xmlStr), strip(QuoteRequestXml % time.strftime('%Y%m%d')))

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
    [], 
    [
        {
            'carrier': 'UPS', 
            'code': '9380216', 
            'message': 'Missing or Invalid Handling Unit One Quantity'
        }, 
        {
            'carrier': 'UPS', 
            'code': '9360541', 
            'message': 'Missing or Invalid Pickup Date.'
        }
    ]
]

ParsedQuoteMissingArgsError = [
    [], 
    [
        {
            'carrier': 'UPS', 
            'code': '250002', 
            'message': 'Invalid Authentication Information.'
        }
    ]
]

ParsedQuoteResponse = [
    [
        {
            'base_charge': 909.26, 
            'carrier': 'UPS', 
            'delivery_date': None, 
            'delivery_time': None, 
            'discount': 776.36, 
            'duties_and_taxes': 576.54, 
            'extra_charges': [
                {
                    'name': 'DSCNT', 
                    'amount': 776.36,
                    'currency': None
                }, 
                {
                    'name': 'HOL_WE_PU_DEL', 
                    'amount': 480.0,
                    'currency': None
                }, 
                {
                    'name': '2', 
                    'amount': 66.54,
                    'currency': None
                }, 
                {
                    'name': 'CA_BORDER', 
                    'amount': 30.0,
                    'currency': None
                }
            ], 
            'pickup_date': None, 
            'pickup_time': None, 
            'service_name': None, 
            'service_type': '309', 
            'total_charge': 332.72
        }
    ],
    []
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

QuoteRequestXml = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:frt="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0">
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
        <frt:FreightRateRequest>
            <common:Request>
                <common:RequestOption>1</common:RequestOption>
                <common:TransactionReference>
                    <common:TransactionIdentifier>TransactionIdentifier</common:TransactionIdentifier>
                </common:TransactionReference>
            </common:Request>
            <frt:ShipFrom>
                <frt:Address>
                    <frt:AddressLine>Rue Fake</frt:AddressLine>
                    <frt:City>Montreal</frt:City>
                    <frt:PostalCode>H3N1S4</frt:PostalCode>
                    <frt:CountryCode>CA</frt:CountryCode>
                </frt:Address>
            </frt:ShipFrom>
            <frt:ShipTo>
                <frt:Address>
                    <frt:City>Las Vegas</frt:City>
                    <frt:PostalCode>89109</frt:PostalCode>
                    <frt:CountryCode>US</frt:CountryCode>
                </frt:Address>
            </frt:ShipTo>
            <frt:PaymentInformation>
                <frt:Payer>
                    <frt:Name>CA</frt:Name>
                    <frt:Address>
                        <frt:AddressLine>Rue Fake</frt:AddressLine>
                        <frt:City>Montreal</frt:City>
                        <frt:PostalCode>H3N1S4</frt:PostalCode>
                        <frt:CountryCode>CA</frt:CountryCode>
                    </frt:Address>
                    <frt:ShipperNumber>56GJE</frt:ShipperNumber>
                </frt:Payer>
                <frt:ShipmentBillingOption>
                    <frt:Code>10</frt:Code>
                </frt:ShipmentBillingOption>
            </frt:PaymentInformation>
            <frt:Service>
                <frt:Code>309</frt:Code>
                <frt:Description>UPS Ground Freight</frt:Description>
            </frt:Service>
            <frt:HandlingUnitOne>
                <frt:Quantity>1</frt:Quantity>
                <frt:Type>
                    <frt:Code>SKD</frt:Code>
                </frt:Type>
            </frt:HandlingUnitOne>
            <frt:Commodity>
                <frt:Description>TV</frt:Description>
                <frt:Weight>
                    <frt:Value>4.0</frt:Value>
                    <frt:UnitOfMeasurement>
                        <frt:Code>LBS</frt:Code>
                    </frt:UnitOfMeasurement>
                </frt:Weight>
                <frt:Dimensions>
                    <frt:UnitOfMeasurement>
                        <frt:Code>IN</frt:Code>
                    </frt:UnitOfMeasurement>
                    <frt:Length>10</frt:Length>
                    <frt:Width>3</frt:Width>
                    <frt:Height>3</frt:Height>
                </frt:Dimensions>
                <frt:NumberOfPieces>1</frt:NumberOfPieces>
                <frt:PackagingType>
                    <frt:Code>BAG</frt:Code>
                    <frt:Description>BAG</frt:Description>
                </frt:PackagingType>
                <frt:FreightClass>50</frt:FreightClass>
            </frt:Commodity>
            <frt:ShipmentServiceOptions>
                <frt:PickupOptions>
                    <frt:WeekendPickupIndicator></frt:WeekendPickupIndicator>
                </frt:PickupOptions>
            </frt:ShipmentServiceOptions>
            <frt:PickupRequest>
                <frt:PickupDate>%s</frt:PickupDate>
            </frt:PickupRequest>
            <frt:GFPOptions>
                <frt:OnCallPickupIndicator></frt:OnCallPickupIndicator>
            </frt:GFPOptions>
            <frt:HandlingUnitWeight>
                <frt:Value>1</frt:Value>
                <frt:UnitOfMeasurement>
                    <frt:Code>LB</frt:Code>
                </frt:UnitOfMeasurement>
            </frt:HandlingUnitWeight>
            <frt:AdjustedWeightIndicator></frt:AdjustedWeightIndicator>
            <frt:TimeInTransitIndicator></frt:TimeInTransitIndicator>
            <frt:DensityEligibleIndicator></frt:DensityEligibleIndicator>
        </frt:FreightRateRequest>
    </tns:Body>
</tns:Envelope>
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
                    <common:TransactionIdentifier>ciewgss117q1stRrcn9c3s</common:TransactionIdentifier>
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
                    <freightRate:Code>HOL_WE_PU_DEL</freightRate:Code>
                    <freightRate:Description>HOL_WE_PU_DEL</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>480.00</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>USD</freightRate:Code>
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
                <freightRate:Description>TV</freightRate:Description>
                <freightRate:Weight>
                    <freightRate:Value>4.0</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>LBS</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Weight>
                <freightRate:AdjustedWeight>
                    <freightRate:Value>4.0</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>LBS</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:AdjustedWeight>
            </freightRate:Commodity>
            <freightRate:TotalShipmentCharge>
                <freightRate:CurrencyCode>USD</freightRate:CurrencyCode>
                <freightRate:MonetaryValue>909.26</freightRate:MonetaryValue>
            </freightRate:TotalShipmentCharge>
            <freightRate:BillableShipmentWeight>
                <freightRate:Value>4</freightRate:Value>
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