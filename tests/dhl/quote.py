import unittest
from unittest.mock import patch
from gds_helpers import to_xml, jsonify, export
from openship.domain.entities import Quote
from tests.dhl.fixture import proxy, strip


class TestDHLQuote(unittest.TestCase):

    @patch("openship.mappers.dhl.dhl_proxy.http", return_value='<a></a>')
    def test_create_quote_request(self, http_mock):
        shipper = {"address": {"postal_code":"H3N1S4", "country_code":"CA"}}
        recipient = {"address": {"city":"Lome", "country_code":"TG"}}
        shipment_details = {"packages": [{"id":"1", "height":3, "lenght":10, "width":3,"weight":4.0}]}
        payload = Quote.create(shipper=shipper, recipient=recipient, shipment_details=shipment_details)
        quote_req_xml_obj = proxy.mapper.create_quote_request(payload)

        # remove MessageTime, Date and ReadyTime for testing purpose
        quote_req_xml_obj.GetQuote.Request.ServiceHeader.MessageTime = None
        quote_req_xml_obj.GetQuote.BkgDetails.Date = None
        quote_req_xml_obj.GetQuote.BkgDetails.ReadyTime = None

        proxy.get_quotes(quote_req_xml_obj)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(QuoteRequestXml))

    def test_parse_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(QuoteResponseXml))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedQuoteResponse))


if __name__ == '__main__':
    unittest.main()




ParsedQuoteParsingError = [
    {}
]

ParsedQuoteResponse = [
    [
        {
            'base_charge': 195.32, 
            'carrier': 'carrier_name', 
            'delivery_date': '2018-06-26 11:59:00', 
            'delivery_time': 'PT23H59M', 
            'discount': 0, 
            'duties_and_taxes': 0, 
            'extra_charges': [
                {
                    'name': 'FUEL SURCHARGE', 
                    'value': 12.7
                }
            ], 
            'pickup_date': '2018-06-21', 
            'pickup_time': 'PT17H30M', 
            'service_name': 'EXPRESS WORLDWIDE DOC', 
            'service_type': 'TD', 
            'total_charge': 208.02
        }, 
        {
            'base_charge': 213.47, 
            'carrier': 'carrier_name', 
            'delivery_date': '2018-06-26 11:59:00', 
            'delivery_time': 'PT23H59M', 
            'discount': 0, 
            'duties_and_taxes': 0, 
            'extra_charges': [], 
            'pickup_date': '2018-06-21', 
            'pickup_time': 'PT17H30M', 
            'service_name': 'EXPRESS EASY DOC', 
            'service_type': 'TD', 
            'total_charge': 213.47
        }
    ], 
    []
]


QuoteParsingError = """<?xml version="1.0" encoding="UTF-8"?>
<res:ErrorResponse xmlns:res='http://www.dhl.com' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:schemaLocation= 'http://www.dhl.com err-res.xsd'>
    <Response>
        <ServiceHeader>
            <MessageTime>2018-06-22T04:55:31+01:00</MessageTime>
            <MessageReference>1234567890123456789012345678901</MessageReference>
            <SiteID></SiteID>
            <Password></Password>
        </ServiceHeader>
        <Status>
            <ActionStatus>Error</ActionStatus>
            <Condition>
                <ConditionCode>111</ConditionCode>
                <ConditionData>Error in parsing request XML:Error: The
                    content of element type &quot;ServiceHeader&quot;
                    must match
                    &quot;(MessageTime,MessageReference,SiteID,Password)&quot;.
                    at line 9, column 30</ConditionData>
            </Condition>
        </Status>
    </Response>
</res:ErrorResponse><!-- ServiceInvocationId:20180622045531_96ab_f3e91245-69d2-422e-b943-83fbe8f8181b -->
"""

