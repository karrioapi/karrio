import datetime
import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
# from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestFreightcomRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)
        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.freightcom.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rate",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.freightcom.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "company_name": "Test Company - From",
        "address_line1": "9, Van Der Graaf Court",
        "city": "Brampton",
        "postal_code": "L4T3T1",
        "country_code": "CA",
        "state_code": "ON",
        "email": "shipper@example.com",
        "phone_number": "(123) 114 1499"
    },
    "recipient": {
        "company_name": "Test Company - Destination",
        "address_line1": "1410 Fall River Rd",
        "city": "Fall River",
        "country_code": "CA",
        "postal_code": "B2T1J1",
        "residential": "true",
        "state_code": "NS",
        "email": "recipient@example.com",
        "phone_number": "(999) 999 9999"
    },
    "parcels": [
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "description": "Package 1 Description"
        },
        {
            "height": 30,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "description": "Package 2 Description"
        }
    ],
    "reference": "REF-001",
    "options": {
         "email_notification": True,
        "shipping_date": datetime.datetime(2025, 2, 25, 1,0).strftime("%Y-%m-%dT%H:%M"),
    }
}

ParsedRateResponse = [
  [
    {
      "carrier_id": "freightcom",
      "carrier_name": "freightcom",
      "currency": "CAD",
      "extra_charges": [
        {
          "amount": 33.68,
          "currency": "CAD",
          "name": "Base charge"
        },
        {
          "amount": 10.01,
          "currency": "CAD",
          "name": "fuel"
        },
        {
          "amount": 0.51,
          "currency": "CAD",
          "name": "carbon-surcharge"
        },
        {
          "amount": 2.18,
          "currency": "CAD",
          "name": "residential-delivery"
        },
        {
          "amount": 6.96,
          "currency": "CAD",
          "name": "tax-hst-ns"
        }
      ],
      "meta": {
        "rate_provider": "canpar",
        "service_name": "freightcom_canpar_ground"
      },
      "service": "freightcom_canpar_ground",
      "total_charge": 53.34,
      "transit_days": 2
    },
    {
      "carrier_id": "freightcom",
      "carrier_name": "freightcom",
      "currency": "CAD",
      "extra_charges": [
        {
          "amount": 40.87,
          "currency": "CAD",
          "name": "Base charge"
        },
        {
          "amount": 12.54,
          "currency": "CAD",
          "name": "fuel"
        },
        {
          "amount": 2.78,
          "currency": "CAD",
          "name": "residential-delivery"
        },
        {
          "amount": 8.43,
          "currency": "CAD",
          "name": "tax-hst-ns"
        }
      ],
      "meta": {
        "rate_provider": "fedex",
        "service_name": "freightcom_fedex_ground"
      },
      "service": "freightcom_fedex_ground",
      "total_charge": 64.62,
      "transit_days": 2
    },
      {
          "carrier_id": "freightcom",
          "carrier_name": "freightcom",
          "currency": "CAD",
          "extra_charges": [
              {
                  "amount": 41.34,
                  "currency": "CAD",
                  "name": "Base charge"
              },
              {
                  "amount": 11.24,
                  "currency": "CAD",
                  "name": "fuel"
              },
              {
                  "amount": 7.89,
                  "currency": "CAD",
                  "name": "tax-hst-ns"
              }
          ],
          "meta": {
              "rate_provider": "purolator",
              "service_name": "freightcom_purolator_ground"
          },
          "service": "freightcom_purolator_ground",
          "total_charge": 60.47,
          "transit_days": 3
      }
  ],
    []
]


