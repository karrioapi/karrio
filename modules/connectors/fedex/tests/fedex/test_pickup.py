import unittest
from unittest.mock import patch, ANY

from karrio.schemas.dpdhl.business_interface import CancelPickupResponse
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestFedExPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupUpdateRequest = models.PickupUpdateRequest(**PickupUpdatePayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)

        self.assertEqual(request.serialize(), PickupRequest)

    def test_create_update_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)

        self.assertEqual(request.serialize(), PickupUpdateRequest)

    def test_create_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)

        self.assertEqual(request.serialize(), PickupCancelRequest)

    def test_create_pickup(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickup/v1/pickups",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.side_effect = ["{}", "{}"]
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickup/v1/pickups/cancel",
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/pickup/v1/pickups/cancel",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.side_effect = [PickupCancelResponse, PickupResponse]
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_pickup_response(self):
        with patch("karrio.mappers.fedex.proxy.lib.request") as mock:
            mock.return_value = PickupCancelResponse
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelPickupResponse
            )


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "pickup_date": "2013-10-19",
    "ready_time": "11:00",
    "closing_time": "09:20",
    "package_location": "behind the front desk",
    "address": {
        "company_name": "XYZ Inc.",
        "address_line1": "456 Oak Avenue",
        "address_line2": "Suite 789",
        "city": "Springfield",
        "postal_code": "62701",
        "country_code": "US",
        "person_name": "Jane Smith",
        "phone_number": "2175551234",
        "state_code": "IL",
        "email": "jane.smith@xyz.com",
        "residential": False,
    },
    "parcels": [{"weight": 20, "weight_unit": "LB"}],
    "options": {
        "fedex_carrier_code": "FDXE",
        "fedex_pickup_address_type": "BUSINESS",
    },
}

PickupUpdatePayload = {
    "confirmation_number": "XXX561073",
    "pickup_date": "2013-10-19",
    "ready_time": "11:00",
    "closing_time": "09:20",
    "package_location": "behind the front desk",
    "address": {
        "company_name": "XYZ Inc.",
        "address_line1": "456 Oak Avenue",
        "address_line2": "Suite 789",
        "city": "Springfield",
        "postal_code": "62701",
        "country_code": "US",
        "person_name": "Jane Smith",
        "phone_number": "2175551234",
        "state_code": "IL",
        "email": "jane.smith@xyz.com",
        "residential": False,
    },
    "parcels": [{"weight": 20, "weight_unit": "LB"}],
    "options": {
        "fedex_carrier_code": "FDXE",
        "fedex_pickup_address_type": "BUSINESS",
    },
}

PickupCancelPayload = {
    "confirmation_number": "XXX561073",
    "pickup_date": "2020-07-03",
    "options": {
        "fedex_carrier_code": "FDXE",
        "fedex_pickup_location": "NQAA",
    },
}

ParsedPickupResponse = [
    {
        "carrier_id": "fedex",
        "carrier_name": "fedex",
        "confirmation_number": "NQAA97",
        "pickup_date": "2013-10-19",
    },
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
            "details": {},
            "message": "Recipient Postal-City Mismatch.",
        }
    ],
]

ParsedCancelPickupResponse = [
    {
        "carrier_id": "fedex",
        "carrier_name": "fedex",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [
        {
            "carrier_id": "fedex",
            "carrier_name": "fedex",
            "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
            "details": {},
            "message": "Recipient Postal-City Mismatch.",
        }
    ],
]


PickupRequest = {
    "associatedAccountNumber": {"value": "2349857"},
    "carrierCode": "FDXE",
    "originDetail": {
        "customerCloseTime": "09:20:00",
        "packageLocation": "behind the front desk",
        "pickupAddressType": "BUSINESS",
        "pickupLocation": {
            "accountNumber": {"value": "2349857"},
            "address": {
                "city": "Springfield",
                "countryCode": "US",
                "postalCode": "62701",
                "residential": False,
                "stateOrProvinceCode": "IL",
                "streetLines": ["456 Oak Avenue", "Suite 789"],
            },
            "contact": {
                "companyName": "XYZ Inc.",
                "personName": "Jane Smith",
                "phoneNumber": "2175551234",
            },
        },
        "readyDateTimestamp": "2013-10-19T09:20:00Z",
    },
    "packageCount": 1,
    "pickupNotificationDetail": {
        "emailDetails": [{"address": "jane.smith@xyz.com", "locale": "en_US"}],
        "format": "TEXT",
    },
    "totalWeight": {"units": "LB", "value": 20.0},
}

PickupUpdateRequest = {
    "associatedAccountNumber": {"value": "2349857"},
    "carrierCode": "FDXE",
    "originDetail": {
        "customerCloseTime": "09:20:00",
        "packageLocation": "behind the front desk",
        "pickupAddressType": "BUSINESS",
        "pickupLocation": {
            "accountNumber": {"value": "2349857"},
            "address": {
                "city": "Springfield",
                "countryCode": "US",
                "postalCode": "62701",
                "residential": False,
                "stateOrProvinceCode": "IL",
                "streetLines": ["456 Oak Avenue", "Suite 789"],
            },
            "contact": {
                "companyName": "XYZ Inc.",
                "personName": "Jane Smith",
                "phoneNumber": "2175551234",
            },
        },
        "readyDateTimestamp": "2013-10-19T09:20:00Z",
    },
    "packageCount": 1,
    "pickupNotificationDetail": {
        "emailDetails": [{"address": "jane.smith@xyz.com", "locale": "en_US"}],
        "format": "TEXT",
    },
    "totalWeight": {"units": "LB", "value": 20.0},
}

PickupCancelRequest = {
    "associatedAccountNumber": {"value": "2349857"},
    "pickupConfirmationCode": "XXX561073",
    "carrierCode": "FDXE",
    "scheduledDate": "2020-07-03",
    "location": "NQAA",
}

PickupResponse = """{
  "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "customerTransactionId": "AnyCo_order123456789",
  "output": {
    "pickupConfirmationCode": "3001",
    "message": "Courier on the way",
    "location": "COSA",
    "alerts": [
      {
        "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
        "alertType": "NOTE",
        "message": "Recipient Postal-City Mismatch."
      }
    ]
  }
}
"""

PickupUpdateResponse = """{
  "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "customerTransactionId": "AnyCo_order123456789",
  "output": {
    "pickupConfirmationCode": "3001",
    "message": "Courier on the way",
    "location": "COSA",
    "alerts": []
  }
}
"""

PickupCancelResponse = """{
  "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "customerTransactionId": "AnyCo_order123456789",
  "output": {
    "pickupConfirmationCode": "NQAA97",
    "cancelConfirmationMessage": "Requested pickup has been cancelled Successfully.",
    "alerts": [
      {
        "code": "SHIP.RECIPIENT.POSTALCITY.MISMATCH",
        "alertType": "NOTE",
        "message": "Recipient Postal-City Mismatch."
      }
    ]
  }
}
"""
