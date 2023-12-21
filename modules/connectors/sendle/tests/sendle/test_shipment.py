import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSendleShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.IntlShipmentRequest = models.ShipmentRequest(**IntlShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_intl_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.IntlShipmentRequest)

        self.assertEqual(request.serialize(), IntlShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse]
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args_list[0][1]["url"],
                f"{gateway.settings.server_url}/api/orders",
            )
            self.assertEqual(
                mock.call_args_list[1][1]["url"],
                f"https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6/labels/a4.pdf",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.side_effect = [ShipmentResponse, LabelResponse]
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.return_value = ShipmentCancelResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "shipper": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "address_line2": "test",
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
    ],
    "service": "allied_road_service",
    "options": {
        "instructions": "This is just an instruction",
    },
    "reference": "REF-001",
}

IntlShipmentPayload = {
    "shipper": {
        "company_name": "TESTING COMPANY",
        "address_line1": "17 VULCAN RD",
        "address_line2": "test",
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
        },
    ],
    "service": "sendle_standard_pickup",
    "options": {
        "instructions": "This is just an instruction",
    },
    "reference": "REF-001",
    "customs": {
        "commodities": [
            {
                "description": "Lafuma backpack for men for hiking",
                "quantity": 1,
                "weight": 1,
                "value_amount": 100,
                "hs_code": 420292,
                "origin_country": "FR",
            }
        ],
    },
}


ShipmentCancelPayload = {
    "shipment_identifier": "f5233746-71d4-4b05-bf63-56f4abaed5f6",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "sendle",
        "carrier_name": "sendle",
        "docs": {"label": ANY},
        "label_type": "PDF",
        "meta": {
            "carrier_tracking_link": "https://track.sendle.com/tracking?ref=SNFJJ3",
            "customer_reference": "SupBdayPressie",
            "metadata": {},
            "order_id": "f5233746-71d4-4b05-bf63-56f4abaed5f6",
            "order_url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6",
            "shipment_identifiers": ["f5233746-71d4-4b05-bf63-56f4abaed5f6"],
            "tracking_numbers": ["SNFJJ3"],
        },
        "shipment_identifier": "f5233746-71d4-4b05-bf63-56f4abaed5f6",
        "tracking_number": "SNFJJ3",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "sendle",
        "carrier_name": "sendle",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "sendle",
            "carrier_name": "sendle",
            "code": "payment_required",
            "details": {
                "error_description": "One of the payment methods associated "
                "with this account is expiring in the next "
                "week. Please go to your Account Settings "
                "in your Sendle Dashboard and add a new "
                "payment method."
            },
            "message": "One of the payment methods associated with this account is "
            "expiring in the next week. Please go to your Account Settings "
            "in your Sendle Dashboard and add a new payment method.",
        }
    ],
]


ShipmentRequest = [
    {
        "customer_reference": "REF-001",
        "dimensions": {"height": 50.0, "length": 50.0, "units": "CM", "width": 12.0},
        "metadata": {},
        "product_code": "allied_road_service",
        "receiver": {
            "address": {
                "address_line1": "17 VULCAN RD",
                "address_line2": "test",
                "country": "AU",
                "postcode": "6155",
                "state_name": "WA",
                "suburb": "CANNING VALE",
            },
            "contact": {
                "company": "TESTING COMPANY",
                "email": "test@gmail.com",
                "name": "TEST USER",
            },
        },
        "sender": {
            "address": {
                "address_line1": "17 VULCAN RD",
                "address_line2": "test",
                "country": "AU",
                "postcode": "6155",
                "state_name": "WA",
                "suburb": "CANNING VALE",
            },
            "contact": {
                "company": "TESTING COMPANY",
                "email": "test@gmail.com",
                "name": "TEST USER",
            },
        },
        "volume": {"units": "m3", "value": 0.03},
        "weight": {"units": "KG", "value": 20.0},
    }
]

IntlShipmentRequest = [
    {
        "customer_reference": "REF-001",
        "dimensions": {"height": 50.0, "length": 50.0, "units": "CM", "width": 12.0},
        "metadata": {},
        "parcel_contents": [
            {
                "country_of_origin": "FR",
                "description": "Lafuma backpack for men for hiking",
                "hs_code": 420292,
                "quantity": 1,
                "value": "None",
            }
        ],
        "product_code": "STANDARD-PICKUP",
        "receiver": {
            "address": {
                "address_line1": "23 jardin private",
                "country": "CA",
                "postcode": "k1k 4t3",
                "state_name": "ON",
                "suburb": "Ottawa",
            },
            "contact": {"company": "CGI", "name": "Jain"},
        },
        "sender": {
            "address": {
                "address_line1": "17 VULCAN RD",
                "address_line2": "test",
                "country": "AU",
                "postcode": "6155",
                "state_name": "WA",
                "suburb": "CANNING VALE",
            },
            "contact": {
                "company": "TESTING COMPANY",
                "email": "test@gmail.com",
                "name": "TEST USER",
            },
        },
        "volume": {"units": "m3", "value": 0.03},
        "weight": {"units": "KG", "value": 20.0},
    }
]

