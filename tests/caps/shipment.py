import unittest
from unittest.mock import patch
from gds_helpers import to_xml, export, jsonify, xml_tostring
from pycaps.shipment import ShipmentType
from pycaps.ncshipment import NonContractShipmentType
from purplship.domain.Types import ShipmentRequest
from purplship.mappers.caps import CanadaPostProxy
from tests.caps.fixture import proxy
from tests.utils import strip


MockedShipmentResponseXML = """<shipment-info>
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
</shipment-info>
"""


class TestCanadaPostShipment(unittest.TestCase):
    def setUp(self):
        self.Shipment = ShipmentType()
        self.Shipment.build(to_xml(ShipmentRequestXML))

        self.NCShipment = NonContractShipmentType()
        self.NCShipment.build(to_xml(NCShipmentRequestXML))

    def test_create_shipment_request(self):
        payload = ShipmentRequest(**shipment_data)
        Shipment_ = proxy.mapper.create_shipment_request(payload)
        self.assertEqual(export(Shipment_), export(self.Shipment))

    def test_create_ncshipment_request(self):
        payload = ShipmentRequest(**ncshipment_data)
        NCShipment_ = proxy.mapper.create_shipment_request(payload)
        # removed for testing purpose
        NCShipment_.delivery_spec.parcel_characteristics.document = None
        self.assertEqual(export(NCShipment_), export(self.NCShipment))

    @patch("purplship.mappers.caps.caps_proxy.http", return_value="<a></a>")
    def test_create_shipment(self, http_mock):
        proxy.create_shipment(self.Shipment)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(ShipmentRequestXML))

    @patch("purplship.mappers.caps.caps_proxy.http", return_value="<a></a>")
    def test_create_ncshipment(self, http_mock):
        proxy.create_shipment(self.NCShipment)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(NCShipmentRequestXML))

    def test_parse_shipment_response(self):
        parsed_response = proxy.mapper.parse_shipment_response(
            to_xml(ShipmentResponseXML)
        )
        self.assertEqual(jsonify(parsed_response), jsonify(ParsedShipmentResponse))

    def test_parse_ncshipment_response(self):
        parsed_response = proxy.mapper.parse_shipment_response(
            to_xml(NCShipmentResponseXML)
        )
        self.assertEqual(jsonify(parsed_response), jsonify(NCParsedShipmentResponse))

    @patch(
        "purplship.mappers.caps.caps_proxy.http", return_value=MockedShipmentResponseXML
    )
    def test_get_info_calls(self, http_mock):
        with patch.object(
            CanadaPostProxy, "_get_info", return_value="<a></a>"
        ) as get_info_mock:
            proxy_ = CanadaPostProxy(proxy.client)
            proxy_.create_shipment(self.NCShipment)

            link = xml_tostring(get_info_mock.call_args[0][0])
            self.assertEqual(strip(link), strip(ShipmentPriceLinkXML))

    @patch("purplship.mappers.caps.caps_proxy.http", return_value="<a></a>")
    def test_get_info(self, http_mock):
        proxy._get_info(to_xml(ShipmentPriceLinkXML))

        args = http_mock.call_args[1]
        self.assertEqual(jsonify(args), GetInfoRequestArgs)


if __name__ == "__main__":
    unittest.main()


