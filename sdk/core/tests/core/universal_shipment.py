import unittest
from purplship.core.utils import DP, Serializable
from purplship.core.models import ShipmentRequest
from purplship.universal.mappers.shipping_proxy import (
    ShippingMixinSettings,
    ShippingMixinProxy,
)


class TestUniversalShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
