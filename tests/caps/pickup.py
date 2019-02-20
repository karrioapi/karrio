import unittest
from unittest.mock import patch
import time
from gds_helpers import to_xml, jsonify, export
from pycaps.pickuprequest import PickupRequestDetailsType
from tests.caps.fixture import proxy
from tests.utils import strip


class TestPickup(unittest.TestCase):
    def setUp(self):
        self.PickupRequest = PickupRequestDetailsType()
        self.PickupRequest.build(to_xml(PickupRequestXml))

    @patch("purplship.mappers.caps.caps_proxy.http", return_value="<a></a>")
    def test_request_pickup(self, http_mock):
        proxy.request_pickup(self.PickupRequest)

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(PickupRequestXml))

    @patch.object(proxy, "request_pickup")
    def test_modify_pickup(self, proxy_mock):
        proxy.modify_pickup(self.PickupRequest)

        proxy_mock.assert_called()


if __name__ == "__main__":
    unittest.main()

PickupRequestXml = """<pickup-request-details xmlns="http://www.canadapost.ca/ws/pickuprequest">
  <pickup-type>OnDemand</pickup-type>
  <pickup-location>
    <business-address-flag>false</business-address-flag>
    <alternate-address>
      <company>Jim Duggan</company>
      <address-line-1>2271 Herring Cove</address-line-1>
      <city>Halifax</city><province>NS</province>
      <postal-code>B3L2C2</postal-code>
    </alternate-address>
  </pickup-location>
  <contact-info>
    <contact-name>John Doe</contact-name>
    <email>john.doe@canadapost.ca</email>
    <contact-phone>800-555-1212</contact-phone>
    <receive-email-updates-flag>true</receive-email-updates-flag>
  </contact-info>
  <location-details>
    <five-ton-flag>false</five-ton-flag>
    <loading-dock-flag>true</loading-dock-flag>
    <pickup-instructions>Door at Back</pickup-instructions>
  </location-details>
  <items-characteristics>
    <pww-flag>true</pww-flag>
    <priority-flag>false</priority-flag>
    <returns-flag>true</returns-flag>
    <heavy-item-flag>true</heavy-item-flag>
  </items-characteristics>
  <pickup-volume>50</pickup-volume>
  <pickup-times>
    <on-demand-pickup-time>
      <date>2015-01-28</date>
      <preferred-time>14:00</preferred-time>
      <closing-time>17:00</closing-time>
    </on-demand-pickup-time>
  </pickup-times>
</pickup-request-details>
"""
