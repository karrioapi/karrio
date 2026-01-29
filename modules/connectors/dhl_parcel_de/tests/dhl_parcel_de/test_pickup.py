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
        self.PickupRequestASAP = models.PickupRequest(**PickupPayloadASAP)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        self.assertEqual(request.serialize(), PickupRequest)

    def test_create_pickup_request_asap(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequestASAP)
        self.assertEqual(request.serialize(), PickupRequestASAP)

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
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_pickup_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = PickupCancelResponse
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelPickupResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = PickupErrorResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedPickupErrorResponse
            )


if __name__ == "__main__":
    unittest.main()


# Payload matching sandbox API format
PickupPayload = {
    "pickup_date": "2099-04-21",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "instruction": "Test API pickup",
    "address": {
        "company_name": "Maxi Mustermann",
        "address_line1": "Charles-de-Gaulle-Str. 20",
        "city": "Bonn",
        "postal_code": "53113",
        "country_code": "DE",
        "phone_number": "015155555",
        "email": "maxi@post.de",
    },
    "parcels": [{"weight": 5, "weight_unit": "KG"}],
    "options": {
        "dhl_parcel_de_transportation_type": "PAKET",
        "dhl_parcel_de_send_confirmation_email": True,
        "dhl_parcel_de_send_time_window_email": True,
        "billing_number": "22222222220801",
    },
}

# ASAP pickup payload (uses ASAP pickup date type)
PickupPayloadASAP = {
    "pickup_date": "",  # Empty date for ASAP pickup
    "ready_time": "09:00",
    "closing_time": "17:00",
    "instruction": "Test API pickup ASAP",
    "address": {
        "company_name": "Maxi Mustermann",
        "address_line1": "Charles-de-Gaulle-Str. 20",
        "city": "Bonn",
        "postal_code": "53113",
        "country_code": "DE",
        "phone_number": "015155555",
        "email": "maxi@post.de",
    },
    "parcels": [{"weight": 2, "weight_unit": "KG"}],
    "options": {
        "dhl_parcel_de_transportation_type": "PAKET",
        "dhl_parcel_de_send_confirmation_email": True,
        "dhl_parcel_de_send_time_window_email": True,
        "dhl_parcel_de_pickup_date_type": "ASAP",  # Explicitly set ASAP
        "billing_number": "22222222220801",
    },
}

PickupCancelPayload = {
    "confirmation_number": "837624af601a4fab9550e20e746cb1fe",
}

ParsedPickupResponse = [
    {
        "carrier_id": "dhl_parcel_de",
        "carrier_name": "dhl_parcel_de",
        "confirmation_number": "837624af601a4fab9550e20e746cb1fe",
        "pickup_date": "2026-01-29",
        "meta": {
            "pickup_type": "EZA",
            "free_of_charge": False,
            "confirmed_shipments": [
                {
                    "transportation_type": "PAKET",
                    "order_date": "2026-01-28 00:34:00",
                }
            ],
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

ParsedPickupErrorResponse = [
    None,
    [
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "422",
            "message": "Invalid request data",
            "details": {
                "title": "Validation failed",
            },
        },
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "456",
            "message": "customerDetails.billingNumber: Unknown billingnumber",
            "details": {
                "property": "customerDetails.billingNumber",
                "validationState": "error",
            },
        },
    ],
]


PickupRequest = {
    "customerDetails": {
        "billingNumber": "22222222220801",
    },
    "pickupLocation": {
        "type": "Address",
        "pickupAddress": {
            "name1": "Maxi Mustermann",
            "addressStreet": "Charles-de-Gaulle-Str.",
            "addressHouse": "20",
            "postalCode": "53113",
            "city": "Bonn",
            "country": "DE",
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
            "name": "Maxi Mustermann",
            "phone": "015155555",
            "email": "maxi@post.de",
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
        "comment": "Test API pickup",
    },
    "shipmentDetails": {
        "shipments": [
            {
                "transportationType": "PAKET",
            }
        ]
    },
}

PickupRequestASAP = {
    "customerDetails": {
        "billingNumber": "22222222220801",
    },
    "pickupLocation": {
        "type": "Address",
        "pickupAddress": {
            "name1": "Maxi Mustermann",
            "addressStreet": "Charles-de-Gaulle-Str.",
            "addressHouse": "20",
            "postalCode": "53113",
            "city": "Bonn",
            "country": "DE",
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
            "name": "Maxi Mustermann",
            "phone": "015155555",
            "email": "maxi@post.de",
            "emailNotification": {
                "sendPickupConfirmationEmail": True,
                "sendPickupTimeWindowEmail": True,
            },
        }
    ],
    "pickupDetails": {
        "pickupDate": {
            "type": "ASAP",
        },
        "totalWeight": {
            "uom": "g",
            "value": 2000,
        },
        "comment": "Test API pickup ASAP",
    },
    "shipmentDetails": {
        "shipments": [
            {
                "transportationType": "PAKET",
            }
        ]
    },
}

PickupCancelRequest = {
    "orderID": "837624af601a4fab9550e20e746cb1fe",
}

PickupResponse = """{
    "confirmation": {
        "type": "ORDERPICKUP",
        "value": {
            "orderID": "837624af601a4fab9550e20e746cb1fe",
            "pickupDate": "2026-01-29",
            "freeOfCharge": false,
            "pickupType": "EZA",
            "confirmedShipments": [
                {
                    "transportationType": "PAKET",
                    "shipmentNo": "",
                    "orderDate": "2026-01-28 00:34:00"
                }
            ]
        }
    }
}"""

PickupCancelResponse = """{
    "confirmedCancellations": [
        {
            "orderID": "837624af601a4fab9550e20e746cb1fe",
            "orderState": "STORNIERT",
            "message": "Order successfully cancelled"
        }
    ],
    "failedCancellations": []
}"""

PickupErrorResponse = """{
    "status": 422,
    "title": "Validation failed",
    "detail": "Invalid request data",
    "items": [
        {
            "validationMessages": [
                {
                    "property": "customerDetails.billingNumber",
                    "validationState": "error",
                    "validationMessage": "Unknown billingnumber",
                    "validationMessageCode": "456"
                }
            ]
        }
    ]
}"""
