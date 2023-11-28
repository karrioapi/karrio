import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest


class TestFreightcomShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)
        self.ShipmentCancelRequest = ShipmentCancelRequest(**shipment_cancel_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequestXML)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequestXML)

    def test_create_shipment(self):
        with patch("karrio.mappers.freightcom.proxy.http") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(url, gateway.settings.server_url)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.freightcom.proxy.http") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(url, gateway.settings.server_url)

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.freightcom.proxy.http") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.freightcom.proxy.http") as mock:
            mock.return_value = ShipmentCancelResponseXML
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedCancelShipmentResponse)
            )


if __name__ == "__main__":
    unittest.main()

shipment_cancel_data = {"shipment_identifier": "383363"}

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
    "parcels": [
        {
            "height": 9,
            "length": 6,
            "width": 12,
            "weight": 20.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "service": "freightcom_central_transport",
    "options": {"cash_on_delivery": 10.5, "insurance": 70.0},
}

ParsedShipmentResponse = [
    {
        "carrier_id": "freightcom",
        "carrier_name": "freightcom",
        "docs": {"label": ANY, "invoice": ANY},
        "meta": {"rate_provider": "Freightcom", "service_name": "central_transport"},
        "selected_rate": {
            "carrier_id": "freightcom",
            "carrier_name": "freightcom",
            "currency": "CAD",
            "extra_charges": [
                {"amount": 30.74, "currency": "CAD", "name": "Base charge"},
                {"amount": 1.08, "currency": "CAD", "name": "Other"},
            ],
            "meta": {
                "rate_provider": "Freightcom",
                "service_name": "central_transport",
            },
            "service": "freightcom_central_transport",
            "total_charge": 31.82,
            "transit_days": 0,
        },
        "shipment_identifier": "181004",
        "tracking_number": "052800410000484",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "freightcom",
        "carrier_name": "freightcom",
        "operation": "Cancel Shipment",
        "success": True,
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
            <Package length="3" width="5" height="4" weight="45" type="Package"/>
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

ShipmentCancelRequestXML = """<Freightcom xmlns="http://www.freightcom.net/XMLSchema" username="username" password="password" version="3.1.0">
    <ShipmentCancelRequest>
        <Order orderId="383363"/>
    </ShipmentCancelRequest>
</Freightcom>
"""

ShipmentCancelResponseXML = """<Freightcom xmlns="http://www.freightcom.net/XMLSchema" version="3.1.0">
    <ShipmentCancelReply>
        <Order orderId="383363" message="Order has been cancelled!" />
        <Status statusId="4" />
    </ShipmentCancelReply>
</Freightcom>
"""
