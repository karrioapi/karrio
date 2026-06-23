"""Amazon Shipping rating tests."""

import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.sdk as karrio

from .fixture import gateway


class TestAmazonShippingRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RATE_PAYLOAD)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertDictEqual(request.serialize(), RateRequestJSON)

    def test_get_rate(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v2/shipments/rates",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = RateResponseJSON
            parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertListEqual(
                lib.to_dict(parsed_response),
                ParsedRateResponse,
            )


if __name__ == "__main__":
    unittest.main()


RATE_PAYLOAD = {
    "reference": "order #1111",
    "recipient": {
        "company_name": "AmazonShipping",
        "address_line1": "417 Montgomery Street",
        "address_line2": "5th Floor",
        "city": "San Francisco",
        "state_code": "CA",
        "postal_code": "94104",
        "country_code": "US",
        "phone_number": "415-528-7555",
        "email": "test@example.com",
    },
    "shipper": {
        "person_name": "George Costanza",
        "company_name": "Vandelay Industries",
        "address_line1": "1 E 161st St.",
        "city": "Bronx",
        "state_code": "NY",
        "postal_code": "10451",
        "country_code": "US",
    },
    "parcels": [{"length": 9.0, "width": 6.0, "height": 2.0, "weight": 10.0}],
    "options": {"shipment_date": "2024-01-15"},
}

RateRequestJSON = {
    "shipFrom": {
        "name": "Vandelay Industries",
        "addressLine1": "1 E 161st St.",
        "companyName": "Vandelay Industries",
        "stateOrRegion": "NY",
        "city": "Bronx",
        "countryCode": "US",
        "postalCode": "10451",
    },
    "shipTo": {
        "name": "AmazonShipping",
        "addressLine1": "417 Montgomery Street",
        "addressLine2": "5th Floor",
        "companyName": "AmazonShipping",
        "stateOrRegion": "CA",
        "city": "San Francisco",
        "countryCode": "US",
        "postalCode": "94104",
        "email": "test@example.com",
        "phoneNumber": "415-528-7555",
    },
    "shipDate": "2024-01-15T00:00:00Z",
    "packages": [
        {
            "dimensions": {
                "length": 9.0,
                "width": 6.0,
                "height": 2.0,
                "unit": "INCH",
            },
            "weight": {
                "value": 10.0,
                "unit": "POUND",
            },
            "insuredValue": {"value": 0.0, "unit": "USD"},
            "packageClientReferenceId": "1",
        }
    ],
    "channelDetails": {
        "channelType": "EXTERNAL",
    },
    "labelSpecifications": {
        "format": "PNG",
        "size": {
            "length": 6,
            "width": 4,
            "unit": "INCH",
        },
        "dpi": 300,
        "pageLayout": "DEFAULT",
        "needFileJoining": False,
        "requestedDocumentTypes": ["LABEL"],
    },
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "amazon_shipping",
            "carrier_name": "amazon_shipping",
            "currency": "USD",
            "extra_charges": [{"amount": 5.25, "currency": "USD", "name": "Base Rate"}],
            "meta": {
                "carrier_id": "AMZN",
                "carrier_name": "Amazon",
                "rate_id": "rate-12345",
                "service_id": "AMZN_US_STD",
                "service_name": "Amazon Shipping Standard",
            },
            "service": "amazon_shipping_standard",
            "total_charge": 5.25,
        }
    ],
    [],
]


RateResponseJSON = """{
  "payload": {
    "rates": [
      {
        "rateId": "rate-12345",
        "carrierId": "AMZN",
        "carrierName": "Amazon",
        "serviceId": "AMZN_US_STD",
        "serviceName": "Amazon Shipping Standard",
        "totalCharge": {
          "value": 5.25,
          "unit": "USD"
        },
        "rateItemList": [
          {
            "rateItemID": "BASE",
            "rateItemNameLocalization": "Base Rate",
            "rateItemCharge": {
              "value": 5.25,
              "unit": "USD"
            }
          }
        ],
        "promise": {
          "deliveryWindow": {
            "start": "2024-01-17T18:00:00Z",
            "end": "2024-01-17T21:00:00Z"
          },
          "pickupWindow": {
            "start": "2024-01-15T09:00:00Z",
            "end": "2024-01-15T17:00:00Z"
          }
        }
      }
    ]
  }
}
"""
