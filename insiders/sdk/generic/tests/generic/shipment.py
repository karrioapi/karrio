import unittest
from unittest.mock import patch
import purplship
from purplship.core.utils import DP
from purplship.core.models import ShipmentRequest
from tests.generic.fixture import gateway


class TestGenericShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None


if __name__ == "__main__":
    unittest.main()
