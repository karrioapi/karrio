import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUPSPickup(unittest.TestCase):
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
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/pickupcreation/v2409/pickup",
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertIn(
                f"{gateway.settings.server_url}/api/shipments/v2409/pickup/02",
                mock.call_args[1]["url"],
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_pickup_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = PickupCancelResponse
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelPickupResponse
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = PickupErrorResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedPickupErrorResponse
            )


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "pickup_date": "2024-12-15",
    "ready_time": "09:00",
    "closing_time": "17:00",
    "instruction": "Ring doorbell",
    "address": {
        "company_name": "Test Company",
        "person_name": "John Doe",
        "address_line1": "315 Saddle Bridge Drive",
        "city": "Allendale",
        "state_code": "NJ",
        "postal_code": "07401",
        "country_code": "US",
        "phone_number": "5551234567",
        "email": "test@example.com",
    },
    "parcels": [{"weight": 10, "weight_unit": "LB"}],
}

PickupCancelPayload = {
    "confirmation_number": "2929AONCALL02",
}

ParsedPickupResponse = [
    {
        "carrier_id": "ups",
        "carrier_name": "ups",
        "confirmation_number": "2929AONCALL02",
        "meta": {
            "rate_type": "SD",
        },
        "pickup_charge": {
            "amount": 6.5,
            "currency": "USD",
            "name": "Pickup Charge",
        },
    },
    [],
]

ParsedCancelPickupResponse = [
    {
        "carrier_id": "ups",
        "carrier_name": "ups",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]

ParsedPickupErrorResponse = [
    None,
    [
        {
            "carrier_id": "ups",
            "carrier_name": "ups",
            "code": "9560131",
            "level": "error",
            "message": "Invalid pickup date",
        },
    ],
]


PickupRequest = {
    "PickupCreationRequest": {
        "AlternateAddressIndicator": "Y",
        "Notification": {
            "ConfirmationEmailAddress": "test@example.com",
        },
        "OverweightIndicator": "N",
        "PaymentMethod": "01",
        "PickupAddress": {
            "AddressLine": "315 Saddle Bridge Drive",
            "City": "Allendale",
            "CompanyName": "Test Company",
            "ContactName": "John Doe",
            "CountryCode": "US",
            "Phone": {"Number": "5551234567"},
            "PostalCode": "07401",
            "ResidentialIndicator": "N",
            "StateProvince": "NJ",
        },
        "PickupDateInfo": {
            "CloseTime": "1700",
            "PickupDate": "20241215",
            "ReadyTime": "0900",
        },
        "PickupPiece": [
            {
                "ContainerCode": "01",
                "DestinationCountryCode": "US",
                "Quantity": "1",
                "ServiceCode": "001",
            }
        ],
        "RatePickupIndicator": "Y",
        "Request": {
            "SubVersion": "2409",
            "TransactionReference": {"CustomerContext": "Pickup Request"},
        },
        "Shipper": {
            "Account": {
                "AccountCountryCode": "US",
                "AccountNumber": "Your Account Number",
            },
        },
        "SpecialInstruction": "Ring doorbell",
        "TotalWeight": {"UnitOfMeasurement": "LBS", "Weight": "10.0"},
    }
}

PickupCancelRequest = {
    "prn": "2929AONCALL02",
    "cancel_by": "02",
}

PickupResponse = """{
    "PickupCreationResponse": {
        "Response": {
            "ResponseStatus": {
                "Code": "1",
                "Description": "Success"
            },
            "TransactionReference": {
                "CustomerContext": "Pickup Request"
            }
        },
        "PRN": "2929AONCALL02",
        "RateStatus": {
            "Code": "01",
            "Description": "Rate available"
        },
        "RateResult": {
            "RateType": "SD",
            "CurrencyCode": "USD",
            "ChargeDetail": [
                {
                    "ChargeCode": "B",
                    "ChargeDescription": "BASE CHARGE",
                    "ChargeAmount": "6.50"
                }
            ],
            "GrandTotalOfAllCharge": "6.50"
        }
    }
}"""

PickupCancelResponse = """{
    "PickupCancelResponse": {
        "Response": {
            "ResponseStatus": {
                "Code": "1",
                "Description": "Success"
            }
        },
        "PickupType": "01"
    }
}"""

PickupErrorResponse = """{
    "response": {
        "errors": [
            {
                "code": "9560131",
                "message": "Invalid pickup date"
            }
        ]
    }
}"""
