import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestEasyshipTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/2023-01/shipments/ESSG10006002",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["89108749065090"],
    "options": {"easyship_shipment_id": "ESSG10006002"},
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "easyship",
            "carrier_name": "easyship",
            "delivered": False,
            "events": [{"code": "1", "date": "12:21", "time": "12:21"}],
            "status": "in_transit",
            "tracking_number": "Courier 1",
        }
    ],
    [
        {
            "carrier_id": "easyship",
            "carrier_name": "easyship",
            "code": "warning",
            "details": {"shipment_id": "ESSG10006002"},
            "message": "string",
        }
    ],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "easyship",
            "carrier_name": "easyship",
            "code": "over_limit",
            "details": {
                "details": [
                    "We were unable to generate a label as your maximum "
                    "balance limit has been reached. Please contact "
                    "your account manager."
                ],
                "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477",
                "shipment_id": "ESSG10006002",
                "type": "invalid_request_error",
            },
            "message": "You have reached your plan limit. Please upgrade your "
            "subscription plan.",
        }
    ],
]


TrackingRequest = ["ESSG10006002"]

TrackingResponse = """{
  "meta": {
    "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477",
    "status": "success",
    "unavailable_couriers": [
      {
        "id": "01563646-58c1-4607-8fe0-cae3e33c0001",
        "name": "Courier 1",
        "message": "message"
      }
    ],
    "errors": ["string"]
  },
  "shipment": {
    "buyer_regulatory_identifiers": {
      "ein": "",
      "vat_number": ""
    },
    "consignee_tax_id": "",
    "courier": {
      "id": "01563646-58c1-4607-8fe0-cae3e33c0001",
      "name": "Courier 1"
    },
    "created_at": "2022-02-22T12:21:00Z",
    "currency": "HKD",
    "delivery_state": "not_created",
    "destination_address": {
      "city": "Hong Kong",
      "company_name": "Test Plc.",
      "contact_email": "asd@asd.com",
      "contact_name": "Foo Bar",
      "contact_phone": "+85230085678",
      "country_alpha2": "HK",
      "line_1": "Kennedy Town",
      "line_2": "Block 3",
      "postal_code": "0000",
      "state": "Yuen Long"
    },
    "easyship_shipment_id": "ESSG10006002",
    "eei_reference": "",
    "incoterms": "DDU",
    "insurance": {
      "insured_amount": 0,
      "insured_currency": "HKD",
      "is_insured": false
    },
    "label_generated_at": "",
    "label_paid_at": "",
    "label_state": "not_created",
    "last_failure_http_response_messages": [
      {
        "code": "string",
        "message": "string"
      }
    ],
    "metadata": [],
    "order_created_at": "",
    "order_data": {
      "buyer_notes": "",
      "buyer_selected_courier_name": "",
      "order_created_at": "",
      "order_tag_list": [""],
      "platform_name": "",
      "platform_order_number": "",
      "seller_notes": ""
    },
    "origin_address": {
      "city": "Hong Kong",
      "company_name": "Test Plc.",
      "contact_email": "asd@asd.com",
      "contact_name": "Foo Bar",
      "contact_phone": "+852-3008-5678",
      "country_alpha2": "HK",
      "line_1": "Kennedy Town",
      "line_2": "Block 3",
      "postal_code": "0000",
      "state": "Yuen Long"
    },
    "parcels": [
      {
        "box": {
          "id": "",
          "name": "",
          "outer_dimensions": {
            "height": 2,
            "length": 3,
            "width": 2
          },
          "slug": "",
          "type": "box",
          "weight": 0
        },
        "id": "01563646-58c1-4607-8fe0-cae3e33c0001",
        "items": [
          {
            "actual_weight": 10,
            "category": "",
            "contains_battery_pi966": true,
            "contains_battery_pi967": true,
            "contains_liquids": true,
            "declared_currency": "USD",
            "declared_customs_value": 20,
            "description": "item",
            "dimensions": {
              "height": 3,
              "length": 1,
              "width": 2
            },
            "hs_code": "12345600",
            "id": "12663646-58c1-4607-8fe0-cae3e33c0001",
            "origin_country_alpha2": "HK",
            "origin_currency": "HKD",
            "origin_customs_value": 140,
            "quantity": 2,
            "sku": "sku"
          }
        ],
        "total_actual_weight": 1
      }
    ],
    "pickup_state": "not_requested",
    "rates": [
      {
        "additional_services_surcharge": 0,
        "available_handover_options": ["dropoff", "free_pickup"],
        "cost_rank": 2,
        "courier_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
        "courier_logo_url": "",
        "courier_name": "Courier 1",
        "courier_remarks": "",
        "currency": "USD",
        "ddp_handling_fee": "",
        "delivery_time_rank": 4,
        "description": "description",
        "discount": "",
        "easyship_rating": 2,
        "estimated_import_duty": "",
        "estimated_import_tax": "",
        "fuel_surcharge": 1000,
        "full_description": "full description",
        "import_duty_charge": "",
        "import_tax_charge": "",
        "import_tax_non_chargeable": "",
        "incoterms": "DDU",
        "insurance_fee": 0,
        "is_above_threshold": true,
        "max_delivery_time": 39,
        "min_delivery_time": 19,
        "minimum_pickup_fee": 0,
        "other_surcharges": {
          "details": [
            {
              "fee": 0,
              "name": "Peak Surcharge",
              "origin_fee": 0
            }
          ],
          "total_fee": 0
        },
        "oversized_surcharge": 0,
        "payment_recipient": "Easyship",
        "provincial_sales_tax": 0,
        "rates_in_origin_currency": {
          "additional_services_surcharge": 0,
          "currency": "HKD",
          "ddp_handling_fee": "",
          "estimated_import_duty": "",
          "estimated_import_tax": "",
          "fuel_surcharge": 1400,
          "import_duty_charge": "",
          "import_tax_charge": "",
          "import_tax_non_chargeable": "",
          "insurance_fee": 0,
          "minimum_pickup_fee": 0,
          "oversized_surcharge": 0,
          "provincial_sales_tax": 0,
          "remote_area_surcharge": 0,
          "residential_discounted_fee": 0,
          "residential_full_fee": 0,
          "sales_tax": 0,
          "shipment_charge": 140,
          "shipment_charge_total": 1540,
          "total_charge": 1540,
          "warehouse_handling_fee": 0
        },
        "remote_area_surcharge": 0,
        "remote_area_surcharges": "",
        "residential_discounted_fee": 0,
        "residential_full_fee": 0,
        "sales_tax": 0,
        "shipment_charge": 100,
        "shipment_charge_total": 1100,
        "total_charge": 1100,
        "tracking_rating": 2,
        "value_for_money_rank": 4,
        "warehouse_handling_fee": 0
      }
    ],
    "regulatory_identifiers": {
      "eori": "",
      "ioss": "",
      "vat_number": ""
    },
    "return": false,
    "return_address": {
      "city": "Hong Kong",
      "company_name": "Test Plc.",
      "contact_email": "asd@asd.com",
      "contact_name": "Foo Bar",
      "contact_phone": "+852-3008-5678",
      "country_alpha2": "HK",
      "line_1": "Kennedy Town",
      "line_2": "Block 3",
      "postal_code": "0000",
      "state": "Yuen Long"
    },
    "sender_address": {
      "city": "Hong Kong",
      "company_name": "Test Plc.",
      "contact_email": "asd@asd.com",
      "contact_name": "Foo Bar",
      "contact_phone": "+852-3008-5678",
      "country_alpha2": "HK",
      "line_1": "Kennedy Town",
      "line_2": "Block 3",
      "postal_code": "0000",
      "state": "Yuen Long"
    },
    "set_as_residential": false,
    "shipment_state": "created",
    "shipping_documents": [
      {
        "base64_encoded_strings": ["base64_encoded"],
        "category": "label",
        "format": "png",
        "page_size": "4x6",
        "required": true,
        "url": null
      },
      {
        "base64_encoded_strings": ["base64_encoded"],
        "category": "packing_slip",
        "format": "png",
        "page_size": "4x6",
        "required": true,
        "url": null
      }
    ],
    "shipping_settings": {
      "b13a_filing": ""
    },
    "tracking_page_url": "http://localhost:9003/shipment-tracking/ESSG10006002",
    "trackings": [
      {
        "alternate_tracking_number": "Courier 1",
        "handler": "easyship",
        "leg_number": 1,
        "local_tracking_number": "Courier 1",
        "tracking_number": "Courier 1",
        "tracking_state": "in_transit"
      }
    ],
    "updated_at": "2022-02-22T12:21:00Z",
    "warehouse_state": "none"
  }
}
"""

ErrorResponse = """{
  "error": {
    "code": "over_limit",
    "details": [
      "We were unable to generate a label as your maximum balance limit has been reached. Please contact your account manager."
    ],
    "message": "You have reached your plan limit. Please upgrade your subscription plan.",
    "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477",
    "type": "invalid_request_error"
  }
}
"""
