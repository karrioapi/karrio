import unittest
from unittest.mock import patch, ANY
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from karrio import Shipment
from tests.amazon_mws.fixture import gateway


class TestAmazonMwsShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**{})
        self.ShipmentCancelRequest = ShipmentCancelRequest(**{})


if __name__ == "__main__":
    unittest.main()
