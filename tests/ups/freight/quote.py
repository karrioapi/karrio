import unittest
from unittest.mock import patch
from gds_helpers import to_xml, to_dict, export
from pyups.freight_rate import FreightRateRequest
from purplship.domain import Types as T
from tests.ups.freight.fixture import proxy
from tests.utils import strip, get_node_from_xml


class TestUPSQuote(unittest.TestCase):
    def setUp(self):

        self.FreightRateRequest = FreightRateRequest()
        self.FreightRateRequest.build(
            get_node_from_xml(FreightRateRequestXML, "FreightRateRequest")
        )

    def test_create_quote_request(self):
        payload = T.RateRequest(**rate_req_data)

        FreightRateRequest_ = proxy.mapper.create_quote_request(payload)
        self.assertEqual(export(FreightRateRequest_), export(self.FreightRateRequest))

    @patch("purplship.carriers.ups.ups_proxy.http", return_value="<a></a>")
    def test_freight_get_quotes(self, http_mock):
        proxy.get_quotes(self.FreightRateRequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(FreightRateRequestXML))

    def test_parse_freight_quote_response(self):
        parsed_response = proxy.mapper.parse_quote_response(
            to_xml(FreightRateResponseXML)
        )
        self.assertEqual(to_dict(parsed_response), to_dict(ParsedFreightRateResponse))


if __name__ == "__main__":
    unittest.main()


ParsedFreightRateResponse = [
    [
        {
            "base_charge": 909.26,
            "carrier": "UPS",
            "currency": "USD",
            "delivery_date": None,
            "discount": 776.36,
            "duties_and_taxes": 576.54,
            "extra_charges": [
                {"amount": 776.36, "currency": "USD", "name": "DSCNT"},
                {"amount": 480.0, "currency": "USD", "name": "HOL_WE_PU_DEL"},
                {"amount": 66.54, "currency": "USD", "name": "2"},
                {"amount": 30.0, "currency": "USD", "name": "CA_BORDER"},
            ],
            "service_name": None,
            "service_type": "309",
            "total_charge": 332.72,
        }
    ],
    [],
]

FreightRateRequestXML = f"""<tns:Envelope xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0" xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0" xmlns:wsf="http://www.ups.com/schema/wsf" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:frt="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0">
    <tns:Header>
        <upss:UPSSecurity>
            <upss:UsernameToken>
                <upss:Username>username</upss:Username>
                <upss:Password>password</upss:Password>
            </upss:UsernameToken>
            <upss:ServiceAccessToken>
                <upss:AccessLicenseNumber>FG09H9G8H09GH8G0</upss:AccessLicenseNumber>
            </upss:ServiceAccessToken>
        </upss:UPSSecurity>
    </tns:Header>
    <tns:Body>
        <frt:FreightRateRequest>
            <common:Request>
                <common:RequestOption>1</common:RequestOption>
                <common:TransactionReference>
                    <common:TransactionIdentifier>TransactionIdentifier</common:TransactionIdentifier>
                </common:TransactionReference>
            </common:Request>
            <frt:ShipFrom>
                <frt:Address>
                    <frt:AddressLine>Rue Fake</frt:AddressLine>
                    <frt:City>Montreal</frt:City>
                    <frt:PostalCode>H3N1S4</frt:PostalCode>
                    <frt:CountryCode>CA</frt:CountryCode>
                </frt:Address>
            </frt:ShipFrom>
            <frt:ShipTo>
                <frt:Address>
                    <frt:City>Las Vegas</frt:City>
                    <frt:PostalCode>89109</frt:PostalCode>
                    <frt:CountryCode>US</frt:CountryCode>
                </frt:Address>
            </frt:ShipTo>
            <frt:PaymentInformation>
                <frt:Payer>
                    <frt:Name>CA</frt:Name>
                    <frt:Address>
                        <frt:AddressLine>Rue Fake</frt:AddressLine>
                        <frt:City>Montreal</frt:City>
                        <frt:PostalCode>H3N1S4</frt:PostalCode>
                        <frt:CountryCode>CA</frt:CountryCode>
                    </frt:Address>
                    <frt:ShipperNumber>56GJE</frt:ShipperNumber>
                </frt:Payer>
                <frt:ShipmentBillingOption>
                    <frt:Code>10</frt:Code>
                </frt:ShipmentBillingOption>
            </frt:PaymentInformation>
            <frt:Service>
                <frt:Code>309</frt:Code>
            </frt:Service>
            <frt:HandlingUnitOne>
                <frt:Quantity>1</frt:Quantity>
                <frt:Type>
                    <frt:Code>SKD</frt:Code>
                </frt:Type>
            </frt:HandlingUnitOne>
            <frt:Commodity>
                <frt:Description>TV</frt:Description>
                <frt:Weight>
                    <frt:Value>4.0</frt:Value>
                    <frt:UnitOfMeasurement>
                        <frt:Code>LBS</frt:Code>
                    </frt:UnitOfMeasurement>
                </frt:Weight>
                <frt:Dimensions>
                    <frt:UnitOfMeasurement>
                        <frt:Code>IN</frt:Code>
                    </frt:UnitOfMeasurement>
                    <frt:Length>170</frt:Length>
                    <frt:Width>3</frt:Width>
                    <frt:Height>3</frt:Height>
                </frt:Dimensions>
                <frt:NumberOfPieces>1</frt:NumberOfPieces>
                <frt:PackagingType>
                    <frt:Code>BAG</frt:Code>
                </frt:PackagingType>
                <frt:FreightClass>50</frt:FreightClass>
            </frt:Commodity>
            <frt:ShipmentServiceOptions>
                <frt:PickupOptions>
                    <frt:WeekendPickupIndicator></frt:WeekendPickupIndicator>
                </frt:PickupOptions>
            </frt:ShipmentServiceOptions>
            <frt:GFPOptions/>
            <frt:HandlingUnitWeight>
                <frt:Value>1</frt:Value>
                <frt:UnitOfMeasurement>
                    <frt:Code>LBS</frt:Code>
                </frt:UnitOfMeasurement>
            </frt:HandlingUnitWeight>
            <frt:AdjustedWeightIndicator></frt:AdjustedWeightIndicator>
            <frt:TimeInTransitIndicator></frt:TimeInTransitIndicator>
            <frt:DensityEligibleIndicator></frt:DensityEligibleIndicator>
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


rate_req_data = {
    "shipper": {
        "account_number": "56GJE",
        "postal_code": "H3N1S4",
        "country_code": "CA",
        "city": "Montreal",
        "address_lines": ["Rue Fake"],
    },
    "recipient": {
        "postal_code": "89109", "city": "Las Vegas", "country_code": "US"
    },
    "shipment": {
         "items": [
                {
                    "id": "1",
                    "height": 3,
                    "length": 170,
                    "width": 3,
                    "weight": 4.0,
                    "packaging_type": "Bag",
                    "description": "TV",
                }
        ]
    },
}
