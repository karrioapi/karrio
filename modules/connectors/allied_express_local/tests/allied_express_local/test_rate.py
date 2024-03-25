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
        with patch("karrio.mappers.allied_express_local.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/calculatePrice",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.allied_express_local.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.allied_express_local.proxy.lib.request") as mock:
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
    "services": ["allied_local_normal_service"],
    "options": {
        "instructions": "This is just an instruction",
    },
    "reference": "REF-001",
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "allied_express_local",
            "carrier_name": "allied_express_local",
            "currency": "AUD",
            "meta": {"service_name": "allied_local_normal_service"},
            "service": "allied_local_normal_service",
            "total_charge": 0.0,
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "allied_express_local",
            "carrier_name": "allied_express_local",
            "code": "500",
            "details": {},
            "message": "WRONG serviceLevel",
        }
    ],
]


RateRequest = {
    "account": "ACCOUNT",
    "bookedBy": "TEST USER",
    "readyDate": ANY,
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
    "serviceLevel": "N",
    "volume": 0.1,
    "weight": 40.0,
}

RateResponse = """{
  "soapenv:Envelope": {
    "@xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
    "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "soapenv:Body": {
      "ns1:quoteLocalCourierJobResponse": {
        "@xmlns:ns1": "http://neptune.alliedexpress.com.au/ttws-ejb",
        "result": {
          "account": {
            "accountCode": "ACCOUNT",
            "accountHash": "0Rpe7aSFxSt/DFYpqWPWhVp9ZhWZN/Pj3eC4tAqASjI=",
            "accountKey": "-900000",
            "accountLedger": "A",
            "accountName": "NORMA PACIFIC P/L",
            "accountState": "WA",
            "defaultAddress": "C/- ALLIED EXPRESS  881 ABERNETHY RD",
            "defaultContact": "SANDI WRIGHT",
            "defaultPhoneNo": "1300 252 677",
            "defaultPostCode": "6058",
            "defaultState": "WA",
            "defaultSuburbName": "FORRESTFIELD",
            "discountLevel": "0",
            "priceSuppressed": "false",
            "shippingDivision": "AET"
          },
          "bookedBy": "TESTING USER",
          "cubicWeight": "0.0",
          "docketNumber": "AET1021113",
          "instructions": "This is just an instruction",
          "itemCount": "2",
          "items": [
            {
              "dangerous": "false",
              "height": "50.0",
              "itemCount": "1",
              "length": "50.0",
              "volume": "0.036",
              "weight": "20.0",
              "width": "12.0"
            },
            {
              "dangerous": "true",
              "height": "50.0",
              "itemCount": "1",
              "length": "50.0",
              "volume": "0.036",
              "weight": "20.0",
              "width": "12.0"
            }
          ],
          "jobNumber": "-1",
          "jobStops": [
            {
              "companyName": "TESTING COMPANY",
              "contact": "FADI MUBARAK",
              "emailAddress": "test@gmail.com",
              "geographicAddress": {
                "address1": "17 VULCAN RD",
                "address2": "test",
                "country": "AU",
                "postCode": "6155",
                "sortCode": "PER",
                "state": "WA",
                "suburb": "CANNING VALE"
              },
              "stopNumber": "1",
              "stopType": "P"
            },
            {
              "companyName": "TESTING COMPANY",
              "contact": "TESTING USER",
              "emailAddress": "test@gmail.com",
              "geographicAddress": {
                "address1": "17 VULCAN RD",
                "address2": "test",
                "country": "AU",
                "postCode": "6155",
                "sortCode": "PER",
                "state": "WA",
                "suburb": "CANNING VALE"
              },
              "phoneNumber": "(07) 3114 1499",
              "stopNumber": "2",
              "stopType": "D"
            }
          ],
          "price": {
            "chargeQuantity": "0",
            "cubicFactor": "0",
            "discountRate": "0.0",
            "grossPrice": "0.0",
            "netPrice": "0.0",
            "reason": "No Hire time found"
          },
          "readyDate": "2024-01-31T16:06:07.000+11:00",
          "referenceNumbers": [
            "REF-001",
            "REF-001"
          ],
          "scheduledDeliveryDate": "2024-02-13T17:50:57.000+11:00",
          "serviceLevel": "N",
          "validatedHash": "edpLj6sbDhumb5N4RRUJ4njAq93IjyVsqD0sj1CQogE=",
          "vehicle": {
            "vehicleID": "-1"
          },
          "volume": "0.072",
          "weight": "41.0"
        }
      }
    }
  }
}
"""

ErrorResponse = """{
  "Message": "WRONG serviceLevel"
}
"""
