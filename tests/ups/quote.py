import unittest
from unittest.mock import patch
from gds_helpers import to_xml, jsonify, export
from pyups.freight_rate import FreightRateRequest
from pyups.package_rate import RateRequest
from purplship.domain.Types import Quote
from tests.ups.fixture import proxy
from tests.utils import strip, get_node_from_xml
import time


class TestUPSQuote(unittest.TestCase):
    def setUp(self):

        self.FreightRateRequest = FreightRateRequest()
        self.FreightRateRequest.build(
            get_node_from_xml(FreightRateRequestXML, "FreightRateRequest")
        )

        self.RateRequest = RateRequest()
        self.RateRequest.build(get_node_from_xml(RateRequestXML, "RateRequest"))

    def test_create_quote_request(self):
        payload = Quote.create(**rate_req_data)
        RateRequest_ = proxy.mapper.create_quote_request(payload)
        self.assertEqual(
            export(RateRequest_),
            export(self.RateRequest).replace("common:Code", "rate:Code"),
        )

    def test_create_freight_quote_request(self):
        shipper = {
            "account_number": "56GJE",
            "postal_code": "H3N1S4",
            "country_code": "CA",
            "city": "Montreal",
            "address_lines": ["Rue Fake"],
        }
        recipient = {"postal_code": "89109", "city": "Las Vegas", "country_code": "US"}
        shipment = {
            "items": [
                {
                    "id": "1",
                    "height": 3,
                    "length": 170,
                    "width": 3,
                    "weight": 4.0,
                    "packaging_type": "Bag",
                    "description": "TV",
                }
            ]
        }
        payload = Quote.create(shipper=shipper, recipient=recipient, shipment=shipment)

        FreightRateRequest_ = proxy.mapper.create_freight_quote_request(payload)
        self.assertEqual(export(FreightRateRequest_), export(self.FreightRateRequest))

    @patch("purplship.mappers.ups.ups_proxy.http", return_value="<a></a>")
    def test_package_get_quotes(self, http_mock):
        proxy.get_quotes(self.RateRequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(RateRequestXML))

    @patch("purplship.mappers.ups.ups_proxy.http", return_value="<a></a>")
    def test_freight_get_quotes(self, http_mock):
        proxy.get_quotes(self.FreightRateRequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(FreightRateRequestXML))

    def test_parse_freight_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(FreightRateResponseXML)
        )
        self.assertEqual(jsonify(parsed_response), jsonify(ParsedFreightRateResponse))

    def test_parse_package_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(to_xml(RateResponseXML))
        self.assertEqual(jsonify(parsed_response), jsonify(ParsedRateResponse))

    def test_parse_quote_error(self):
        parsed_response = proxy.mapper.parse_quote_response(to_xml(QuoteParsingError))
        self.assertEqual(jsonify(parsed_response), jsonify(ParsedQuoteParsingError))

    def test_parse_quote_missing_args_error(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteMissingArgsError)
        )
        self.assertEqual(jsonify(parsed_response), jsonify(ParsedQuoteMissingArgsError))


if __name__ == "__main__":
    unittest.main()


ParsedQuoteParsingError = [
    [],
    [
        {
            "carrier": "UPS",
            "code": "9380216",
            "message": "Missing or Invalid Handling Unit One Quantity",
        },
        {
            "carrier": "UPS",
            "code": "9360541",
            "message": "Missing or Invalid Pickup Date.",
        },
    ],
]

ParsedQuoteMissingArgsError = [
    [],
    [
        {
            "carrier": "UPS",
            "code": "250002",
            "message": "Invalid Authentication Information.",
        }
    ],
]

ParsedFreightRateResponse = [[{'base_charge': 909.26, 'carrier': 'UPS', 'currency': 'USD', 'delivery_date': None, 'discount': 776.36, 'duties_and_taxes': 576.54, 'extra_charges': [{'amount': 776.36, 'currency': 'USD', 'name': 'DSCNT'}, {'amount': 480.0, 'currency': 'USD', 'name': 'HOL_WE_PU_DEL'}, {'amount': 66.54, 'currency': 'USD', 'name': '2'}, {'amount': 30.0, 'currency': 'USD', 'name': 'CA_BORDER'}], 'service_name': None, 'service_type': '309', 'total_charge': 332.72}], []]