QuoteMissingArgsError = """<?xml version="1.0" ?>
<DCTResponse>
    <GetQuoteResponse>
        <Response>
            <ServiceHeader>
                <MessageTime>2018-06-22T04:49:29.292000+01:00</MessageTime>
                <MessageReference>1234567890123456789012345678901</MessageReference>
                <SiteID></SiteID>
            </ServiceHeader>
        </Response>
        <Note>
            <ActionStatus>Failure</ActionStatus>
            <Condition>
                <ConditionCode>340004</ConditionCode>
                <ConditionData>The location information is missing. At least one attribute post code, city name or suburb name should be provided</ConditionData>
            </Condition>
            <Condition>
                <ConditionCode>220001</ConditionCode>
                <ConditionData>Failure - request</ConditionData>
            </Condition>
        </Note>
    </GetQuoteResponse>
</DCTResponse>
"""

QuoteRequestXml = """<p:DCTRequest schemaVersion="1.0" xmlns:p="http://www.dhl.com" xmlns:p1="http://www.dhl.com/datatypes" xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.dhl.com DCT-req.xsd ">
    <GetQuote>
        <Request>
            <ServiceHeader>
                <MessageReference>1234567890123456789012345678901</MessageReference>
                <SiteID>site_id</SiteID>
                <Password>password</Password>
            </ServiceHeader>
            <MetaData>
                <SoftwareName>3PV</SoftwareName>
                <SoftwareVersion>1.0</SoftwareVersion>
            </MetaData>
        </Request>
        <From>
            <CountryCode>CA</CountryCode>
            <Postalcode>H3N1S4</Postalcode>
        </From>
        <BkgDetails>
            <PaymentCountryCode>CA</PaymentCountryCode>
            <DimensionUnit>IN</DimensionUnit>
            <WeightUnit>LB</WeightUnit>
            <Pieces>
                <Piece>
                    <PieceID>1</PieceID>
                    <PackageTypeCode></PackageTypeCode>
                    <Height>3.</Height>
                    <Depth>10.</Depth>
                    <Width>3.</Width>
                    <Weight>4.</Weight>
                </Piece>
            </Pieces>
            <PaymentAccountNumber>1203598305</PaymentAccountNumber>
            <IsDutiable>N</IsDutiable>
            <NetworkTypeCode>AL</NetworkTypeCode>
        </BkgDetails>
        <To>
            <CountryCode>TG</CountryCode>
            <City>Lome</City>
        </To>
    </GetQuote>
</p:DCTRequest>
"""

