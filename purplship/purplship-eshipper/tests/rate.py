import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import RateRequest
from purplship.core.errors import RequiredFieldError
from purplship.package import rating
from tests.fixture import gateway


class TestEShipperRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequestXML)

    def test_create_rate_request_with_package_preset_missing_weight(self):
        with self.assertRaises(RequiredFieldError):
            gateway.mapper.create_rate_request(
                RateRequest(**RateWithPresetMissingDimensionPayload)
            )

    @patch("purplship.extension.mappers.eshipper.proxy.http", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, gateway.proxy.settings.server_url)

    def test_parse_rate_response(self):
        with patch("purplship.extension.mappers.eshipper.proxy.http") as mock:
            mock.return_value = RateResponseXml
            parsed_response = rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertEqual(to_dict(parsed_response), to_dict(ParsedQuoteResponse))


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {"postal_code": "H8Z2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcel": {
        "height": 3,
        "length": 10,
        "width": 3,
        "weight": 4.0,
        "services": [],
        "dimension_unit": "CM",
        "weight_unit": "KG",
    },
}

RateWithPresetMissingDimensionPayload = {
    "shipper": {"postal_code": "H8Z2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcel": {"services": []},
}

ParsedQuoteResponse = [
    [
        {
            "base_charge": 177.0,
            "carrier": "EShipper",
            "currency": "CAD",
            "estimated_delivery": "1",
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "Fuel surcharge"}
            ],
            "service": "eshipper_central_transport",
            "total_charge": 177.0,
        },
        {
            "base_charge": 28.650_000_000_000_002,
            "carrier": "EShipper",
            "currency": "CAD",
            "estimated_delivery": "1",
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "Fuel surcharge"}
            ],
            "service": "eshipper_2107",
            "total_charge": 28.65,
        },
        {
            "base_charge": 46.270_000_457_763_67,
            "carrier": "EShipper",
            "currency": "CAD",
            "estimated_delivery": "0",
            "extra_charges": [
                {"amount": 6.25, "currency": "CAD", "name": "Fuel surcharge"}
            ],
            "service": "eshipper_1911",
            "total_charge": 52.52,
        },
    ],
    [
        {
            "carrier": "EShipper",
            "message": "Polaris:Military Base Delivery,Saturday Pickup,Construction Site,BORDER FEE,Homeland Security,Limited Access,Saturday Delivery,Sort and Segregate Charge,Pier Charge",
        }
    ],
]

RateRequestXML = f"""<EShipper xmlns="http://www.eshipper.net/XMLSchema" username="merchantinc." password="9999" version="3.0.0">
    <QuoteRequest serviceId="0" stackable="true">
        <From id="123" company="Test Company" address1="650 CIT Drive" city="Livingston" state="ON" country="CA" zip="L4J7Y9" />
        <To company="Test Company" address1="650 CIT Drive" city="Livingston" state="MA" zip="01603" country="CA" />
        <COD paymentType="Check">
            <CODReturnAddress codCompany="ABC Towing" codName="Alfred" codAddress1="444 Highway 401" codCity="Toronto" codStateCode="ON" codZip="A1B2C3" codCountry="CA"/>
        </COD>
        <Packages type="Package">
            <Package length="15" width="10" height="12" weight="10" type="Pallet" freightClass="70" nmfcCode="123456" insuranceAmount="0.0" codAmount="0.0" description="desc."/>
            <Package length="15" width="10" height="10" weight="5" type="Pallet" freightClass="70" insuranceAmount="0.0" codAmount="0.0" description="desc."/>
        </Packages>
        <Pickup contactName="Test Name" phoneNumber="888-888-8888" pickupDate="2009-08-03" pickupTime="16:30" closingTime="17:45" location="Front Door"/>
    </QuoteRequest>
</EShipper>
"""

RateResponseXml = """<EShipper xmlns="http://www.eshipper.net/XMLSchema" version="3.1.0">
    <QuoteReply>
        <Quote carrierId="20" carrierName="EShipper" serviceId="2029" serviceName="Central Transport" modeTransport="A" transitDays="1" baseCharge="177.0" fuelSurcharge="0.0" totalCharge="177.0" currency="CAD">
        </Quote>
        <Quote carrierId="21" carrierName="EShipper" serviceId="2107" serviceName="Estes" modeTransport="G" transitDays="1" baseCharge="28.650000000000002" fuelSurcharge="0.0" totalCharge="28.65" currency="CAD">
        </Quote>
        <Quote carrierId="19" carrierName="EShipper" serviceId="1911" serviceName="USF Holland" modeTransport="null" transitDays="0" baseCharge="46.27000045776367" fuelSurcharge="6.25" totalCharge="52.52" currency="CAD">
        </Quote>
        <CarrierErrorMessage size="1" errorMessage0="Polaris:Military Base Delivery,Saturday Pickup,Construction Site,BORDER FEE,Homeland Security,Limited Access,Saturday Delivery,Sort and Segregate Charge,Pier Charge">
        </CarrierErrorMessage>
    </QuoteReply>
</EShipper>
"""