NCParsedShipmentResponse = [
    {
        "carrier": "CanadaPost",
        "charges": [
            {"amount": "18.10", "currency": "CAD", "name": "base-amount"},
            {"amount": "0.00", "currency": "CAD", "name": "gst-amount"},
            {"amount": "0.00", "currency": "CAD", "name": "pst-amount"},
            {"amount": "2.53", "currency": "CAD", "name": "hst-amount"},
            {"amount": "1.36", "currency": "CAD", "name": "FUELSC"},
            {"amount": "0", "currency": "CAD", "name": "DC"},
        ],
        "documents": [
            "https://ct.soa-gw.canadapost.ca/rs/artifact/76108cb5192002d5/10238/0"
        ],
        "reference": {"type": "Shipment Id", "value": "406951321983787352"},
        "services": ["DOM.EP", "DC"],
        "shipment_date": "2012-03-14",
        "total_charge": {
            "amount": "21.99",
            "currency": "CAD",
            "name": "Shipment charge",
        },
        "tracking_numbers": ["12345678901234"],
    },
    [],
]

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
        "services": ["DOM.EP", "DC", "UP"],
        "shipment_date": "2011-10-07",
        "total_charge": {
            "amount": "19.88",
            "currency": "CAD",
            "name": "Shipment charge",
        },
        "tracking_numbers": ["12345"],
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
   <customer-request-id>123456789</customer-request-id>
   <cpc-pickup-indicator>true</cpc-pickup-indicator>
   <requested-shipping-point>K2B8J6</requested-shipping-point>
   <delivery-spec>
      <service-code>DOM.EP</service-code>
      <sender>
         <name>Bob</name>
         <company>CGI</company>
         <contact-phone>1 (450) 823-8432</contact-phone>
         <address-details>
            <address-line-1>502 MAIN ST N</address-line-1>
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
            <city>Ottawa</city>
            <prov-state>ON</prov-state>
            <country-code>CA</country-code>
            <postal-zip-code>K1K4T3</postal-zip-code>
         </address-details>
      </destination>
      <options>
         <option>
            <option-code>COD</option-code>
         </option>
      </options>
      <parcel-characteristics>
         <weight>20.</weight>
         <dimensions>
            <length>6</length>
            <width>12</width>
            <height>9</height>
         </dimensions>
         <mailing-tube>false</mailing-tube>
      </parcel-characteristics>
      <notification>
         <email>john.doe@yahoo.com</email>
         <on-shipment>true</on-shipment>
         <on-exception>false</on-exception>
         <on-delivery>true</on-delivery>
      </notification>
      <print-preferences>
         <output-format>8.5x11</output-format>
      </print-preferences>
      <preferences>
         <show-packing-instructions>true</show-packing-instructions>
         <show-postage-rate>false</show-postage-rate>
         <show-insured-value>true</show-insured-value>
      </preferences>
      <settlement-info>
         <contract-id>0040662505</contract-id>
         <intended-method-of-payment>Account</intended-method-of-payment>
      </settlement-info>
   </delivery-spec>
</shipment>
"""

ShipmentResponseXML = """<wrapper>
    <shipment-info>
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
    </shipment-info>
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
</wrapper>
"""

NCShipmentRequestXML = """<non-contract-shipment xmlns="http://www.canadapost.ca/ws/ncshipment-v4">
   <requested-shipping-point>J8R1A2</requested-shipping-point>
   <delivery-spec>
      <service-code>DOM.EP</service-code>
      <sender>
         <company>Canada Post Corporation</company>
         <contact-phone>555-555-5555</contact-phone>
         <address-details>
            <address-line-1>2701 Riverside Drive</address-line-1>
            <city>Ottawa</city>
            <prov-state>ON</prov-state>
            <postal-zip-code>K1A0B1</postal-zip-code>
         </address-details>
      </sender>
      <destination>
         <name>John Doe</name>
         <company>Consumer</company>
         <address-details>
            <address-line-1>2701 Receiver Drive</address-line-1>
            <city>Ottawa</city>
            <prov-state>ON</prov-state>
            <country-code>CA</country-code>
            <postal-zip-code>K1A0B1</postal-zip-code>
         </address-details>
      </destination>
      <options>
         <option>
            <option-code>COD</option-code>
         </option>
      </options>
      <parcel-characteristics>
         <weight>15.</weight>
         <dimensions>
            <length>1</length>
            <width>1</width>
            <height>1</height>
         </dimensions>
      </parcel-characteristics>
      <preferences>
         <show-packing-instructions>true</show-packing-instructions>
      </preferences>
   </delivery-spec>
