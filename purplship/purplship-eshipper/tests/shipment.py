import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import ShipmentRequest
from purplship.package import shipment
from tests.fixture import gateway


class TestEShipperShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequestXML)

    def test_create_shipment(self):
        with patch("purplship.extension.mappers.eshipper.proxy.http") as mock:
            mock.return_value = "<a></a>"
            shipment.create(self.ShipmentRequest).with_(gateway)

            url = mock.call_args[1]["url"]
            self.assertEqual(url, gateway.settings.server_url)

    def test_parse_shipment_response(self):
        with patch("purplship.extension.mappers.eshipper.proxy.http") as mock:
            mock.return_value = ShipmentResponseXML
            parsed_response = (
                shipment.create(self.ShipmentRequest).with_(gateway).parse()
            )

            self.assertEqual(to_dict(parsed_response), to_dict(ParsedShipmentResponse))


if __name__ == "__main__":
    unittest.main()

shipment_data = {
    "shipper": {
        "company_name": "CGI",
        "address_line_1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line_1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "K1K4T3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "parcel": {
        "height": 9,
        "length": 6,
        "width": 12,
        "weight": 20.0,
        "services": ["caps_expedited_parcel"],
        "dimension_unit": "CM",
        "weight_unit": "KG",
        "options": {
            "cash_on_delivery": {"amount": 10.5},
            "insurance": {"amount": 70.0},
        },
    },
}

ParsedShipmentResponse = [
    {
        "carrier": "EShipper",
        "label": "[base-64 encoded String]",
        "selected_rate": {
            "base_charge": 30.739999771118164,
            "carrier": "EShipper",
            "currency": "CAD",
            "estimated_delivery": 0,
            "extra_charges": [
                {"amount": 0.0, "currency": "CAD", "name": "Fuel Surcharge"}
            ],
            "service": "eshipper_central_transport",
            "total_charge": 31.82,
        },
        "tracking_number": 52800410000484,
    },
    [],
]

ShipmentRequestXML = """<EShipper xmlns="http://www.eshipper.net/XMLSchema" username="merchantinc." password="abcd" version="3.0.0">
    <ShippingRequest serviceId="3" stackable="true">
        <From id="123" company="Test Company" address1="650 CIT Drive" city="Livingston" state="ON" zip="L8E5X9" country="CA" phone="9052223333" attention="Riz" email="riz@shaw.ca" residential="true" />
        <To company="Test Company" address1="650 CIT Drive" city="Livingston" state="BC" zip="V3N4R3" country="CA" phone="4162223333" attention="RizTo" email="riz@shaw.ca"/>
        <COD paymentType="Check">
            <CODReturnAddress codCompany="ABC Towing" codName="Alfred" codAddress1="444 Highway 401" codCity="Toronto" codStateCode="On" codZip="A1B2C3" codCountry="CA"/>
        </COD>
        <Packages type="Package">
            <Package length="15" width="10" height="12" weight="12" type="Pallet" freightClass="70" insuranceAmount="0.0" codAmount="0.0" description="desc."/>
            <Package length="15" width="10" height="10" weight="14" type="Pallet" freightClass="70" nmfcCode="123456" insuranceAmount="0.0" codAmount="0.0" description="desc."/>
        </Packages>
        <Pickup contactName="Test Name" phoneNumber="888-888-8888" pickupDate="2009-08-03" pickupTime="16:30" closingTime="17:45" location="Front Door"/>
        <Payment type="3rd Party" />
        <Reference name="" code="123456" />
        <Reference name="" code="" />
        <Reference name="" code="" />
        <CustomsInvoice brokerName="John Doe" contactCompany="MERITCON INC" contactName="Jim">
            <BillTo company="ABC Towing" name="Alfred" address1="444 Highway 401" city="Toronto" state="ON" zip="A1B 2C3" country="CA" />
            <Contact name="Rizwan" phone="555-555-4444" />
            <Item code="1234" description="Laptop computer" originCountry="US" quantity="100" unitPrice="1000.00"/>
            <DutiesTaxes dutiable="true" billTo="receiver" />
            <InBondManifest locationOfGoods="CANADA WORLDWIDE SLC4358" nameOfCarrier="AIR CANADA" vehicleIdentification="12345" customsClearedBy="CANADA WORLDWIDE" handlingInfo="CANADA WORLDWIDE SERVICES INC. TO ARRANGE DELIVERY" previousCargoControlNum="1234" weight="12.34" weightUOM="LBS"/>
        </CustomsInvoice>
    </ShippingRequest>
</EShipper>
"""

ShipmentResponseXML = """<EShipper xmlns="http://www.eshipper.net/xml/XMLSchema" version="3.0.0">
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
