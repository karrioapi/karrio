import unittest
from unittest.mock import patch
from purplship.core.utils.helpers import to_dict
from purplship.core.models import ShipmentRequest
from purplship.package import shipment
from tests.caps.fixture import gateway


class TestCanadaPostShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**shipment_data)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequestXML)

    @patch("purplship.package.mappers.caps.proxy.http", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        shipment.create(self.ShipmentRequest).with_(gateway)

        url = http_mock.call_args[1]["url"]
        self.assertEqual(
            url,
            f"{gateway.settings.server_url}/rs/{gateway.settings.account_number}/{gateway.settings.account_number}/shipment",
        )

    def test_parse_shipment_response(self):
        with patch("purplship.package.mappers.caps.proxy.http") as mock:
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
            "caps_signature": True,
            "collect_on_delivery": True,
            "insurance": {
                "amount": 70.0
            }
        },
    },
}


ParsedShipmentResponse = [
    {
        "carrier": "CanadaPost",
        "charges": [
            {"amount": "9.19", "currency": "CAD", "name": "base-amount"},
            {"amount": "0.00", "currency": "CAD", "name": "gst-amount"},
            {"amount": "0", "currency": "CAD", "name": "pst-amount"},
            {"amount": "2.29", "currency": "CAD", "name": "hst-amount"},
            {"amount": "0.00", "currency": "CAD", "name": "AUTDISC"},
            {"amount": "0.90", "currency": "CAD", "name": "FUELSC"},
            {"amount": "0", "currency": "CAD", "name": "DC"},
            {"amount": "7.50", "currency": "CAD", "name": "UP"},
        ],
        "documents": ["https://XX/rs/artifact/11111111/5555555/0"],
        "reference": {"type": "Shipment Id", "value": "347881315405043891"},
        "service": "caps_expedited_parcel",
        "shipment_date": "2011-10-07",
        "total_charge": {
            "amount": "19.88",
            "currency": "CAD",
            "name": "Shipment charge",
        },
        "tracking_number": "12345",
    },
    [],
]


GetInfoRequestArgs = {
    "url": "https://XX/rs/111111111/2222222222/shipment/347881315405043891/price",
    "headers": {
        "Accept": "application/vnd.cpc.shipment-v8+xml",
        "Authorization": "Basic dXNlcm5hbWU6cGFzc3dvcmQ=",
        "Accept-language": "en-CA",
    },
    "method": "GET",
}


ShipmentPriceLinkXML = """
<link rel="price" href="https://XX/rs/111111111/2222222222/shipment/347881315405043891/price" media-type="application/vnd.cpc.shipment-v8+xml" />
"""


ShipmentRequestXML = """<shipment xmlns="http://www.canadapost.ca/ws/shipment-v8">
    <customer-request-id>1234567</customer-request-id>
    <requested-shipping-point>H2B1A0</requested-shipping-point>
    <provide-pricing-info>true</provide-pricing-info>
    <delivery-spec>
        <service-code>DOM.EP</service-code>
        <sender>
            <name>Bob</name>
            <company>CGI</company>
            <contact-phone>1 (450) 823-8432</contact-phone>
            <address-details>
                <address-line-1>502 MAIN ST N</address-line-1>
                <address-line-2></address-line-2>
                <city>MONTREAL</city>
                <prov-state>QC</prov-state>
                <country-code>CA</country-code>
                <postal-zip-code>H2B1A0</postal-zip-code>
            </address-details>
        </sender>
        <destination>
            <name>Jain</name>
            <company>CGI</company>
            <address-details>
                <address-line-1>23 jardin private</address-line-1>
                <address-line-2></address-line-2>
                <city>Ottawa</city>
                <prov-state>ON</prov-state>
                <country-code>CA</country-code>
                <postal-zip-code>K1K4T3</postal-zip-code>
            </address-details>
        </destination>
        <options>
            <option>
                <option-code>SO</option-code>
            </option>
            <option>
                <option-code>COV</option-code>
                <option-amount>70.0</option-amount>
            </option>
        </options>
        <parcel-characteristics>
            <weight>20.</weight>
            <dimensions>
                <length>6.0</length>
                <width>12.0</width>
                <height>9.0</height>
            </dimensions>
        </parcel-characteristics>
        <print-preferences>
            <output-format>8.5x11</output-format>
        </print-preferences>
        <preferences>
            <show-packing-instructions>true</show-packing-instructions>
            <show-postage-rate>true</show-postage-rate>
            <show-insured-value>true</show-insured-value>
        </preferences>
        <references>
            <customer-ref-1></customer-ref-1>
        </references>
    </delivery-spec>
</shipment>
"""


ShipmentResponseXML = """<shipment-info>
    <shipment-id>347881315405043891</shipment-id>
    <shipment-status>created</shipment-status>
    <tracking-pin>12345</tracking-pin>
    <links>
        <link rel="self" href="https://XX/rs/111111111/2222222222/shipment/347881315405043891" media-type="application/vnd.cpc.shipment-v8+xml" />
        <link rel="details" href="https://XX/rs/111111111/2222222222/shipment/347881315405043891/details" media-type="application/vnd.cpc.shipment-v8+xml" />
        <link rel="group" href="https://XX/rs/111111111/2222222222/shipment?groupid=bobo" media-type="application/vnd.cpc.shipment-v8+xml" />
        <link rel="price" href="https://XX/rs/111111111/2222222222/shipment/347881315405043891/price" media-type="application/vnd.cpc.shipment-v8+xml" />
        <link rel="label" href="https://XX/rs/artifact/11111111/5555555/0" media-type="application/pdf" index="0" />
    </links>
    <shipment-price>
        <service-code>DOM.EP</service-code>
        <base-amount>9.19</base-amount>
        <priced-options>
            <priced-option>
                <option-code>DC</option-code>
                <option-price>0</option-price>
            </priced-option>
            <priced-option>
                <option-code>UP</option-code>
                <option-price>7.50</option-price>
            </priced-option>
        </priced-options>
        <adjustments>
            <adjustment>
                <adjustment-code>AUTDISC</adjustment-code>
                <adjustment-amount>0.00</adjustment-amount>
            </adjustment>
            <adjustment>
                <adjustment-code>FUELSC</adjustment-code>
                <adjustment-amount>0.90</adjustment-amount>
            </adjustment>
        </adjustments>
        <pre-tax-amount>17.59</pre-tax-amount>
        <gst-amount>0.00</gst-amount>
        <pst-amount>0</pst-amount>
        <hst-amount>2.29</hst-amount>
        <due-amount>19.88</due-amount>
        <service-standard>
            <am-delivery>false</am-delivery>
            <guaranteed-delivery>true</guaranteed-delivery>
            <expected-transmit-time>2</expected-transmit-time>
            <expected-delivery-date>2011-10-07</expected-delivery-date>
        </service-standard>
        <rated-weight>10.000</rated-weight>
    </shipment-price>
</shipment-info>
"""
