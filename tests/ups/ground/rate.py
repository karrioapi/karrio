import unittest
from unittest.mock import patch
from purplship.core.utils import DP
from purplship.core.models import RateRequest
from tests.ups.fixture import freight_gateway
from purplship import Rating


class TestUPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_req_data)

    def test_create_rate_request(self):
        request = freight_gateway.mapper.create_rate_request(self.RateRequest)
        import logging; logging.warning(request.serialize())
        self.assertEqual(request.serialize(), RateRequestXML)

    @patch("purplship.mappers.ups_ground.proxy.http", return_value="<a></a>")
    def test_package_get_quotes(self, http_mock):
        Rating.fetch(self.RateRequest).from_(freight_gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{freight_gateway.settings.server_url}/RateFreight")

    # def test_parse_package_quote_response(self):
    #     with patch("purplship.mappers.ups_ground.proxy.http") as mock:
    #         mock.return_value = RateResponseXML
    #         parsed_response = Rating.fetch(self.RateRequest).from_(freight_gateway).parse()
    #         self.assertEqual(
    #             DP.to_dict(parsed_response), DP.to_dict(ParsedRateResponse)
    #         )


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
    "parcels": [
        {
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 4.0,
            "packaging_type": "pallet",
            "description": "TVs",
        }
    ],
    "reference": "Your Customer Context",
    "services": ["ups_standard"],
    "options": {"negotiated_rates_indicator": True},
}


ParsedRateMissingArgsError = [
    [],
    [
        {
            "carrier_name": "ups",
            "carrier_id": "ups",
            "code": "250002",
            "message": "Invalid Authentication Information.",
        }
    ],
]

ParsedRateResponse = [
    [
        {
            "base_charge": 9.86,
            "carrier_name": "ups",
            "carrier_id": "ups",
            "currency": "USD",
            "duties_and_taxes": 0.0,
            "service": "ups_ground",
            "total_charge": 9.86,
            "meta": {"service_name": "ups_ground"},
        }
    ],
    [],
]


