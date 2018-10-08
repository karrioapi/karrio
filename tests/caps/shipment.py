import unittest
from unittest.mock import patch
import time
from gds_helpers import to_xml
from pycaps.shipment import ShipmentType
from pycaps.ncshipment import NonContractShipmentType
from purplship.domain.entities import Shipment
from tests.caps.fixture import proxy
from tests.utils import strip


class TestShipment(unittest.TestCase):
    def setUp(self):
        self.Shipment = ShipmentType()
        self.Shipment.build(to_xml(ShipmentRequestXML))

        self.NCShipment = NonContractShipmentType()
        self.NCShipment.build(to_xml(NCShipmentRequestXML))

    @patch("purplship.mappers.caps.caps_proxy.http", return_value='<a></a>')
    def test_create_shipment(self, http_mock):
        proxy.create_shipment(self.Shipment)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(ShipmentRequestXML))

    @patch("purplship.mappers.caps.caps_proxy.http", return_value='<a></a>')
    def test_create_ncshipment(self, http_mock):
        proxy.create_shipment(self.NCShipment)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(NCShipmentRequestXML))


if __name__ == '__main__':
    unittest.main()

ShipmentRequestXML = """<shipment xmlns="http://www.canadapost.ca/ws/shipment-v8">
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
            <option-code>DC</option-code>
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
            <option-code>DC</option-code>
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