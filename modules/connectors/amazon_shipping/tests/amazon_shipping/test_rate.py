import unittest
from unittest.mock import patch, ANY
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio import Rating
from .fixture import gateway


class TestAmazonShippingRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**PAYLOAD)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequestJSON)

    def test_get_rate(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = "{}"
            Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v1/rates",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.amazon_shipping.proxy.lib.request") as mock:
            mock.return_value = RateResponseJSON
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


PAYLOAD = {
    "reference": "order #1111",
    "recipient": {
        "company_name": "AmazonShipping",
        "address_line1": "417 Montgomery Street",
        "address_line2": "5th Floor",
        "city": "San Francisco",
        "state_code": "CA",
        "postal_code": "94104",
        "phone_number": "415-528-7555",
    },
    "shipper": {
        "person_name": "George Costanza",
        "company_name": "Vandelay Industries",
        "address_line1": "1 E 161st St.",
        "city": "Bronx",
        "state_code": "NY",
        "postal_code": "10451",
    },
    "parcels": [{"length": 9.0, "width": 6.0, "height": 2.0, "weight": 10.0}],
    "options": {"shipment_date": "2020-04-04"},
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "amazon_shipping",
            "carrier_name": "amazon_shipping",
            "currency": "GBP",
            "meta": {"service_name": "Amazon Shipping Standard"},
            "service": "amazon_shipping_standard",
            "total_charge": 3.25,
            "transit_days": 2,
        }
    ],
    [],
]


RateRequestJSON = {
    "containerSpecifications": [
        {
            "dimensions": {"height": 2.0, "length": 9.0, "unit": "IN", "width": 6.0},
            "weight": {"unit": "LB", "value": 10.0},
        }
    ],
    "shipDate": "2020-04-04T00:00:00.000000Z",
    "shipFrom": {
        "addressLine1": "1 E 161st St.",
        "city": "Bronx",
        "name": "George Costanza",
        "stateOrRegion": "NY",
    },
    "shipTo": {
        "addressLine1": "417 Montgomery Street",
        "addressLine2": "5th Floor",
        "city": "San Francisco",
        "phoneNumber": "415-528-7555",
        "stateOrRegion": "CA",
    },
}

RateResponseJSON = """{
  "serviceRates": [
    {
      "billableWeight": {
        "value": 4,
        "unit": "kg"
      },
      "totalCharge": {
        "value": 3.25,
        "unit": "GBP"
      },
      "serviceType": "Amazon Shipping Standard",
      "promise": {
        "deliveryWindow": {
          "start": "2018-08-25T20:22:30.737Z",
          "end": "2018-08-26T20:22:30.737Z"
        },
        "receiveWindow": {
          "start": "2018-08-23T09:22:30.737Z",
          "end": "2018-08-23T11:22:30.737Z"
        }
      }
    }
  ]
}
"""
