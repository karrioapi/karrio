import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestEasyshipShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
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
    "service": "carrier_service",
    "options": {
        "signature_required": True,
    },
    "reference": "#Order 11111",
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = []

ParsedCancelShipmentResponse = ParsedCancelShipmentResponse = [
    {
        "carrier_id": "easyship",
        "carrier_name": "easyship",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "buyer_regulatory_identifiers": {"ein": "12-3456789", "vat_number": "EU1234567890"},
    "courier_selection": {
        "allow_courier_fallback": False,
        "apply_shipping_rules": True,
        "list_unavailable_couriers": True,
        "selected_courier_id": "courier_id",
    },
    "destination_address": {
        "city": "Hong Kong",
        "company_name": "Test Plc.",
        "contact_email": "asd@asd.com",
        "contact_name": "Foo Bar",
        "contact_phone": "+852-3008-5678",
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
    "consignee_tax_id": "1234567890",
    "eei_reference": "1234567890",
    "incoterms": "DDU",
    "metadata": {},
    "insurance": {"is_insured": False},
    "order_data": {
        "buyer_notes": "test_notes",
        "buyer_selected_courier_name": "test_courier",
        "order_created_at": "2024-01-31T18:00:00Z",
        "platform_name": "test plat_form",
        "platform_order_number": "test_order_number",
        "order_tag_list": ["test_tag"],
        "seller_notes": "test_seller_notes",
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
        "state": "Yuen Long",
        "validation": {
            "detail": "Address is not valid",
            "status": "invalid_address",
            "comparison": {"changes": "", "post": "", "pre": ""},
        },
    },
    "regulatory_identifiers": {
        "eori": "DE 123456789 12345",
        "ioss": "IM1234567890",
        "vat_number": "EU1234567890",
    },
    "return": False,
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
        "state": "Yuen Long",
        "validation": {
            "detail": "Address is not valid",
            "status": "invalid_address",
            "comparison": {"changes": "", "post": "", "pre": ""},
        },
    },
    "return_address_id": "return_address_id",
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
        "state": "Yuen Long",
        "validation": {
            "detail": "Address is not valid",
            "status": "invalid_address",
            "comparison": {"changes": "", "post": "", "pre": ""},
        },
    },
    "sender_address_id": "sender_address_id",
    "set_as_residential": False,
    "shipping_settings": {
        "additional_services": {"delivery_confirmation": "string", "qr_code": "none"},
        "b13a_filing": {
            "option": "string",
            "option_export_compliance_statement": "string",
            "permit_number": "string",
        },
        "buy_label": False,
        "buy_label_synchronous": False,
        "printing_options": {
            "commercial_invoice": "A4",
            "format": "png",
            "label": "4x6",
            "packing_slip": "4x6",
            "remarks": "string",
        },
        "units": {"dimensions": "cm", "weight": "kg"},
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
                    "actual_weight": 10,
                    "category": None,
                    "contains_battery_pi966": True,
                    "contains_battery_pi967": True,
                    "contains_liquids": True,
                    "declared_currency": "USD",
                    "declared_customs_value": 20,
                    "description": "item",
                    "dimensions": {"height": 3, "length": 1, "width": 2},
                    "hs_code": "123456",
                    "origin_country_alpha2": "HK",
                    "quantity": 2,
                    "sku": "sku",
                }
            ],
            "total_actual_weight": 1,
        }
    ],
}


ShipmentCancelRequest = {}

ShipmentResponse = """{
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
        "b13a_filing": {
          "option": "not_required",
          "option_export_compliance_statement": "string",
          "permit_number": "string"
        }
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

ShipmentCancelResponse = """{
  "meta": {
    "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477"
  },
  "success": {
    "message": "Shipment successfully cancelled"
  }
}
"""
