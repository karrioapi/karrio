import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAlliedExpressRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {}

ParsedRateResponse = []


RateRequest = {
    "bookedBy": "TEST USER",
    "account": "ACCOUNT",
    "instructions": "This is just an instruction",
    "itemCount": 2,
    "items": [
        {
            "dangerous": False,
            "height": 50,
            "itemCount": 1,
            "length": 50,
            "volume": 0.036,
            "weight": 20,
            "width": 12,
        },
        {
            "dangerous": True,
            "height": 50,
            "itemCount": 1,
            "length": 50,
            "volume": 0.036,
            "weight": 20,
            "width": 12,
        },
    ],
    "jobStops_P": {
        "companyName": "TESTING COMPANY",
        "contact": "TEST USER",
        "emailAddress": "test@gmail.com",
        "geographicAddress": {
            "address1": "17 VULCAN RD",
            "address2": "test",
            "country": "AU",
            "postCode": "6155",
            "state": "WA",
            "suburb": "CANNING VALE",
        },
        "phoneNumber": "(07) 3114 1499",
    },
    "jobStops_D": {
        "companyName": "TESTING COMPANY",
        "contact": "TEST USER",
        "emailAddress": "test@gmail.com",
        "geographicAddress": {
            "address1": "17 VULCAN RD",
            "address2": "test",
            "country": "AU",
            "postCode": "6155",
            "state": "WA",
            "suburb": "CANNING VALE",
        },
        "phoneNumber": "(07) 3114 1499",
    },
    "referenceNumbers": ["REF-001", "REF-001"],
    "serviceLevel": "R",
    "volume": 0.072,
    "weight": 41,
}

RateResponse = """{
    "soapenv:Envelope": {
        "@xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "soapenv:Body": {
            "ns1:calculatePriceResponse": {
                "@xmlns:ns1": "http://neptune.alliedexpress.com.au/ttws-ejb",
                "result": {
                    "jobCharge": "14.18",
                    "surcharges": [
                        {
                            "chargeCode": "ON FWD PICKUP",
                            "description": "ON FORWARD PICKUP",
                            "netValue": "0.0",
                            "quantity": "1"
                        },
                        {
                            "chargeCode": "ON FWD DELIVERY",
                            "description": "ON FORWARD DELIVERY",
                            "netValue": "0.0",
                            "quantity": "1"
                        },
                        {
                            "chargeCode": "HD",
                            "description": "FREIGHT OVERSIZED HOME DELIVERY",
                            "netValue": "0.0",
                            "quantity": "1"
                        },
                        {
                            "chargeCode": "LSC",
                            "description": "LENGTH SURCHARGE",
                            "netValue": "0.0",
                            "quantity": "1"
                        },
                        {
                            "chargeCode": "MHF",
                            "description": "HANDLING FEE",
                            "netValue": "0.0",
                            "quantity": "1"
                        }
                    ],
                    "totalCharge": "40.66"
                }
            }
        }
    }
}
"""
