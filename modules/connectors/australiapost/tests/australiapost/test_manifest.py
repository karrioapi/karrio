import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestAustraliaPostManifest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ManifestRequest = models.ManifestRequest(**ManifestPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_manifest_request(self.ManifestRequest)

        self.assertEqual(request.serialize(), ManifestRequest)

    def test_create_manifest(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.side_effect = [ManifestResponse, "manifest file"]
            karrio.Manifest.create(self.ManifestRequest).from_(gateway)

            create, download = mock.call_args_list
            self.assertEqual(
                create[1]["url"],
                f"{gateway.settings.server_url}/shipping/v1/orders",
            )
            self.assertEqual(
                download[1]["url"],
                f"{gateway.settings.server_url}/shipping/v1/accounts/account-number/orders/AP0000002422/summary",
            )

    def test_parse_manifest_response(self):
        with patch("karrio.mappers.australiapost.proxy.lib.request") as mock:
            mock.side_effect = [ManifestResponse, "manifest file"]
            parsed_response = (
                karrio.Manifest.create(self.ManifestRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedManifestResponse)


if __name__ == "__main__":
    unittest.main()


ManifestPayload = {
    "shipment_identifiers": ["569b9a3accdc791c4ba34d6f"],
    "address": {
        "person_name": "John Citizen",
        "address_line1": "1 Main Street",
        "postal_code": "3000",
        "city": "MELBOURNE",
        "country_code": "AU",
        "email": "john.citizen@citizen.com",
        "phone_number": "0401234567",
    },
    "reference": "My order reference",
}

ParsedManifestResponse = [
    {
        "carrier_id": "australiapost",
        "carrier_name": "australiapost",
        "doc": {"manifest": ANY},
        "meta": {
            "order_creation_date": "2014-08-27T13:55:47+10:00",
            "order_id": "AP0000002422",
            "order_reference": "My order reference",
        },
    },
    [],
]


ManifestRequest = {
    "order_reference": "My order reference",
    "payment_method": "CHARGE_TO_ACCOUNT",
    "consignor": "John Citizen",
    "shipments": [{"shipment_id": "569b9a3accdc791c4ba34d6f"}],
}

ManifestResponse = """{
    "order": {
        "order_id": "AP0000002422",
        "order_reference": "My order reference",
        "order_creation_date": "2014-08-27T13:55:47+10:00",
        "order_summary": {
            "total_cost": 13.29,
            "total_cost_ex_gst": 12.08,
            "total_gst": 1.21,
            "status": "Initiated",
            "tracking_summary": {
                "Sealed": 1
            },
            "number_of_shipments": 1,
            "number_of_items": 1,
            "dangerous_goods_included": false,
            "total_weight": 5.000,
            "shipping_methods": {
                "3H03": 1
            }
        },
        "shipments": [
            {
                "shipment_id": "569b9a3accdc791c4ba34d6f",
                "shipment_reference": "XYZ-001-01",
                "shipment_creation_date": "2014-08-27T13:55:47+10:00",
                "email_tracking_enabled": false,
                "items": [
                    {
                        "weight": 5.000,
                        "authority_to_leave": true,
                        "safe_drop_enabled": true,
                        "allow_partial_delivery": true,
                        "item_id": "NfMK1UnLtDcAAAFyJ1IF297V",
                        "item_reference": "the reference",
                        "tracking_details": {
                            "article_id": "2JD541813301000870900",
                            "consignment_id": "2JD5418133",
                            "barcode_id": "0199312650999998912JD541813301000870900|4200221|8008200703142616"
                        },
                        "product_id": "3H03",
                        "item_summary": {
                            "total_cost": 13.29,
                            "total_cost_ex_gst": 12.08,
                            "total_gst": 1.21,
                            "status": "Sealed"
                        }
                    }
                ],
                "shipment_summary": {
                    "total_cost": 13.29,
                    "total_cost_ex_gst": 12.08,
                    "fuel_surcharge": 0.00,
                    "total_gst": 1.21,
                    "status": "Sealed",
                    "tracking_summary": {
                        "Sealed": 1
                    },
                    "number_of_items": 1
                },
                "movement_type": "DESPATCH",
                "charge_to_account": "0000000000",
                "shipment_modified_date": "2014-08-27T13:55:47+10:00"
            }
        ],
        "payment_method": "CHARGE_TO_ACCOUNT"
    }
}
"""
