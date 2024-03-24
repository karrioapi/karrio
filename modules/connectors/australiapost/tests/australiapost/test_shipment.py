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
                f"{gateway.settings.server_url}/shipping/v1/shipments",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping/v1/shipments/794947717776",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mocks:
            mocks.side_effect = [ShipmentResponse, LabelResponse, "encoded label..."]
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


ShipmentPayload = {
    "service": "T28S",
    "reference": "XYZ-001-01",
    "shipper": {
        "person_name": "John Citizen",
        "address_line1": "1 Main Street",
        "postal_code": "3000",
        "city": "MELBOURNE",
        "country_code": "AU",
        "email": "john.citizen@citizen.com",
        "phone_number": "0401234567",
    },
    "recipient": {
        "person_name": "Jane Smith",
        "company_name": "Smith Pty Ltd",
        "address_line1": "123 Centre Road",
        "postal_code": "2000",
        "city": "Sydney",
        "country_code": "AU",
        "state_code": "NSW",
        "email": "jane.smith@smith.com",
        "phone_number": "0412345678",
    },
    "parcels": [
        {
            "length": 10,
            "height": 10,
            "width": 10,
            "weight": 1,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "description": "This is a description of the item",
            "options": {
                "insurance": 1000.0,
                "australiapost_allow_partial_delivery": True,
            },
        },
        {
            "length": 10,
            "height": 10,
            "width": 10,
            "weight": 1,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        },
        {
            "length": 10,
            "height": 10,
            "width": 10,
            "weight": 1,
            "weight_unit": "KG",
            "dimension_unit": "CM",
            "options": {
                "australiapost_authority_to_leave": True,
            },
        },
    ],
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "australiapost",
        "carrier_name": "australiapost",
        "docs": {"label": "encoded label..."},
        "label_type": "PDF",
        "meta": {
            "article_ids": ["ABC000128B4C5", "ABC000128B4C6", "ABC000128B4C7"],
            "carrier_tracking_link": "https://auspost.com.au/mypost/beta/track/details/ABC000128",
            "label_request_id": "c2991876-9596-42ed-aed3-dd11dcfb03ba",
            "tracking_numbers": ["ABC000128", "ABC000128", "ABC000128"],
            "manifest_required": True,
        },
        "shipment_identifier": "9lesEAOvOm4AAAFI3swaDRYB",
        "tracking_number": "ABC000128",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "australiapost",
        "carrier_name": "australiapost",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "shipment": {
        "shipments": [
            {
                "email_tracking_enabled": True,
                "items": [
                    {
                        "allow_partial_delivery": True,
                        "height": 10.0,
                        "item_description": "This is a description of the item",
                        "item_reference": "1",
                        "length": 10.0,
                        "product_id": "T28S",
                        "weight": 1.0,
                        "width": 10.0,
                    },
                    {
                        "height": 10.0,
                        "item_reference": "2",
                        "length": 10.0,
                        "product_id": "T28S",
                        "weight": 1.0,
                        "width": 10.0,
                    },
                    {
                        "authority_to_leave": True,
                        "height": 10.0,
                        "item_reference": "3",
                        "length": 10.0,
                        "product_id": "T28S",
                        "weight": 1.0,
                        "width": 10.0,
                    },
                ],
                "movement_type": "DESPATCH",
                "from": {
                    "country": "AU",
                    "email": "john.citizen@citizen.com",
                    "lines": ["1 Main Street"],
                    "name": "John Citizen",
                    "phone": "0401234567",
                    "postcode": "3000",
                    "suburb": "MELBOURNE",
                },
                "shipment_reference": "XYZ-001-01",
                "to": {
                    "country": "AU",
                    "email": "jane.smith@smith.com",
                    "lines": ["123 Centre Road"],
                    "name": "Jane Smith",
                    "phone": "0412345678",
                    "postcode": "2000",
                    "state": "NSW",
                    "suburb": "Sydney",
                },
            }
        ]
    },
    "label": {
        "preferences": [
            {
                "format": "PDF",
                "groups": [
                    {
                        "branded": True,
                        "group": "Parcel Post",
                        "layout": "A4-1pp",
                        "left_offset": 0,
                        "top_offset": 0,
                    }
                ],
                "type": "PRINT",
            }
        ],
        "shipments": [{"shipment_id": "[SHIPMENT_ID]"}],
        "wait_for_label_url": True,
    },
}

ShipmentCancelRequest = {"shipment_id": "794947717776"}

ShipmentResponse = """{
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
            "email_tracking_enabled": true,
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
                }
            }
        }
    ]
}
"""

LabelResponse = """{
    "labels": [
        {
            "request_id": "c2991876-9596-42ed-aed3-dd11dcfb03ba",
            "url": "https://ptest.npe.auspost.com.au/lodgement4/labels/c2991876-9596-42ed-aed3-dd11dcfb03ba.pdf?AWSAccessKeyId=AKIAR4N3J3VDHZFMRVFM&Expires=1568274226&Signature=ATq0MzBdb89gf98%2FE%2FGWOiPZ%2BTw%3D",
            "status": "AVAILABLE",
            "request_date": "11-09-2019 17:43:46",
            "url_creation_date": "11-09-2019 17:43:46",
            "shipments": [
                {
                    "shipment_id": "t4AK0EhQTu4AAAFeVsxGqhLO",
                    "options": [],
                    "items": [
                        {
                            "item_id": "t4AK0EhQTu4AAAFeVsxGqhLO"
                        }
                    ]
                }
            ],
            "shipment_ids": [
                "t4AK0EhQTu4AAAFeVsxGqhLO"
            ]
        }
    ]
}
"""

ShipmentCancelResponse = """{}"""

ShipmentErrorResponse = """{
    "errors": [
        {
            "code": "44003",
            "name": "DANGEROUS_GOODS_NOT_SUPPORTED_BY_PRODUCT_ERROR",
            "field": "shipments[0].items[0]",
            "message": "The product T28S specified in an item has indicated that dangerous goods will be included in the parcel, however, the product does not allow dangerous goods to be sent using the service.  Please choose a product that allows dangerous goods to be included within the parcel to be sent."
        }
    ]
}
"""
