import unittest
from unittest.mock import patch
from datetime import datetime
from gds_helpers import to_xml, jsonify
from openship.domain.entities import Quote
from tests.fedex.fixture import proxy
from tests.utils import strip


class TestFeDexQuote(unittest.TestCase):

    @patch("openship.mappers.fedex.fedex_proxy.http", return_value='<a></a>')
    def test_create_quote_request(self, http_mock):
        shipper = {"address": {"postal_code": "H3N1S4", "country_code": "CA"}}
        recipient = {"address": {"city": "Lome", "country_code": "TG"}}
        shipment_details = {"packages": [
            {"id": "1", "height": 3, "lenght": 10, "width": 3, "weight": 4.0}]}
        payload = Quote.create(
            shipper=shipper, recipient=recipient, shipment_details=shipment_details)

        quote_req_xml_obj = proxy.mapper.create_quote_request(payload)
        timestamp = datetime.now()
        # Hard coded for test purpose
        quote_req_xml_obj.RequestedShipment.ShipTimestamp = timestamp

        proxy.get_quotes(quote_req_xml_obj)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(
            QuoteRequestXml % str(timestamp.isoformat())))

    def test_parse_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteResponseXml))
            
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedQuoteResponse))


if __name__ == '__main__':
    unittest.main()

ParsedQuoteResponse = [
    [
        {
            'base_charge': 230.49, 
            'carrier': 'carrier_name', 
            'delivery_date': None, 
            'delivery_time': None, 
            'discount': 0.0, 
            'duties_and_taxes': 0.0, 
            'extra_charges': [
                {
                    'name': 'FUEL', 
                    'value': 9.22
                }
            ], 
            'pickup_date': None, 
            'pickup_time': None, 
            'service_name': 'INTERNATIONAL_PRIORITY', 
            'service_type': 'PAYOR_ACCOUNT_SHIPMENT', 
            'total_charge': 239.71
        }, 
        {
            'base_charge': 207.47, 
            'carrier': 'carrier_name', 
            'delivery_date': None, 
            'delivery_time': None, 
            'discount': 0.0, 
            'duties_and_taxes': 0.0, 
            'extra_charges': [
                {
                    'name': 'FUEL', 
                    'value': 8.3
                }
            ], 
            'pickup_date': None, 
            'pickup_time': None, 
            'service_name': 'INTERNATIONAL_ECONOMY', 
            'service_type': 'PAYOR_ACCOUNT_SHIPMENT', 
            'total_charge': 215.77
        }
    ], 
    []
]

QuoteErrorResponse = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
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
'''

QuoteRequestXml = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://fedex.com/ws/rate/v22">
    <SOAP-ENV:Body>
        <RateRequest>
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
                <Major>22</Major>
                <Intermediate>0</Intermediate>
                <Minor>0</Minor>
            </Version>
            <RequestedShipment>
                <ShipTimestamp>%s</ShipTimestamp>
                <PackagingType>YOUR_PACKAGING</PackagingType>
                <TotalWeight>
                    <Units>LB</Units>
                    <Value>4.</Value>
                </TotalWeight>
                <PreferredCurrency>USD</PreferredCurrency>
                <Shipper>
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
                <ShippingChargesPayment>
                    <PaymentType>SENDER</PaymentType>
                    <Payor>
                        <ResponsibleParty>
                            <AccountNumber>2349857</AccountNumber>
                        </ResponsibleParty>
                    </Payor>
                </ShippingChargesPayment>
                <RateRequestTypes>LIST</RateRequestTypes>
                <PackageCount>1</PackageCount>
                <RequestedPackageLineItems>
                    <GroupPackageCount>1</GroupPackageCount>
                    <Weight>
                        <Units>LB</Units>
                        <Value>4.</Value>
                    </Weight>
                    <Dimensions>
                        <Length>10</Length>
                        <Width>3</Width>
                        <Height>3</Height>
                        <Units>IN</Units>
                    </Dimensions>
                </RequestedPackageLineItems>
            </RequestedShipment>
        </RateRequest>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''

QuoteResponseXml = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
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
</SOAP-ENV:Envelope>'''
