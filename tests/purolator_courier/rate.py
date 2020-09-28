import unittest
from datetime import datetime
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import RateRequest
from purplship import Rating
from tests.purolator_courier.fixture import gateway


class TestPurolatorQuote(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RATE_REQUEST_PAYLOAD)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RATE_REQUEST_XML)

    @patch("purplship.mappers.purolator_courier.proxy.http", return_value="<a></a>")
    def test_create_rate(self, http_mock):
        Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}/EWS/V2/Estimating/EstimatingService.asmx",
        )

    def test_parse_rate_response(self):
        with patch("purplship.mappers.purolator_courier.proxy.http") as mock:
            mock.return_value = RATE_RESPONSE_XML
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(to_dict(parsed_response), to_dict(PARSED_RATE_RESPONSE))


if __name__ == "__main__":
    unittest.main()


RATE_REQUEST_PAYLOAD = {
    "shipper": {
        "person_name": "Aaron Summer",
        "state_code": "ON",
        "city": "Mississauga",
        "country_code": "CA",
        "postal_code": "L4W5M8",
        "address_line1": "Main Street",
        "phone_number": "1 514 5555555",
    },
    "recipient": {
        "person_name": "Aaron Summer",
        "state_code": "BC",
        "city": "Burnaby",
        "country_code": "CA",
        "postal_code": "V5C5A9",
        "address_line1": "Douglas Road",
        "phone_number": "1 514 2982181",
    },
    "parcels": [
        {
            "weight": 10,
            "weight_unit": "LB",
        }
    ],
    "services": ["purolator_express"],
    "reference": "Reference For Shipment",
}

RATE_REQUEST_WITH_PRESET_PAYLOAD = {
    "shipper": {
        "person_name": "Aaron Summer",
        "state_code": "ON",
        "city": "Mississauga",
        "country_code": "CA",
        "postal_code": "L4W5M8",
        "address_line1": "Main Street",
        "phone_number": "5555555",
    },
    "recipient": {
        "person_name": "Aaron Summer",
        "state_code": "BC",
        "city": "Burnaby",
        "country_code": "CA",
        "postal_code": "V5C5A9",
        "address_line1": "Douglas Road",
        "phone_number": "2982181",
    },
    "parcels": [
        {
            "package_preset": "purolator_express_box",
            "services": ["purolator_express"],
        }
    ],
    "reference": "Reference For Shipment",
}

PARSED_RATE_RESPONSE = [
    [
        {
            "base_charge": 62.35,
            "carrier_name": "purolator_courier",
            "carrier_id": "purolator_courier",
            "currency": "CAD",
            "duties_and_taxes": 5.15,
            "transit_days": 1,
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "PST/QST"},
                {"amount": 0.0, "currency": "CAD", "name": "HST"},
                {"amount": 5.15, "currency": "CAD", "name": "GST"},
                {"amount": 1.85, "currency": "CAD", "name": "Residential Delivery"},
                {"amount": 2.81, "currency": "CAD", "name": "Fuel"},
                {
                    "amount": 36.0,
                    "currency": "CAD",
                    "name": "Dangerous Goods Classification",
                },
            ],
            "service": "purolator_express_9_am",
            "total_charge": 108.16,
        },
        {
            "base_charge": 55.0,
            "carrier_name": "purolator_courier",
            "carrier_id": "purolator_courier",
            "currency": "CAD",
            "duties_and_taxes": 4.77,
            "transit_days": 1,
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "PST/QST"},
                {"amount": 0.0, "currency": "CAD", "name": "HST"},
                {"amount": 4.77, "currency": "CAD", "name": "GST"},
                {"amount": 1.85, "currency": "CAD", "name": "Residential Delivery"},
                {"amount": 2.48, "currency": "CAD", "name": "Fuel"},
                {
                    "amount": 36.0,
                    "currency": "CAD",
                    "name": "Dangerous Goods Classification",
                },
            ],
            "service": "purolator_express_10_30_am",
            "total_charge": 100.1,
        },
        {
            "base_charge": 46.15,
            "carrier_name": "purolator_courier",
            "carrier_id": "purolator_courier",
            "currency": "CAD",
            "duties_and_taxes": 4.3,
            "transit_days": 1,
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "PST/QST"},
                {"amount": 0.0, "currency": "CAD", "name": "HST"},
                {"amount": 4.3, "currency": "CAD", "name": "GST"},
                {"amount": 1.85, "currency": "CAD", "name": "Residential Delivery"},
                {"amount": 2.08, "currency": "CAD", "name": "Fuel"},
                {
                    "amount": 36.0,
                    "currency": "CAD",
                    "name": "Dangerous Goods Classification",
                },
            ],
            "service": "purolator_express",
            "total_charge": 90.38,
        },
        {
            "base_charge": 29.6,
            "carrier_name": "purolator_courier",
            "carrier_id": "purolator_courier",
            "currency": "CAD",
            "duties_and_taxes": 3.44,
            "transit_days": 4,
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "PST/QST"},
                {"amount": 0.0, "currency": "CAD", "name": "HST"},
                {"amount": 3.44, "currency": "CAD", "name": "GST"},
                {"amount": 1.85, "currency": "CAD", "name": "Residential Delivery"},
                {"amount": 1.33, "currency": "CAD", "name": "Fuel"},
                {
                    "amount": 36.0,
                    "currency": "CAD",
                    "name": "Dangerous Goods Classification",
                },
            ],
            "service": "purolator_ground",
            "total_charge": 72.22,
        },
        {
            "base_charge": 87.69,
            "carrier_name": "purolator_courier",
            "carrier_id": "purolator_courier",
            "currency": "CAD",
            "duties_and_taxes": 6.47,
            "transit_days": 4,
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "PST/QST"},
                {"amount": 0.0, "currency": "CAD", "name": "HST"},
                {"amount": 6.47, "currency": "CAD", "name": "GST"},
                {"amount": 1.85, "currency": "CAD", "name": "Residential Delivery"},
                {"amount": 3.95, "currency": "CAD", "name": "Fuel"},
                {
                    "amount": 36.0,
                    "currency": "CAD",
                    "name": "Dangerous Goods Classification",
                },
            ],
            "service": "purolator_ground",
            "total_charge": 135.96,
        },
    ],
    [],
]


