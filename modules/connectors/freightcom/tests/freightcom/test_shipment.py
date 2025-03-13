import datetime
import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
# from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestFreightcomShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(**ShipmentCancelPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)
        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )
        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.freightcom.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipment",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.freightcom.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipment/{self.ShipmentCancelRequest.shipment_identifier}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.freightcom.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            response =  karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            with patch("karrio.providers.freightcom.utils.request") as mock:
                mock.return_value = ""
                parsed_response = response.parse()
                print(parsed_response)

                self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.freightcom.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
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
    "service": "freightcom_canpar_ground",
    "options": {
        "signature_confirmation": True,
        "shipping_date": datetime.datetime(2025, 2, 25, 1, 0).strftime("%Y-%m-%dT%H:%M"),
    },
    "reference": "#Order 11111",
}

ShipmentCancelPayload = {
    "shipment_identifier": "shipment_id",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "freightcom",
        "carrier_name": "freightcom",
        "docs": {},
        'label_type': 'PDF',
        "meta": {
            'carrier_tracking_link': 'https://www.ups.com/WebTracking?trackingNumber=1ZXXXXXXXXXXXXXXXX',
            'freightcom_service_id': 'ups.standard',
            'freightcom_unique_id': '38a8b937-4262-497b-8f5c-b9d9d4c6bae6',
            'rate_provider': 'ups',
            'service_name': 'freightcom_ups_standard',
            'tracking_numbers': ['1ZXXXXXXXXXXXXXXXX']
        },

            "shipment_identifier": "uQeh1XwbVIbIyP9mEPtVM2puAFZYmAYA",
            "tracking_number": "1ZXXXXXXXXXXXXXXXX"
        },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "freightcom",
        "carrier_name": "freightcom",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ShipmentRequest = {
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
            "signature_requirement": "required"
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
        "reference_codes": ["#Order 11111"]
    },
    'payment_method_id': 'string',
    "service_id": "canpar.ground",
    "unique_id": ANY
}

ShipmentCancelRequest = "shipment_id"


ShipmentResponse = """
{
"shipment": {
    "id": "uQeh1XwbVIbIyP9mEPtVM2puAFZYmAYA",
    "unique_id": "38a8b937-4262-497b-8f5c-b9d9d4c6bae6",
    "state": "waiting-for-scheduling",
    "transaction_number": "19989362",
    "primary_tracking_number": "1ZXXXXXXXXXXXXXXXX",
    "tracking_numbers": [
      "1ZXXXXXXXXXXXXXXXX",
      "1ZXXXXXXXXXXXXXXXX"
    ],
    "tracking_url": "https://www.ups.com/WebTracking?trackingNumber=1ZXXXXXXXXXXXXXXXX",
    "return_tracking_number": "",
    "bolnumber": "",
    "pickup_confirmation_number": "",
    "details": {
      "id": "HNrzG2iRHKJ6XN0CQwYgKBQnABvx2Yi5",
      "expected_ship_date": {
        "year": 2025,
        "month": 2,
        "day": 12
      },
      "origin": {
        "searchable_id": "",
        "name": "Cheques Plus",
        "address": {
          "address_line1": "4054 Rue Alfred Laliberté",
          "address_line2": "",
          "unit_number": "",
          "city": "Boisbriand",
          "region": "QC",
          "country": "CA",
          "postal_code": "J7H 1P8",
          "validated": false
        },
        "residential": false,
        "business_type": "",
        "tailgate_required": false,
        "instructions": "",
        "contact_name": "Shipping",
        "phone_number": {
          "number": "+1 450-323-6247",
          "extension": ""
        },
        "email_addresses": [
          "sales@chequesplus.com"
        ],
        "receives_email_updates": false,
        "address_book_contact_id": ""
      },
      "destination": {
        "searchable_id": "",
        "name": "ASAP Cheques",
        "address": {
          "address_line1": "623 Fortune Crescent #100",
          "address_line2": "",
          "unit_number": "",
          "city": "Kingston",
          "region": "ON",
          "country": "CA",
          "postal_code": "K7P 0L5",
          "validated": false
        },
        "residential": false,
        "business_type": "",
        "tailgate_required": false,
        "instructions": "",
        "contact_name": "ASAP Cheques Kingston",
        "phone_number": {
          "number": "+1 888-324-3783",
          "extension": ""
        },
        "email_addresses": [
          "admin@shipngo.ca"
        ],
        "receives_email_updates": false,
        "address_book_contact_id": "",
        "ready_at": {
          "hour": 10,
          "minute": 0,
          "populated": true
        },
        "ready_until": {
          "hour": 17,
          "minute": 0,
          "populated": true
        },
        "signature_requirement": "not-required"
      },
      "alternate_destination": null,
      "reference_codes": [
        "ss"
      ],
      "packaging_type": "package",
      "packaging_properties": {
        "packages": [
          {
            "measurements": {
              "cuboid": {
                "l": 10,
                "w": 20,
                "h": 18.2,
                "unit": "cm"
              },
              "weight": {
                "value": 1,
                "unit": "kg"
              }
            },
            "description": "N/A",
            "special_handling_required": false
          },
          {
            "measurements": {
              "cuboid": {
                "l": 10,
                "w": 33.7,
                "h": 18.2,
                "unit": "cm"
              },
              "weight": {
                "value": 1,
                "unit": "kg"
              }
            },
            "description": "N/A",
            "special_handling_required": false
          }
        ],
        "includes_return_label": false
      },
      "insurance": null,
      "billing_contact": null
    },
    "transport_data": null,
    "labels": [
      {
        "size": "letter",
        "format": "pdf",
        "url": "https://s3.us-east-2.amazonaws.com/ssd-test-external/labels/uQeh1XwbVIbIyP9mEPtVM2puAFZYmAYA/yRWNRmUkCGMKIZOjMHNUSy9JlXPYjvVb/shipping-label-19989362-letter.pdf",
        "padded": false
      },
      {
        "size": "a6",
        "format": "zpl",
        "url": "https://s3.us-east-2.amazonaws.com/ssd-test-external/labels/uQeh1XwbVIbIyP9mEPtVM2puAFZYmAYA/yRWNRmUkCGMKIZOjMHNUSy9JlXPYjvVb/shipping-label-19989362-a6.zpl",
        "padded": false
      },
      {
        "size": "a6",
        "format": "pdf",
        "url": "https://s3.us-east-2.amazonaws.com/ssd-test-external/labels/uQeh1XwbVIbIyP9mEPtVM2puAFZYmAYA/yRWNRmUkCGMKIZOjMHNUSy9JlXPYjvVb/shipping-label-19989362-a6.pdf",
        "padded": false
      },
      {
        "size": "a6",
        "format": "pdf",
        "url": "https://s3.us-east-2.amazonaws.com/ssd-test-external/labels/uQeh1XwbVIbIyP9mEPtVM2puAFZYmAYA/yRWNRmUkCGMKIZOjMHNUSy9JlXPYjvVb/shipping-label-19989362-a6-w-padding.pdf",
        "padded": true
      }
    ],
    "customs_invoice_url": "",
    "rate": {
      "service_id": "ups.standard",
      "valid_until": {
        "year": 2025,
        "month": 2,
        "day": 20
      },
      "total": {
        "value": "1779",
        "currency": "CAD"
      },
      "base": {
        "value": "1779",
        "currency": "CAD"
      },
      "surcharges": [],
      "taxes": [],
      "transit_time_days": 1,
      "transit_time_not_available": false,
      "carrier_name": "UPS",
      "service_name": "Standard"
    },
    "order_source": "Api"
  }
}
"""

ShipmentCancelResponse = """{}
"""
