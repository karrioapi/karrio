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
                f"{gateway.settings.server_url}/2023-01/rates",
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
        "company_name": None,
        "address_line1": "Kennedy Town",
        "address_line2": "Block 3",
        "city": "Hong Kong",
        "postal_code": "0000",
        "country_code": "HK",
        "person_name": "Foo Bar",
        "state_code": "Yuen Long",
        "email": "asd@asd.com",
        "phone_number": None,
    },
    "recipient": {
        "company_name": None,
        "address_line1": "Kennedy Town",
        "address_line2": "Block 3",
        "city": "Hong Kong",
        "postal_code": "0000",
        "country_code": "HK",
        "person_name": "Foo Bar",
        "state_code": "Yuen Long",
        "email": "asd@asd.com",
        "phone_number": None,
    },
    "parcels": [
        {
            "height": 3,
            "length": 1,
            "width": 2,
            "weight": 1,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "items": [
                {
                    "sku": "sku",
                    "quantity": 2,
                    "weight": 10,
                    "weight_unit": "KG",
                    "origin_country": "HK",
                    "value_amount": 20,
                    "value_currency": "USD",
                    "description": "item",
                    "category": "fashion",
                    "metadata": {
                        "contains_battery_pi966": True,
                        "contains_battery_pi967": True,
                        "contains_liquids": True,
                    },
                }
            ],
        }
    ],
    "options": {
        "easyship_apply_shipping_rules": True,
        "easyship_show_courier_logo_url": False,
        "easyship_incoterms": "DDU",
    },
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "easyship",
            "carrier_name": "easyship",
            "currency": "USD",
            "extra_charges": [
                {"amount": 2.8, "currency": "USD", "name": "Shipment Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Insurance"},
                {"amount": 0.0, "currency": "USD", "name": "Fuel Surcharge"},
                {"amount": 0.0, "currency": "USD", "name": "Additional Surcharge"},
                {"amount": 0.0, "currency": "USD", "name": "Import Duty Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Import Tax Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Minimum Pickup Fee"},
                {"amount": 0.0, "currency": "USD", "name": "Oversized Surcharge"},
                {"amount": 0.0, "currency": "USD", "name": "Provincial Sales Tax"},
                {"amount": 0.0, "currency": "USD", "name": "Remote Area Surcharge"},
                {"amount": 0.0, "currency": "USD", "name": "Sales Tax"},
                {"amount": 0.0, "currency": "USD", "name": "Warehouse Handling Fee"},
                {"amount": 0.0, "currency": "USD", "name": "Discount"},
            ],
            "meta": {
                "available_handover_options": ["dropoff", "free_pickup"],
                "cost_rank": 1,
                "delivery_time_rank": 1,
                "easyship_courier_id": "64b5d8b2-4c60-4faf-bf1b-9f7b1b7ca1c8",
                "easyship_incoterms": "DDU",
                "max_delivery_time": 2,
                "min_delivery_time": 1,
                "service_name": "SF Express - Domestic",
                "tracking_rating": 3,
                "value_for_money_rank": 1,
            },
            "service": "64b5d8b2-4c60-4faf-bf1b-9f7b1b7ca1c8",
            "total_charge": 2.8,
            "transit_days": 2,
        },
        {
            "carrier_id": "easyship",
            "carrier_name": "easyship",
            "currency": "USD",
            "extra_charges": [
                {"amount": 9.56, "currency": "USD", "name": "Shipment Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Insurance"},
                {"amount": 0.0, "currency": "USD", "name": "Fuel Surcharge"},
                {"amount": 0.0, "currency": "USD", "name": "Additional Surcharge"},
                {"amount": 0.0, "currency": "USD", "name": "Import Duty Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Import Tax Charge"},
                {"amount": 0.0, "currency": "USD", "name": "Minimum Pickup Fee"},
                {"amount": 0.0, "currency": "USD", "name": "Oversized Surcharge"},
                {"amount": 0.0, "currency": "USD", "name": "Provincial Sales Tax"},
                {"amount": 0.0, "currency": "USD", "name": "Remote Area Surcharge"},
                {"amount": 0.0, "currency": "USD", "name": "Sales Tax"},
                {"amount": 0.0, "currency": "USD", "name": "Warehouse Handling Fee"},
                {"amount": 0.0, "currency": "USD", "name": "Discount"},
            ],
            "meta": {
                "available_handover_options": ["dropoff"],
                "cost_rank": 2,
                "delivery_time_rank": 2,
                "easyship_courier_id": "d6cfc6d2-3857-4f42-a2a4-9e10ac9766ac",
                "easyship_incoterms": "DDU",
                "max_delivery_time": 10,
                "min_delivery_time": 2,
                "service_name": "HK Post - Local Parcel",
                "tracking_rating": 1,
                "value_for_money_rank": 2,
            },
            "service": "d6cfc6d2-3857-4f42-a2a4-9e10ac9766ac",
            "total_charge": 9.56,
            "transit_days": 10,
        },
    ],
    [],
]