RATE_REQUEST_XML = f"""<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://purolator.com/pws/datatypes/v2">
    <soap:Header>
        <v2:RequestContext>
            <v2:Version>2.1</v2:Version>
            <v2:Language>en</v2:Language>
            <v2:GroupID></v2:GroupID>
            <v2:RequestReference></v2:RequestReference>
            <v2:UserToken>token</v2:UserToken>
        </v2:RequestContext>
    </soap:Header>
    <soap:Body>
        <v2:GetFullEstimateRequest>
            <v2:Shipment>
                <v2:SenderInformation>
                    <v2:Address>
                        <v2:Name>Aaron Summer</v2:Name>
                        <v2:StreetNumber></v2:StreetNumber>
                        <v2:StreetName>Main Street</v2:StreetName>
                        <v2:City>Mississauga</v2:City>
                        <v2:Province>ON</v2:Province>
                        <v2:Country>CA</v2:Country>
                        <v2:PostalCode>L4W5M8</v2:PostalCode>
                        <v2:PhoneNumber>
                            <v2:CountryCode>1</v2:CountryCode>
                            <v2:AreaCode>514</v2:AreaCode>
                            <v2:Phone>5555555</v2:Phone>
                        </v2:PhoneNumber>
                    </v2:Address>
                </v2:SenderInformation>
                <v2:ReceiverInformation>
                    <v2:Address>
                        <v2:Name>Aaron Summer</v2:Name>
                        <v2:StreetNumber></v2:StreetNumber>
                        <v2:StreetName>Douglas Road</v2:StreetName>
                        <v2:City>Burnaby</v2:City>
                        <v2:Province>BC</v2:Province>
                        <v2:Country>CA</v2:Country>
                        <v2:PostalCode>V5C5A9</v2:PostalCode>
                        <v2:PhoneNumber>
                            <v2:CountryCode>1</v2:CountryCode>
                            <v2:AreaCode>514</v2:AreaCode>
                            <v2:Phone>2982181</v2:Phone>
                        </v2:PhoneNumber>
                    </v2:Address>
                </v2:ReceiverInformation>
                <v2:ShipmentDate>{str(datetime.now().strftime("%Y-%m-%d"))}</v2:ShipmentDate>
                <v2:PackageInformation>
                    <v2:ServiceID>PurolatorExpress</v2:ServiceID>
                    <v2:TotalWeight>
                        <v2:Value>10</v2:Value>
                        <v2:WeightUnit>lb</v2:WeightUnit>
                    </v2:TotalWeight>
                    <v2:TotalPieces>1</v2:TotalPieces>
                    <v2:PiecesInformation>
                        <v2:Piece>
                            <v2:Weight>
                                <v2:Value>10.</v2:Value>
                                <v2:WeightUnit>lb</v2:WeightUnit>
                            </v2:Weight>
                        </v2:Piece>
                    </v2:PiecesInformation>
                </v2:PackageInformation>
                <v2:PaymentInformation>
                    <v2:PaymentType>Sender</v2:PaymentType>
                    <v2:RegisteredAccountNumber>12398576956</v2:RegisteredAccountNumber>
                </v2:PaymentInformation>
                <v2:PickupInformation>
                    <v2:PickupType>DropOff</v2:PickupType>
                </v2:PickupInformation>
                <v2:TrackingReferenceInformation>
                    <v2:Reference1>Reference For Shipment</v2:Reference1>
                </v2:TrackingReferenceInformation>
            </v2:Shipment>
            <v2:ShowAlternativeServicesIndicator>false</v2:ShowAlternativeServicesIndicator>
        </v2:GetFullEstimateRequest>
    </soap:Body>
</soap:Envelope>
"""

