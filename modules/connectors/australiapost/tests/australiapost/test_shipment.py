import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAustraliaPostShipping(unittest.TestCase):
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
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
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


ShipmentPayload = {}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = []

ParsedCancelShipmentResponse = []


ShipmentRequest = {
    "shipments": [
        {
            "shipment_reference": "XYZ-001-01",
            "customer_reference_1": "Order 001",
            "customer_reference_2": "SKU-1, SKU-2, SKU-3",
            "email_tracking_enabled": True,
            "from": {
                "name": "John Citizen",
                "lines": ["1 Main Street"],
                "suburb": "MELBOURNE",
                "state": "VIC",
                "postcode": "3000",
                "phone": "0401234567",
                "email": "john.citizen@citizen.com",
            },
            "to": {
                "name": "Jane Smith",
                "business_name": "Smith Pty Ltd",
                "lines": ["123 Centre Road"],
                "suburb": "Sydney",
                "state": "NSW",
                "postcode": "2000",
                "phone": "0412345678",
                "email": "jane.smith@smith.com",
            },
            "items": [
                {
                    "item_reference": "SKU-1",
                    "product_id": "T28S",
                    "length": 10.0,
                    "height": 10.0,
                    "width": 10.0,
                    "weight": 1.0,
                    "cubic_volume": 0.001,
                    "authority_to_leave": False,
                    "allow_partial_delivery": True,
                    "contains_dangerous_goods": False,
                    "item_description": "This is a description of the item",
                    "features": {
                        "feature": {
                            "attributes": {
                                "cover_amount": 1000.0,
                                "rate": 0.0,
                                "included_cover": 0.0,
                                "maximum_cover": 1000.0,
                            }
                        }
                    },
                },
                {
                    "item_reference": "SKU-2",
                    "product_id": "T28S",
                    "length": 10.0,
                    "height": 10.0,
                    "width": 10.0,
                    "weight": 1.0,
                    "authority_to_leave": False,
                    "allow_partial_delivery": True,
                },
                {
                    "item_reference": "SKU-3",
                    "product_id": "T28S",
                    "length": 10.0,
                    "height": 10.0,
                    "width": 10.0,
                    "weight": 1.0,
                    "authority_to_leave": False,
                    "allow_partial_delivery": True,
                },
            ],
            "movement_type": "DESPATCH",
        },
        {
            "shipment_reference": "shipment reference 1",
            "from": {
                "country": "AU",
                "email": "larry.citizen@citizen.com",
                "lines": ["123 Main Street"],
                "name": "Larry Smith",
                "phone": "0412345678",
                "postcode": "3000",
                "state": "VIC",
                "suburb": "Melbourne",
            },
            "to": {
                "email": "jane.buyer@citizen.com",
                "lines": ["5 Main Street"],
                "name": "Jane Buyer",
                "phone": "1234567890",
                "postcode": "6012",
                "state": "WLG",
                "suburb": "Karori",
                "country": "NZ",
            },
            "items": [
                {
                    "classification_type": "OTHER",
                    "commercial_value": True,
                    "description_of_other": "This is a classification description",
                    "export_declaration_number": "1234567890",
                    "import_reference_number": "111222333",
                    "item_contents": [
                        {
                            "country_of_origin": "AU",
                            "description": "description",
                            "sku": "ABC1243567",
                            "quantity": 1,
                            "tariff_code": "123456",
                            "value": 55.55,
                            "weight": 0.5,
                            "item_contents_reference": "IC123456",
                        }
                    ],
                    "item_description": "This is a description of the item",
                    "item_reference": "TD1234567",
                    "length": 10.0,
                    "height": 10.0,
                    "weight": 2.0,
                    "product_id": "PTI8",
                    "width": 10.0,
                    "contains_dangerous_goods": False,
                    "authority_to_leave": False,
                    "allow_partial_delivery": True,
                }
            ],
        },
    ]
}

ShipmentCancelRequest = {"shipment_id": "794947717776"}

ShipmentResponse = """ {
    "shipments": [
        {
            "shipment_id": "9lesEAOvOm4AAAFI3swaDRYB",
            "shipment_reference": "XYZ-001-01",
            "shipment_creation_date": "2014-08-27T15:48:09+10:00",
            "shipment_modified_date": "2014-08-27T15:48:09+10:00",
            "customer_reference_1": "Order 001",
            "customer_reference_2": "SKU-1, SKU-2, SKU-3",
            "sender_references": [
            "Order 001",
            "SKU-1, SKU-2, SKU-3"
      	     ],
            "email_tracking_enabled":True,
            "items": [
                {
                    "item_id": "LDCsEAOvU_oAAAFI6MwaDRYB",
                    "item_reference": "SKU-1",
                    "tracking_details": {
                        "article_id": "ABC000128B4C5",
                        "consignment_id": "ABC000128"
                    },
                    "product_id": "T28S",
                    "item_summary": {
                        "total_cost": 5,
                        "total_cost_ex_gst": 4.55,
                        "total_gst": 0.45,
                        "manual_handling_surcharge": 7.60,
                        "status": "Created"
                    }
                },
                {
                    "item_id": "ynesEAOvnlAAAAFI88waDRYB",
                    "item_reference": "SKU-3",
                    "tracking_details": {
                        "article_id": "ABC000128B4C6",
                        "consignment_id": "ABC000128"
                    },
                    "product_id": "T28S",
                    "item_summary": {
                        "total_cost": 4,
                        "total_cost_ex_gst": 3.64,
                        "total_gst": 0.36,
                        "status": "Created"
                    }
                },
                {
                    "item_id": "TkGsEAOv9.4AAAFI8MwaDRYB",
                    "item_reference": "SKU-2",
                    "tracking_details": {
                        "article_id": "ABC000128B4C7",
                        "consignment_id": "ABC000128"
                    },
                    "product_id": "T28S",
                    "item_summary": {
                        "total_cost": 4,
                        "total_cost_ex_gst": 3.64,
                        "total_gst": 0.36,
                        "status": "Created"
                    }
                }
            ],
            "shipment_summary": {
                "total_cost": 13,
                "total_cost_ex_gst": 11.82,
                "fuel_surcharge": 2.15,
                "total_gst": 1.18,
                "manual_handling_surcharge": 7.60,
                "status": "Created",
                "number_of_items": 3,
                "tracking_summary": {
                    "Initiated": 3
                },
            }
        }
    ]
}
"""

ShipmentCancelResponse = """"""
