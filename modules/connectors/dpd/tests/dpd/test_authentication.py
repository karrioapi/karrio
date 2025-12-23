import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import datetime
import karrio.lib as lib


class TestDPDAuthentication(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_authenticate(self):
        # Create a fresh gateway without cached auth to test the login flow
        import karrio.sdk as karrio

        fresh_gateway = karrio.gateway["dpd"].create(
            dict(
                delis_id="KD*****",
                password="****",
                test_mode=True,
            ),
        )

        with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
            mock.return_value = LoginResponse
            # Call authenticate directly on the proxy
            result = fresh_gateway.proxy.authenticate()
            parsed_response = result.deserialize()

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{fresh_gateway.settings.server_url}/soap/services/LoginService/V2_1",
            )
            self.assertEqual(
                mock.call_args[1]["data"],
                LoginRequest,
            )
            # Compare token returned
            self.assertEqual(
                parsed_response,
                "GFadfGob14GWWgQcIldI6zYtuR7cyEHe2z6eWzb7BpFmcFvrzclRljlcV1OF",
            )

    def test_parse_error_response(self):
        # Create a fresh gateway without cached auth to test the login flow
        import karrio.sdk as karrio

        fresh_gateway = karrio.gateway["dpd"].create(
            dict(
                delis_id="KD*****",
                password="****",
                test_mode=True,
            ),
        )

        with patch("karrio.mappers.dpd.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse

            with self.assertRaises(Exception):
                fresh_gateway.proxy.authenticate()


if __name__ == "__main__":
    unittest.main()


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