RateRequest = {
    "details": {
        "destination": {
            "address": {
                "address_line_1": "1410 Fall River Rd",
                "city": "Fall River",
                "country": "CA",
                "postal_code": "B2T1J1",
                "region": "NS",
            },
            "email_addresses": ["recipient@example.com"],
            'name': 'Test Company - Destination',
            "phone_number": {"number": "(999) 999 9999"},
            "ready_at": {
                "hour": 10, "minute": 0
            },
            "ready_until": {
                "hour": 17, "minute": 0
            },
            "receives_email_updates": True,
            "residential": False,
            "signature_requirement": "not-required"
        },
        "origin": {
            "address": {
                "address_line_1": "9, Van Der Graaf Court",
                "city": "Brampton",
                "country": "CA",
                "postal_code": "L4T3T1",
                "region": "ON",
            },
            "name": "Test Company - From",
            "email_addresses": ["shipper@example.com"],
            "phone_number": {"number": "(123) 114 1499"},
            "residential": False
        },
        "expected_ship_date": {"day": 25, "month": 2, "year": 2025},
        "packaging_type": "package",
        "packaging_properties": {
            "packages": [
                {
                    "description": "Package 1 Description",
                    "measurements": {
                        "cuboid": {
                            "h": 50.0,
                            "l": 50.0,
                            "unit": "cm",
                            "w": 12.0
                        },
                        "weight": {
                            "unit": "kg",
                            "value": 20.0
                        }
                    }
                },
                {
                    "description": "Package 2 Description",
                    "measurements": {
                        "cuboid": {
                            "h": 30.0,
                            "l": 50.0,
                            "unit": "cm",
                            "w": 12.0
                        },
                        "weight": {
                            "unit": "kg",
                            "value": 20.0
                        }
                    }
                }
            ],
        },
        "reference_codes": ["REF-001"]
        }
}

RateResponse = """
{
  "status": {
    "done": true,
    "total": 99,
    "complete": 99
  },
  "rates": [
    {
      "service_id": "canpar.ground",
      "valid_until": {
        "year": 2025,
        "month": 3,
        "day": 3
      },
      "total": {
        "value": "5334",
        "currency": "CAD"
      },
      "base": {
        "value": "3368",
        "currency": "CAD"
      },
      "surcharges": [
        {
          "type": "fuel",
          "amount": {
            "value": "1001",
            "currency": "CAD"
          }
        },
        {
          "type": "carbon-surcharge",
          "amount": {
            "value": "51",
            "currency": "CAD"
          }
        },
        {
          "type": "residential-delivery",
          "amount": {
            "value": "218",
            "currency": "CAD"
          }
        }
      ],
      "taxes": [
        {
          "type": "tax-hst-ns",
          "amount": {
            "value": "696",
            "currency": "CAD"
          }
        }
      ],
      "transit_time_days": 2,
      "transit_time_not_available": false,
      "carrier_name": "Canpar",
      "service_name": "Ground"
    },
    {
      "service_id": "fedex-courier.ground",
      "valid_until": {
        "year": 2025,
        "month": 3,
        "day": 3
      },
      "total": {
        "value": "6462",
        "currency": "CAD"
      },
      "base": {
        "value": "4087",
        "currency": "CAD"
      },
      "surcharges": [
        {
          "type": "fuel",
          "amount": {
            "value": "1254",
            "currency": "CAD"
          }
        },
        {
          "type": "residential-delivery",
          "amount": {
            "value": "278",
            "currency": "CAD"
          }
        }
      ],
      "taxes": [
        {
          "type": "tax-hst-ns",
          "amount": {
            "value": "843",
            "currency": "CAD"
          }
        }
      ],
      "transit_time_days": 2,
      "transit_time_not_available": false,
      "carrier_name": "FedEx Courier",
      "service_name": "Ground"
    },
    {
      "service_id": "purolatorcourier.ground",
      "valid_until": {
        "year": 2025,
        "month": 3,
        "day": 3
      },
      "total": {
        "value": "6047",
        "currency": "CAD"
      },
      "base": {
        "value": "4134",
        "currency": "CAD"
      },
      "surcharges": [
        {
          "type": "fuel",
          "amount": {
            "value": "1124",
            "currency": "CAD"
          }
        }
      ],
      "taxes": [
        {
          "type": "tax-hst-ns",
          "amount": {
            "value": "789",
            "currency": "CAD"
          }
        }
      ],
      "transit_time_days": 3,
      "transit_time_not_available": false,
      "carrier_name": "Purolator",
      "service_name": "Ground"
    }
  ]
}
"""
