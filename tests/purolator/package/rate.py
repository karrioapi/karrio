import re
import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import RateRequest
from purplship.package import rating
from tests.dhl.package.fixture import gateway


class TestDHLQuote(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RATE_REQUEST_PAYLOAD)


if __name__ == "__main__":
    unittest.main()


RATE_REQUEST_PAYLOAD = {}

RATE_REQUEST_XML = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:ns1="http://purolator.com/pws/datatypes/v1">
    <SOAP-ENV:Header>
        <ns1:RequestContext>
            <ns1:Version>1.0</ns1:Version>
            <ns1:Language>en</ns1:Language>
            <ns1:GroupID>xxx</ns1:GroupID>
            <ns1:RequestReference>Rating Example</ns1:RequestReference>
        </ns1:RequestContext>
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
        <ns1:GetFullEstimateRequest>
            <ns1:Shipment>
                <ns1:SenderInformation>
                    <ns1:Address>
                        <ns1:Name>Aaron Summer</ns1:Name>
                        <ns1:StreetNumber>1234</ns1:StreetNumber>
                        <ns1:StreetName>Main Street</ns1:StreetName>
                        <ns1:City>Mississauga</ns1:City>
                        <ns1:Province>ON</ns1:Province>
                        <ns1:Country>CA</ns1:Country>
                        <ns1:PostalCode>L4W5M8</ns1:PostalCode>
                        <ns1:PhoneNumber>
                            <ns1:CountryCode>1</ns1:CountryCode>
                            <ns1:AreaCode>905</ns1:AreaCode>
                            <ns1:Phone>5555555</ns1:Phone>
                        </ns1:PhoneNumber>
                    </ns1:Address>
                </ns1:SenderInformation>
                <ns1:ReceiverInformation>
                    <ns1:Address>
                        <ns1:Name>Aaron Summer</ns1:Name>
                        <ns1:StreetNumber>2245</ns1:StreetNumber>
                        <ns1:StreetName>Douglas Road</ns1:StreetName>
                        <ns1:City>Burnaby</ns1:City>
                        <ns1:Province>BC</ns1:Province>
                        <ns1:Country>CA</ns1:Country>
                        <ns1:PostalCode>V5C5A9</ns1:PostalCode>
                        <ns1:PhoneNumber>
                            <ns1:CountryCode>1</ns1:CountryCode>
                            <ns1:AreaCode>604</ns1:AreaCode>
                            <ns1:Phone>2982181</ns1:Phone>
                        </ns1:PhoneNumber>
                    </ns1:Address>
                </ns1:ReceiverInformation>
                <ns1:PackageInformation>
                    <ns1:ServiceID>PurolatorExpress</ns1:ServiceID>
                    <ns1:TotalWeight>
                        <ns1:Value>10</ns1:Value>
                        <ns1:WeightUnit>lb</ns1:WeightUnit>
                    </ns1:TotalWeight>
                    <ns1:TotalPieces>1</ns1:TotalPieces>
                    <ns1:OptionsInformation>
                        <ns1:Options>
                            <ns1:OptionIDValuePair>
                                <ns1:ID>DangerousGoods</ns1:ID>
                                <ns1:Value>true</ns1:Value>
                            </ns1:OptionIDValuePair>
                            <ns1:OptionIDValuePair>
                                <ns1:ID>DangerousGoodsMode</ns1:ID>
                                <ns1:Value>Air</ns1:Value>
                            </ns1:OptionIDValuePair>
                            <ns1:OptionIDValuePair>
                                <ns1:ID>DangerousGoodsClass</ns1:ID>
                                <ns1:Value>FullyRegulated</ns1:Value>
                            </ns1:OptionIDValuePair>
                        </ns1:Options>
                    </ns1:OptionsInformation>
                </ns1:PackageInformation>
                <ns1:PaymentInformation>
                    <ns1:PaymentType>Sender</ns1:PaymentType>
                    <ns1:RegisteredAccountNumber>YOUR_ACCOUNT_HERE</ns1:RegisteredAccountNumber>
                    <ns1:BillingAccountNumber>YOUR_ACCOUNT_HERE</ns1:BillingAccountNumber>
                </ns1:PaymentInformation>
                <ns1:PickupInformation>
                    <ns1:PickupType>DropOff</ns1:PickupType>
                </ns1:PickupInformation>
            </ns1:Shipment>
            <ns1:ShowAlternativeServicesIndicator>true</ns1:ShowAlternativeServicesIndicator>
        </ns1:GetFullEstimateRequest>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

