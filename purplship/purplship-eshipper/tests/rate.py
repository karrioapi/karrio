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
    "shipper": {
        "id": "123",
        "company_name": "Test Company",
        "address_line1": "650 CIT Drive",
        "city": "Livingston",
        "postal_code": "L8E5X9",
        "country_code": "CA",
        "person_name": "Riz",
        "state_code": "ON",
        "phone_number": "9052223333",
        "residential": "true",
        "email": "riz@shaw.ca"
    },
    "recipient": {
        "company_name": "Test Company",
        "address_line1": "650 CIT Drive",
        "city": "Livingston",
        "postal_code": "V3N4R3",
        "person_name": "RizTo",
        "country_code": "CA",
        "state_code": "BC",
        "phone_number": "4162223333",
        "email": "riz@shaw.ca",
    },
    "parcel": {
        "height": 9,
        "length": 6,
        "width": 12,
        "weight": 20.0,
        "description": "desc.",
        "packaging_type": "eshipper_pallet"
    },
    "options": {
        "freight_class": "eshipper_freight_class_70",
        "cash_on_delivery": {"amount": 10.5},
        "insurance": {"amount": 70.0},
    },
}

RateWithPresetMissingDimensionPayload = {
    "shipper": {"postal_code": "H8Z2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcel": {},
}

ParsedQuoteResponse = [[{'base_charge': 177.0, 'carrier': 'eshipper', 'carrier_name': 'eShipper', 'currency': 'CAD', 'estimated_delivery': '1', 'extra_charges': [{'amount': 0.0, 'currency': 'CAD', 'name': 'Fuel surcharge'}], 'service': 'eshipper_purolator_air', 'total_charge': 177.0}, {'base_charge': 28.65, 'carrier': 'eshipper', 'carrier_name': 'eShipper', 'currency': 'CAD', 'estimated_delivery': '1', 'extra_charges': [{'amount': 0.0, 'currency': 'CAD', 'name': 'Fuel surcharge'}], 'service': 'eshipper_purolator_ground', 'total_charge': 28.65}, {'base_charge': 46.27, 'carrier': 'eshipper', 'carrier_name': 'eShipper', 'currency': 'CAD', 'estimated_delivery': '0', 'extra_charges': [{'amount': 6.25, 'currency': 'CAD', 'name': 'Fuel surcharge'}], 'service': 'eshipper_fedex_priority', 'total_charge': 52.52}, {'base_charge': 30.74, 'carrier': 'eshipper', 'carrier_name': 'eShipper', 'currency': 'CAD', 'estimated_delivery': '0', 'extra_charges': [{'amount': 0.0, 'currency': 'CAD', 'name': 'Fuel surcharge'}], 'service': 'eshipper_fedex_ground', 'total_charge': 31.82}, {'base_charge': 300.0, 'carrier': 'eshipper', 'carrier_name': 'eShipper', 'currency': 'CAD', 'estimated_delivery': '0', 'extra_charges': [{'amount': 36.0, 'currency': 'CAD', 'name': 'Fuel surcharge'}], 'service': 'eshipper_canada_worldwide_air_freight', 'total_charge': 336.0}, {'base_charge': 165.0, 'carrier': 'eshipper', 'carrier_name': 'eShipper', 'currency': 'CAD', 'estimated_delivery': '0', 'extra_charges': [{'amount': 19.8, 'currency': 'CAD', 'name': 'Fuel surcharge'}], 'service': 'eshipper_canada_worldwide_next_flight_out', 'total_charge': 184.8}], []]

RateRequestXML = f"""<EShipper xmlns="http://www.eshipper.net/XMLSchema" username="username" password="password" version="3.0.0">
    <QuoteRequest insuranceType="True" serviceId="0">
        <From id="123" company="Test Company" email="riz@shaw.ca" attention="Riz" phone="9052223333" residential="true" address1="650 CIT Drive" city="Livingston" state="ON" country="CA" zip="L8E5X9"/>
        <To company="Test Company" email="riz@shaw.ca" attention="RizTo" phone="4162223333" residential="False" address1="650 CIT Drive" city="Livingston" state="BC" zip="V3N4R3" country="CA"/>
        <Packages>
            <Package length="6" width="12" height="9" weight="20" type="Pallet" description="desc."/>
        </Packages>
    </QuoteRequest>
</EShipper>
"""

RateResponseXml = """<?xml version="1.0" encoding="UTF-8"?>
<EShipper xmlns="http://www.eshipper.net/XMLSchema" version="3.0.0">
   <QuoteReply>
      <Quote carrierId="2" carrierName="Purolator" serviceId="4" serviceName="Air" modeTransport="A" transitDays="1" baseCharge="177.0" fuelSurcharge="0.0" totalCharge="177.0" currency="CAD" />
      <Quote carrierId="2" carrierName="Purolator" serviceId="13" serviceName="Ground" modeTransport="G" transitDays="1" baseCharge="28.650000000000002" fuelSurcharge="0.0" totalCharge="28.65" currency="CAD" />
      <Quote carrierId="1" carrierName="Federal Express" serviceId="1" serviceName="Priority" modeTransport="null" transitDays="0" baseCharge="46.27000045776367" fuelSurcharge="6.25" totalCharge="52.52" currency="CAD" />
      <Quote carrierId="1" carrierName="Federal Express" serviceId="3" serviceName="Ground" modeTransport="null" transitDays="0" baseCharge="30.739999771118164" fuelSurcharge="0.0" totalCharge="31.82" currency="CAD">
         <Surcharge id="null" name="Other" amount="1.0800000429153442" />
      </Quote>
      <Quote carrierId="3" carrierName="Canada WorldWide" serviceId="16" serviceName="Air Freight" modeTransport="null" transitDays="0" baseCharge="300.0" fuelSurcharge="36.0" totalCharge="336.0" currency="CAD" />
      <Quote carrierId="3" carrierName="Canada WorldWide" serviceId="15" serviceName="Next Flight Out" modeTransport="null" transitDays="0" baseCharge="165.0" fuelSurcharge="19.8" totalCharge="184.8" currency="CAD" />
   </QuoteReply>
</EShipper>
"""
