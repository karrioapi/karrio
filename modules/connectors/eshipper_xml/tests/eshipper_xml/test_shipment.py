import unittest
from unittest.mock import patch, ANY
import karrio
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from .fixture import gateway


class TestEShipperShipment(unittest.TestCase):
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
        with patch("karrio.mappers.eshipper_xml.proxy.http") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(url, gateway.settings.server_url)

    def test_cancel_shipment(self):
        with patch("karrio.mappers.eshipper_xml.proxy.http") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(url, gateway.settings.server_url)

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.eshipper_xml.proxy.http") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(DP.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.eshipper_xml.proxy.http") as mock:
            mock.return_value = ShipmentCancelResponseXML
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()

shipment_cancel_data = {"shipment_identifier": "383363"}

shipment_data = {
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
            "freight_class": "70",
            "options": {"insurance": 100},
        }
    ],
    "service": "eshipper_fedex_ground",
    "options": {
        "cash_on_delivery": 10.5,
        "insurance": 70.0,
    },
    "customs": {
        "duty": {"paid_by": "recipient"},
        "commodities": [
            {
                "sku": "098765",
                "hs_code": "1234",
                "title": "Laptop computer",
                "origin_country": "US",
                "quantity": 100,
                "value_amount": 1000.00,
            }
        ],
    },
    "payment": {"paid_by": "third_party"},
}

ParsedShipmentResponse = [
    {
        "carrier_id": "eshipper_xml",
        "carrier_name": "eshipper_xml",
        "docs": {"label": ANY, "invoice": ANY},
        "meta": {
            "rate_provider": "fedex",
            "service_name": "fedex_ground",
            "tracking_url": "http://www.fedex.com/Tracking?tracknumbers=052800410000484",
        },
        "selected_rate": {
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
        "shipment_identifier": "181004",
        "tracking_number": "052800410000484",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "eshipper_xml",
        "carrier_name": "eshipper_xml",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequestXML = """<EShipper xmlns="http://www.eshipper.net/XMLSchema" username="username" password="password" version="3.0.0">
    <ShippingRequest serviceId="3" insuranceType="True">
        <From company="Test Company" email="riz@shaw.ca" attention="Riz" phone="9052223333" residential="true" address1="650 CIT Drive" city="Livingston" state="ON" country="CA" zip="L8E5X9"/>
        <To company="Test Company" email="riz@shaw.ca" attention="RizTo" phone="4162223333" residential="False" address1="650 CIT Drive" city="Livingston" state="BC" country="CA" zip="V3N4R3"/>
        <COD paymentType="Receiver">
            <CODReturnAddress codCompany="Test Company" codName="RizTo" codAddress1="650 CIT Drive" codCity="Livingston" codStateCode="BC" codZip="V3N4R3" codCountry="CA"/>
        </COD>
        <Packages type="Pallet">
            <Package length="3" width="5" height="4" weight="5" type="Pallet" freightClass="70" insuranceAmount="100." description="desc."/>
        </Packages>
        <Payment type="3rd Party"/>
        <CustomsInvoice contactCompany="Test Company" contactName="RizTo" contactPhone="4162223333">
            <BillTo company="Test Company" name="RizTo" address1="650 CIT Drive" city="Livingston" state="BC" zip="V3N4R3" country="CA"/>
            <Contact name="RizTo" phone="4162223333"/>
            <Item code="1234" description="Laptop computer" originCountry="US" quantity="100" unitPrice="1000." skuCode="098765"/>
            <DutiesTaxes dutiable="Yes" billTo="Receiver"/>
        </CustomsInvoice>
    </ShippingRequest>
</EShipper>
"""

ShipmentResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<EShipper xmlns="http://www.eshipper.net/xml/XMLSchema" version="3.0.0">
    <ShippingReply>
        <Order id="181004" />
        <Carrier carrierName="Federal Express" serviceName="FedEx Ground" />
        <Reference code="1234567" name="RizReference" />
        <Package trackingNumber="052800410000484" />
        <Package trackingNumber="052800410000491" />
        <Pickup confirmationNumber ="123456789" />
        <TrackingURL>http://www.fedex.com/Tracking?tracknumbers=052800410000484</TrackingURL>
        <Labels>[base-64 encoded String]</Labels>
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
        <CustomsInvoice>[base-64 encoded String]</CustomsInvoice>
        <Quote carrierId="1" carrierName="Federal Express" serviceId="3" serviceName="Ground" modeTransport="null" transitDays="0" baseCharge="30.739999771118164" fuelSurcharge="0.0" totalCharge="31.82" currency="CAD">
            <Surcharge id="null" name="Other" amount="1.0800000429153442"/>
        </Quote>
    </ShippingReply>
</EShipper>
"""

ShipmentCancelRequestXML = """<EShipper xmlns="http://www.eshipper.net/XMLSchema" username="username" password="password" version="3.0.0">
    <ShipmentCancelRequest>
        <Order orderId="383363"/>
    </ShipmentCancelRequest>
</EShipper>
"""

ShipmentCancelResponseXML = """<EShipper xmlns="http://www.eshipper.net/xml/XMLSchema" version="3.0.0">
    <ShipmentCancelReply>
        <Order orderId="383363" message="Order has been cancelled!" />
        <Status statusId="4" />
    </ShipmentCancelReply>
</EShipper>
"""
