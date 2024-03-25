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

        self.assertEqual(lib.to_dict(request.serialize()), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/calculatePrice",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.allied_express.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "person_name": "TEST USER",
        "state_code": "WA",
        "email": "test@gmail.com",
        "phone_number": "(07) 3114 1499",
    },
    "recipient": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "address_line2": "test",
        "city": "CANNING VALE",
        "postal_code": "6155",
        "country_code": "AU",
        "person_name": "TEST USER",
        "state_code": "WA",
        "email": "test@gmail.com",
    },
    "parcels": [
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "options": {"dangerous_good": False},
        },
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "options": {"dangerous_good": True},
        },
    ],
    "services": ["allied_road_service"],
    "options": {
        "instructions": "This is just an instruction",
    },
    "reference": "REF-001",
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "allied_express",
            "carrier_name": "allied_express",
            "currency": "AUD",
            "extra_charges": [
                {"amount": 14.18, "currency": "AUD", "name": "Job charge"}
            ],
            "meta": {"service_name": "allied_road_service"},
            "service": "allied_road_service",
            "total_charge": 40.66,
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "allied_express",
            "carrier_name": "allied_express",
            "code": "400",
            "details": {},
            "message": "Validation failed: java.lang.Exception: Exception thrown in "
            "SuburbDAO.getSuburb :java.lang.Exception: No valid JNDI name "
            "found for state UM",
        }
    ],
]


RateRequest = {
    "account": "ACCOUNT",
    "bookedBy": "TEST USER",
    "instructions": "This is just an instruction",
    "itemCount": 2,
    "items": [
        {
            "dangerous": False,
            "height": 50.0,
            "itemCount": 1,
            "length": 50.0,
            "volume": 0.1,
            "weight": 20.0,
            "width": 12.0,
        },
        {
            "dangerous": True,
            "height": 50.0,
            "itemCount": 1,
            "length": 50.0,
            "volume": 0.1,
            "weight": 20.0,
            "width": 12.0,
        },
    ],
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
        "phoneNumber": "(00) 0000 0000",
    },
    "jobStops_P": {
        "companyName": "TESTING COMPANY",
        "contact": "TEST USER",
        "emailAddress": "test@gmail.com",
        "geographicAddress": {
            "address1": "17 VULCAN RD",
            "address2": " ",
            "country": "AU",
            "postCode": "6155",
            "state": "WA",
            "suburb": "CANNING VALE",
        },
        "phoneNumber": "(07) 3114 1499",
    },
    "referenceNumbers": ["REF-001"],
    "serviceLevel": "R",
    "volume": 0.1,
    "weight": 40.0,
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

ErrorResponse = """{
    "soapenv:Envelope": {
        "@xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "soapenv:Body": {
            "ns1:calculatePriceResponse": {
                "@xmlns:ns1": "http://neptune.alliedexpress.com.au/ttws-ejb",
                "result": {
                    "errors": "Validation failed: java.lang.Exception: Exception thrown in SuburbDAO.getSuburb :java.lang.Exception: No valid JNDI name found for state UM",
                    "jobCharge": "0.0",
                    "totalCharge": "0.0"
                }
            }
        }
    }
}
"""
