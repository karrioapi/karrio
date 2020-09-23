import re
import unittest
import logging
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import RateRequest
from purplship.api import Rating
from tests.fedex_express.fixture import gateway

logger = logging.getLogger(__name__)


class TestFeDexQuote(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RateRequestPayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        # Remove timeStamp for testing
        serialized_request = re.sub(
            "<v26:ShipTimestamp>[^>]+</v26:ShipTimestamp>", "", request.serialize()
        )
        self.assertEqual(serialized_request, RateRequestXml)

    def test_create_rate_request_with_preset_package(self):
        request = gateway.mapper.create_rate_request(
            RateRequest(**RateWithPresetPayload)
        )
        # Remove timeStamp for testing
        serialized_request = re.sub(
            "<v26:ShipTimestamp>[^>]+</v26:ShipTimestamp>", "", request.serialize()
        )

        self.assertEqual(serialized_request, RateRequestUsingPackagePresetXML)

    @patch("purplship.api.mappers.fedex_express.proxy.http", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/rate")

    def test_parse_rate_response(self):
        with patch("purplship.api.mappers.fedex_express.proxy.http") as mock:
            mock.return_value = RateResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(to_dict(parsed_response), to_dict(ParsedRateResponse))

    def test_parse_rate_error_response(self):
        with patch("purplship.api.mappers.fedex_express.proxy.http") as mock:
            mock.return_value = RateErrorResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(to_dict(parsed_response), to_dict(ParsedRateErrorResponse))


if __name__ == "__main__":
    unittest.main()

RateRequestPayload = {
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "parcels": [{"id": "1", "height": 3, "length": 10, "width": 3, "weight": 4.0}],
    "options": {"currency": "USD"},
}

RateWithPresetPayload = {
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "parcels": [{"id": "1", "package_preset": "fedex_pak"}],
    "options": {"currency": "USD"},
}

ParsedRateResponse = [
    [
        {
            "base_charge": 230.49,
            "carrier_name": "fedex_express",
            "carrier_id": "carrier_id",
            "currency": "USD",
            "discount": 0.0,
            "duties_and_taxes": 0.0,
            "extra_charges": [{"amount": 9.22, "currency": "USD", "name": "Fuel"}],
            "service": "international_priority",
            "total_charge": 239.71,
        },
        {
            "base_charge": 207.47,
            "carrier_name": "fedex_express",
            "carrier_id": "carrier_id",
            "currency": "USD",
            "discount": 0.0,
            "duties_and_taxes": 0.0,
            "extra_charges": [{"amount": 8.3, "currency": "USD", "name": "Fuel"}],
            "service": "international_economy",
            "total_charge": 215.77,
        },
    ],
    [],
]

ParsedRateErrorResponse = [
    [],
    [
        {
            "carrier_name": "fedex_express",
            "carrier_id": "carrier_id",
            "code": "873",
            "message": "All specified account numbers must match.  ",
        }
    ],
]

RateErrorResponseXml = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header/>
    <SOAP-ENV:Body>
        <RateReply xmlns="http://fedex.com/ws/rate/v22">
            <HighestSeverity>ERROR</HighestSeverity>
            <Notifications>
                <Severity>ERROR</Severity>
                <Source>crs</Source>
                <Code>873</Code>
                <Message>All specified account numbers must match.  </Message>
                <LocalizedMessage>All specified account numbers must match.  </LocalizedMessage>
            </Notifications>
            <TransactionDetail>
                <CustomerTransactionId>TC023_US_PRIORITY_OVERNIGHT with Your Packaging</CustomerTransactionId>
            </TransactionDetail>
            <Version>
                <ServiceId>crs</ServiceId>
                <Major>22</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
        </RateReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

RateRequestXml = f"""<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:v26="http://fedex.com/ws/rate/v26">
    <tns:Body>
        <v26:RateRequest>
            <v26:WebAuthenticationDetail>
                <v26:UserCredential>
                    <v26:Key>user_key</v26:Key>
                    <v26:Password>password</v26:Password>
                </v26:UserCredential>
            </v26:WebAuthenticationDetail>
            <v26:ClientDetail>
                <v26:AccountNumber>2349857</v26:AccountNumber>
                <v26:MeterNumber>1293587</v26:MeterNumber>
            </v26:ClientDetail>
            <v26:TransactionDetail>
                <v26:CustomerTransactionId>FTC</v26:CustomerTransactionId>
            </v26:TransactionDetail>
            <v26:Version>
                <v26:ServiceId>crs</v26:ServiceId>
                <v26:Major>26</v26:Major>
                <v26:Intermediate>0</v26:Intermediate>
                <v26:Minor>0</v26:Minor>
            </v26:Version>
            <v26:ReturnTransitAndCommit>true</v26:ReturnTransitAndCommit>
            <v26:RequestedShipment>
                
                <v26:DropoffType>REGULAR_PICKUP</v26:DropoffType>
                <v26:PackagingType>YOUR_PACKAGING</v26:PackagingType>
                <v26:TotalWeight>
                    <v26:Units>LB</v26:Units>
                    <v26:Value>4.</v26:Value>
                </v26:TotalWeight>
                <v26:PreferredCurrency>USD</v26:PreferredCurrency>
                <v26:Shipper>
                    <v26:AccountNumber>2349857</v26:AccountNumber>
                    <v26:Address>
                        <v26:PostalCode>H3N1S4</v26:PostalCode>
                        <v26:CountryCode>CA</v26:CountryCode>
                    </v26:Address>
                </v26:Shipper>
                <v26:Recipient>
                    <v26:Address>
                        <v26:City>Lome</v26:City>
                        <v26:CountryCode>TG</v26:CountryCode>
                    </v26:Address>
                </v26:Recipient>
                <v26:RateRequestTypes>LIST</v26:RateRequestTypes>
                <v26:RateRequestTypes>PREFERRED</v26:RateRequestTypes>
                <v26:PackageCount>1</v26:PackageCount>
                <v26:RequestedPackageLineItems>
                    <v26:SequenceNumber>1</v26:SequenceNumber>
                    <v26:GroupPackageCount>1</v26:GroupPackageCount>
                    <v26:Weight>
                        <v26:Units>LB</v26:Units>
                        <v26:Value>4.</v26:Value>
                    </v26:Weight>
                    <v26:Dimensions>
                        <v26:Length>10</v26:Length>
                        <v26:Width>3</v26:Width>
                        <v26:Height>3</v26:Height>
                        <v26:Units>IN</v26:Units>
                    </v26:Dimensions>
                </v26:RequestedPackageLineItems>
            </v26:RequestedShipment>
        </v26:RateRequest>
    </tns:Body>
</tns:Envelope>
"""

RateRequestUsingPackagePresetXML = f"""<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:v26="http://fedex.com/ws/rate/v26">
    <tns:Body>
        <v26:RateRequest>
            <v26:WebAuthenticationDetail>
                <v26:UserCredential>
                    <v26:Key>user_key</v26:Key>
                    <v26:Password>password</v26:Password>
                </v26:UserCredential>
            </v26:WebAuthenticationDetail>
            <v26:ClientDetail>
                <v26:AccountNumber>2349857</v26:AccountNumber>
                <v26:MeterNumber>1293587</v26:MeterNumber>
            </v26:ClientDetail>
            <v26:TransactionDetail>
                <v26:CustomerTransactionId>FTC</v26:CustomerTransactionId>
            </v26:TransactionDetail>
            <v26:Version>
                <v26:ServiceId>crs</v26:ServiceId>
                <v26:Major>26</v26:Major>
                <v26:Intermediate>0</v26:Intermediate>
                <v26:Minor>0</v26:Minor>
            </v26:Version>
            <v26:ReturnTransitAndCommit>true</v26:ReturnTransitAndCommit>
            <v26:RequestedShipment>
                
                <v26:DropoffType>REGULAR_PICKUP</v26:DropoffType>
                <v26:PackagingType>FEDEX_PAK</v26:PackagingType>
                <v26:TotalWeight>
                    <v26:Units>LB</v26:Units>
                    <v26:Value>2.2</v26:Value>
                </v26:TotalWeight>
                <v26:PreferredCurrency>USD</v26:PreferredCurrency>
                <v26:Shipper>
                    <v26:AccountNumber>2349857</v26:AccountNumber>
                    <v26:Address>
                        <v26:PostalCode>H3N1S4</v26:PostalCode>
                        <v26:CountryCode>CA</v26:CountryCode>
                    </v26:Address>
                </v26:Shipper>
                <v26:Recipient>
                    <v26:Address>
                        <v26:City>Lome</v26:City>
                        <v26:CountryCode>TG</v26:CountryCode>
                    </v26:Address>
                </v26:Recipient>
                <v26:RateRequestTypes>LIST</v26:RateRequestTypes>
                <v26:RateRequestTypes>PREFERRED</v26:RateRequestTypes>
                <v26:PackageCount>1</v26:PackageCount>
                <v26:RequestedPackageLineItems>
                    <v26:SequenceNumber>1</v26:SequenceNumber>
                    <v26:GroupPackageCount>1</v26:GroupPackageCount>
                    <v26:Weight>
                        <v26:Units>LB</v26:Units>
                        <v26:Value>2.2</v26:Value>
                    </v26:Weight>
                    <v26:Dimensions>
                        <v26:Width>11</v26:Width>
                        <v26:Height>14</v26:Height>
                        <v26:Units>IN</v26:Units>
                    </v26:Dimensions>
                </v26:RequestedPackageLineItems>
            </v26:RequestedShipment>
        </v26:RateRequest>
    </tns:Body>
</tns:Envelope>
"""

RateResponseXml = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header/>
    <SOAP-ENV:Body>
        <RateReply xmlns="http://fedex.com/ws/rate/v22">
            <HighestSeverity>NOTE</HighestSeverity>
            <Notifications>
                <Severity>NOTE</Severity>
                <Source>crs</Source>
                <Code>825</Code>
                <Message>The routing code was derived from the city for the destination. </Message>
                <LocalizedMessage>The routing code was derived from the city for the destination. </LocalizedMessage>
                <MessageParameters>
                    <Id>ORIGIN_OR_DESTINATION</Id>
                    <Value>destination</Value>
                </MessageParameters>
            </Notifications>
            <TransactionDetail>
                <CustomerTransactionId>FTC</CustomerTransactionId>
            </TransactionDetail>
            <Version>
                <ServiceId>crs</ServiceId>
                <Major>22</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <RateReplyDetails>
                <ServiceType>INTERNATIONAL_PRIORITY</ServiceType>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <DestinationAirportId>BRU</DestinationAirportId>
                <IneligibleForMoneyBackGuarantee>false</IneligibleForMoneyBackGuarantee>
                <OriginServiceArea>AM</OriginServiceArea>
                <DestinationServiceArea>PM</DestinationServiceArea>
                <SignatureOption>SERVICE_DEFAULT</SignatureOption>
                <ActualRateType>PAYOR_ACCOUNT_SHIPMENT</ActualRateType>
                <RatedShipmentDetails>
                    <EffectiveNetDiscount>
                        <Currency>USD</Currency>
                        <Amount>0.0</Amount>
                    </EffectiveNetDiscount>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_ACCOUNT_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>CA003O</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>ACTUAL</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>USD</IntoCurrency>
                            <Rate>0.83</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>139</DimDivisor>
                        <DimDivisorType>COUNTRY</DimDivisorType>
                        <FuelSurchargePercent>4.0</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>LB</Units>
                            <Value>4.0</Value>
                        </TotalBillingWeight>
                        <TotalBaseCharge>
                            <Currency>USD</Currency>
                            <Amount>230.49</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>USD</Currency>
                            <Amount>230.49</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>USD</Currency>
                            <Amount>9.22</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>USD</Currency>
                            <Amount>239.71</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>USD</Currency>
                            <Amount>239.71</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>239.71</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>USD</Currency>
                                <Amount>9.22</Amount>
                            </Amount>
                        </Surcharges>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
                <RatedShipmentDetails>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_LIST_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>CA003O</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>ACTUAL</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>USD</IntoCurrency>
                            <Rate>0.83</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>139</DimDivisor>
                        <DimDivisorType>COUNTRY</DimDivisorType>
                        <FuelSurchargePercent>4.0</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>LB</Units>
                            <Value>4.0</Value>
                        </TotalBillingWeight>
                        <TotalBaseCharge>
                            <Currency>USD</Currency>
                            <Amount>230.49</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>USD</Currency>
                            <Amount>230.49</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>USD</Currency>
                            <Amount>9.22</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>USD</Currency>
                            <Amount>239.71</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>USD</Currency>
                            <Amount>239.71</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>239.71</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>USD</Currency>
                                <Amount>9.22</Amount>
                            </Amount>
                        </Surcharges>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
            </RateReplyDetails>
            <RateReplyDetails>
                <ServiceType>INTERNATIONAL_ECONOMY</ServiceType>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <DestinationAirportId>BRU</DestinationAirportId>
                <IneligibleForMoneyBackGuarantee>false</IneligibleForMoneyBackGuarantee>
                <OriginServiceArea>AM</OriginServiceArea>
                <DestinationServiceArea>PM</DestinationServiceArea>
                <SignatureOption>SERVICE_DEFAULT</SignatureOption>
                <ActualRateType>PAYOR_ACCOUNT_SHIPMENT</ActualRateType>
                <RatedShipmentDetails>
                    <EffectiveNetDiscount>
                        <Currency>USD</Currency>
                        <Amount>0.0</Amount>
                    </EffectiveNetDiscount>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_ACCOUNT_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>CA003O</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>ACTUAL</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>USD</IntoCurrency>
                            <Rate>0.83</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>139</DimDivisor>
                        <DimDivisorType>COUNTRY</DimDivisorType>
                        <FuelSurchargePercent>4.0</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>LB</Units>
                            <Value>4.0</Value>
                        </TotalBillingWeight>
                        <TotalBaseCharge>
                            <Currency>USD</Currency>
                            <Amount>207.47</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>USD</Currency>
                            <Amount>207.47</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>USD</Currency>
                            <Amount>8.3</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>USD</Currency>
                            <Amount>215.77</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>USD</Currency>
                            <Amount>215.77</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>215.77</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>USD</Currency>
                                <Amount>8.3</Amount>
                            </Amount>
                        </Surcharges>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
                <RatedShipmentDetails>
                    <ShipmentRateDetail>
                        <RateType>PAYOR_LIST_SHIPMENT</RateType>
                        <RateScale>0000000</RateScale>
                        <RateZone>CA003O</RateZone>
                        <PricingCode>ACTUAL</PricingCode>
                        <RatedWeightMethod>ACTUAL</RatedWeightMethod>
                        <CurrencyExchangeRate>
                            <FromCurrency>CAD</FromCurrency>
                            <IntoCurrency>USD</IntoCurrency>
                            <Rate>0.83</Rate>
                        </CurrencyExchangeRate>
                        <DimDivisor>139</DimDivisor>
                        <DimDivisorType>COUNTRY</DimDivisorType>
                        <FuelSurchargePercent>4.0</FuelSurchargePercent>
                        <TotalBillingWeight>
                            <Units>LB</Units>
                            <Value>4.0</Value>
                        </TotalBillingWeight>
                        <TotalBaseCharge>
                            <Currency>USD</Currency>
                            <Amount>207.47</Amount>
                        </TotalBaseCharge>
                        <TotalFreightDiscounts>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalFreightDiscounts>
                        <TotalNetFreight>
                            <Currency>USD</Currency>
                            <Amount>207.47</Amount>
                        </TotalNetFreight>
                        <TotalSurcharges>
                            <Currency>USD</Currency>
                            <Amount>8.3</Amount>
                        </TotalSurcharges>
                        <TotalNetFedExCharge>
                            <Currency>USD</Currency>
                            <Amount>215.77</Amount>
                        </TotalNetFedExCharge>
                        <TotalTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalTaxes>
                        <TotalNetCharge>
                            <Currency>USD</Currency>
                            <Amount>215.77</Amount>
                        </TotalNetCharge>
                        <TotalRebates>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalRebates>
                        <TotalDutiesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesAndTaxes>
                        <TotalAncillaryFeesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalAncillaryFeesAndTaxes>
                        <TotalDutiesTaxesAndFees>
                            <Currency>USD</Currency>
                            <Amount>0.0</Amount>
                        </TotalDutiesTaxesAndFees>
                        <TotalNetChargeWithDutiesAndTaxes>
                            <Currency>USD</Currency>
                            <Amount>215.77</Amount>
                        </TotalNetChargeWithDutiesAndTaxes>
                        <Surcharges>
                            <SurchargeType>FUEL</SurchargeType>
                            <Description>Fuel</Description>
                            <Amount>
                                <Currency>USD</Currency>
                                <Amount>8.3</Amount>
                            </Amount>
                        </Surcharges>
                    </ShipmentRateDetail>
                </RatedShipmentDetails>
            </RateReplyDetails>
        </RateReply>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""
