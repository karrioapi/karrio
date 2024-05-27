import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio.core.errors import FieldError
from karrio import Rating
from .fixture import gateway


class TestEShipperRating(unittest.TestCase):
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

    @patch("karrio.mappers.eshipper_xml.proxy.http", return_value="<a></a>")
    def test_get_rates(self, http_mock):
        Rating.fetch(self.RateRequest).from_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(url, gateway.proxy.settings.server_url)

    def test_parse_rate_response(self):
        with patch("karrio.mappers.eshipper_xml.proxy.http") as mock:
            mock.return_value = RateResponseXml
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertListEqual(DP.to_dict(parsed_response), ParsedQuoteResponse)


if __name__ == "__main__":
    unittest.main()

RatePayload = {
    "shipper": {
        "company_name": "Test Company",
        "address_line1": "650 CIT Drive",
        "city": "Livingston",
        "postal_code": "L8E5X9",
        "country_code": "CA",
        "person_name": "Riz",
        "state_code": "ON",
        "phone_number": "9052223333",
        "residential": "true",
        "email": "riz@shaw.ca",
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
    "parcels": [
        {
            "height": 9,
            "length": 6,
            "width": 12,
            "weight": 2.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "description": "desc.",
            "packaging_type": "eshipper_pallet",
        }
    ],
    "options": {
        "eshipper_inside_delivery": True,
        "freight_class": "eshipper_freight_class_70",
        "cash_on_delivery": 10.5,
        "insurance": 70.0,
    },
}

RateWithPresetMissingDimensionPayload = {
    "shipper": {"postal_code": "H8Z2Z3", "country_code": "CA"},
    "recipient": {"postal_code": "H8Z2V4", "country_code": "CA"},
    "parcels": [{}],
}

ParsedQuoteResponse = [
    [
        {
            "carrier_id": "eshipper_xml",
            "carrier_name": "eshipper_xml",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 177.0, "currency": "CAD", "name": "Base charge"}
            ],
            "meta": {"rate_provider": "purolator", "service_name": "purolator_air"},
            "service": "eshipper_purolator_air",
            "total_charge": 177.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "eshipper_xml",
            "carrier_name": "eshipper_xml",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 28.65, "currency": "CAD", "name": "Base charge"}
            ],
            "meta": {"rate_provider": "purolator", "service_name": "purolator_ground"},
            "service": "eshipper_purolator_ground",
            "total_charge": 28.65,
            "transit_days": 1,
        },
        {
            "carrier_id": "eshipper_xml",
            "carrier_name": "eshipper_xml",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 46.27, "currency": "CAD", "name": "Base charge"},
                {"amount": 6.25, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "meta": {"rate_provider": "fedex", "service_name": "fedex_priority"},
            "service": "eshipper_fedex_priority",
            "total_charge": 52.52,
            "transit_days": 0,
        },
        {
            "carrier_id": "eshipper_xml",
            "carrier_name": "eshipper_xml",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 30.74, "currency": "CAD", "name": "Base charge"},
                {"amount": 1.08, "currency": "CAD", "name": "Other"},
            ],
            "meta": {"rate_provider": "fedex", "service_name": "fedex_ground"},
            "service": "eshipper_fedex_ground",
            "total_charge": 31.82,
            "transit_days": 0,
        },
        {
            "carrier_id": "eshipper_xml",
            "carrier_name": "eshipper_xml",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 300.0, "currency": "CAD", "name": "Base charge"},
                {"amount": 36.0, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "meta": {
                "rate_provider": "canada_worldwide",
                "service_name": "canada_worldwide_air_freight",
            },
            "service": "eshipper_canada_worldwide_air_freight",
            "total_charge": 336.0,
            "transit_days": 0,
        },
        {
            "carrier_id": "eshipper_xml",
            "carrier_name": "eshipper_xml",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 165.0, "currency": "CAD", "name": "Base charge"},
                {"amount": 19.8, "currency": "CAD", "name": "Fuel surcharge"},
            ],
            "meta": {
                "rate_provider": "canada_worldwide",
                "service_name": "canada_worldwide_next_flight_out",
            },
            "service": "eshipper_canada_worldwide_next_flight_out",
            "total_charge": 184.8,
            "transit_days": 0,
        },
    ],
    [],
]

RateRequestXML = f"""<EShipper xmlns="http://www.eshipper.net/XMLSchema" username="username" password="password" version="3.0.0">
    <QuoteRequest serviceId="0" insuranceType="True" insideDelivery="True">
        <From company="Test Company" email="riz@shaw.ca" attention="Riz" phone="9052223333" residential="true" address1="650 CIT Drive" city="Livingston" state="ON" country="CA" zip="L8E5X9"/>
        <To company="Test Company" email="riz@shaw.ca" attention="RizTo" phone="4162223333" residential="False" address1="650 CIT Drive" city="Livingston" state="BC" country="CA" zip="V3N4R3"/>
        <Packages type="Pallet">
            <Package length="3" width="5" height="4" weight="5" type="Pallet" description="desc."/>
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