RateRequestXML = """<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"
    xmlns:wsf="http://www.ups.com/schema/wsf"
    xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
    <env:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>Username</upss:Username>
                <upss:Password>Password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>AccessLicenseNumber</upss:AccessLicenseNumber>
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
                    <XOLTWS:AddressLine>AddressLine</XOLTWS:AddressLine>
                    <XOLTWS:City>City</XOLTWS:City>
                    <XOLTWS:StateProvinceCode>StateProvinceCode</XOLTWS:StateProvinceCode>
                    <XOLTWS:PostalCode>PostalCode</XOLTWS:PostalCode>
                    <XOLTWS:CountryCode>CountryCode</XOLTWS:CountryCode>
                </XOLTWS:Address>
                <XOLTWS:AttentionName>Contact</XOLTWS:AttentionName>
                <XOLTWS:Phone>
                    <XOLTWS:Number>Phone number</XOLTWS:Number>
                    <XOLTWS:Extension>Extension number</XOLTWS:Extension>
                </XOLTWS:Phone>
                <XOLTWS:EMailAddress>EMailAddress</XOLTWS:EMailAddress>
            </XOLTWS:ShipFrom>
            <XOLTWS:ShipperNumber>ShipperNumber</XOLTWS:ShipperNumber>
            <XOLTWS:ShipTo>
                <XOLTWS:Name>ShipTo name</XOLTWS:Name>
                <XOLTWS:Address>
                    <XOLTWS:AddressLine>AddressLine</XOLTWS:AddressLine>
                    <XOLTWS:City>City</XOLTWS:City>
                    <XOLTWS:StateProvinceCode>StateProvinceCode</XOLTWS:StateProvinceCode>
                    <XOLTWS:PostalCode>PostalCode</XOLTWS:PostalCode>
                    <XOLTWS:CountryCode>CountryCode</XOLTWS:CountryCode>
                </XOLTWS:Address>
                <XOLTWS:AttentionName>AttentionName</XOLTWS:AttentionName>
                <XOLTWS:Phone>
                    <XOLTWS:Number>Phone number</XOLTWS:Number>
                    <XOLTWS:Extension>Extension number</XOLTWS:Extension>
                </XOLTWS:Phone>
            </XOLTWS:ShipTo>
            <XOLTWS:PaymentInformation>
                <XOLTWS:Payer>
                    <XOLTWS:Name>Payer Name</XOLTWS:Name>
                    <XOLTWS:Address>
                        <XOLTWS:AddressLine>AddressLine</XOLTWS:AddressLine>
                        <XOLTWS:City>City</XOLTWS:City>
                        <XOLTWS:StateProvinceCode>StateProvinceCode</XOLTWS:StateProvinceCode>
                        <XOLTWS:PostalCode>PostalCode</XOLTWS:PostalCode>
                        <XOLTWS:CountryCode>CountryCode</XOLTWS:CountryCode>
                    </XOLTWS:Address>
                    <XOLTWS:ShipperNumber>Payer's shipper Number</XOLTWS:ShipperNumber>
                    <XOLTWS:AccountType>AccountType</XOLTWS:AccountType>
                    <XOLTWS:AttentionName>AttentionName</XOLTWS:AttentionName>
                    <XOLTWS:Phone>
                        <XOLTWS:Number>Phone number</XOLTWS:Number>
                        <XOLTWS:Extension>Extension number</XOLTWS:Extension>
                    </XOLTWS:Phone>
                    <XOLTWS:EMailAddress>EMailAddress</XOLTWS:EMailAddress>
                </XOLTWS:Payer>
                <XOLTWS:ShipmentBillingOption>
                    <XOLTWS:Code>ShipmentBillingOption</XOLTWS:Code>
                </XOLTWS:ShipmentBillingOption>
            </XOLTWS:PaymentInformation>
            <XOLTWS:Service>
                <XOLTWS:Code>Service code</XOLTWS:Code>
            </XOLTWS:Service>
            <XOLTWS:HandlingUnitOne>
                <XOLTWS:Quantity>HandlingUnitOne quantity</XOLTWS:Quantity>
                <XOLTWS:Type>
                    <XOLTWS:Code>HandlingUnitOne code</XOLTWS:Code>
                </XOLTWS:Type>
            </XOLTWS:HandlingUnitOne>
            <XOLTWS:Commodity>
                <XOLTWS:Description>Commodity description</XOLTWS:Description>
                <XOLTWS:Weight>
                    <XOLTWS:UnitOfMeasurement>
                        <XOLTWS:Code>UnitOfMeasurement code</XOLTWS:Code>
                    </XOLTWS:UnitOfMeasurement>
                    <XOLTWS:Value>Weight</XOLTWS:Value>
                </XOLTWS:Weight>
                <XOLTWS:NumberOfPieces>NumberOfPieces</XOLTWS:NumberOfPieces>
                <XOLTWS:PackagingType>
                    <XOLTWS:Code>PackagingType code</XOLTWS:Code>
                </XOLTWS:PackagingType>
                <XOLTWS:FreightClass>FreightClass</XOLTWS:FreightClass>
            </XOLTWS:Commodity>
            <XOLTWS:ShipmentServiceOption>
                <XOLTWS:WeekendPickupIndicator/>
            </XOLTWS:ShipmentServiceOption>
            <XOLTWS:DensityEligibleIndicator/>
            <XOLTWS:AdjustedWeightIndicator/>
            <XOLTWS:HandlingUnitWeight>
                <XOLTWS:Value>HandlingUnitWeight</XOLTWS:Value>
                <XOLTWS:UnitOfMeasurement>
                    <XOLTWS:Code>UnitOfMeasurement code</XOLTWS:Code>
                </XOLTWS:UnitOfMeasurement>
            </XOLTWS:HandlingUnitWeight>
            <XOLTWS:AlternateRateOptions>
                <XOLTWS:Code>AlternateRateOptions code</XOLTWS:Code>
            </XOLTWS:AlternateRateOptions>
            <XOLTWS:PickupRequest>
                <XOLTWS:PickupDate>PickupDate</XOLTWS:PickupDate>
            </XOLTWS:PickupRequest>
            <XOLTWS:TimeInTransitIndicator/>
            <XOLTWS:GFPOptions>
                <XOLTWS:OnCallInformation>
                    <XOLTWS:OnCallPickupIndicator/>
                </XOLTWS:OnCallInformation>
            </XOLTWS:GFPOptions>
        </XOLTWS:FreightRateRequest>
    </env:Body>
</env:Envelope>
"""