ShipmentCancelRequest = [{"id": "f5233746-71d4-4b05-bf63-56f4abaed5f6"}]

ShipmentResponse = """{
    "order_id": "f5233746-71d4-4b05-bf63-56f4abaed5f6",
    "state": "Pickup",
    "order_url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6",
    "sendle_reference": "SNFJJ3",
    "tracking_url": "https://track.sendle.com/tracking?ref=SNFJJ3",
    "labels": [
        {
            "format": "pdf",
            "size": "a4",
            "url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6/labels/a4.pdf"
        },
        {
            "format": "pdf",
            "size": "cropped",
            "url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6/labels/cropped.pdf"
        }
    ],
    "scheduling": {
        "is_cancellable": true,
        "pickup_date": "2015-11-24",
        "picked_up_on": "",
        "delivered_on": "",
        "estimated_delivery_date_minimum": "2021-11-29",
        "estimated_delivery_date_maximum": "2021-12-03",
        "status": ""
    },
    "hide_pickup_address": false,
    "description": "Kryptonite",
    "weight": {
        "units": "kg",
        "value": "1.0"
    },
    "volume": {
        "units": "m3",
        "value": "0.01"
    },
    "dimensions": {
        "length": "30.0",
        "width": "20.0",
        "height": "17.0",
        "units": "cm"
    },
    "customer_reference": "SupBdayPressie",
    "metadata": {},
    "sender": {
        "contact": {
            "name": "Lex Luthor",
            "phone": "0491 570 313",
            "email": "lluthor@example.com",
            "company": "LexCorp",
            "sendle_id": "sendleID"
        },
        "address": {
            "address_line1": "123 Gotham Ln",
            "address_line2": "",
            "suburb": "Sydney",
            "state_name": "NSW",
            "postcode": "2000",
            "country": "Australia"
        },
        "instructions": "Knock loudly"
    },
    "receiver": {
        "contact": {
            "name": "Clark Kent",
            "phone": "",
            "email": "clarkissuper@dailyplanet.xyz",
            "company": "Daily Planet"
        },
        "address": {
            "address_line1": "80 Wentworth Park Road",
            "address_line2": "",
            "suburb": "Glebe",
            "state_name": "NSW",
            "postcode": "2037",
            "country": "Australia"
        },
        "instructions": "Give directly to Clark"
    },
    "route": {
        "description": "Sydney to Sydney",
        "type": "same-city",
        "delivery_guarantee_status": "eligible"
    },
    "price": {
        "gross": {
            "amount": 7.7,
            "currency": "AUD"
        },
        "net": {
            "amount": 7.7,
            "currency": "AUD"
        },
        "tax": {
            "amount": 0.0,
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
            "amount": 0.0,
            "currency": "AUD"
        },
        "fuel_surcharge": {
            "amount": 0.2,
            "currency": "AUD"
        },
        "base_tax": {
            "amount": 0.0,
            "currency": "AUD"
        },
        "discount_tax": {
            "amount": 0.0,
            "currency": "AUD"
        },
        "cover_tax": {
            "amount": 0.0,
            "currency": "AUD"
        },
        "fuel_surcharge_tax": {
            "amount": 0.0,
            "currency": "AUD"
        }
    },
    "tax_breakdown": {
        "gst": {
            "amount": 0.87,
            "currency": "CAD",
            "rate": 0.05
        },
        "qst": {
            "amount": 1.73,
            "currency": "CAD",
            "rate": 0.09975
        }
    },
    "cover": {
        "price": {
            "gross": {
                "amount": 0,
                "currency": "CAD"
            },
            "net": {
                "amount": 0,
                "currency": "CAD"
            },
            "tax": {
                "amount": 0,
                "currency": "CAD"
            }
        }
    },
    "packaging_type": "box",
    "contents": {
        "description": "Kryptonite",
        "country_of_origin": "krypton",
        "value": "900.0",
        "currency": "AUD"
    },
    "parcel_contents": [
        {
            "description": "Kryptonite",
            "country_of_origin": "krypton",
            "value": "900.0",
            "currency": "AUD",
            "hs_code": "6815.99.41",
            "quantity": 1
        }
    ],
    "contents_type": "Gift",
    "label_provider": "customer",
    "product": {
        "atl_only": false,
        "code": "STANDARD-PICKUP",
        "name": "Standard Pickup",
        "first_mile_option": "pickup",
        "service": "standard"
    }
}
"""

