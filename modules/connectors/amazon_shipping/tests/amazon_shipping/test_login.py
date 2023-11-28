import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.lib as lib
import karrio.providers.amazon_shipping.utils as utils


class TestAmazonShippingLogin(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_login(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            parsed_response = utils.login(gateway.settings)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/authorization/v1/authorizationCode?developerId=DEVELOPER_ID&sellingPartnerId=SELLER_ID&mwsAuthToken=wJalrXUtnFEMI%2FK7MDENG%2FbPxRfiCYEXAMPLEKEY",
            )
            self.assertDictEqual(
                lib.to_dict(parsed_response),
                ParsedLoginResponse,
            )


if __name__ == "__main__":
    unittest.main()


ParsedLoginResponse = {
    "expiry": ANY,
    "authorizationCode": "authorizationCode",
    "payload": {"authorizationCode": "authorizationCode"},
}

LoginResponse = """{
    "payload": {"authorizationCode": "authorizationCode"}
}
"""