ParsedRateResponse = [[{'base_charge': 9.86, 'carrier': 'UPS', 'currency': 'USD', 'delivery_date': 'None', 'discount': None, 'duties_and_taxes': 0.0, 'extra_charges': [{'amount': 0.0, 'currency': 'USD', 'name': None}], 'service_name': '', 'service_type': '03', 'total_charge': 9.86}], []]


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

FreightRateRequestXML = f"""<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:frt="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0">
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
                    <frt:Length>170</frt:Length>
                    <frt:Width>3</frt:Width>
                    <frt:Height>3</frt:Height>
                </frt:Dimensions>
                <frt:NumberOfPieces>1</frt:NumberOfPieces>
                <frt:PackagingType>
                    <frt:Code>BAG</frt:Code>
                </frt:PackagingType>
                <frt:FreightClass>50</frt:FreightClass>
            </frt:Commodity>
            <frt:ShipmentServiceOptions>
                <frt:PickupOptions>
                    <frt:WeekendPickupIndicator></frt:WeekendPickupIndicator>
                </frt:PickupOptions>
            </frt:ShipmentServiceOptions>
            <frt:GFPOptions/>
            <frt:HandlingUnitWeight>
                <frt:Value>1</frt:Value>
                <frt:UnitOfMeasurement>
                    <frt:Code>LBS</frt:Code>
                </frt:UnitOfMeasurement>
            </frt:HandlingUnitWeight>
            <frt:AdjustedWeightIndicator></frt:AdjustedWeightIndicator>
            <frt:TimeInTransitIndicator></frt:TimeInTransitIndicator>
            <frt:DensityEligibleIndicator></frt:DensityEligibleIndicator>
        </frt:FreightRateRequest>
    </tns:Body>
</tns:Envelope>
"""

FreightRateResponseXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
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

RateRequestXML = """<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/Rate/v1.1">
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
        <rate:RateRequest>
            <common:Request>
                <common:RequestOption>Rate</common:RequestOption>
                <common:TransactionReference>
                    <common:CustomerContext>Your Customer Context</common:CustomerContext>
                </common:TransactionReference>
            </common:Request>
            <rate:Shipment>
                <rate:Shipper>
                    <rate:Name>Shipper Name</rate:Name>
                    <rate:ShipperNumber>Your Shipper Number</rate:ShipperNumber>
                    <rate:Address>
                        <rate:AddressLine>Address Line</rate:AddressLine>
                        <rate:City>Montreal</rate:City>
                        <rate:PostalCode>H3N1S4</rate:PostalCode>
                        <rate:CountryCode>CountryCode</rate:CountryCode>
                    </rate:Address>
                </rate:Shipper>
                <rate:ShipTo>
                    <rate:Name>Ship To Name</rate:Name>
                    <rate:Address>
                        <rate:AddressLine>Address Line</rate:AddressLine>
                        <rate:City>Las Vegas</rate:City>
                        <rate:StateProvinceCode>StateProvinceCode</rate:StateProvinceCode>
                        <rate:PostalCode>89109</rate:PostalCode>
                        <rate:CountryCode>US</rate:CountryCode>
                    </rate:Address>
                </rate:ShipTo>
                <rate:ShipFrom>
                    <rate:Address>
                        <rate:AddressLine>Address Line</rate:AddressLine>
                        <rate:City>City</rate:City>
                        <rate:StateProvinceCode>StateProvinceCode</rate:StateProvinceCode>
                        <rate:PostalCode>PostalCode</rate:PostalCode>
                        <rate:CountryCode>CountryCode</rate:CountryCode>
                    </rate:Address>
                </rate:ShipFrom>
                <rate:Service>
                    <rate:Code>03</rate:Code>
                </rate:Service>
                <rate:Package>
                    <rate:PackagingType>
                        <rate:Code>02</rate:Code>
                    </rate:PackagingType>
                    <rate:Dimensions>
                        <rate:UnitOfMeasurement>
                            <rate:Code>IN</rate:Code>
                        </rate:UnitOfMeasurement>
                        <rate:Length>10</rate:Length>
                        <rate:Width>3</rate:Width>
                        <rate:Height>3</rate:Height>
                    </rate:Dimensions>
                    <rate:PackageWeight>
                        <rate:UnitOfMeasurement>
                            <rate:Code>LBS</rate:Code>
                        </rate:UnitOfMeasurement>
                        <rate:Weight>4.0</rate:Weight>
                    </rate:PackageWeight>
                </rate:Package>
                <rate:ShipmentRatingOptions>
                    <rate:NegotiatedRatesIndicator></rate:NegotiatedRatesIndicator>
                </rate:ShipmentRatingOptions>
            </rate:Shipment>
        </rate:RateRequest>
    </tns:Body>
</tns:Envelope>
"""

RateResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Header />
   <soapenv:Body>
      <rate:RateResponse xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/Rate/v1.1">
         <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
            <common:ResponseStatus>
               <common:Code>1</common:Code>
               <common:Description>Success</common:Description>
            </common:ResponseStatus>
            <common:Alert>
               <common:Code>110971</common:Code>
               <common:Description>Your invoice may vary from the displayed reference rates</common:Description>
            </common:Alert>
            <common:TransactionReference>
               <common:CustomerContext>Your Customer Context</common:CustomerContext>
            </common:TransactionReference>
         </common:Response>
         <rate:RatedShipment>
            <rate:Service>
               <rate:Code>03</rate:Code>
               <rate:Description />
            </rate:Service>
            <rate:RatedShipmentAlert>
               <rate:Code>110971</rate:Code>
               <rate:Description>Your invoice may vary from the displayed reference rates</rate:Description>
            </rate:RatedShipmentAlert>
            <rate:BillingWeight>
               <rate:UnitOfMeasurement>
                  <rate:Code>LBS</rate:Code>
                  <rate:Description>Pounds</rate:Description>
               </rate:UnitOfMeasurement>
               <rate:Weight>2.0</rate:Weight>
            </rate:BillingWeight>
            <rate:TransportationCharges>
               <rate:CurrencyCode>USD</rate:CurrencyCode>
               <rate:MonetaryValue>9.86</rate:MonetaryValue>
            </rate:TransportationCharges>
            <rate:ServiceOptionsCharges>
               <rate:CurrencyCode>USD</rate:CurrencyCode>
               <rate:MonetaryValue>0.00</rate:MonetaryValue>
            </rate:ServiceOptionsCharges>
            <rate:TotalCharges>
               <rate:CurrencyCode>USD</rate:CurrencyCode>
               <rate:MonetaryValue>9.86</rate:MonetaryValue>
            </rate:TotalCharges>
            <rate:RatedPackage>
               <rate:TransportationCharges>
                  <rate:CurrencyCode>USD</rate:CurrencyCode>
                  <rate:MonetaryValue>9.86</rate:MonetaryValue>
               </rate:TransportationCharges>
               <rate:ServiceOptionsCharges>
                  <rate:CurrencyCode>USD</rate:CurrencyCode>
                  <rate:MonetaryValue>0.00</rate:MonetaryValue>
               </rate:ServiceOptionsCharges>
               <rate:TotalCharges>
                  <rate:CurrencyCode>USD</rate:CurrencyCode>
                  <rate:MonetaryValue>9.86</rate:MonetaryValue>
               </rate:TotalCharges>
               <rate:Weight>1.0</rate:Weight>
               <rate:BillingWeight>
                  <rate:UnitOfMeasurement>
                     <rate:Code>LBS</rate:Code>
                     <rate:Description>Pounds</rate:Description>
                  </rate:UnitOfMeasurement>
                  <rate:Weight>2.0</rate:Weight>
               </rate:BillingWeight>
            </rate:RatedPackage>
         </rate:RatedShipment>
      </rate:RateResponse>
   </soapenv:Body>
</soapenv:Envelope>
"""


rate_req_data = {
    "shipper": {
        "company_name": "Shipper Name",
        "account_number": "Your Shipper Number",
        "postal_code": "H3N1S4",
        "country_code": "CountryCode",
        "city": "Montreal",
        "address_lines": ["Address Line"],
    },
    "recipient": {
        "company_name": "Ship To Name",
        "address_lines": ["Address Line"],
        "postal_code": "89109",
        "city": "Las Vegas",
        "country_code": "US",
        "state_code": "StateProvinceCode",
    },
    "shipment": {
        "references": ["Your Customer Context"],
        "services": ["UPS_Ground"],
        "items": [
            {
                "id": "1",
                "height": 3,
                "length": 10,
                "width": 3,
                "weight": 4.0,
                "packaging_type": "Package",
                "description": "TV",
            }
        ],
        "extra": {
            "ShipFrom": {
                "address_lines": ["Address Line"],
                "city": "City",
                "state_code": "StateProvinceCode",
                "postal_code": "PostalCode",
                "country_code": "CountryCode",
            }
        },
    },
}
