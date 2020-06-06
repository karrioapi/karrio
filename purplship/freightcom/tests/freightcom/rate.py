import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import RateRequest
from purplship.core.errors import RequiredFieldError
from purplship.package import Rating
from tests.freightcom.fixture import gateway


class TestFreightcomRating(unittest.TestCase):
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

    @patch("purplship.package.mappers.freightcom.proxy.http", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, gateway.proxy.settings.server_url)

    def test_parse_rate_response(self):
        with patch("purplship.package.mappers.freightcom.proxy.http") as mock:
            mock.return_value = RateResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

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
        "dimension_unit": "CM",
        "weight_unit": "KG",
    },
}

RateWithPresetMissingDimensionPayload = {
    "shipper": {"postal_code": "H8Z2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcel": {},
}

ParsedQuoteResponse = [
    [
        {
            "base_charge": 177.0,
            "carrier_name": "freightcom",
            "carrier_id": "freightcom",
            "currency": "CAD",
            "estimated_delivery": "1",
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "Fuel surcharge"}
            ],
            "service": "freightcom_central_transport",
            "total_charge": 177.0,
        },
        {
            "base_charge": 28.65,
            "carrier_name": "freightcom",
            "carrier_id": "freightcom",
            "currency": "CAD",
            "estimated_delivery": "1",
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "Fuel surcharge"}
            ],
            "service": "freightcom_2107",
            "total_charge": 28.65,
        },
        {
            "base_charge": 46.27,
            "carrier_name": "freightcom",
            "carrier_id": "freightcom",
            "currency": "CAD",
            "estimated_delivery": "0",
            "extra_charges": [
                {"amount": 6.25, "currency": "CAD", "name": "Fuel surcharge"}
            ],
            "service": "freightcom_1911",
            "total_charge": 52.52,
        },
    ],
    [
        {
            "carrier_name": "freightcom",
            "carrier_id": "freightcom",
            "message": "Polaris:Military Base Delivery,Saturday Pickup,Construction Site,BORDER FEE,Homeland Security,Limited Access,Saturday Delivery,Sort and Segregate Charge,Pier Charge",
        }
    ],
]

RateRequestXML = f"""<Freightcom xmlns="http://www.freightcom.net/XMLSchema" username="username" password="password" version="3.1.0">
    <QuoteRequest insuranceType="False" serviceId="2029">
        <From residential="False" country="CA" zip="H8Z2Z3"/>
        <To residential="False" zip="H8Z2V4" country="CA"/>
        <Packages>
            <Package length="10." width="3." height="3." weight="4." type="Boxes"/>
        </Packages>
    </QuoteRequest>
</Freightcom>
"""

RateResponseXml = """<Freightcom xmlns="http://www.freightcom.net/XMLSchema" version="3.1.0">
    <QuoteReply>
        <Quote carrierId="20" carrierName="Freightcom" serviceId="2029" serviceName="Central Transport" modeTransport="A" transitDays="1" baseCharge="177.0" fuelSurcharge="0.0" totalCharge="177.0" currency="CAD">
        </Quote>
        <Quote carrierId="21" carrierName="Freightcom" serviceId="2107" serviceName="Estes" modeTransport="G" transitDays="1" baseCharge="28.650000000000002" fuelSurcharge="0.0" totalCharge="28.65" currency="CAD">
        </Quote>
        <Quote carrierId="19" carrierName="Freightcom" serviceId="1911" serviceName="USF Holland" modeTransport="null" transitDays="0" baseCharge="46.27000045776367" fuelSurcharge="6.25" totalCharge="52.52" currency="CAD">
        </Quote>
        <CarrierErrorMessage size="1" errorMessage0="Polaris:Military Base Delivery,Saturday Pickup,Construction Site,BORDER FEE,Homeland Security,Limited Access,Saturday Delivery,Sort and Segregate Charge,Pier Charge">
        </CarrierErrorMessage>
    </QuoteReply>
</Freightcom>
"""
