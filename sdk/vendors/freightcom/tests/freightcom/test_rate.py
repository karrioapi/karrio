import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio.core.errors import FieldError
from karrio import Rating
from .fixture import gateway


class TestFreightcomRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequestXML)

    def test_create_rate_request_from_package_preset_missing_weight(self):
        with self.assertRaises(FieldError):
            gateway.mapper.create_rate_request(
                RateRequest(**RateWithPresetMissingDimensionPayload)
            )

    @patch("karrio.mappers.freightcom.proxy.http", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, gateway.proxy.settings.server_url)

    def test_parse_rate_response(self):
        with patch("karrio.mappers.freightcom.proxy.http") as mock:
            mock.return_value = RateResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertListEqual(DP.to_dict(parsed_response), ParsedQuoteResponse)

    def test_parse_rate_response_error(self):
        with patch("karrio.mappers.freightcom.proxy.http") as mock:
            mock.return_value = RateErrorResponseXML
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertListEqual(DP.to_dict(parsed_response), ParsedRateError)


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {"postal_code": "H8Z2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcels": [
        {
            "height": 3,
            "length": 10,
            "width": 3,
            "weight": 4.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "services": ["freightcom_central_transport"],
}

RateWithPresetMissingDimensionPayload = {
    "shipper": {"postal_code": "H8Z2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcels": [{}],
}

ParsedQuoteResponse = [
    [
        {
            "carrier_id": "freightcom",
            "carrier_name": "freightcom",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 177.0, "currency": "CAD", "name": "Base charge"}
            ],
            "meta": {
                "rate_provider": "Freightcom",
                "service_name": "central_transport",
            },
            "service": "freightcom_central_transport",
            "total_charge": 177.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "freightcom",
            "carrier_name": "freightcom",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 28.65, "currency": "CAD", "name": "Base charge"}
            ],
            "meta": {"rate_provider": "Freightcom", "service_name": "estes"},
            "service": "freightcom_estes",
            "total_charge": 28.65,
            "transit_days": 1,
        },
        {
            "carrier_id": "freightcom",
            "carrier_name": "freightcom",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 46.27, "currency": "CAD", "name": "Base charge"},
                {"amount": 6.25, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "meta": {"rate_provider": "Freightcom", "service_name": "usf_holland"},
            "service": "freightcom_usf_holland",
            "total_charge": 52.52,
            "transit_days": 0,
        },
    ],
    [
        {
            "carrier_id": "freightcom",
            "carrier_name": "freightcom",
            "code": "CarrierErrorMessage",
            "message": "Polaris:Military Base Delivery,Saturday Pickup,Construction Site,BORDER FEE,Homeland Security,Limited Access,Saturday Delivery,Sort and Segregate Charge,Pier Charge",
        }
    ],
]

ParsedRateError = [
    [],
    [
        {
            "code": "Error",
            "carrier_id": "freightcom",
            "carrier_name": "freightcom",
            "message": "Required field: company is missing.",
        }
    ],
]

RateRequestXML = f"""<Freightcom xmlns="http://www.freightcom.net/XMLSchema" username="username" password="password" version="3.1.0">
    <QuoteRequest insuranceType="False" serviceId="2029">
        <From company=" " residential="False" country="CA" zip="H8Z2Z3"/>
        <To company=" " residential="False" zip="H8Z2V4" country="CA"/>
        <Packages type="Package">
            <Package length="4" width="2" height="2" weight="9" type="Package"/>
        </Packages>
    </QuoteRequest>
</Freightcom>
"""

RateErrorResponseXML = f"""<Freightcom xmlns="http://www.freightcom.net/xml/XMLSchema" version="3.1.0">
    <ErrorReply>
        <Error Message="Required field: company is missing."/>
    </ErrorReply>
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
