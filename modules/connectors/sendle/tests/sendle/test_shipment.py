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
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.sendle.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
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


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {}

ShipmentCancelPayload = {
    "shipment_identifier": "f5233746-71d4-4b05-bf63-56f4abaed5f6",
}

ParsedShipmentResponse = []

ParsedIntlShipmentResponse = []

ParsedCancelShipmentResponse = []


ShipmentRequest = {}

IntlShipmentRequest = {}

ShipmentCancelRequest = {"id": "f5233746-71d4-4b05-bf63-56f4abaed5f6"}

ShipmentResponse = """{
  "order_id": "f5233746-71d4-4b05-bf63-56f4abaed5f6",
  "state": "Pickup",
  "order_url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6",
  "sendle_reference": "S34WER4S",
  "tracking_url": "https://track.sendle.com/tracking?ref=S34WER4S",
  "metadata": {},
  "labels": [
    {
      "format": "pdf",
      "size": "letter",
      "url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6/labels/letter.pdf"
    },
    {
      "format": "pdf",
      "size": "cropped",
      "url": "https://api.sendle.com/api/orders/f5233746-71d4-4b05-bf63-56f4abaed5f6/labels/cropped.pdf"
    }
  ],
  "scheduling": {
    "is_cancellable": true,
    "pickup_date": "2022-07-29",
    "picked_up_on": null,
    "delivered_on": null,
    "estimated_delivery_date_minimum": "2022-08-01",
    "estimated_delivery_date_maximum": "2022-08-02",
    "status": null
  },
  "hide_pickup_address": false,
  "description": "Care package",
  "kilogram_weight": "2.7",
  "weight": {
    "units": "kg",
    "value": "2.7"
  },
  "customer_reference": "#123",
  "sender": {
    "contact": {
      "name": "Georgia",
      "phone": "18005555555",
      "email": "georgia@catsocksltd.com",
      "company": "Cat Socks",
      "sendle_id": "georgia_cat_socks"
    },
    "address": {
      "address_line1": "121 Crumble Road",
      "address_line2": null,
      "suburb": "Ottowa",
      "state_name": "ON",
      "postcode": "K1G 6P8",
      "country": "Canada"
    },
    "instructions": null
  },
  "receiver": {
    "contact": {
      "name": "Tony",
      "phone": null,
      "email": "tony@example.org",
      "company": null
    },
    "address": {
      "address_line1": "5128 Av. Louis Fréchette",
      "address_line2": null,
      "suburb": "Ottowasda",
      "state_name": "QC",
      "postcode": "G1S 3N4",
      "country": "Canada"
    },
    "instructions": "Near the front door please!"
  },
  "route": {
    "delivery_guarantee_status": "ineligible",
    "type": "export",
    "description": "Ontario, Canada to Quebec, Canada"
  },
  "price": {
    "gross": {
      "amount": 19.95,
      "currency": "CAD"
    },
    "net": {
      "amount": 17.35,
      "currency": "CAD"
    },
    "tax": {
      "amount": 2.6,
      "currency": "CAD"
    }
  },
  "packaging_type": "box",
  "price_breakdown": {
    "base": {
      "amount": 12.95,
      "currency": "CAD"
    },
    "base_tax": {
      "amount": 1.94,
      "currency": "CAD"
    },
    "cover": {
      "amount": 0,
      "currency": "CAD"
    },
    "cover_tax": {
      "amount": 0,
      "currency": "CAD"
    },
    "discount": {
      "amount": 0,
      "currency": "CAD"
    },
    "discount_tax": {
      "amount": 0,
      "currency": "CAD"
    },
    "fuel_surcharge": {
      "amount": 4.4,
      "currency": "CAD"
    },
    "fuel_surcharge_tax": {
      "amount": 0.66,
      "currency": "CAD"
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
  "label_provider": "customer",
  "product": {
    "atl_only": true,
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