QuoteResponseXml = """<?xml version="1.0" ?>
<DCTResponse>
    <GetQuoteResponse>
        <Response>
            <ServiceHeader>
                <MessageTime>2018-06-21T11:33:15.103000+01:00</MessageTime>
                <MessageReference>1234567890123456789012345678901</MessageReference>
                <SiteID>...</SiteID>
            </ServiceHeader>
        </Response>
        <BkgDetails>
            <QtdShp>
                <OriginServiceArea>
                    <FacilityCode>GTW</FacilityCode>
                    <ServiceAreaCode>YUL</ServiceAreaCode>
                </OriginServiceArea>
                <DestinationServiceArea>
                    <FacilityCode>LFW</FacilityCode>
                    <ServiceAreaCode>LFW</ServiceAreaCode>
                </DestinationServiceArea>
                <GlobalProductCode>D</GlobalProductCode>
                <LocalProductCode>D</LocalProductCode>
                <ProductShortName>EXPRESS WORLDWIDE</ProductShortName>
                <LocalProductName>EXPRESS WORLDWIDE DOC</LocalProductName>
                <NetworkTypeCode>TD</NetworkTypeCode>
                <POfferedCustAgreement>N</POfferedCustAgreement>
                <TransInd>Y</TransInd>
                <PickupDate>2018-06-21</PickupDate>
                <PickupCutoffTime>PT17H30M</PickupCutoffTime>
                <BookingTime>PT16H30M</BookingTime>
                <CurrencyCode>CAD</CurrencyCode>
                <ExchangeRate>0.662335</ExchangeRate>
                <WeightCharge>195.319999999999993</WeightCharge>
                <WeightChargeTax>0.</WeightChargeTax>
                <TotalTransitDays>5</TotalTransitDays>
                <PickupPostalLocAddDays>0</PickupPostalLocAddDays>
                <DeliveryPostalLocAddDays>0</DeliveryPostalLocAddDays>
                <DeliveryTime>PT23H59M</DeliveryTime>
                <DimensionalWeight>0.647</DimensionalWeight>
                <WeightUnit>LB</WeightUnit>
                <PickupDayOfWeekNum>4</PickupDayOfWeekNum>
                <DestinationDayOfWeekNum>2</DestinationDayOfWeekNum>
                <QuotedWeight>4.</QuotedWeight>
                <QuotedWeightUOM>LB</QuotedWeightUOM>
                <QtdShpExChrg>
                    <SpecialServiceType>FF</SpecialServiceType>
                    <LocalServiceType>FF</LocalServiceType>
                    <GlobalServiceName>FUEL SURCHARGE</GlobalServiceName>
                    <LocalServiceTypeName>FUEL SURCHARGE</LocalServiceTypeName>
                    <SOfferedCustAgreement>N</SOfferedCustAgreement>
                    <ChargeCodeType>SCH</ChargeCodeType>
                    <CurrencyCode>CAD</CurrencyCode>
                    <ChargeValue>12.699999999999999</ChargeValue>
                    <QtdSExtrChrgInAdCur>
                        <ChargeValue>12.699999999999999</ChargeValue>
                        <CurrencyCode>CAD</CurrencyCode>
                        <CurrencyRoleTypeCode>BILLC</CurrencyRoleTypeCode>
                    </QtdSExtrChrgInAdCur>
                    <QtdSExtrChrgInAdCur>
                        <ChargeValue>12.699999999999999</ChargeValue>
                        <CurrencyCode>CAD</CurrencyCode>
                        <CurrencyRoleTypeCode>PULCL</CurrencyRoleTypeCode>
                    </QtdSExtrChrgInAdCur>
                    <QtdSExtrChrgInAdCur>
                        <ChargeValue>8.41</ChargeValue>
                        <CurrencyCode>EUR</CurrencyCode>
                        <CurrencyRoleTypeCode>BASEC</CurrencyRoleTypeCode>
                    </QtdSExtrChrgInAdCur>
                </QtdShpExChrg>
                <PricingDate>2018-06-21</PricingDate>
                <ShippingCharge>208.02000000000001</ShippingCharge>
                <TotalTaxAmount>0.</TotalTaxAmount>
                <PickupWindowEarliestTime>09:00:00</PickupWindowEarliestTime>
                <PickupWindowLatestTime>19:00:00</PickupWindowLatestTime>
                <BookingCutoffOffset>PT1H</BookingCutoffOffset>
                <DeliveryDate>
                    <DeliveryType>QDDC</DeliveryType>
                    <DlvyDateTime>2018-06-26 11:59:00</DlvyDateTime>
                    <DeliveryDateTimeOffset>+00:00</DeliveryDateTimeOffset>
                </DeliveryDate>
            </QtdShp>
            <QtdShp>
                <OriginServiceArea>
                    <FacilityCode>GTW</FacilityCode>
                    <ServiceAreaCode>YUL</ServiceAreaCode>
                </OriginServiceArea>
                <DestinationServiceArea>
                    <FacilityCode>LFW</FacilityCode>
                    <ServiceAreaCode>LFW</ServiceAreaCode>
                </DestinationServiceArea>
                <GlobalProductCode>7</GlobalProductCode>
                <LocalProductCode>7</LocalProductCode>
                <ProductShortName>EXPRESS EASY</ProductShortName>
                <LocalProductName>EXPRESS EASY DOC</LocalProductName>
                <NetworkTypeCode>TD</NetworkTypeCode>
                <POfferedCustAgreement>Y</POfferedCustAgreement>
                <TransInd>N</TransInd>
                <PickupDate>2018-06-21</PickupDate>
                <PickupCutoffTime>PT17H30M</PickupCutoffTime>
                <BookingTime>PT16H30M</BookingTime>
                <CurrencyCode>CAD</CurrencyCode>
                <ExchangeRate>0.662335</ExchangeRate>
                <WeightCharge>213.469999999999999</WeightCharge>
                <WeightChargeTax>0.</WeightChargeTax>
                <TotalTransitDays>5</TotalTransitDays>
                <PickupPostalLocAddDays>0</PickupPostalLocAddDays>
                <DeliveryPostalLocAddDays>0</DeliveryPostalLocAddDays>
                <DeliveryTime>PT23H59M</DeliveryTime>
                <DimensionalWeight>0.647</DimensionalWeight>
                <WeightUnit>LB</WeightUnit>
                <PickupDayOfWeekNum>4</PickupDayOfWeekNum>
                <DestinationDayOfWeekNum>2</DestinationDayOfWeekNum>
                <QuotedWeight>4.</QuotedWeight>
                <QuotedWeightUOM>LB</QuotedWeightUOM>
                <PricingDate>2018-06-21</PricingDate>
                <ShippingCharge>213.469999999999999</ShippingCharge>
                <TotalTaxAmount>0.</TotalTaxAmount>
                <PickupWindowEarliestTime>09:00:00</PickupWindowEarliestTime>
                <PickupWindowLatestTime>19:00:00</PickupWindowLatestTime>
                <BookingCutoffOffset>PT1H</BookingCutoffOffset>
                <DeliveryDate>
                    <DeliveryType>QDDC</DeliveryType>
                    <DlvyDateTime>2018-06-26 11:59:00</DlvyDateTime>
                    <DeliveryDateTimeOffset>+00:00</DeliveryDateTimeOffset>
                </DeliveryDate>
            </QtdShp>
        </BkgDetails>
        <Srvs>
            <Srv>
                <GlobalProductCode>D</GlobalProductCode>
                <MrkSrv>
                    <LocalProductCode>D</LocalProductCode>
                    <ProductShortName>EXPRESS WORLDWIDE</ProductShortName>
                    <LocalProductName>EXPRESS WORLDWIDE DOC</LocalProductName>
                    <ProductDesc>EXPRESS WORLDWIDE DOC</ProductDesc>
                    <NetworkTypeCode>TD</NetworkTypeCode>
                    <POfferedCustAgreement>N</POfferedCustAgreement>
                    <TransInd>Y</TransInd>
                    <LocalProductCtryCd>CA</LocalProductCtryCd>
                    <GlobalServiceType>D</GlobalServiceType>
                    <LocalServiceName>EXPRESS WORLDWIDE DOC</LocalServiceName>
                </MrkSrv>
                <MrkSrv>
                    <LocalServiceType>FF</LocalServiceType>
                    <GlobalServiceName>FUEL SURCHARGE</GlobalServiceName>
                    <LocalServiceTypeName>FUEL SURCHARGE</LocalServiceTypeName>
                    <SOfferedCustAgreement>N</SOfferedCustAgreement>
                    <ChargeCodeType>SCH</ChargeCodeType>
                    <MrkSrvInd>N</MrkSrvInd>
                    <GlobalServiceType>FF</GlobalServiceType>
                    <LocalServiceName>FUEL SURCHARGE</LocalServiceName>
                </MrkSrv>
            </Srv>
            <Srv>
                <GlobalProductCode>7</GlobalProductCode>
                <MrkSrv>
                    <LocalProductCode>7</LocalProductCode>
                    <ProductShortName>EXPRESS EASY</ProductShortName>
                    <LocalProductName>EXPRESS EASY DOC</LocalProductName>
                    <ProductDesc>EXPRESS EASY DOC</ProductDesc>
                    <NetworkTypeCode>TD</NetworkTypeCode>
                    <POfferedCustAgreement>Y</POfferedCustAgreement>
                    <TransInd>N</TransInd>
                    <LocalProductCtryCd>CA</LocalProductCtryCd>
                    <GlobalServiceType>7</GlobalServiceType>
                    <LocalServiceName>EXPRESS EASY DOC</LocalServiceName>
                </MrkSrv>
            </Srv>
        </Srvs>
        <Note>
            <ActionStatus>Success</ActionStatus>
        </Note>
    </GetQuoteResponse>
</DCTResponse>
"""