RATE_RESPONSE_XML = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Header>
        <h:ResponseContext xmlns:h="http://purolator.com/pws/datatypes/v1" 
            xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <h:ResponseReference>Rating Example</h:ResponseReference>
        </h:ResponseContext>
    </s:Header>
    <s:Body>
        <GetFullEstimateResponse xmlns="http://purolator.com/pws/datatypes/v1" 
            xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <ResponseInformation>
                <Errors/>
                <InformationalMessages i:nil="true"/>
            </ResponseInformation>
            <ShipmentEstimates>
                <ShipmentEstimate>
                    <ServiceID>PurolatorExpress9AM</ServiceID>
                    <ShipmentDate>2009-04-16</ShipmentDate>
                    <ExpectedDeliveryDate>2009-04-17</ExpectedDeliveryDate>
                    <EstimatedTransitDays>1</EstimatedTransitDays>
                    <BasePrice>62.35</BasePrice>
                    <Surcharges>
                        <Surcharge>
                            <Amount>1.85</Amount>
                            <Type>ResidentialDelivery</Type>
                            <Description>Residential Delivery</Description>
                        </Surcharge>
                        <Surcharge>
                            <Amount>2.81</Amount>
                            <Type>Fuel</Type>
                            <Description>Fuel</Description>
                        </Surcharge>
                    </Surcharges>
                    <Taxes>
                        <Tax>
                            <Amount>0</Amount>
                            <Type>PSTQST</Type>
                            <Description>PST/QST</Description>
                        </Tax>
                        <Tax>
                            <Amount>0</Amount>
                            <Type>HST</Type>
                            <Description>HST</Description>
                        </Tax>
                        <Tax>
                            <Amount>5.15</Amount>
                            <Type>GST</Type>
                            <Description>GST</Description>
                        </Tax>
                    </Taxes>
                    <OptionPrices>
                        <OptionPrice>
                            <Amount>36</Amount>
                            <ID>DangerousGoodsClass</ID>
                            <Description>Dangerous Goods Classification</Description>
                        </OptionPrice>
                    </OptionPrices>
                    <TotalPrice>108.16</TotalPrice>
                </ShipmentEstimate>
                <ShipmentEstimate>
                    <ServiceID>PurolatorExpress10:30AM</ServiceID>
                    <ShipmentDate>2009-04-16</ShipmentDate>
                    <ExpectedDeliveryDate>2009-04-17</ExpectedDeliveryDate>
                    <EstimatedTransitDays>1</EstimatedTransitDays>
                    <BasePrice>55</BasePrice>
                    <Surcharges>
                        <Surcharge>
                            <Amount>1.85</Amount>
                            <Type>ResidentialDelivery</Type>
                            <Description>Residential Delivery</Description>
                        </Surcharge>
                        <Surcharge>
                            <Amount>2.48</Amount>
                            <Type>Fuel</Type>
                            <Description>Fuel</Description>
                        </Surcharge>
                    </Surcharges>
                    <Taxes>
                        <Tax>
                            <Amount>0</Amount>
                            <Type>PSTQST</Type>
                            <Description>PST/QST</Description>
                        </Tax>
                        <Tax>
                            <Amount>0</Amount>
                            <Type>HST</Type>
                            <Description>HST</Description>
                        </Tax>
                        <Tax>
                            <Amount>4.77</Amount>
                            <Type>GST</Type>
                            <Description>GST</Description>
                        </Tax>
                    </Taxes>
                    <OptionPrices>
                        <OptionPrice>
                            <Amount>36</Amount>
                            <ID>DangerousGoodsClass</ID>
                            <Description>Dangerous Goods Classification</Description>
                        </OptionPrice>
                    </OptionPrices>
                    <TotalPrice>100.1</TotalPrice>
                </ShipmentEstimate>
                <ShipmentEstimate>
                    <ServiceID>PurolatorExpress</ServiceID>
                    <ShipmentDate>2009-04-16</ShipmentDate>
                    <ExpectedDeliveryDate>2009-04-17</ExpectedDeliveryDate>
                    <EstimatedTransitDays>1</EstimatedTransitDays>
                    <BasePrice>46.15</BasePrice>
                    <Surcharges>
                        <Surcharge>
                            <Amount>1.85</Amount>
                            <Type>ResidentialDelivery</Type>
                            <Description>Residential Delivery</Description>
                        </Surcharge>
                        <Surcharge>
                            <Amount>2.08</Amount>
                            <Type>Fuel</Type>
                            <Description>Fuel</Description>
                        </Surcharge>
                    </Surcharges>
                    <Taxes>
                        <Tax>
                            <Amount>0</Amount>
                            <Type>PSTQST</Type>
                            <Description>PST/QST</Description>
                        </Tax>
                        <Tax>
                            <Amount>0</Amount>
                            <Type>HST</Type>
                            <Description>HST</Description>
                        </Tax>
                        <Tax>
                            <Amount>4.3</Amount>
                            <Type>GST</Type>
                            <Description>GST</Description>
                        </Tax>
                    </Taxes>
                    <OptionPrices>
                        <OptionPrice>
                            <Amount>36</Amount>
                            <ID>DangerousGoodsClass</ID>
                            <Description>Dangerous Goods Classification</Description>
                        </OptionPrice>
                    </OptionPrices>
                    <TotalPrice>90.38</TotalPrice>
                </ShipmentEstimate>
                <ShipmentEstimate>
                    <ServiceID>PurolatorGround</ServiceID>
                    <ShipmentDate>2009-04-16</ShipmentDate>
                    <ExpectedDeliveryDate>2009-04-22</ExpectedDeliveryDate>
                    <EstimatedTransitDays>4</EstimatedTransitDays>
                    <BasePrice>29.6</BasePrice>
                    <Surcharges>
                        <Surcharge>
                            <Amount>1.85</Amount>
                            <Type>ResidentialDelivery</Type>
                            <Description>Residential Delivery</Description>
                        </Surcharge>
                        <Surcharge>
                            <Amount>1.33</Amount>
                            <Type>Fuel</Type>
                            <Description>Fuel</Description>
                        </Surcharge>
                    </Surcharges>
                    <Taxes>
                        <Tax>
                            <Amount>0</Amount>
                            <Type>PSTQST</Type>
                            <Description>PST/QST</Description>
                        </Tax>
                        <Tax>
                            <Amount>0</Amount>
                            <Type>HST</Type>
                            <Description>HST</Description>
                        </Tax>
                        <Tax>
                            <Amount>3.44</Amount>
                            <Type>GST</Type>
                            <Description>GST</Description>
                        </Tax>
                    </Taxes>
                    <OptionPrices>
                        <OptionPrice>
                            <Amount>36</Amount>
                            <ID>DangerousGoodsClass</ID>
                            <Description>Dangerous Goods Classification</Description>
                        </OptionPrice>
                    </OptionPrices>
                    <TotalPrice>72.22</TotalPrice>
                </ShipmentEstimate>
                <ShipmentEstimate>
                    <ServiceID>PurolatorGroundDistribution</ServiceID>
                    <ShipmentDate>2009-04-16</ShipmentDate>
                    <ExpectedDeliveryDate>2009-04-22</ExpectedDeliveryDate>
                    <EstimatedTransitDays>4</EstimatedTransitDays>
                    <BasePrice>87.69</BasePrice>
                    <Surcharges>
                        <Surcharge>
                            <Amount>1.85</Amount>
                            <Type>ResidentialDelivery</Type>
                            <Description>Residential Delivery</Description>
                        </Surcharge>
                        <Surcharge>
                            <Amount>3.95</Amount>
                            <Type>Fuel</Type>
                            <Description>Fuel</Description>
                        </Surcharge>
                    </Surcharges>
                    <Taxes>
                        <Tax>
                            <Amount>0</Amount>
                            <Type>PSTQST</Type>
                            <Description>PST/QST</Description>
                        </Tax>
                        <Tax>
                            <Amount>0</Amount>
                            <Type>HST</Type>
                            <Description>HST</Description>
                        </Tax>
                        <Tax>
                            <Amount>6.47</Amount>
                            <Type>GST</Type>
                            <Description>GST</Description>
                        </Tax>
                    </Taxes>
                    <OptionPrices>
                        <OptionPrice>
                            <Amount>36</Amount>
                            <ID>DangerousGoodsClass</ID>
                            <Description>Dangerous Goods Classification</Description>
                        </OptionPrice>
                    </OptionPrices>
                    <TotalPrice>135.96</TotalPrice>
                </ShipmentEstimate>
            </ShipmentEstimates>
            <ReturnShipmentEstimates i:nil="true"/>
        </GetFullEstimateResponse>
    </s:Body>
</s:Envelope>
"""