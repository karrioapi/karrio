import unittest
from karrio.core.models import RateRequest


class TestAmazonMwsRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**{})


if __name__ == "__main__":
    unittest.main()
