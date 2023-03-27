import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.lib as lib
import karrio.providers.dpd.utils as utils


class TestDPDLogin(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_login(self):
        with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            parsed_response = utils.login(gateway.settings)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/soap/services/LoginService/V2_1",
            )
            self.assertEqual(
                mock.call_args[1]["data"],
                LoginRequest,
            )
            self.assertDictEqual(
                lib.to_dict(parsed_response),
                ParsedLoginResponse,
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse

            with self.assertRaises(Exception):
                utils.login(gateway.settings)


if __name__ == "__main__":
    unittest.main()


ParsedLoginResponse = {
    "expiry": ANY,
    "depot": "0530",
    "token": "GFadfGob14GWWgQcIldI6zYtuR7cyEHe2z6eWzb7BpFmcFvrzclRljlcV1OF",
}


LoginRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://dpd.com/common/service/types/LoginService/2.1">
    <soapenv:Header/>
    <soapenv:Body>
        <ns:getAuth>
            <delisId>KD*****</delisId>
            <password>****</password>
            <messageLanguage>en_EN</messageLanguage>
        </ns:getAuth>
    </soapenv:Body>
</soapenv:Envelope>
"""

LoginResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <soap:Body>
      <getAuthResponse xmlns="http://dpd.com/common/service/types/LoginService/2.1">
         <return>
            <delisId>KD*****</delisId>
            <customerUid>*******</customerUid>
            <authToken>GFadfGob14GWWgQcIldI6zYtuR7cyEHe2z6eWzb7BpFmcFvrzclRljlcV1OF</authToken>
            <depot>0530</depot>
            <authTokenExpires>2020-05-08T13:02:56.06</authTokenExpires>
         </return>
      </getAuthResponse>
   </soap:Body>
</soap:Envelope>
"""


ErrorResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
        <soap:Fault>
            <faultcode>soap:Server</faultcode>
            <faultstring>Fault occured</faultstring>
            <detail>
                <ns:authenticationFault
                    xmlns:ns="http://dpd.com/common/service/types/Authentication/2.0">
                    <errorCode>DELICOM_ERR_AUTHENTICATION</errorCode>
                    <errorMessage>Authentication failure, check delisId and password.</errorMessage>
                </ns:authenticationFault>
            </detail>
        </soap:Fault>
    </soap:Body>
</soap:Envelope>
"""
