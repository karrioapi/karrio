import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import ShipmentRequest
from purplship.package import Shipment
from tests.freightcom.fixture import gateway


class TestFreightcomShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequestXML)

    def test_create_shipment(self):
        with patch("purplship.package.mappers.freightcom.proxy.http") as mock:
            mock.return_value = "<a></a>"
            Shipment.create(self.ShipmentRequest).with_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(url, gateway.settings.server_url)

    def test_parse_shipment_response(self):
        with patch("purplship.package.mappers.freightcom.proxy.http") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = (
                Shipment.create(self.ShipmentRequest).with_(gateway).parse()
            )

            self.assertEqual(to_dict(parsed_response), to_dict(ParsedShipmentResponse))


if __name__ == "__main__":
    unittest.main()

shipment_data = {
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "K1K4T3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "parcels": [{
        "height": 9,
        "length": 6,
        "width": 12,
        "weight": 20.0,
        "dimension_unit": "CM",
        "weight_unit": "KG",
    }],
    "service": "freightcom_central_transport",
    "options": {"cash_on_delivery": {"amount": 10.5}, "insurance": {"amount": 70.0},},
}

ParsedShipmentResponse = [
    {
        "carrier_id": "freightcom",
        "carrier_name": "freightcom",
        "label": "[base-64 encoded String]",
        "meta": {"carrier_name": "freightcom"},
        "selected_rate": {
            "base_charge": 30.74,
            "carrier_id": "freightcom",
            "carrier_name": "freightcom",
            "currency": "CAD",
            "transit_days": 0,
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "Fuel surcharge"},
                {"amount": 1.08, "currency": "CAD", "name": "Other"},
            ],
            "service": "freightcom_central_transport",
            "total_charge": 31.82,
        },
        "tracking_number": 52800410000484,
    },
    [],
]

ShipmentRequestXML = """<Freightcom xmlns="http://www.freightcom.net/XMLSchema" username="username" password="password" version="3.1.0">
    <ShippingRequest insuranceType="True" serviceId="2029">
        <From company="CGI" attention="Bob" phone="1 (450) 823-8432" residential="False" address1="502 MAIN ST N" city="MONTREAL" state="QC" country="CA" zip="H2B1A0"/>
        <To company="CGI" attention="Jain" residential="False" address1="23 jardin private" city="Ottawa" state="ON" zip="K1K4T3" country="CA"/>
        <COD paymentType="Recipient">
            <CODReturnAddress codCompany="CGI" codName="Jain" codAddress1="23 jardin private" codCity="Ottawa" codStateCode="ON" codZip="K1K4T3" codCountry="CA"/>
        </COD>
        <Packages type="Package">
            <Package length="6" width="12" height="9" weight="20" type="Boxes"/>
        </Packages>
    </ShippingRequest>
</Freightcom>
"""

ShipmentResponseXML = """<Freightcom xmlns="http://www.freightcom.net/XMLSchema" version="3.1.0">
    <ShippingReply>
        <Order id="181004" />
        <Carrier carrierName="Freightcom" serviceName="Central Transport" SCAC="RLCA" />
        <Reference code="XXXX567" name="TestReference" />
        <Package trackingNumber="052800410000484" />
        <Package trackingNumber="052800410000491" />
        <Pickup confirmationNumber ="XXXX56789" />
        <Labels>[base-64 encoded String]</Labels>
        <CustomsInvoice>[base-64 encoded String]</CustomsInvoice>
        <LabelData>
            <Label>
                <Type>PNG</Type>
                <Data>[base-64 encoded String]</Data>
            </Label>
            <Label>
                <Type>PNG</Type>
                <Data>[base-64 encoded String]</Data>
            </Label>
        </LabelData>
        <Quote carrierId="20" carrierName="Freightcom" serviceId="2029" serviceName="Central Transport" modeTransport="null" transitDays="0" baseCharge="30.739999771118164" fuelSurcharge="0.0" totalCharge="31.82" currency="CAD">
            <Surcharge id="null" name="Other" amount="1.0800000429153442"/>
        </Quote>
        <BillingAddress CompanyName="Freightcom Inc. FCPC (10)" Address1="7699 Bath Road" Address2="" City="Mississauga" ProvinceCode="ON" CountryCode="CA" zip="L4T3T1" PhoneNo="">
        </BillingAddress>
    </ShippingReply>
</Freightcom>
"""
