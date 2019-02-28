import unittest
from unittest.mock import patch
from purplship.domain import interface as purplship
from tests.caps.fixture import proxy as caps
from tests.ups.fixture import proxy as ups
from tests.caps.shipment import shipment_data, ShipmentRequestXML
from tests.caps.tracking import TrackingRequestURL
from tests.ups.quote import rate_req_data, RateRequestXML
from tests.utils import strip


class TestFluentInterface(unittest.TestCase):

    @patch("purplship.mappers.caps.caps_proxy.http", return_value="<a></a>")
    def test_shipment_create(self, http_mock):
        purplship.shipment.create(**shipment_data).with_(caps).parse()

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(ShipmentRequestXML))

    @patch("purplship.mappers.ups.ups_proxy.http", return_value="<a></a>")
    def test_rating_fetch(self, http_mock):
        purplship.rating.fetch(**rate_req_data).from_(ups).parse()

        xmlStr = http_mock.call_args[1]["data"].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(RateRequestXML))

    @patch("purplship.mappers.caps.caps_proxy.http", return_value="<a></a>")
    def test_tracking_fetch(self, http_mock):
        purplship.tracking.fetch(tracking_numbers=["1Z12345E6205277936"]).from_(caps).parse()

        reqUrl = http_mock.call_args[1]["url"]
        self.assertEqual(reqUrl, TrackingRequestURL)
