import unittest
import urllib.parse
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSendleRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertListEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.side_effect = ["{}", "{}"]
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/products?{urllib.parse.urlencode(RateRequest[0])}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.side_effect = [RateResponse, RateResponse]
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.side_effect = [ErrorResponse, ErrorResponse]
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
            "carrier_id": "sendle",
            "carrier_name": "sendle",
            "currency": "AUD",
            "extra_charges": [
                {"amount": 30.0, "currency": "AUD", "name": "base"},
                {"amount": 3.0, "currency": "AUD", "name": "base_tax"},
                {"amount": 0.4, "currency": "AUD", "name": "fuel_surcharge"},
                {"amount": 0.04, "currency": "AUD", "name": "fuel_surcharge_tax"},
                {"amount": 1.54, "currency": "AUD", "name": "gst"},
            ],
            "meta": {
                "date_range": ["2022-02-28", "2022-03-03"],
                "days_range": [1, 4],
                "plan": "Sendle Pro",
                "service_name": "sendle_standard_pickup",
            },
            "service": "sendle_standard_pickup",
            "total_charge": 16.94,
            "transit_days": 4,
        },
        {
            "carrier_id": "sendle",
            "carrier_name": "sendle",
            "currency": "AUD",
            "extra_charges": [
                {"amount": 30.0, "currency": "AUD", "name": "base"},
                {"amount": 3.0, "currency": "AUD", "name": "base_tax"},
                {"amount": 0.4, "currency": "AUD", "name": "fuel_surcharge"},
                {"amount": 0.04, "currency": "AUD", "name": "fuel_surcharge_tax"},
                {"amount": 1.54, "currency": "AUD", "name": "gst"},
            ],
            "meta": {
                "date_range": ["2022-02-28", "2022-03-03"],
                "days_range": [1, 4],
                "plan": "Sendle Pro",
                "service_name": "sendle_standard_dropoff",
            },
            "service": "sendle_standard_dropoff",
            "total_charge": 16.94,
            "transit_days": 4,
        },
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "sendle",
            "carrier_name": "sendle",
            "code": "unprocessable_entity",
            "details": {
                "error_description": "The data you supplied is invalid. Error "
                "messages are in the messages section. "
                "Please fix those fields and try again.",
                "messages": {
                    "receiver_country": ["can't be blank"],
                    "receiver_postcode": ["can't be blank"],
                    "receiver_suburb": ["can't be blank"],
                    "sender_country": [
                        "can't be blank",
                        "products are not currently "
                        "available from the specified "
                        "country of origin",
                    ],
                    "sender_postcode": ["can't be blank"],
                    "sender_suburb": ["can't be blank"],
                    "weight_units": ["is not included in the list", "can't be blank"],
                    "weight_value": ["is not a number", "can't be blank"],
                },
            },
            "message": "The data you supplied is invalid. Error messages are in the "
            "messages section. Please fix those fields and try again.",
        },
        {
            "carrier_id": "sendle",
            "carrier_name": "sendle",
            "code": "unprocessable_entity",
            "details": {
                "error_description": "The data you supplied is invalid. Error "
                "messages are in the messages section. "
                "Please fix those fields and try again.",
                "messages": {
                    "receiver_country": ["can't be blank"],
                    "receiver_postcode": ["can't be blank"],
                    "receiver_suburb": ["can't be blank"],
                    "sender_country": [
                        "can't be blank",
                        "products are not currently "
                        "available from the specified "
                        "country of origin",
                    ],
                    "sender_postcode": ["can't be blank"],
                    "sender_suburb": ["can't be blank"],
                    "weight_units": ["is not included in the list", "can't be blank"],
                    "weight_value": ["is not a number", "can't be blank"],
                },
            },
            "message": "The data you supplied is invalid. Error messages are in the "
            "messages section. Please fix those fields and try again.",
        },
    ],
]


RateRequest = [
    {
        "dimension_units": "cm",
        "height_value": 50.0,
        "length_value": 50.0,
        "receiver_address_line1": "17 VULCAN RD",
        "receiver_address_line2": "test",
        "receiver_country": "AU",
        "receiver_postcode": "6155",
        "receiver_suburb": "CANNING VALE",
        "sender_address_line1": "17 VULCAN RD",
        "sender_country": "AU",
        "sender_postcode": "6155",
        "sender_suburb": "CANNING VALE",
        "volume_units": "m3",
        "volume_value": 0.03,
        "weight_units": "kg",
        "weight_value": 20.0,
        "width_value": 12.0,
    },
    {
        "dimension_units": "cm",
        "height_value": 50.0,
        "length_value": 50.0,
        "receiver_address_line1": "17 VULCAN RD",
        "receiver_address_line2": "test",
        "receiver_country": "AU",
        "receiver_postcode": "6155",
        "receiver_suburb": "CANNING VALE",
        "sender_address_line1": "17 VULCAN RD",
        "sender_country": "AU",
        "sender_postcode": "6155",
        "sender_suburb": "CANNING VALE",
        "volume_units": "m3",
        "volume_value": 0.03,
        "weight_units": "kg",
        "weight_value": 20.0,
        "width_value": 12.0,
    },
]