IntlShipmentResponse = """{
  "order_id": "f5233746-71d4-4b05-bf63-56f4abaed5f6",
  "state": "Pickup",
  "order_url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6",
  "sendle_reference": "SNFJJ3",
  "tracking_url": "https://track.sendle.com/tracking?ref=SNFJJ3",
  "labels": [
    {
      "format": "pdf",
      "size": "a4",
      "url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6/labels/a4.pdf"
    },
    {
      "format": "pdf",
      "size": "cropped",
      "url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6/labels/cropped.pdf"
    }
  ],
  "scheduling": {
    "is_cancellable": true,
    "pickup_date": "2015-11-24",
    "picked_up_on": null,
    "delivered_on": null,
    "estimated_delivery_date_minimum": "2021-11-29",
    "estimated_delivery_date_maximum": "2021-12-03",
    "status": null
  },
  "hide_pickup_address": false,
  "description": "Kryptonite",
  "weight": {
    "units": "kg",
    "value": "1.0"
  },
  "volume": {
    "units": "m3",
    "value": "0.01"
  },
  "dimensions": {
    "length": "30.0",
    "width": "20.0",
    "height": "17.0",
    "units": "cm"
  },
  "customer_reference": "SupBdayPressie",
  "metadata": {
    "your_data": "XYZ123"
  },
  "sender": {
    "contact": {
      "name": "Lex Luthor",
      "phone": "0491 570 313",
      "email": "lluthor@example.com",
      "company": "LexCorp",
      "sendle_id": "sendleID"
    },
    "address": {
      "address_line1": "123 Gotham Ln",
      "address_line2": null,
      "suburb": "Sydney",
      "state_name": "NSW",
      "postcode": "2000",
      "country": "Australia"
    },
    "instructions": "Knock loudly"
  },
  "receiver": {
    "contact": {
      "name": "Clark Kent",
      "phone": null,
      "email": "clarkissuper@dailyplanet.xyz",
      "company": "Daily Planet"
    },
    "address": {
      "address_line1": "80 Wentworth Park Road",
      "address_line2": null,
      "suburb": "Glebe",
      "state_name": "NSW",
      "postcode": "2037",
      "country": "Australia"
    },
    "instructions": "Give directly to Clark"
  },
  "route": {
    "type": "export",
    "description": "Sydney, Australia to New Zealand"
  },
  "price": {
    "gross": {
      "amount": 7.7,
      "currency": "AUD"
    },
    "net": {
      "amount": 7.7,
      "currency": "AUD"
    },
    "tax": {
      "amount": 0,
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
      "amount": 0,
      "currency": "AUD"
    },
    "discount_tax": {
      "amount": 0,
      "currency": "AUD"
    },
    "cover_tax": {
      "amount": 0,
      "currency": "AUD"
    },
    "fuel_surcharge_tax": {
      "amount": 0,
      "currency": "AUD"
    }
  },
  "tax_breakdown": {
    "gst": {
      "amount": 0,
      "currency": "AUD",
      "rate": 0.1
    }
  },
  "packaging_type": "box",
  "contents": {
    "description": "Kryptonite",
    "country_of_origin": "krypton",
    "value": "900.0",
    "currency": "AUD"
  },
  "parcel_contents": [
    {
      "description": "Kryptonite",
      "country_of_origin": "krypton",
      "value": "900.0",
      "currency": "AUD",
      "hs_code": "6815.99.41",
      "quantity": 1
    }
  ],
  "contents_type": "Gift",
  "product": {
    "atl_only": false,
    "code": "STANDARD-PICKUP",
    "name": "Standard Pickup",
    "first_mile_option": "pickup",
    "service": "standard"
  }
}
"""

ShipmentCancelResponse = """{
  "order_id": "f5233746-71d4-4b05-bf63-56f4abaed5f6",
  "state": "Cancelled",
  "order_url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6",
  "sendle_reference": "S34WER4S",
  "tracking_url": "https://track.sendle.com/tracking?ref=S34WER4S",
  "customer_reference": "SupBdayPressie",
  "metadata": {},
  "cancelled_at": "2015-10-15 00:56:51 UTC",
  "cancellation_message": "Cancelled by S6LRX64PV8MABbBbzu6DoBHD during picking up"
}
"""

ErrorResponse = """{
    "error": "payment_required",
    "error_description": "One of the payment methods associated with this account is expiring in the next week. Please go to your Account Settings in your Sendle Dashboard and add a new payment method."
}
"""

LabelResponse = {"label": "label content."}