RateRequest = {
    "courier_selection": {
        "apply_shipping_rules": True,
        "show_courier_logo_url": False,
    },
    "destination_address": {
        "country_alpha2": "HK",
        "city": "Hong Kong",
        "contact_email": "asd@asd.com",
        "contact_name": "Foo Bar",
        "line_1": "Kennedy Town",
        "line_2": "Block 3",
        "postal_code": "0000",
        "state": "Yuen Long",
    },
    "incoterms": "DDU",
    "insurance": {
        "is_insured": False,
    },
    "origin_address": {
        "city": "Hong Kong",
        "contact_email": "asd@asd.com",
        "contact_name": "Foo Bar",
        "country_alpha2": "HK",
        "line_1": "Kennedy Town",
        "line_2": "Block 3",
        "postal_code": "0000",
        "state": "Yuen Long",
    },
    "parcels": [
        {
            "box": {
                "height": 3.0,
                "length": 1.0,
                "width": 2.0,
            },
            "items": [
                {
                    "contains_battery_pi966": True,
                    "contains_battery_pi967": True,
                    "contains_liquids": True,
                    "declared_currency": "USD",
                    "origin_country_alpha2": "HK",
                    "quantity": 2,
                    "actual_weight": 10.0,
                    "category": "fashion",
                    "declared_customs_value": 20,
                    "description": "item",
                    "sku": "sku",
                }
            ],
            "total_actual_weight": 1.0,
        }
    ],
    "shipping_settings": {"units": {"dimensions": "cm", "weight": "kg"}},
}

