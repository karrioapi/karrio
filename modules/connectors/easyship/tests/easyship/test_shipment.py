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
                f"{gateway.settings.server_url}/2023-01/shipments",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/2023-01/shipments/ESUS220509144/cancel",
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

    def test_parse_shipment_response_without_label(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = ShipmentWithoutLabelResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertEqual(
                lib.to_dict(parsed_response), ParsedShipmentResponseWithoutLabel
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "company_name": "Test Plc.",
        "address_line1": "Kennedy Town",
        "address_line2": "Block 3",
        "city": "Hong Kong",
        "postal_code": "0000",
        "country_code": "HK",
        "person_name": "Foo Bar",
        "state_code": "Yuen Long",
        "email": "asd@asd.com",
        "phone_number": "+852-3008-5678",
    },
    "recipient": {
        "company_name": "Test Plc.",
        "address_line1": "Kennedy Town",
        "address_line2": "Block 3",
        "city": "Hong Kong",
        "postal_code": "0000",
        "country_code": "HK",
        "person_name": "Foo Bar",
        "state_code": "Yuen Long",
        "email": "asd@asd.com",
        "phone_number": "+852-3008-5678",
    },
    "parcels": [
        {
            "height": 10.0,
            "length": 10.0,
            "weight": 1.0,
            "width": 10.0,
            "dimension_unit": "CM",
            "weight_unit": "KG",
            "options": {
                "easyship_box_slug": "custom",
            },
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
                    "hs_code": "123456",
                    "metadata": {
                        "contains_battery_pi966": True,
                        "contains_battery_pi967": True,
                        "contains_liquids": True,
                    },
                }
            ],
        }
    ],
    "service": "easyship_ups_ground_saver",
    "reference": "string",
    "options": {
        "easyship_signature_required": True,
        "easyship_allow_courier_fallback": False,
        "easyship_apply_shipping_rules": True,
        "easyship_list_unavailable_couriers": True,
        "easyship_incoterms": "DDU",
        "easyship_courier_id": "b85683b8-1d32-41d7-b9af-63ae712ef3fe",
    },
}

ShipmentCancelPayload = {
    "shipment_identifier": "ESUS220509144",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "easyship",
        "carrier_name": "easyship",
        "docs": {"label": ANY},
        "label_type": "PNG",
        "meta": {
            "easyship_courier_account_id": "7505df80-af51-46a0-b2ee-ac9eacfcd3e4",
            "easyship_courier_id": "b85683b8-1d32-41d7-b9af-63ae712ef3fe",
            "easyship_shipment_id": "ESUS220509144",
            "tracking_numbers": ["9405509104250026972189"],
            "rate_provider": "ups",
        },
        "shipment_identifier": "ESUS220509144",
        "tracking_number": "9405509104250026972189",
    },
    [],
]

ParsedCancelShipmentResponse = ParsedCancelShipmentResponse = [
    {
        "carrier_id": "easyship",
        "carrier_name": "easyship",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ParsedShipmentResponseWithoutLabel = [
    None,
    [
        {
            "carrier_id": "easyship",
            "carrier_name": "easyship",
            "code": "warning",
            "details": {},
            "message": "Invalid address provided for Receiver Address - Unable to "
            "identify address if street number is missing.",
        }
    ],
]


ShipmentRequest = {
    "courier_selection": {
        "allow_courier_fallback": False,
        "apply_shipping_rules": True,
        "list_unavailable_couriers": True,
        "selected_courier_id": "b85683b8-1d32-41d7-b9af-63ae712ef3fe",
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
    },
    "incoterms": "DDU",
    "metadata": {},
    "insurance": {"is_insured": False},
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
    },
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
        "state": "Yuen Long",
    },
    "set_as_residential": False,
    "shipping_settings": {
        "buy_label": True,
        "buy_label_synchronous": True,
        "printing_options": {
            "commercial_invoice": "A4",
            "format": "pdf",
            "label": "4x6",
            "remarks": "string",
        },
        "units": {
            "dimensions": "cm",
            "weight": "kg",
        },
    },
    "parcels": [
        {
            "box": {
                "height": 10.0,
                "length": 10.0,
                "width": 10.0,
                "slug": "custom",
            },
            "items": [
                {
                    "category": "bags_luggages",
                    "actual_weight": 10.0,
                    "contains_battery_pi966": True,
                    "contains_battery_pi967": True,
                    "contains_liquids": True,
                    "declared_currency": "USD",
                    "declared_customs_value": 20,
                    "description": "item",
                    "hs_code": "123456",
                    "origin_country_alpha2": "HK",
                    "quantity": 2,
                    "sku": "sku",
                }
            ],
            "total_actual_weight": 1.0,
        }
    ],
}

