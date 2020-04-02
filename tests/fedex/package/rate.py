import re
import unittest
from unittest.mock import patch
from pyfedex.rate_service_v26 import RateRequest
from purplship.core.utils.helpers import to_dict
from purplship.core.models import RateRequest
from purplship.package import Rating
from tests.fedex.package.fixture import gateway


class TestFeDexQuote(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RateRequestPayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        # Remove timeStamp for testing
        serialized_request = re.sub(
            "<ShipTimestamp>[^>]+</ShipTimestamp>", "", request.serialize()
        )

        self.assertEqual(serialized_request, RateRequestXml)

    def test_create_rate_request_with_preset_package(self):
        request = gateway.mapper.create_rate_request(
            RateRequest(**RateWithPresetPayload)
        )
        # Remove timeStamp for testing
        serialized_request = re.sub(
            "<ShipTimestamp>[^>]+</ShipTimestamp>", "", request.serialize()
        )

        self.assertEqual(serialized_request, RateRequestUsingPackagePresetXML)

    @patch("purplship.package.mappers.fedex.proxy.http", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, gateway.settings.server_url)

    def test_parse_rate_response(self):
        with patch("purplship.package.mappers.fedex.proxy.http") as mock:
            mock.return_value = RateResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(to_dict(parsed_response), to_dict(ParsedRateResponse))

    def test_parse_rate_error_response(self):
        with patch("purplship.package.mappers.fedex.proxy.http") as mock:
            mock.return_value = RateErrorResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(to_dict(parsed_response), to_dict(ParsedRateErrorResponse))


if __name__ == "__main__":
    unittest.main()

RateRequestPayload = {
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "parcel": {"id": "1", "height": 3, "length": 10, "width": 3, "weight": 4.0},
    "options": {"currency": "USD"},
}

RateWithPresetPayload = {
    "shipper": {"postal_code": "H3N1S4", "country_code": "CA"},
    "recipient": {"city": "Lome", "country_code": "TG"},
    "parcel": {"id": "1", "package_preset": "fedex_pak"},
    "options": {"currency": "USD"},
}

ParsedRateResponse = [
    [
        {
            "base_charge": 230.49,
            "carrier": "fedex",
            "carrier_name": "carrier_name",
            "currency": "USD",
            "discount": 0.0,
            "duties_and_taxes": 0.0,
            "extra_charges": [{"amount": 9.22, "currency": "USD", "name": "Fuel"}],
            "service": "international_priority",
            "total_charge": 239.71,
        },
        {
            "base_charge": 207.47,
            "carrier": "fedex",
            "carrier_name": "carrier_name",
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
            "carrier": "fedex",
            "carrier_name": "carrier_name",
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

RateRequestXml = f"""<tns:Envelope tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://fedex.com/ws/rate/v26">
    <tns:Body>
        <ns:RateRequest>
            <WebAuthenticationDetail>
                <UserCredential>
                    <Key>user_key</Key>
                    <Password>password</Password>
                </UserCredential>
            </WebAuthenticationDetail>
            <ClientDetail>
                <AccountNumber>2349857</AccountNumber>
                <MeterNumber>1293587</MeterNumber>
            </ClientDetail>
            <TransactionDetail>
                <CustomerTransactionId>FTC</CustomerTransactionId>
            </TransactionDetail>
            <Version>
                <ServiceId>crs</ServiceId>
                <Major>26</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <ReturnTransitAndCommit>true</ReturnTransitAndCommit>
            <RequestedShipment>
                
                <DropoffType>REGULAR_PICKUP</DropoffType>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <TotalWeight>
                    <Units>LB</Units>
                    <Value>4.</Value>
                </TotalWeight>
                <PreferredCurrency>USD</PreferredCurrency>
                <Shipper>
                    <AccountNumber>2349857</AccountNumber>
                    <Address>
                        <PostalCode>H3N1S4</PostalCode>
                        <CountryCode>CA</CountryCode>
                    </Address>
                </Shipper>
                <Recipient>
                    <Address>
                        <City>Lome</City>
                        <CountryCode>TG</CountryCode>
                    </Address>
                </Recipient>
                <RateRequestTypes>LIST</RateRequestTypes>
                <RateRequestTypes>PREFERRED</RateRequestTypes>
            </RequestedShipment>
        </ns:RateRequest>
    </tns:Body>
</tns:Envelope>
"""

RateRequestUsingPackagePresetXML = f"""<tns:Envelope tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://fedex.com/ws/rate/v26">
    <tns:Body>
        <ns:RateRequest>
            <WebAuthenticationDetail>
                <UserCredential>
                    <Key>user_key</Key>
                    <Password>password</Password>
                </UserCredential>
            </WebAuthenticationDetail>
            <ClientDetail>
                <AccountNumber>2349857</AccountNumber>
                <MeterNumber>1293587</MeterNumber>
            </ClientDetail>
            <TransactionDetail>
                <CustomerTransactionId>FTC</CustomerTransactionId>
            </TransactionDetail>
            <Version>
                <ServiceId>crs</ServiceId>
                <Major>26</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <ReturnTransitAndCommit>true</ReturnTransitAndCommit>
            <RequestedShipment>
                
                <DropoffType>REGULAR_PICKUP</DropoffType>
                <PackagingType>FEDEX_PAK</PackagingType>
                <TotalWeight>
                    <Units>LB</Units>
                    <Value>2.2</Value>
                </TotalWeight>
                <PreferredCurrency>USD</PreferredCurrency>
                <Shipper>
                    <AccountNumber>2349857</AccountNumber>
                    <Address>
                        <PostalCode>H3N1S4</PostalCode>
                        <CountryCode>CA</CountryCode>
                    </Address>
                </Shipper>
                <Recipient>
                    <Address>
                        <City>Lome</City>
                        <CountryCode>TG</CountryCode>
                    </Address>
                </Recipient>
                <RateRequestTypes>LIST</RateRequestTypes>
                <RateRequestTypes>PREFERRED</RateRequestTypes>
            </RequestedShipment>
        </ns:RateRequest>
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
