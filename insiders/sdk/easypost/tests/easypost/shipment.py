import unittest
from unittest.mock import patch, ANY
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from karrio import Shipment
from tests.easypost.fixture import gateway


class TestEasyPostShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**{})
        self.ShipmentCancelRequest = ShipmentCancelRequest(**{})


if __name__ == "__main__":
    unittest.main()