RateResponse = """{
  "rates": [
    {
      "additional_services_surcharge": 0,
      "available_handover_options": [
        "dropoff",
        "free_pickup"
      ],
      "cost_rank": 1,
      "courier_id": "64b5d8b2-4c60-4faf-bf1b-9f7b1b7ca1c8",
      "courier_logo_url": null,
      "courier_name": "SF Express - Domestic",
      "courier_remarks": null,
      "currency": "USD",
      "ddp_handling_fee": 0,
      "delivery_time_rank": 1,
      "description": "No additional taxes to be paid at delivery",
      "discount": {
        "amount": 0,
        "origin_amount": 0
      },
      "easyship_rating": null,
      "estimated_import_duty": 0,
      "estimated_import_tax": 0,
      "fuel_surcharge": 0,
      "full_description": "SF Express - Domestic (1-2 working days) No additional taxes to be paid at delivery",
      "import_duty_charge": 0,
      "import_tax_charge": 0,
      "import_tax_non_chargeable": 0,
      "incoterms": "DDU",
      "insurance_fee": 0,
      "is_above_threshold": false,
      "max_delivery_time": 2,
      "min_delivery_time": 1,
      "minimum_pickup_fee": 0,
      "other_surcharges": null,
      "oversized_surcharge": 0,
      "payment_recipient": "Easyship",
      "provincial_sales_tax": 0,
      "rates_in_origin_currency": {
        "additional_services_surcharge": 0,
        "currency": "HKD",
        "ddp_handling_fee": 0,
        "estimated_import_duty": 0,
        "estimated_import_tax": 0,
        "fuel_surcharge": 0,
        "import_duty_charge": 0,
        "import_tax_charge": 0,
        "import_tax_non_chargeable": 0,
        "insurance_fee": 0,
        "minimum_pickup_fee": 0,
        "oversized_surcharge": 0,
        "provincial_sales_tax": 0,
        "remote_area_surcharge": 0,
        "residential_discounted_fee": null,
        "residential_full_fee": null,
        "sales_tax": 0,
        "shipment_charge": 22,
        "shipment_charge_total": 22,
        "total_charge": 22,
        "warehouse_handling_fee": 0
      },
      "remote_area_surcharge": 0,
      "remote_area_surcharges": null,
      "residential_discounted_fee": null,
      "residential_full_fee": null,
      "sales_tax": 0,
      "shipment_charge": 2.8,
      "shipment_charge_total": 2.8,
      "total_charge": 2.8,
      "tracking_rating": 3,
      "value_for_money_rank": 1,
      "warehouse_handling_fee": 0
    },
    {
      "additional_services_surcharge": 0,
      "available_handover_options": [
        "dropoff"
      ],
      "cost_rank": 2,
      "courier_id": "d6cfc6d2-3857-4f42-a2a4-9e10ac9766ac",
      "courier_logo_url": null,
      "courier_name": "HK Post - Local Parcel",
      "courier_remarks": null,
      "currency": "USD",
      "ddp_handling_fee": 0,
      "delivery_time_rank": 2,
      "description": "No additional taxes to be paid at delivery",
      "discount": {
        "amount": 0,
        "origin_amount": 0
      },
      "easyship_rating": null,
      "estimated_import_duty": 0,
      "estimated_import_tax": 0,
      "fuel_surcharge": 0,
      "full_description": "HK Post - Local Parcel (2-10 working days) No additional taxes to be paid at delivery",
      "import_duty_charge": 0,
      "import_tax_charge": 0,
      "import_tax_non_chargeable": 0,
      "incoterms": "DDU",
      "insurance_fee": 0,
      "is_above_threshold": false,
      "max_delivery_time": 10,
      "min_delivery_time": 2,
      "minimum_pickup_fee": 0,
      "other_surcharges": null,
      "oversized_surcharge": 0,
      "payment_recipient": "Courier",
      "provincial_sales_tax": 0,
      "rates_in_origin_currency": {
        "additional_services_surcharge": 0,
        "currency": "HKD",
        "ddp_handling_fee": 0,
        "estimated_import_duty": 0,
        "estimated_import_tax": 0,
        "fuel_surcharge": 0,
        "import_duty_charge": 0,
        "import_tax_charge": 0,
        "import_tax_non_chargeable": 0,
        "insurance_fee": 0,
        "minimum_pickup_fee": 0,
        "oversized_surcharge": 0,
        "provincial_sales_tax": 0,
        "remote_area_surcharge": 0,
        "residential_discounted_fee": null,
        "residential_full_fee": null,
        "sales_tax": 0,
        "shipment_charge": 75,
        "shipment_charge_total": 75,
        "total_charge": 75,
        "warehouse_handling_fee": 0
      },
      "remote_area_surcharge": 0,
      "remote_area_surcharges": null,
      "residential_discounted_fee": null,
      "residential_full_fee": null,
      "sales_tax": 0,
      "shipment_charge": 9.56,
      "shipment_charge_total": 9.56,
      "total_charge": 9.56,
      "tracking_rating": 1,
      "value_for_money_rank": 2,
      "warehouse_handling_fee": 0
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "next": null,
      "count": 2
    },
    "request_id": "d5f9d482b46f9ac995f7b56228305713"
  }
}
"""