RateResponseXML = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header/>
    <soapenv:Body>
        <freightRate:FreightRateResponse xmlns:freightRate="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0">
            <common:Response xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0">
                <common:ResponseStatus>
                    <common:Code>1</common:Code>
                    <common:Description>Success</common:Description>
                </common:ResponseStatus>
                <common:Alert>
                    <common:Code>9369055</common:Code>
                    <common:Description>User is not eligible for contract rates.</common:Description>
                </common:Alert>
                <common:TransactionReference>
                    <common:TransactionIdentifier>TransactionIdentifier</common:TransactionIdentifier>
                </common:TransactionReference>
            </common:Response>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>DSCNT</freightRate:Code>
                    <freightRate:Description>DSCNT</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>Value</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>DSCNT_RATE</freightRate:Code>
                    <freightRate:Description>DSCNT_RATE</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>Value</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>2</freightRate:Code>
                    <freightRate:Description>2</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>Value</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>DEFICITRATE</freightRate:Code>
                    <freightRate:Description>DEFICITRATE</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>Value</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>DEFICITWGHT</freightRate:Code>
                    <freightRate:Description>DEFICITWGHT</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>Value</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>DFCT_AMT</freightRate:Code>
                    <freightRate:Description>DFCT_AMT</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>Value</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>LND_GROSS</freightRate:Code>
                    <freightRate:Description>LND_GROSS</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>Value</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:Rate>
                <freightRate:Type>
                    <freightRate:Code>AFTR_DSCNT</freightRate:Code>
                    <freightRate:Description>AFTR_DSCNT</freightRate:Description>
                </freightRate:Type>
                <freightRate:Factor>
                    <freightRate:Value>Value</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Factor>
            </freightRate:Rate>
            <freightRate:FreightDensityRate>
                <freightRate:Density>Density</freightRate:Density>
                <freightRate:TotalCubicFeet>TotalCubicFeet</freightRate:TotalCubicFeet>
            </freightRate:FreightDensityRate>
            <freightRate:Commodity>
                <freightRate:Description>Freight</freightRate:Description>
                <freightRate:Weight>
                    <freightRate:Value>Weight</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:Weight>
                <freightRate:AdjustedWeight>
                    <freightRate:Value>AdjustedWeight</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:AdjustedWeight>
            </freightRate:Commodity>
            <freightRate:TotalShipmentCharge>
                <freightRate:CurrencyCode>CurrencyCode</freightRate:CurrencyCode>
                <freightRate:MonetaryValue>TotalShipmentCharge MonetaryValue</freightRate:MonetaryValue>
            </freightRate:TotalShipmentCharge>
            <freightRate:BillableShipmentWeight>
                <freightRate:Value>BillableShipmentWeight</freightRate:Value>
                <freightRate:UnitOfMeasurement>
                    <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                </freightRate:UnitOfMeasurement>
            </freightRate:BillableShipmentWeight>
            <freightRate:DimensionalWeight>
                <freightRate:Value>DimensionalWeight value</freightRate:Value>
                <freightRate:UnitOfMeasurement>
                    <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                </freightRate:UnitOfMeasurement>
            </freightRate:DimensionalWeight>
            <freightRate:Service>
                <freightRate:Code>Service code</freightRate:Code>
            </freightRate:Service>
            <freightRate:GuaranteedIndicator/>
            <freightRate:AlternateRatesResponse>
                <freightRate:AlternateRateType>
                    <freightRate:Code>AlternateRateType</freightRate:Code>
                    <freightRate:Description>AlternateRateType description</freightRate:Description>
                </freightRate:AlternateRateType>
                <freightRate:Rate>
                    <freightRate:Type>
                        <freightRate:Code>DSCNT</freightRate:Code>
                        <freightRate:Description>DSCNT</freightRate:Description>
                    </freightRate:Type>
                    <freightRate:Factor>
                        <freightRate:Value>Value</freightRate:Value>
                        <freightRate:UnitOfMeasurement>
                            <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                        </freightRate:UnitOfMeasurement>
                    </freightRate:Factor>
                </freightRate:Rate>
                <freightRate:Rate>
                    <freightRate:Type>
                        <freightRate:Code>DSCNT_RATE</freightRate:Code>
                        <freightRate:Description>DSCNT_RATE</freightRate:Description>
                    </freightRate:Type>
                    <freightRate:Factor>
                        <freightRate:Value>Value</freightRate:Value>
                        <freightRate:UnitOfMeasurement>
                            <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                        </freightRate:UnitOfMeasurement>
                    </freightRate:Factor>
                </freightRate:Rate>
                <freightRate:Rate>
                    <freightRate:Type>
                        <freightRate:Code>DEFICITRATE</freightRate:Code>
                        <freightRate:Description>DEFICITRATE</freightRate:Description>
                    </freightRate:Type>
                    <freightRate:Factor>
                        <freightRate:Value>Value</freightRate:Value>
                        <freightRate:UnitOfMeasurement>
                            <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                        </freightRate:UnitOfMeasurement>
                    </freightRate:Factor>
                </freightRate:Rate>
                <freightRate:Rate>
                    <freightRate:Type>
                        <freightRate:Code>DEFICITWGHT</freightRate:Code>
                        <freightRate:Description>DEFICITWGHT</freightRate:Description>
                    </freightRate:Type>
                    <freightRate:Factor>
                        <freightRate:Value>Value</freightRate:Value>
                        <freightRate:UnitOfMeasurement>
                            <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                        </freightRate:UnitOfMeasurement>
                    </freightRate:Factor>
                </freightRate:Rate>
                <freightRate:Rate>
                    <freightRate:Type>
                        <freightRate:Code>DFCT_AMT</freightRate:Code>
                        <freightRate:Description>DFCT_AMT</freightRate:Description>
                    </freightRate:Type>
                    <freightRate:Factor>
                        <freightRate:Value>Value</freightRate:Value>
                        <freightRate:UnitOfMeasurement>
                            <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                        </freightRate:UnitOfMeasurement>
                    </freightRate:Factor>
                </freightRate:Rate>
                <freightRate:Rate>
                    <freightRate:Type>
                        <freightRate:Code>LND_GROSS</freightRate:Code>
                        <freightRate:Description>LND_GROSS</freightRate:Description>
                    </freightRate:Type>
                    <freightRate:Factor>
                        <freightRate:Value>Value</freightRate:Value>
                        <freightRate:UnitOfMeasurement>
                            <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                        </freightRate:UnitOfMeasurement>
                    </freightRate:Factor>
                </freightRate:Rate>
                <freightRate:Rate>
                    <freightRate:Type>
                        <freightRate:Code>AFTR_DSCNT</freightRate:Code>
                        <freightRate:Description>AFTR_DSCNT</freightRate:Description>
                    </freightRate:Type>
                    <freightRate:Factor>
                        <freightRate:Value>Value</freightRate:Value>
                        <freightRate:UnitOfMeasurement>
                            <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                        </freightRate:UnitOfMeasurement>
                    </freightRate:Factor>
                </freightRate:Rate>
                <freightRate:Rate>
                    <freightRate:Type>
                        <freightRate:Code>FRS_ONCALL_PICKUP_CHARGE</freightRate:Code>
                        <freightRate:Description>FRS_ONCALL_PICKUP_CHARGE</freightRate:Description>
                    </freightRate:Type>
                    <freightRate:Factor>
                        <freightRate:Value>Value</freightRate:Value>
                    </freightRate:Factor>
                </freightRate:Rate>
                <freightRate:FreightDensityRate>
                    <freightRate:Density>Density</freightRate:Density>
                    <freightRate:TotalCubicFeet>TotalCubicFeet</freightRate:TotalCubicFeet>
                </freightRate:FreightDensityRate>
                <freightRate:BillableShipmentWeight>
                    <freightRate:Value>BillableShipmentWeight</freightRate:Value>
                    <freightRate:UnitOfMeasurement>
                        <freightRate:Code>UnitOfMeasurement code</freightRate:Code>
                    </freightRate:UnitOfMeasurement>
                </freightRate:BillableShipmentWeight>
                <freightRate:TimeInTransit>
                    <freightRate:DaysInTransit>DaysInTransit</freightRate:DaysInTransit>
                </freightRate:TimeInTransit>
            </freightRate:AlternateRatesResponse>
            <freightRate:TimeInTransit>
                <freightRate:DaysInTransit>DaysInTransit</freightRate:DaysInTransit>
            </freightRate:TimeInTransit>
        </freightRate:FreightRateResponse>
    </soapenv:Body>
</soapenv:Envelope>
"""
