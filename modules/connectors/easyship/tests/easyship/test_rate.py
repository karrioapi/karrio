import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestEasyshipRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


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
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "k1k 4t3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "parcels": [
        {
            "height": 50,
            "length": 50,
            "weight": 20,
            "width": 12,
            "dimension_unit": "CM",
            "weight_unit": "KG",
        }
    ],
    "options": {},
    "reference": "REF-001",
}

ParsedRateResponse = []


RateRequest = {
    "courier_selection": {"apply_shipping_rules": True, "show_courier_logo_url": False},
    "destination_address": {
        "country_alpha2": "HK",
        "city": "Hong Kong",
        "company_name": None,
        "contact_email": "asd@asd.com",
        "contact_name": "Foo Bar",
        "contact_phone": None,
        "line_1": "Kennedy Town",
        "line_2": "Block 3",
        "postal_code": "0000",
        "state": "Yuen Long",
    },
    "incoterms": "DDU",
    "insurance": {
        "insured_amount": 10.0,
        "insured_currency": "USD",
        "is_insured": False,
    },
    "origin_address": {
        "city": "Hong Kong",
        "company_name": None,
        "contact_email": "asd@asd.com",
        "contact_name": "Foo Bar",
        "contact_phone": None,
        "country_alpha2": "HK",
        "line_1": "Kennedy Town",
        "line_2": "Block 3",
        "postal_code": "0000",
        "state": "Yuen Long",
        "validation": {
            "detail": "Address is not valid",
            "status": "invalid_address",
            "comparison": {"changes": "", "post": "", "pre": ""},
        },
    },
    "parcels": [
        {
            "box": {
                "height": 10,
                "length": 10,
                "weight": 10,
                "width": 10,
                "slug": "custom",
            },
            "items": [
                {
                    "contains_battery_pi966": True,
                    "contains_battery_pi967": True,
                    "contains_liquids": True,
                    "declared_currency": "USD",
                    "dimensions": {"height": 3, "length": 1, "width": 2},
                    "origin_country_alpha2": "HK",
                    "quantity": 2,
                    "actual_weight": 10,
                    "category": "fashion",
                    "declared_customs_value": 20,
                    "description": "item",
                    "sku": "sku",
                }
            ],
            "total_actual_weight": 1,
        }
    ],
    "shipping_settings": {
        "output_currency": "USD",
        "units": {"dimensions": "cm", "weight": "kg"},
    },
}


RateResponse = """{
  "meta": {
    "pagination": {
      "count": 1,
      "next": "string",
      "page": 1
    },
    "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477"
  },
  "rates": [
    {
      "additional_services_surcharge": 0,
      "available_handover_options": [],
      "cost_rank": 1,
      "courier_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
      "courier_logo_url": "string",
      "courier_name": "Courier 1",
      "courier_remarks": "string",
      "currency": "HKD",
      "ddp_handling_fee": 0,
      "delivery_time_rank": 2,
      "description": "Estimated  65.96 tax & duty due on delivery (Tax handling fees may apply)",
      "discount": {
        "amount": 1,
        "origin_amount": 1
      },
      "easyship_rating": 2,
      "estimated_import_duty": 0,
      "estimated_import_tax": 65.96,
      "fuel_surcharge": 1400,
      "full_description": "Courier 1 (19-39 working days) Estimated  65.96 tax & duty due on delivery (Tax handling fees may apply)",
      "import_duty_charge": 0,
      "import_tax_charge": 0,
      "import_tax_non_chargeable": 0,
      "incoterms": "DDU",
      "insurance_fee": 0,
      "is_above_threshold": true,
      "max_delivery_time": 39,
      "min_delivery_time": 19,
      "minimum_pickup_fee": 0,
      "other_surcharges": {
        "details": [
          {
            "fee": 1,
            "name": "Surcharge Name",
            "origin_fee": 1
          }
        ],
        "total_fee": 2
      },
      "oversized_surcharge": 0,
      "payment_recipient": "Easyship",
      "provincial_sales_tax": 0,
      "rates_in_origin_currency": {
        "additional_services_surcharge": 0,
        "currency": "HKD",
        "ddp_handling_fee": 0,
        "estimated_import_duty": 0,
        "estimated_import_tax": 65.96,
        "fuel_surcharge": 1400,
        "import_duty_charge": 0,
        "import_tax_charge": 0,
        "import_tax_non_chargeable": 0,
        "insurance_fee": 0,
        "minimum_pickup_fee": 0,
        "oversized_surcharge": 0,
        "provincial_sales_tax": 0,
        "remote_area_surcharge": 2,
        "residential_discounted_fee": 0,
        "residential_full_fee": 0,
        "sales_tax": 0,
        "shipment_charge": 140,
        "shipment_charge_total": 1544,
        "total_charge": 1544,
        "warehouse_handling_fee": 0
      },
      "remote_area_surcharge": 2,
      "remote_area_surcharges": {
        "destination": {
          "base": 1,
          "name": "Destination Surcharge Name"
        },
        "origin": {
          "base": 1,
          "name": "Origin Surcharge Name"
        }
      },
      "residential_discounted_fee": 0,
      "residential_full_fee": 0,
      "sales_tax": 0,
      "shipment_charge": 140,
      "shipment_charge_total": 1544,
      "total_charge": 1544,
      "tracking_rating": 2,
      "value_for_money_rank": 1,
      "warehouse_handling_fee": 0
    }
  ]
}
"""
