import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLParcelDEPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)

        self.assertEqual(request.serialize(), PickupRequest)

    def test_create_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)

        self.assertEqual(request.serialize(), PickupCancelRequest)

    def test_create_pickup(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.pickup_server_url}/orders",
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertIn(
                f"{gateway.settings.pickup_server_url}/orders?",
                mock.call_args[1]["url"],
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            print(parsed_response)
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_pickup_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = PickupCancelResponse
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelPickupResponse
            )


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "pickup_date": "2099-04-21",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "instruction": "Please pickup 3 packages",
    "address": {
        "company_name": "Deutsche Post DHL Group",
        "person_name": "Max Mustermann",
        "address_line1": "Charles-de-Gaulle-Strasse 20",
        "city": "Bonn",
        "postal_code": "53113",
        "country_code": "DE",
        "phone_number": "09999 100111820",
        "state_code": "NRW",
        "email": "max@post.de",
    },
    "parcels": [{"weight": 5, "weight_unit": "KG"}],
    "options": {
        "dhl_parcel_de_transportation_type": "PAKET",
        "dhl_parcel_de_send_confirmation_email": True,
        "dhl_parcel_de_send_time_window_email": True,
    },
}

PickupCancelPayload = {
    "confirmation_number": "123e4567e89b12d3a456426614174000",
}

ParsedPickupResponse = [
    {
        "carrier_id": "dhl_parcel_de",
        "carrier_name": "dhl_parcel_de",
        "confirmation_number": "123e4567e89b12d3a456426614174000",
        "pickup_date": "2099-04-21",
        "meta": {
            "pickup_type": "EZA",
            "free_of_charge": True,
        },
    },
    [],
]

ParsedCancelPickupResponse = [
    {
        "carrier_id": "dhl_parcel_de",
        "carrier_name": "dhl_parcel_de",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupRequest = {
    "customerDetails": {
        "accountNumber": "33333333330102",
        "billingNumber": "33333333330102",
    },
    "pickupLocation": {
        "type": "Address",
        "pickupAddress": {
            "name1": "Deutsche Post DHL Group",
            "name2": "Max Mustermann",
            "addressStreet": "20 Charles-de-Gaulle-Strasse",
            "addressHouse": "20",
            "postalCode": "53113",
            "city": "Bonn",
            "country": "DE",
            "state": "NRW",
        },
    },
    "businessHours": [
        {
            "timeFrom": "09:00",
            "timeUntil": "17:00",
        }
    ],
    "contactPerson": [
        {
            "name": "Max Mustermann",
            "phone": "09999 100111820",
            "email": "max@post.de",
            "emailNotification": {
                "sendPickupConfirmationEmail": True,
                "sendPickupTimeWindowEmail": True,
            },
        }
    ],
    "pickupDetails": {
        "pickupDate": {
            "type": "Date",
            "value": "2099-04-21",
        },
        "totalWeight": {
            "uom": "g",
            "value": 5000,
        },
        "comment": "Please pickup 3 packages",
    },
    "shipmentDetails": {
        "shipments": [
            {
                "transportationType": "PAKET",
                "replacement": False,
            }
        ]
    },
}

PickupCancelRequest = {
    "orderID": "123e4567e89b12d3a456426614174000",
}

PickupResponse = """{
  "confirmation": {
    "type": "ORDERPICKUP",
    "value": {
      "orderID": "123e4567e89b12d3a456426614174000",
      "pickupDate": "2099-04-21",
      "freeOfCharge": true,
      "pickupType": "EZA",
      "confirmedShipments": [
        {
          "transportationType": "PAKET",
          "shipmentNo": "1234567890",
          "orderDate": "2024-01-15T14:30:00"
        }
      ]
    }
  }
}
"""

PickupCancelResponse = """{
  "confirmedCancellations": [
    {
      "orderID": "123e4567e89b12d3a456426614174000",
      "orderState": "STORNIERT",
      "message": "Order successfully cancelled"
    }
  ],
  "failedCancellations": []
}
"""