</non-contract-shipment>
"""

NCShipmentResponseXML = """<wrapper>
    <non-contract-shipment-info>
        <shipment-id>406951321983787352</shipment-id>
        <tracking-pin>12345678901234</tracking-pin>
        <links>
            <link rel="self" href="https://ct.soa-gw.canadapost.ca/rs/0007023211/ncshipment/406951321983787352" media-type="application/vnd.cpc.ncshipment-v4+xml" />
            <link rel="details" href="https://ct.soa-gw.canadapost.ca/rs/0007023211/ncshipment/406951321983787352/details" media-type="application/vnd.cpc.ncshipment-v4+xml" />
            <link rel="receipt" href="https://ct.soa-gw.canadapost.ca/rs/0007023211/ncshipment/406951321983787352/receipt" media-type="application/vnd.cpc.ncshipment-v4+xml" />
            <link rel="label" href="https://ct.soa-gw.canadapost.ca/rs/artifact/76108cb5192002d5/10238/0" media-type="application/pdf" index="0" />
        </links>
    </non-contract-shipment-info>
    <non-contract-shipment-receipt>
        <final-shipping-point>J4W4T0</final-shipping-point>
        <shipping-point-name>BP BROSSARD</shipping-point-name>
        <shipping-point-id>0192</shipping-point-id>
        <mailed-by-customer>0001111111</mailed-by-customer>
        <service-code>DOM.EP</service-code>
        <rated-weight>15.000</rated-weight>
        <base-amount>18.10</base-amount>
        <pre-tax-amount>19.46</pre-tax-amount>
        <gst-amount>0.00</gst-amount>
        <pst-amount>0.00</pst-amount>
        <hst-amount>2.53</hst-amount>
        <priced-options>
            <priced-option>
                <option-code>DC</option-code>
                <option-price>0</option-price>
            </priced-option>
        </priced-options>
        <adjustments>
            <adjustment>
                <adjustment-code>FUELSC</adjustment-code>
                <adjustment-amount>1.36</adjustment-amount>
            </adjustment>
        </adjustments>
        <cc-receipt-details>
            <merchant-name>Canada Post Corporation</merchant-name>
            <merchant-url>www.canadapost.ca</merchant-url>
            <name-on-card>John Doe</name-on-card>
            <auth-code>076838</auth-code>
            <auth-timestamp>2012-03-13T08:27:20-05:00</auth-timestamp>
            <card-type>VIS</card-type>
            <charge-amount>21.99</charge-amount>
            <currency>CAD</currency>
            <transaction-type>Sale</transaction-type>
        </cc-receipt-details>
        <service-standard>
            <am-delivery>false</am-delivery>
            <guaranteed-delivery>true</guaranteed-delivery>
            <expected-transit-time>1</expected-transit-time>
            <expected-delivery-date>2012-03-14</expected-delivery-date>
        </service-standard>
    </non-contract-shipment-receipt>
</wrapper>
"""

shipment_data = {
    "shipper": {
        "company_name": "CGI",
        "address_lines": ["502 MAIN ST N"],
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
        "account_number": "123456789",
    },
    "recipient": {
        "company_name": "CGI",
        "address_lines": ["23 jardin private"],
        "city": "Ottawa",
        "postal_code": "K1K4T3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "shipment": {
        "items": [{"height": 9, "length": 6, "width": 12, "weight": 20.0}],
        "label": {"format": "8.5x11"},
        "services": ["Expedited_Parcel"],
        "dimension_unit": "CM",
        "weight_unit": "KG",
        "options": [{"code": "Collect_on_delivery"}],
        "extra": {
            "cpc-pickup-indicator": True,
            "requested-shipping-point": "K2B8J6",
            "mailing-tube": False,
            "notification": {
                "email": "john.doe@yahoo.com",
                "on-shipment": True,
                "on-exception": False,
                "on-delivery": True,
            },
            "preferences": {
                "show-packing-instructions": True,
                "show-postage-rate": False,
                "show-insured-value": True,
            },
            "settlement-info": {
                "contract-id": "0040662505",
                "intended-method-of-payment": "Account",
            },
        },
    },
}

ncshipment_data = {
    "shipper": {
        "company_name": "Canada Post Corporation",
        "address_lines": ["2701 Riverside Drive"],
        "city": "Ottawa",
        "postal_code": "K1A0B1",
        "phone_number": "555-555-5555",
        "account_number": "123456789",
        "state_code": "ON",
    },
    "recipient": {
        "company_name": "Consumer",
        "address_lines": ["2701 Receiver Drive"],
        "city": "Ottawa",
        "postal_code": "K1A0B1",
        "country_code": "CA",
        "person_name": "John Doe",
        "state_code": "ON",
    },
    "shipment": {
        "items": [{"height": 1, "length": 1, "width": 1, "weight": 15.0}],
        "dimension_unit": "CM",
        "weight_unit": "KG",
        "services": ["Expedited_Parcel"],
        "options": [{"code": "Collect_on_delivery"}],
        "extra": {
            "requested-shipping-point": "J8R1A2",
            "preferences": {"show-packing-instructions": True},
        },
    },
}
