import unittest
from unittest.mock import patch
from pyfedex.rate_v22 import RateRequest
from gds_helpers import to_xml, to_dict, export
from purplship.domain import Types as T
from tests.fedex.fixture import proxy
from tests.utils import strip, get_node_from_xml


class TestFeDexQuote(unittest.TestCase):
    def setUp(self):
        req_xml = get_node_from_xml(QuoteRequestXml, "RateRequest")
        self.RateRequest = RateRequest()
        self.RateRequest.build(req_xml)

    def test_create_quote_request(self):
        shipper = {
            "postal_code": "H3N1S4",
            "country_code": "CA",
            "account_number": "2349857",
        }
        recipient = {"city": "Lome", "country_code": "TG"}
        shipment = {
            "currency": "USD",
            "payment_account_number": "2349857",
            "items": [
                {"id": "1", "height": 3, "length": 10, "width": 3, "weight": 4.0}
            ],
        }
        payload = T.RateRequest(shipper=shipper, recipient=recipient, shipment=shipment)

        RateRequest_ = proxy.mapper.create_quote_request(payload)
        # Remove timeStamp for testing
        RateRequest_.RequestedShipment.ShipTimestamp = None
        self.assertEqual(export(RateRequest_), export(self.RateRequest))

    @patch("purplship.mappers.fedex.fedex_proxy.http", return_value="<a></a>")
    def test_get_quotes(self, http_mock):
        proxy.get_quotes(self.RateRequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(QuoteRequestXml))

    def test_parse_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(to_xml(QuoteResponseXml))

        self.assertEqual(to_dict(parsed_response), to_dict(ParsedQuoteResponse))

    def test_parse_quote_error_response(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteErrorResponseXml)
        )

        self.assertEqual(to_dict(parsed_response), to_dict(ParsedQuoteErrorResponse))


if __name__ == "__main__":
    unittest.main()

ParsedQuoteResponse = [
    [
        {
            "base_charge": 230.49,
            "carrier": "carrier_name",
            "currency": "USD",
            "delivery_date": None,
            "discount": 0.0,
            "duties_and_taxes": 0.0,
            "extra_charges": [{"amount": 9.22, "currency": "USD", "name": "FUEL"}],
            "service_name": "INTERNATIONAL_PRIORITY",
            "service_type": "PAYOR_ACCOUNT_SHIPMENT",
            "total_charge": 239.71,
        },
        {
            "base_charge": 207.47,
            "carrier": "carrier_name",
            "currency": "USD",
            "delivery_date": None,
            "discount": 0.0,
            "duties_and_taxes": 0.0,
            "extra_charges": [{"amount": 8.3, "currency": "USD", "name": "FUEL"}],
            "service_name": "INTERNATIONAL_ECONOMY",
            "service_type": "PAYOR_ACCOUNT_SHIPMENT",
            "total_charge": 215.77,
        },
    ],
    [],
]

ParsedQuoteErrorResponse = [
    [],
    [
        {
            "carrier": "carrier_name",
            "code": "873",
            "message": "All specified account numbers must match.  ",
        }
    ],
]

QuoteErrorResponseXml = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
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

QuoteRequestXml = f"""<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ns="http://fedex.com/ws/rate/v22">
    <tns:Body>
        <ns:RateRequest>
            <ns:WebAuthenticationDetail>
                <ns:UserCredential>
                    <ns:Key>user_key</ns:Key>
                    <ns:Password>password</ns:Password>
                </ns:UserCredential>
            </ns:WebAuthenticationDetail>
            <ns:ClientDetail>
                <ns:AccountNumber>2349857</ns:AccountNumber>
                <ns:MeterNumber>1293587</ns:MeterNumber>
            </ns:ClientDetail>
            <ns:TransactionDetail>
                <ns:CustomerTransactionId>FTC</ns:CustomerTransactionId>
            </ns:TransactionDetail>
            <ns:Version>
                <ns:ServiceId>crs</ns:ServiceId>
                <ns:Major>22</ns:Major>
                <ns:Intermediate>0</ns:Intermediate>
                <ns:Minor>0</ns:Minor>
            </ns:Version>
            <ns:ReturnTransitAndCommit>true</ns:ReturnTransitAndCommit>
            <ns:RequestedShipment>
                <ns:PackagingType>YOUR_PACKAGING</ns:PackagingType>
                <ns:TotalWeight>
                    <ns:Units>LB</ns:Units>
                    <ns:Value>4.</ns:Value>
                </ns:TotalWeight>
                <ns:PreferredCurrency>USD</ns:PreferredCurrency>
                <ns:Shipper>
                    <ns:AccountNumber>2349857</ns:AccountNumber>
                    <ns:Address>
                        <ns:PostalCode>H3N1S4</ns:PostalCode>
                        <ns:CountryCode>CA</ns:CountryCode>
                    </ns:Address>
                </ns:Shipper>
                <ns:Recipient>
                    <ns:Address>
                        <ns:City>Lome</ns:City>
                        <ns:CountryCode>TG</ns:CountryCode>
                    </ns:Address>
                </ns:Recipient>
                <ns:ShippingChargesPayment>
                    <ns:PaymentType>SENDER</ns:PaymentType>
                    <ns:Payor>
                        <ns:ResponsibleParty>
                            <ns:AccountNumber>2349857</ns:AccountNumber>
                        </ns:ResponsibleParty>
                    </ns:Payor>
                </ns:ShippingChargesPayment>
                <ns:RateRequestTypes>LIST</ns:RateRequestTypes>
                <ns:RateRequestTypes>PREFERRED</ns:RateRequestTypes>
                <ns:PackageCount>1</ns:PackageCount>
                <ns:RequestedPackageLineItems>
                    <ns:GroupPackageCount>1</ns:GroupPackageCount>
                    <ns:Weight>
                        <ns:Units>LB</ns:Units>
                        <ns:Value>4.</ns:Value>
                    </ns:Weight>
                    <ns:Dimensions>
                        <ns:Length>10</ns:Length>
                        <ns:Width>3</ns:Width>
                        <ns:Height>3</ns:Height>
                        <ns:Units>IN</ns:Units>
                    </ns:Dimensions>
                </ns:RequestedPackageLineItems>
            </ns:RequestedShipment>
        </ns:RateRequest>
    </tns:Body>
</tns:Envelope>
"""

QuoteResponseXml = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
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
</SOAP-ENV:Envelope>"""
