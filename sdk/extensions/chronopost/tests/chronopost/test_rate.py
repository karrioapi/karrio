import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestChronopostRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/quickcost-cxf/QuickcostServiceWS",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_rate_error_response(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = RateErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateErrorResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {"postal_code": "75001", "country_code": "FR"},
    "recipient": {"postal_code": "91210", "country_code": "FR"},
    "parcels": [
        {
            "weight": 4.0,
            "weight_unit": "KG",
        }
    ],
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "chronopost",
            "carrier_name": "chronopost",
            "currency": "EUR",
            "extra_charges": [{"amount": 1.2, "currency": "EUR", "name": "TVA"}],
            "meta": {"service_name": "chronopost_retrait_bureau"},
            "service": "chronopost_retrait_bureau",
            "total_charge": 7.2,
        }
    ],
    [],
]

ParsedRateErrorResponse = [
    [],
    [
        {
            "carrier_id": "chronopost",
            "carrier_name": "chronopost",
            "code": 3,
            "message": "invalid account or password",
        }
    ],
]


RateRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.quickcost.soap.chronopost.fr/">
    <soapenv:Body>
        <soapenv:calculateProducts>
            <accountNumber>1234</accountNumber>
            <password>password</password>
            <depCountryCode>FR</depCountryCode>
            <depZipCode>75001</depZipCode>
            <arrCountryCode>FR</arrCountryCode>
            <arrZipCode>91210</arrZipCode>
            <type>M</type>
            <weight>4.0</weight>
        </soapenv:calculateProducts>
    </soapenv:Body>
</soapenv:Envelope>
"""

RateResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns1:calculateProductsResponse xmlns:ns1="http://cxf.quickcost.soap.chronopost.fr/">
            <return>
                <errorCode>0</errorCode>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>5A</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>4T</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>4U</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>4I</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>2O</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>2L</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>1O</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>75</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>86</productCode>
                </productList>
                <productList>
                    <amount>6.0</amount>
                    <amountTTC>7.2</amountTTC>
                    <amountTVA>1.2</amountTVA>
                    <productCode>0</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>1</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>16</productCode>
                </productList>
                <productList>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <productCode>2</productCode>
                </productList>
            </return>
        </ns1:calculateProductsResponse>
    </soap:Body>
</soap:Envelope>
"""

RateErrorResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns1:calculateProductsResponse xmlns:ns1="http://cxf.quickcost.soap.chronopost.fr/">
            <return>
                <errorCode>3</errorCode>
                <errorMessage>invalid account or password</errorMessage>
            </return>
        </ns1:calculateProductsResponse>
    </soap:Body>
</soap:Envelope>
"""
