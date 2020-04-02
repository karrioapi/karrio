import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import RateRequest
from tests.ups.package.fixture import gateway
from purplship.package import rating


class TestUPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_req_data)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(request.serialize(), RateRequestXML)

    def test_create_rate_with_package_preset_request(self):
        request = gateway.mapper.create_rate_request(
            RateRequest(**rate_req_with_package_preset_data)
        )
        self.assertEqual(request.serialize(), RateRequestWithPackagePresetXML)

    @patch("purplship.package.mappers.ups.proxy.http", return_value="<a></a>")
    def test_package_get_quotes(self, http_mock):
        rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/Rate")

    def test_parse_package_quote_response(self):
        with patch("purplship.package.mappers.ups.proxy.http") as mock:
            mock.return_value = RateResponseXML
            parsed_response = rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(to_dict(parsed_response), to_dict(ParsedRateResponse))

    def test_parse_rate_error(self):
        with patch("purplship.package.mappers.ups.proxy.http") as mock:
            mock.return_value = RateteParsingErrorXML
            parsed_response = rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(
                to_dict(parsed_response), to_dict(ParsedRateteParsingError)
            )

    def test_parse_rate_missing_args_error(self):
        with patch("purplship.package.mappers.ups.proxy.http") as mock:
            mock.return_value = RateMissingArgsErrorXML
            parsed_response = rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(
                to_dict(parsed_response), to_dict(ParsedRateMissingArgsError)
            )


if __name__ == "__main__":
    unittest.main()


rate_req_data = {
    "shipper": {
        "company_name": "Shipper Name",
        "postal_code": "H3N1S4",
        "country_code": "CountryCode",
        "city": "Montreal",
        "address_line1": "Address Line",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "address_line1": "Address Line",
        "postal_code": "89109",
        "city": "Las Vegas",
        "country_code": "US",
        "state_code": "StateProvinceCode",
    },
    "parcel": {
        "reference": "Your Customer Context",
        "height": 3,
        "length": 10,
        "width": 3,
        "weight": 4.0,
        "packaging_type": "ups_package",
        "description": "TV",
    },
    "services": ["ups_standard"],
    "options": {"negotiated_rates_indicator": True},
}


rate_req_with_package_preset_data = {
    "shipper": {
        "company_name": "Shipper Name",
        "postal_code": "H3N1S4",
        "country_code": "CountryCode",
        "city": "Montreal",
        "address_line1": "Address Line",
    },
    "recipient": {
        "company_name": "Ship To Name",
        "address_line1": "Address Line",
        "postal_code": "89109",
        "city": "Las Vegas",
        "country_code": "US",
        "state_code": "StateProvinceCode",
    },
    "parcel": {
        "reference": "Your Customer Context",
        "package_preset": "ups_express_pak",
        "packaging_type": "ups_package",
        "description": "TV",
    },
    "services": ["ups_standard"],
    "options": {"negotiated_rates_indicator": True},
}


ParsedRateteParsingError = [
    [],
    [
        {
            "carrier": "ups",
            "carrier_name": "UPS",
            "code": "9380216",
            "message": "Missing or Invalid Handling Unit One Quantity",
        },
        {
            "carrier": "ups",
            "carrier_name": "UPS",
            "code": "9360541",
            "message": "Missing or Invalid Pickup Date.",
        },
    ],
]

ParsedRateMissingArgsError = [
    [],
    [
        {
            "carrier": "ups",
            "carrier_name": "UPS",
            "code": "250002",
            "message": "Invalid Authentication Information.",
        }
    ],
]

ParsedRateResponse = [
    [
        {
            "base_charge": 9.86,
            "carrier": "ups",
            "carrier_name": "UPS",
            "currency": "USD",
            "duties_and_taxes": 0.0,
            "extra_charges": [{"amount": 0.0, "currency": "USD", "name": None}],
            "service": "ups_ground",
            "total_charge": 9.86,
        }
    ],
    [],
]


RateteParsingErrorXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
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

RateMissingArgsErrorXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
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

RateRequestXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/Rate/v1.1" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" >
    <tns:Header>
        <upss:UPSSecurity>
            <UsernameToken>
                <Username>username</Username>
                <Password>password</Password>
            </UsernameToken>
            <ServiceAccessToken>
                <AccessLicenseNumber>FG09H9G8H09GH8G0</AccessLicenseNumber>
            </ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <rate:RateRequest>
            <common:Request>
                <RequestOption>Rate</RequestOption>
                <TransactionReference>
                    <CustomerContext>Your Customer Context</CustomerContext>
                </TransactionReference>
            </common:Request>
            <Shipment>
                <Shipper>
                    <Name>Shipper Name</Name>
                    <ShipperNumber>Your Account Number</ShipperNumber>
                    <Address>
                        <AddressLine>Address Line</AddressLine>
                        <City>Montreal</City>
                        <PostalCode>H3N1S4</PostalCode>
                        <CountryCode>CountryCode</CountryCode>
                    </Address>
                </Shipper>
                <ShipTo>
                    <Name>Ship To Name</Name>
                    <Address>
                        <AddressLine>Address Line</AddressLine>
                        <City>Las Vegas</City>
                        <StateProvinceCode>StateProvinceCode</StateProvinceCode>
                        <PostalCode>89109</PostalCode>
                        <CountryCode>US</CountryCode>
                    </Address>
                </ShipTo>
                <Service>
                    <Code>11</Code>
                </Service>
                <Package>
                    <PackagingType>
                        <Code>02</Code>
                    </PackagingType>
                    <Dimensions>
                        <UnitOfMeasurement>
                            <Code>IN</Code>
                        </UnitOfMeasurement>
                        <Length>10.0</Length>
                        <Width>3.0</Width>
                        <Height>3.0</Height>
                    </Dimensions>
                    <PackageWeight>
                        <UnitOfMeasurement>
                            <Code>LBS</Code>
                        </UnitOfMeasurement>
                        <Weight>4.0</Weight>
                    </PackageWeight>
                </Package>
                <ShipmentRatingOptions>
                    <NegotiatedRatesIndicator></NegotiatedRatesIndicator>
                </ShipmentRatingOptions>
            </Shipment>
        </rate:RateRequest>
    </tns:Body>
</tns:Envelope>
"""

RateRequestWithPackagePresetXML = """<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/Rate/v1.1" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" >
    <tns:Header>
        <upss:UPSSecurity>
            <UsernameToken>
                <Username>username</Username>
                <Password>password</Password>
            </UsernameToken>
            <ServiceAccessToken>
                <AccessLicenseNumber>FG09H9G8H09GH8G0</AccessLicenseNumber>
            </ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <rate:RateRequest>
            <common:Request>
                <RequestOption>Rate</RequestOption>
                <TransactionReference>
                    <CustomerContext>Your Customer Context</CustomerContext>
                </TransactionReference>
            </common:Request>
            <Shipment>
                <Shipper>
                    <Name>Shipper Name</Name>
                    <ShipperNumber>Your Account Number</ShipperNumber>
                    <Address>
                        <AddressLine>Address Line</AddressLine>
                        <City>Montreal</City>
                        <PostalCode>H3N1S4</PostalCode>
                        <CountryCode>CountryCode</CountryCode>
                    </Address>
                </Shipper>
                <ShipTo>
                    <Name>Ship To Name</Name>
                    <Address>
                        <AddressLine>Address Line</AddressLine>
                        <City>Las Vegas</City>
                        <StateProvinceCode>StateProvinceCode</StateProvinceCode>
                        <PostalCode>89109</PostalCode>
                        <CountryCode>US</CountryCode>
                    </Address>
                </ShipTo>
                <Service>
                    <Code>11</Code>
                </Service>
                <Package>
                    <PackagingType>
                        <Code>02</Code>
                    </PackagingType>
                    <Dimensions>
                        <UnitOfMeasurement>
                            <Code>IN</Code>
                        </UnitOfMeasurement>
                        <Width>16.0</Width>
                        <Height>11.75</Height>
                    </Dimensions>
                </Package>
                <ShipmentRatingOptions>
                    <NegotiatedRatesIndicator></NegotiatedRatesIndicator>
                </ShipmentRatingOptions>
            </Shipment>
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
