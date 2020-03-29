import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import RateRequest
from tests.ups.freight.fixture import gateway
from purplship.freight import rating


class TestUPSRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**rate_req_data)

    def test_create_freight_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(request.serialize(), FreightRateRequestXML)

    @patch("purplship.freight.mappers.ups.proxy.http", return_value="<a></a>")
    def test_freight_get_rates(self, http_mock):
        rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, f"{gateway.settings.server_url}/FreightRate")

    def test_parse_freight_get_rates_response(self):
        with patch("purplship.freight.mappers.ups.proxy.http") as mock:
            mock.return_value = FreightRateResponseXML
            parsed_response = rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertEqual(
                to_dict(parsed_response), to_dict(ParsedFreightRateResponse)
            )


if __name__ == "__main__":
    unittest.main()


rate_req_data = {
    "shipper": {
        "postal_code": "H3N1S4",
        "country_code": "CA",
        "city": "Montreal",
        "address_line_1": "Rue Fake",
    },
    "recipient": {"postal_code": "89109", "city": "Las Vegas", "country_code": "US"},
    "parcel": {
        "id": "1",
        "height": 3,
        "length": 170,
        "width": 3,
        "weight": 4.0,
        "packaging_type": "box",
        "description": "TV",
    },
}


ParsedFreightRateResponse = [
    [
        {
            "base_charge": 909.26,
            "carrier": "ups",
            "carrier_name": "UPS Freight",
            "currency": "USD",
            "estimated_delivery": None,
            "discount": 776.36,
            "duties_and_taxes": 576.54,
            "extra_charges": [
                {"amount": 776.36, "currency": "USD", "name": "DSCNT"},
                {"amount": 480.0, "currency": "USD", "name": "HOL_WE_PU_DEL"},
                {"amount": 66.54, "currency": "USD", "name": "2"},
                {"amount": 30.0, "currency": "USD", "name": "CA_BORDER"},
            ],
            "total_charge": 332.72,
        }
    ],
    [],
]

FreightRateRequestXML = f"""<tns:Envelope  xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:frt="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0" >
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
        <frt:FreightRateRequest>
            <common:Request>
                <RequestOption>1</RequestOption>
                <TransactionReference>
                    <TransactionIdentifier>TransactionIdentifier</TransactionIdentifier>
                </TransactionReference>
            </common:Request>
            <ShipFrom>
                <Address>
                    <AddressLine>Rue Fake</AddressLine>
                    <City>Montreal</City>
                    <PostalCode>H3N1S4</PostalCode>
                    <CountryCode>CA</CountryCode>
                </Address>
            </ShipFrom>
            <ShipTo>
                <Address>
                    <City>Las Vegas</City>
                    <PostalCode>89109</PostalCode>
                    <CountryCode>US</CountryCode>
                </Address>
            </ShipTo>
            <Service>
                <Code>309</Code>
            </Service>
            <HandlingUnitOne>
                <Quantity>1</Quantity>
                <Type>
                    <Code>SKD</Code>
                </Type>
            </HandlingUnitOne>
            <Commodity>
                <Description>TV</Description>
                <Weight>
                    <Value>4.0</Value>
                    <UnitOfMeasurement>
                        <Code>LBS</Code>
                    </UnitOfMeasurement>
                </Weight>
                <Dimensions>
                    <UnitOfMeasurement>
                        <Code>IN</Code>
                    </UnitOfMeasurement>
                    <Length>170.0</Length>
                    <Width>3.0</Width>
                    <Height>3.0</Height>
                </Dimensions>
                <PackagingType>
                    <Code>BOX</Code>
                </PackagingType>
                <FreightClass>50</FreightClass>
            </Commodity>
            <ShipmentServiceOptions>
                <PickupOptions>
                    <WeekendPickupIndicator></WeekendPickupIndicator>
                </PickupOptions>
            </ShipmentServiceOptions>
            <AdjustedWeightIndicator></AdjustedWeightIndicator>
            <TimeInTransitIndicator></TimeInTransitIndicator>
            <DensityEligibleIndicator></DensityEligibleIndicator>
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