RATE_REQUEST_WITH_PRESET_XML = f"""<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v2="http://purolator.com/pws/datatypes/v2">
    <SOAP-ENV:Header>
        <v2:RequestContext>
            <v2:Version>2.1</v2:Version>
            <v2:Language>en</v2:Language>
            <v2:UserToken>token</v2:UserToken>
        </v2:RequestContext>
    </SOAP-ENV:Header>
    <SOAP-ENV:Body>
        <v2:GetFullEstimateRequest>
            <v2:Shipment>
                <v2:SenderInformation>
                    <v2:Address>
                        <v2:Name>Aaron Summer</v2:Name>
                        <v2:StreetName>Main Street</v2:StreetName>
                        <v2:City>Mississauga</v2:City>
                        <v2:Province>ON</v2:Province>
                        <v2:Country>CA</v2:Country>
                        <v2:PostalCode>L4W5M8</v2:PostalCode>
                        <v2:PhoneNumber>
                            <v2:CountryCode>1</v2:CountryCode>
                            <v2:AreaCode>514</v2:AreaCode>
                            <v2:Phone>5555555</v2:Phone>
                        </v2:PhoneNumber>
                    </v2:Address>
                </v2:SenderInformation>
                <v2:ReceiverInformation>
                    <v2:Address>
                        <v2:Name>Aaron Summer</v2:Name>
                        <v2:StreetName>Douglas Road</v2:StreetName>
                        <v2:City>Burnaby</v2:City>
                        <v2:Province>BC</v2:Province>
                        <v2:Country>CA</v2:Country>
                        <v2:PostalCode>V5C5A9</v2:PostalCode>
                        <v2:PhoneNumber>
                            <v2:CountryCode>1</v2:CountryCode>
                            <v2:AreaCode>514</v2:AreaCode>
                            <v2:Phone>2982181</v2:Phone>
                        </v2:PhoneNumber>
                    </v2:Address>
                </v2:ReceiverInformation>
                <v2:ShipmentDate>{str(datetime.now().strftime("%Y-%m-%d"))}</v2:ShipmentDate>
                <v2:PackageInformation>
                    <v2:ServiceID>PurolatorExpress</v2:ServiceID>
                    <v2:TotalWeight>
                        <v2:Value>10</v2:Value>
                        <v2:WeightUnit>lb</v2:WeightUnit>
                    </v2:TotalWeight>
                    <v2:TotalPieces>1</v2:TotalPieces>
                    <v2:PiecesInformation>
                        <v2:Piece>
                            <v2:Weight>
                                <v2:Value>7.</v2:Value>
                                <v2:WeightUnit>lb</v2:WeightUnit>
                            </v2:Weight>
                        </v2:Piece>
                    </v2:PiecesInformation>
                </v2:PackageInformation>
                <v2:PickupInformation>
                    <v2:PickupType>DropOff</v2:PickupType>
                </v2:PickupInformation>
                <v2:TrackingReferenceInformation>
                    <v2:Reference1>Reference For Shipment</v2:Reference1>
                </v2:TrackingReferenceInformation>
            </v2:Shipment>
            <v2:ShowAlternativeServicesIndicator>false</v2:ShowAlternativeServicesIndicator>
        </v2:GetFullEstimateRequest>
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
                    <ServiceID>PurolatorGround</ServiceID>
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