RateResponse = """[
  {
    "quote": {
      "gross": {
        "amount": 8.47,
        "currency": "AUD"
      },
      "net": {
        "amount": 7.7,
        "currency": "AUD"
      },
      "tax": {
        "amount": 0.77,
        "currency": "AUD"
      }
    },
    "price_breakdown": {
      "base": {
        "amount": 15,
        "currency": "AUD"
      },
      "discount": {
        "amount": -7.5,
        "currency": "AUD"
      },
      "cover": {
        "amount": 0,
        "currency": "AUD"
      },
      "fuel_surcharge": {
        "amount": 0.2,
        "currency": "AUD"
      },
      "base_tax": {
        "amount": 1.5,
        "currency": "AUD"
      },
      "discount_tax": {
        "amount": -0.75,
        "currency": "AUD"
      },
      "cover_tax": {
        "amount": 0,
        "currency": "AUD"
      },
      "fuel_surcharge_tax": {
        "amount": 0.02,
        "currency": "AUD"
      }
    },
    "tax_breakdown": {
      "gst": {
        "amount": 0.77,
        "currency": "AUD",
        "rate": 0.1
      }
    },
    "plan": "Sendle Pro",
    "eta": {
      "days_range": [
        1,
        4
      ],
      "date_range": [
        "2022-02-28",
        "2022-03-03"
      ],
      "for_send_date": "2022-02-25"
    },
    "route": {
      "type": "same-city",
      "description": "Sydney, Australia to Sydney, Australia"
    },
    "allowed_packaging": "any",
    "product": {
      "code": "STANDARD-PICKUP",
      "name": "Standard Pickup",
      "first_mile_option": "pickup",
      "service": "standard"
    },
    "cover": {
      "price": {
        "gross": {
          "amount": 0,
          "currency": "AUD"
        },
        "net": {
          "amount": 0,
          "currency": "AUD"
        },
        "tax": {
          "amount": 0,
          "currency": "AUD"
        }
      }
    }
  },
  {
    "quote": {
      "gross": {
        "amount": 8.47,
        "currency": "AUD"
      },
      "net": {
        "amount": 7.7,
        "currency": "AUD"
      },
      "tax": {
        "amount": 0.77,
        "currency": "AUD"
      }
    },
    "price_breakdown": {
      "base": {
        "amount": 15,
        "currency": "AUD"
      },
      "discount": {
        "amount": -7.5,
        "currency": "AUD"
      },
      "cover": {
        "amount": 0,
        "currency": "AUD"
      },
      "fuel_surcharge": {
        "amount": 0.2,
        "currency": "AUD"
      },
      "base_tax": {
        "amount": 1.5,
        "currency": "AUD"
      },
      "discount_tax": {
        "amount": -0.75,
        "currency": "AUD"
      },
      "cover_tax": {
        "amount": 0,
        "currency": "AUD"
      },
      "fuel_surcharge_tax": {
        "amount": 0.02,
        "currency": "AUD"
      }
    },
    "tax_breakdown": {
      "gst": {
        "amount": 0.77,
        "currency": "AUD",
        "rate": 0.1
      }
    },
    "plan": "Sendle Pro",
    "eta": {
      "days_range": [
        1,
        4
      ],
      "date_range": [
        "2022-02-28",
        "2022-03-03"
      ],
      "for_send_date": "2022-02-25"
    },
    "route": {
      "type": "same-city",
      "description": "Sydney, Australia to Sydney, Australia"
    },
    "allowed_packaging": "any",
    "product": {
      "code": "STANDARD-DROPOFF",
      "name": "Standard Drop Off",
      "first_mile_option": "drop off",
      "service": "standard"
    },
    "cover": {
      "price": {
        "gross": {
          "amount": 0,
          "currency": "AUD"
        },
        "net": {
          "amount": 0,
          "currency": "AUD"
        },
        "tax": {
          "amount": 0,
          "currency": "AUD"
        }
      }
    }
  }
]
"""

ErrorResponse = """{
  "messages": {
    "sender_suburb": [
      "can't be blank"
    ],
    "sender_postcode": [
      "can't be blank"
    ],
    "sender_country": [
      "can't be blank",
      "products are not currently available from the specified country of origin"
    ],
    "receiver_country": [
      "can't be blank"
    ],
    "receiver_suburb": [
      "can't be blank"
    ],
    "receiver_postcode": [
      "can't be blank"
    ],
    "weight_units": [
      "is not included in the list",
      "can't be blank"
    ],
    "weight_value": [
      "is not a number",
      "can't be blank"
    ]
  },
  "error": "unprocessable_entity",
  "error_description": "The data you supplied is invalid. Error messages are in the messages section. Please fix those fields and try again."
}
"""
