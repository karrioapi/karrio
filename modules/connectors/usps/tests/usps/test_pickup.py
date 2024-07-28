import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUSPSPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = models.PickupRequest(**PickupPayload)
        self.PickupUpdateRequest = models.PickupUpdateRequest(**PickupUpdatePayload)
        self.PickupCancelRequest = models.PickupCancelRequest(**PickupCancelPayload)

    def test_create_pickup_request(self):
        request = gateway.mapper.create_pickup_request(self.PickupRequest)
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), PickupRequest)

    def test_create_update_pickup_request(self):
        request = gateway.mapper.create_pickup_update_request(self.PickupUpdateRequest)
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), PickupUpdateRequest)

    def test_create_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)
        logger.debug(request.serialize())
        self.assertEqual(request.serialize(), PickupCancelRequest)

    def test_create_pickup(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v3/carrier-pickup",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v3/carrier-pickup/100094XXX",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/v3/carrier-pickup/100094XXX",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_pickup_response(self):
        with patch("karrio.mappers.usps.proxy.lib.request") as mock:
            mock.return_value = PickupCancelResponse
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            logger.debug(lib.to_dict(parsed_response))
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelPickupResponse
            )


if __name__ == "__main__":
    unittest.main()


PickupPayload = {
    "pickup_date": "2013-10-19",
    "ready_time": "10:20",
    "closing_time": "09:20",
    "instruction": "behind the front desk",
    "address": {
        "company_name": "ABC Corp.",
        "address_line1": "1098 N Fraser Street",
        "city": "Georgetown",
        "postal_code": "29440",
        "country_code": "US",
        "person_name": "Tall Tom",
        "phone_number": "8005554526",
        "state_code": "SC",
    },
    "parcels": [{"weight": 20, "weight_unit": "LB"}],
    "options": {"usps_package_type": "FIRST-CLASS_PACKAGE_SERVICE"},
}

PickupUpdatePayload = {
    "confirmation_number": "100094XXX",
    "pickup_date": "2013-10-19",
    "ready_time": "10:20",
    "closing_time": "09:20",
    "instruction": "behind the front desk",
    "address": {
        "company_name": "ABC Corp.",
        "address_line1": "1098 N Fraser Street",
        "city": "Georgetown",
        "postal_code": "29440",
        "country_code": "US",
        "person_name": "Tall Tom",
        "phone_number": "8005554526",
        "state_code": "SC",
    },
    "parcels": [{"weight": 20, "weight_unit": "LB"}],
}

PickupCancelPayload = {"confirmation_number": "100094XXX"}

ParsedPickupResponse = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "confirmation_number": "string",
        "pickup_date": "2019-08-24",
    },
    [],
]

ParsedCancelPickupResponse = [
    {
        "carrier_id": "usps",
        "carrier_name": "usps",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupRequest = {
    "estimatedWeight": 20.0,
    "packages": [{"packageCount": 1, "packageType": "FIRST-CLASS_PACKAGE_SERVICE"}],
    "pickupAddress": {
        "address": {
            "ZIPCode": "29440",
            "city": "Georgetown",
            "streetAddress": "1098 N Fraser Street",
        },
        "firm": "ABC Corp.",
        "firstName": "Tall Tom",
    },
    "pickupDate": "2013-10-19",
    "pickupLocation": {"specialInstructions": "behind the front desk"},
}

PickupUpdateRequest = {
    "carrierPickupRequest": {
        "estimatedWeight": 20.0,
        "packages": [{"packageCount": 1, "packageType": "OTHER"}],
        "pickupAddress": {
            "address": {
                "ZIPCode": "29440",
                "city": "Georgetown",
                "streetAddress": "1098 N Fraser Street",
            },
            "firm": "ABC Corp.",
            "firstName": "Tall Tom",
        },
        "pickupDate": "2013-10-19",
        "pickupLocation": {"specialInstructions": "behind the front desk"},
    },
    "pickupDate": "2013-10-19",
}

PickupCancelRequest = {"confirmationNumber": "100094XXX"}


PickupResponse = """{
  "confirmationNumber": "string",
  "pickupDate": "2019-08-24",
  "carrierPickupRequest": {
    "pickupDate": "2019-08-24",
    "pickupAddress": {
      "firstName": "string",
      "lastName": "string",
      "firm": "string",
      "address": {
        "streetAddress": "string",
        "streetAddressAbbreviation": "string",
        "secondaryAddress": "string",
        "cityAbbreviation": "string",
        "city": "string",
        "state": "st",
        "ZIPCode": "string",
        "ZIPPlus4": "string",
        "urbanization": "string"
      },
      "contact": [
        {
          "email": "user@example.com"
        }
      ]
    },
    "packages": [
      {
        "packageType": "FIRST-CLASS_PACKAGE_SERVICE",
        "packageCount": 0
      }
    ],
    "estimatedWeight": 0,
    "pickupLocation": {
      "packageLocation": "FRONT_DOOR",
      "specialInstructions": "string"
    }
  }
}
"""

PickupUpdateResponse = """{
  "confirmationNumber": "string",
  "pickupDate": "2019-08-24",
  "carrierPickupRequest": {
    "pickupDate": "2019-08-24",
    "pickupAddress": {
      "firstName": "string",
      "lastName": "string",
      "firm": "string",
      "address": {
        "streetAddress": "string",
        "streetAddressAbbreviation": "string",
        "secondaryAddress": "string",
        "cityAbbreviation": "string",
        "city": "string",
        "state": "st",
        "ZIPCode": "string",
        "ZIPPlus4": "string",
        "urbanization": "string"
      },
      "contact": [
        {
          "email": "user@example.com"
        }
      ]
    },
    "packages": [
      {
        "packageType": "FIRST-CLASS_PACKAGE_SERVICE",
        "packageCount": 0
      }
    ],
    "estimatedWeight": 0,
    "pickupLocation": {
      "packageLocation": "FRONT_DOOR",
      "specialInstructions": "string"
    }
  }
}
"""

PickupCancelResponse = """{"ok": true}"""
