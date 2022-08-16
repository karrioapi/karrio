import unittest
from unittest.mock import patch, ANY
from tests.chronopost.fixture import gateway

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
    "services": ["chronopost_retrait_bureau"],
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "chronopost",
            "carrier_name": "chronopost",
            "currency": "EUR",
            "extra_charges": [{"amount": 1.2, "currency": "EUR", "name": "TVA"}],
            "meta": {"service_name": "Sup.Retrait Bureau"},
            "service": "chronopost_sup_retrait_bureau",
            "total_charge": 7.2,
        }
    ],
    [],
]


RateRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.quickcost.soap.chronopost.fr/">
    <soapenv:Body>
        <soapenv:quickCost>
            <accountNumber>1234</accountNumber>
            <password>password</password>
            <depCode>75001</depCode>
            <arrCode>91210</arrCode>
            <weight>4.0</weight>
            <productCode>00</productCode>
        </soapenv:quickCost>
    </soapenv:Body>
</soapenv:Envelope>
"""

RateResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns1:quickCostResponse xmlns:ns1="http://cxf.quickcost.soap.chronopost.fr/">
            <return>
                <amount>6.0</amount>
                <amountTTC>7.2</amountTTC>
                <amountTVA>1.2</amountTVA>
                <errorCode>0</errorCode>
                <service>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <codeService>1</codeService>
                    <label>ESD en France métropolitaine</label>
                </service>
                <service>
                    <amount>6.0</amount>
                    <amountTTC>7.2</amountTTC>
                    <amountTVA>1.2</amountTVA>
                    <codeService>11</codeService>
                    <label>Sup.Retrait Bureau</label>
                </service>
                <service>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <codeService>15</codeService>
                    <label>Sup.Classic livr.du Samedi</label>
                </service>
                <service>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <codeService>4</codeService>
                    <label>Retour Express de Paiement</label>
                </service>
                <service>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <codeService>9</codeService>
                    <label>Supplement Corse</label>
                </service>
                <service>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <codeService>B1</codeService>
                    <label>Livr. Domicile privé</label>
                </service>
                <service>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <codeService>B1</codeService>
                    <label>Livr. Domicile privé</label>
                </service>
                <service>
                    <amount>0.0</amount>
                    <amountTTC>0.0</amountTTC>
                    <amountTVA>0.0</amountTVA>
                    <codeService>S9</codeService>
                    <label>Redevance Sûreté</label>
                </service>
                <zone>NT</zone>
                <assurance>
                    <plafond>0.0</plafond>
                    <taux>0.0</taux>
                </assurance>
            </return>
        </ns1:quickCostResponse>
    </soap:Body>
</soap:Envelope>
"""