ShipmentCancelRequest = {"easyship_shipment_id": "ESUS220509144"}


ShipmentResponse = """{
	"shipment": {
		"easyship_shipment_id": "ESUS220509144",
		"buyer_regulatory_identifiers": {
			"ein": null,
			"ssn": null,
			"vat_number": null
		},
		"consignee_tax_id": null,
		"courier": {
			"id": "7505df80-af51-46a0-b2ee-ac9eacfcd3e4",
			"name": "USPS - Priority Mail"
		},
		"created_at": "2024-09-27T12:52:39Z",
		"currency": "USD",
		"delivery_state": "not_created",
		"destination_address": {
			"city": "Los Angeles",
			"company_name": "Destination Company",
			"contact_email": "destination@example.com",
			"contact_name": "John Doe",
			"contact_phone": "+13101234567",
			"country_alpha2": "US",
			"line_1": "1234 Sunset Blvd",
			"line_2": "Suite 101",
			"postal_code": "90026",
			"state": "CA"
		},
		"incoterms": "DDU",
		"insurance": {
			"is_insured": false,
			"insured_amount": 960.85,
			"insured_currency": "USD"
		},
		"label_generated_at": "2024-09-27T12:52:43Z",
		"label_paid_at": "2024-09-27T12:52:41Z",
		"label_state": "generated",
		"last_failure_http_response_messages": [],
		"metadata": {},
		"order_created_at": null,
		"order_data": {
			"buyer_notes": null,
			"buyer_selected_courier_name": null,
			"order_created_at": null,
			"order_tag_list": [],
			"platform_name": null,
			"platform_order_number": null,
			"seller_notes": null
		},
		"origin_address": {
			"city": "New York",
			"company_name": "Origin Company",
			"contact_email": "origin@example.com",
			"contact_name": "Jane Smith",
			"contact_phone": "+1 212-987-6543",
			"country_alpha2": "US",
			"line_1": "5678 Broadway St",
			"line_2": "Floor 5",
			"postal_code": "10036",
			"state": "NY"
		},
		"parcels": [
			{
				"box": {
					"id": null,
					"name": null,
					"outer_dimensions": {
						"length": 15.0,
						"width": 20.0,
						"height": 10.0
					},
					"slug": null,
					"type": "box",
					"weight": 0.0
				},
				"id": "d69117bd-e78a-48e5-8e21-1a41300e4c7e",
				"items": [
					{
						"actual_weight": 0.5143650953055422,
						"category": null,
						"contains_battery_pi966": null,
						"contains_battery_pi967": null,
						"contains_liquids": null,
						"declared_currency": "USD",
						"declared_customs_value": 500.0,
						"description": "Smartphone",
						"dimensions": {
							"length": 0.0,
							"width": 0.0,
							"height": 0.0
						},
						"hs_code": "1000000000",
						"id": "0e763da2-7aff-479e-89ef-d93751b9f9a1",
						"origin_country_alpha2": "US",
						"origin_currency": "USD",
						"origin_customs_value": 500.0,
						"quantity": 1,
						"sku": "ELEC-001"
					},
					{
						"actual_weight": 0.2468952457466602,
						"category": null,
						"contains_battery_pi966": null,
						"contains_battery_pi967": null,
						"contains_liquids": true,
						"declared_currency": "USD",
						"declared_customs_value": 150.0,
						"description": "Shampoo Bottle",
						"dimensions": {
							"length": 0.0,
							"width": 0.0,
							"height": 0.0
						},
						"hs_code": "1000000001",
						"id": "a037b58a-8055-41b6-9687-4084f85649e5",
						"origin_country_alpha2": "US",
						"origin_currency": "USD",
						"origin_customs_value": 150.0,
						"quantity": 3,
						"sku": "BEAUTY-002"
					}
				],
				"total_actual_weight": 0.761260341052
			}
		],
		"pickup_state": "not_requested",
		"rates": [
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff",
					"free_pickup"
				],
				"cost_rank": 3.0,
				"courier_id": "7505df80-af51-46a0-b2ee-ac9eacfcd3e4",
				"courier_logo_url": null,
				"courier_name": "USPS - Priority Mail",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 10.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 0.0,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 3,
				"min_delivery_time": 1,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 10.85,
				"shipment_charge_total": 10.85,
				"total_charge": 10.85,
				"tracking_rating": 2.0,
				"value_for_money_rank": 1.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff",
					"free_pickup"
				],
				"cost_rank": 8.0,
				"courier_id": "137a79e8-ae1c-4369-9855-44cf8ff784c4",
				"courier_logo_url": null,
				"courier_name": "USPS - Priority Mail Signature",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 9.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 0.0,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 3,
				"min_delivery_time": 1,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 14.55,
				"shipment_charge_total": 14.55,
				"total_charge": 14.55,
				"tracking_rating": 2.0,
				"value_for_money_rank": 3.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff"
				],
				"cost_rank": 9.0,
				"courier_id": "4cf66d63-4e4a-456b-86c1-50964ad9f7b7",
				"courier_logo_url": null,
				"courier_name": "FedEx Ground®",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 6.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 2.13,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 3,
				"min_delivery_time": 1,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 13.29,
				"shipment_charge_total": 15.42,
				"total_charge": 15.42,
				"tracking_rating": 3.0,
				"value_for_money_rank": 4.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff",
					"free_pickup"
				],
				"cost_rank": 1.0,
				"courier_id": "c3e97b11-2842-44f1-84d1-afaa6b3f0a7c",
				"courier_logo_url": null,
				"courier_name": "USPS - Ground Advantage",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 16.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 0.0,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 5,
				"min_delivery_time": 2,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 8.0,
				"shipment_charge_total": 8.0,
				"total_charge": 8.0,
				"tracking_rating": 2.0,
				"value_for_money_rank": 6.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff",
					"free_pickup"
				],
				"cost_rank": 4.0,
				"courier_id": "7a1424ff-0d4e-4d55-bdfe-e4c6661debbf",
				"courier_logo_url": null,
				"courier_name": "USPS - Ground Advantage Signature",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 15.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 0.0,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 5,
				"min_delivery_time": 2,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 11.7,
				"shipment_charge_total": 11.7,
				"total_charge": 11.7,
				"tracking_rating": 2.0,
				"value_for_money_rank": 8.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff"
				],
				"cost_rank": 7.0,
				"courier_id": "eac604a4-34c9-41b6-b5b1-231fb785d071",
				"courier_logo_url": null,
				"courier_name": "FedEx Ground® Economy",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 12.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 0.0,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 5,
				"min_delivery_time": 2,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 14.09,
				"shipment_charge_total": 14.09,
				"total_charge": 14.09,
				"tracking_rating": 3.0,
				"value_for_money_rank": 10.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff",
					"free_pickup"
				],
				"cost_rank": 14.0,
				"courier_id": "a623a62b-5631-4dce-ae15-bbcf89e49c52",
				"courier_logo_url": null,
				"courier_name": "USPS - Priority Mail Express",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 3.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 0.0,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 2,
				"min_delivery_time": 1,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 54.15,
				"shipment_charge_total": 54.15,
				"total_charge": 54.15,
				"tracking_rating": 2.0,
				"value_for_money_rank": 11.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff"
				],
				"cost_rank": 11.0,
				"courier_id": "a9e3f424-713c-4efa-b445-71cd60c88ccd",
				"courier_logo_url": null,
				"courier_name": "FedEx Express Saver®",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 11.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 4.75,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 3,
				"min_delivery_time": 2,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 30.15,
				"shipment_charge_total": 34.9,
				"total_charge": 34.9,
				"tracking_rating": 3.0,
				"value_for_money_rank": 12.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff"
				],
				"cost_rank": 12.0,
				"courier_id": "84135827-1538-4be2-b26e-afd8b3f3b4bd",
				"courier_logo_url": null,
				"courier_name": "FedEx 2Day®",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 5.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 0.0,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 2,
				"min_delivery_time": 2,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 41.67,
				"shipment_charge_total": 41.67,
				"total_charge": 41.67,
				"tracking_rating": 3.0,
				"value_for_money_rank": 13.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff"
				],
				"cost_rank": 13.0,
				"courier_id": "5eee483f-1416-42bb-8f7d-3ad384f3ee36",
				"courier_logo_url": null,
				"courier_name": "FedEx 2Day® A.M.",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 4.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 6.27,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 2,
				"min_delivery_time": 2,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 39.82,
				"shipment_charge_total": 46.09,
				"total_charge": 46.09,
				"tracking_rating": 3.0,
				"value_for_money_rank": 14.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff"
				],
				"cost_rank": 15.0,
				"courier_id": "de8835b8-17c5-4878-b636-9f9fdbab9265",
				"courier_logo_url": null,
				"courier_name": "FedEx Standard Overnight®",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 2.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 11.62,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 1,
				"min_delivery_time": 1,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 73.77,
				"shipment_charge_total": 85.39,
				"total_charge": 85.39,
				"tracking_rating": 3.0,
				"value_for_money_rank": 15.0,
				"warehouse_handling_fee": 0.0
			},
			{
				"additional_services_surcharge": 0.0,
				"available_handover_options": [
					"dropoff"
				],
				"cost_rank": 16.0,
				"courier_id": "8fb58899-7c4d-43b3-be2c-ec4c2d3ba375",
				"courier_logo_url": null,
				"courier_name": "FedEx Priority Overnight®",
				"courier_remarks": null,
				"currency": "USD",
				"ddp_handling_fee": 0.0,
				"delivery_time_rank": 1.0,
				"description": null,
				"discount": {
					"amount": 0,
					"origin_amount": 0
				},
				"easyship_rating": null,
				"estimated_import_duty": 0,
				"estimated_import_tax": 0,
				"fuel_surcharge": 12.75,
				"full_description": null,
				"import_duty_charge": 0.0,
				"import_tax_charge": 0.0,
				"import_tax_non_chargeable": 0.0,
				"incoterms": "DDU",
				"insurance_fee": 0.0,
				"is_above_threshold": false,
				"max_delivery_time": 1,
				"min_delivery_time": 1,
				"minimum_pickup_fee": 0.0,
				"other_surcharges": null,
				"oversized_surcharge": 0.0,
				"payment_recipient": "Easyship",
				"provincial_sales_tax": 0.0,
				"rates_in_origin_currency": null,
				"remote_area_surcharge": 0.0,
				"remote_area_surcharges": null,
				"residential_discounted_fee": null,
				"residential_full_fee": null,
				"sales_tax": 0.0,
				"shipment_charge": 80.96,
				"shipment_charge_total": 93.71,
				"total_charge": 93.71,
				"tracking_rating": 3.0,
				"value_for_money_rank": 16.0,
				"warehouse_handling_fee": 0.0
			}
		],
		"regulatory_identifiers": {
			"eori": null,
			"ioss": null,
			"vat_number": null
		},
		"return": false,
		"return_address": {
			"city": "Los Angeles",
			"company_name": "company",
			"contact_email": "shipper@company.com",
			"contact_name": "Test shipper",
			"contact_phone": "+13234747688",
			"country_alpha2": "US",
			"line_1": "6303 Eunice Ave",
			"line_2": "",
			"postal_code": "90042",
			"state": "California"
		},
		"sender_address": {
			"city": "Los Angeles",
			"company_name": "company",
			"contact_email": "shipper@company.com",
			"contact_name": "Test shipper",
			"contact_phone": "+13234747688",
			"country_alpha2": "US",
			"line_1": "6303 Eunice Ave",
			"line_2": "",
			"postal_code": "90042",
			"state": "California"
		},
		"set_as_residential": false,
		"shipment_state": "created",
		"shipping_documents": [
			{
				"base64_encoded_strings": [
					"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"
				],
				"category": "label",
				"format": "png",
				"page_size": "4x6",
				"required": true,
				"url": null
			},
			{
				"base64_encoded_strings": [
					"iVBORw0KGgoAAAANSUhEUgAABLAAAAcICAAAAAAJO2eWAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAAASwAAAEsAHOI6VIAAAAHdElNRQfoCRsMNC7SLYb8AACAAElEQVR42uz9TY7zzOP2fR356ydG3EI+kRASE+R+NoDcAxbgLMEtMWDqXoKzhGQJzhKSBTCIBywgFoyY8MQzJghswT0CIZmB3+1y4nSnXyr9/Qyuq0/HKdvl8pHy+6oUANjhv6gCALYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1/vOVhWdJlhapJPmO6/u/vFgAv92qvGPcWyMMyip2x2zwqRME/myRpRZ+tKjYRpZJup5ot0YpjmmWFpLjub7vfLCWFxRSHNMskeQ7XuDSLgGjLwuszb6YjuBH/kyRSwNrWbGSVOyTpPrL8Wcy4PYo2W7f+5cTRKORkpma8Jw7CpmMYlyeWrqp/n+6sh7SY/vn9qNjAL9SudwdZZ29mVGi3FzklamV9xdblnk0HCG8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VHID6Zh1289KClxtNzvJ81UcCy+VAndrQWClr4N/OievXcq++lGf40ckjwNk8HzRQyAd3/qFXxxJyl57F310QeifjJ8Zxv4Q9hLwB3cJ++9EUPtuhurIVZk3R1i83Km3kd+/pcT9g1BO89C+fHgsPe6qoS+alBaNv9Mrvi08nhQsNbua08+mQz60AmnD+JOBVZbnyJPkhN3hm0voSCrLPPIk+XFZntxqC7Tgp/3SXtzphL1DRIcumLsl7WebH5ke/3mq+0Duoamtppxe4YfxSF1gTT8zDPkAdgmBJ1HdSuS64yftpakkx/PvKy1JJNfrnc7LjoXke854pLmSp59dG3shAguANbgOC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgsANYgsABYg8ACYA0CC4A1CCwA1iCwAFiDwAJgDQILgDUILADWILAAWIPAAmANAguANQgs4O9Ztf697R9R4Ga1XjBW9v5v9W//kW82/sO6A/6w4ng8nj5fzHHRtF4Lqcg+8M0WgQX8Rd5WkpQlRyWb7WdLS7IlY+0LBb7jfOCbLQIL+Iscv/p/mL0W+88GVvK2aLRMOnzsmy0CC/jT3O17cQw+/v0sS9OFu3XOh7/ZIrCAvy14V/qJwNrvvvObnCUE/ra237Nfv65W/zZtpyd7f1mt1kdtVqtqQLFbr1Yv7+nSkovderX691YXuFrtpFVT1getSlYY8Nes5LenBrMXRVspfWsOf4exJGn/Xv1zW+xUSt0Yzja8WmDj+F5UfwSxI6lJqvL2N+exSwj8bXvJk4p1odDxs3T//2/n7o4bhaEwDL8taEtQSiAl4BLkEnAJUIIpAUowJVglmBJCCVYJ2gsQSdaJl6w9s2b8PTdh/KPo6puDOMe0uQO6Haaw1rdVNn6u3wTrstC3YWeW3EJ2WyhM7ruhG07Aka7l5g6KKCLPBvJ0eTJwjrGBfYwxxj2UMcazwZzS+8QYz5Yixhjj0WCvLTg5G2hijPHs0tLlV3lz+c1rdIYl8oyC995731WbQGmghxKAEnqgCxwymBu26AYzXuUlw4Lu+DZQFgCmMdThTtvWLaHIM+rfB2KKPVCkuzyf/sydWlUYXyim4/mywhd//weYMQExZRW8u8+2VWGJPDOTNw1AludA31VTJ2fPHDHjGZanTvOHsKBg6nHp+aMbi7Z7UIUl8owuH81573vmLofhvd1hvPiUUQvy58MC9n7bVmCJCFDVkFlril9/vpOiqnD/f5cKLBGBqsbtP5VCl1VU/rMlw/cr/TOdYYkIdOQHC3PMZHPeBD+9kHInVNWCEcDs/Ydj+nQOdjsFlojAkDJlekqYkwaTp4k/Rz8lVlcv6VJwhJRY9Y+Ls28psEQE0o1bvxvLoQLGdoZ+6rlysA0AoWJJp7uDaepwN8wdETdTYIkI5Pht67tqA3gPtmR46byvNmFMJ9swvFTe169hUf7YhvC6875+befm09tp+Fnk+VxOHPupkdQcXxkHlHdTadX4bhxYTtPQaTr6+oIfPp8fxoCrauKib35PFZaIQH5yFmz5ljVmbJxqDs5g3LGY2xpOZQbGHZtlSxZvZQZkzdHcbZuqsETkqpchOz3KXtSHJSKX2oHp4MkPd2tKuJ0CS0QuDTW2ABh28AAt7hPdEorIpX4TcLnFtwF3eJhtKbBE5At+mw7bszsemt9KgSUiXwl13wdM5ooH2pQCS0RWQ31YIrIaCiwRWQ0FloishgJLRFZDgSUiq6HAEpHVUGCJyGoosERkNRRYIrIaCiwRWQ0FloishgJLRFZDgSUiq6HAEpHV+A3Be5DJeZSNiQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyNC0wOS0yN1QxMjo1Mjo0NiswMDowMMjQEx8AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjQtMDktMjdUMTI6NTI6NDYrMDA6MDC5jaujAAAAIHRFWHRwZGY6SGlSZXNCb3VuZGluZ0JveAAyODh4NDMyKzArMNYMlnoAAAATdEVYdHBkZjpWZXJzaW9uAFBERi0xLjO6Vf/0AAAAAElFTkSuQmCC"
				],
				"category": "packing_slip",
				"format": "png",
				"page_size": "4x6",
				"required": true,
				"url": null
			}
		],
		"shipping_settings": {
			"b13a_filing": null
		},
		"tracking_page_url": "https://www.trackmyshipment.co/shipment-tracking/ESUS220509144",
		"trackings": [
			{
				"alternate_tracking_number": null,
				"handler": "usps",
				"leg_number": 1,
				"local_tracking_number": null,
				"tracking_number": "9405509104250026972189",
				"tracking_state": "active"
			}
		],
		"updated_at": "2024-09-27T12:52:43Z",
		"warehouse_state": "none"
	},
	"meta": {
		"request_id": "78ce27105cd8fe897b0e7b343e0a0f45",
		"unavailable_couriers": []
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

ShipmentWithoutLabelResponse = """{
  "shipment": {
    "easyship_shipment_id": "ESUS222545538",
    "buyer_regulatory_identifiers": {
      "ein": null,
      "ssn": null,
      "vat_number": null
    },
    "consignee_tax_id": null,
    "courier": {
      "id": "c3e97b11-2842-44f1-84d1-afaa6b3f0a7c",
      "name": "USPS - Ground Advantage"
    },
    "created_at": "2024-10-10T15:55:23Z",
    "currency": "USD",
    "delivery_state": "not_created",
    "destination_address": {
      "city": "North Charleston",
      "company_name": "N/A",
      "contact_email": "user@mail.com",
      "contact_name": "Antoine Jean Philippe Mosneron Dupin",
      "contact_phone": "N/A",
      "country_alpha2": "US",
      "line_1": "Park Circle",
      "line_2": null,
      "postal_code": "29405",
      "state": "SC"
    },
    "eei_reference": null,
    "incoterms": "DDU",
    "insurance": {
      "is_insured": false,
      "insured_amount": 533.75,
      "insured_currency": "USD"
    },
    "label_generated_at": null,
    "label_paid_at": "2024-10-10T15:55:24Z",
    "label_state": "failed",
    "last_failure_http_response_messages": [
      {
        "code": "1019000",
        "content": "Invalid address provided for Receiver Address - Unable to identify address if street number is missing."
      }
    ],
    "metadata": {},
    "order_created_at": null,
    "order_data": {
      "buyer_notes": null,
      "buyer_selected_courier_name": null,
      "order_created_at": null,
      "order_tag_list": [],
      "platform_name": null,
      "platform_order_number": null,
      "seller_notes": null
    },
    "origin_address": {
      "city": "Jamaica",
      "company_name": "N/A",
      "contact_email": "user@mail.com",
      "contact_name": "Mark3 JFK C/O Teleship",
      "contact_phone": "N/A",
      "country_alpha2": "US",
      "line_1": "147-02 181st St",
      "line_2": null,
      "postal_code": "11413",
      "state": "NY"
    },
    "parcels": [
      {
        "box": {
          "id": null,
          "name": null,
          "outer_dimensions": { "length": 40, "width": 30, "height": 16 },
          "slug": null,
          "type": "box",
          "weight": 0
        },
        "id": "d6456c12-0bc0-401f-84d9-ddebf28e404b",
        "items": [
          {
            "actual_weight": 0.18,
            "category": "Bags & Luggages",
            "contains_battery_pi966": false,
            "contains_battery_pi967": false,
            "contains_liquids": false,
            "declared_currency": "GBP",
            "declared_customs_value": 134,
            "description": "These elegant Ilios earrings feature a delicate and intricate flowery design, crafted from high-q...",
            "dimensions": { "length": 0, "width": 0, "height": 0 },
            "hs_code": null,
            "id": "dff7df0b-9c10-4dd8-b5de-8de8e826310a",
            "origin_country_alpha2": "GB",
            "origin_currency": "USD",
            "origin_customs_value": 175.1482878609744,
            "quantity": 3,
            "sku": "stock-1"
          }
        ],
        "total_actual_weight": 1.2
      }
    ],
    "pickup_state": "not_requested",
    "rates": [
      {
        "additional_services_surcharge": 0,
        "available_handover_options": ["dropoff", "free_pickup"],
        "cost_rank": 1,
        "courier_id": "c3e97b11-2842-44f1-84d1-afaa6b3f0a7c",
        "courier_logo_url": null,
        "courier_name": "USPS - Ground Advantage",
        "courier_remarks": null,
        "currency": "USD",
        "ddp_handling_fee": 0,
        "delivery_time_rank": 1,
        "description": null,
        "discount": { "amount": 0, "origin_amount": 0 },
        "easyship_rating": null,
        "estimated_import_duty": 0,
        "estimated_import_tax": 0,
        "fuel_surcharge": 0,
        "full_description": null,
        "import_duty_charge": 0,
        "import_tax_charge": 0,
        "import_tax_non_chargeable": 0,
        "incoterms": "DDU",
        "insurance_fee": 0,
        "is_above_threshold": false,
        "max_delivery_time": 5,
        "min_delivery_time": 2,
        "minimum_pickup_fee": 0,
        "other_surcharges": null,
        "oversized_surcharge": 0,
        "payment_recipient": "Easyship",
        "provincial_sales_tax": 0,
        "rates_in_origin_currency": null,
        "remote_area_surcharge": 0,
        "remote_area_surcharges": null,
        "residential_discounted_fee": null,
        "residential_full_fee": null,
        "sales_tax": 0,
        "shipment_charge": 8.31,
        "shipment_charge_total": 8.31,
        "total_charge": 8.31,
        "tracking_rating": 2,
        "value_for_money_rank": 1,
        "warehouse_handling_fee": 0
      }
    ],
    "regulatory_identifiers": {
      "eori": null,
      "ioss": null,
      "vat_number": null
    },
    "return": false,
    "return_address": {
      "city": "Jamaica",
      "company_name": "N/A",
      "contact_email": "user@mail.com",
      "contact_name": "Mark3 JFK C/O Teleship",
      "contact_phone": "N/A",
      "country_alpha2": "US",
      "line_1": "147-02 181st St",
      "line_2": null,
      "postal_code": "11413",
      "state": "NY"
    },
    "sender_address": {
      "city": "Jamaica",
      "company_name": "N/A",
      "contact_email": "user@mail.com",
      "contact_name": "Mark3 JFK C/O Teleship",
      "contact_phone": "N/A",
      "country_alpha2": "US",
      "line_1": "147-02 181st St",
      "line_2": null,
      "postal_code": "11413",
      "state": "NY"
    },
    "set_as_residential": true,
    "shipment_state": "created",
    "shipping_documents": [],
    "shipping_settings": { "b13a_filing": null },
    "tracking_page_url": "https://www.trackmyshipment.co/shipment-tracking/ESUS222545538",
    "trackings": [],
    "updated_at": "2024-10-10T15:55:25Z",
    "warehouse_state": "none"
  },
  "meta": {
    "errors": [
      "Invalid address provided for Receiver Address - Unable to identify address if street number is missing."
    ],
    "request_id": "a9dc653f7581c0520cf3471595233ff8",
    "status": "partial_success",
    "unavailable_couriers": []
  }
}
"""
