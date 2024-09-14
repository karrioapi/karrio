import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestEasyshipPickup(unittest.TestCase):
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
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_pickup(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_pickup_response(self):
        with patch("karrio.mappers.easyship.proxy.lib.request") as mock:
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
    "confirmation_number": "0074698052",
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

PickupCancelPayload = {"confirmation_number": "0074698052"}

ParsedPickupResponse = [
    {
        "carrier_id": "easyship",
        "carrier_name": "easyship",
        "confirmation_number": "string",
        "pickup_date": "2019-08-24",
    },
    [],
]

ParsedCancelPickupResponse = [
    {
        "carrier_id": "easyship",
        "carrier_name": "easyship",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [],
]


PickupRequest = {
    "courier_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
    "easyship_shipment_ids": ["ESSG10006001"],
    "selected_date": "2022-02-23",
    "selected_from_time": "12:00",
    "selected_to_time": "16:00",
    "time_slot_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
}


PickupUpdateRequest = {
    "courier_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
    "easyship_shipment_ids": ["ESSG10006001"],
    "selected_date": "2022-02-23",
    "selected_from_time": "12:00",
    "selected_to_time": "16:00",
    "time_slot_id": "01563646-58c1-4607-8fe0-cae3e33c0001",
}


PickupCancelRequest = {}


PickupResponse = """{
  "meta": {
    "available_balance": 0,
    "easyship_shipment_ids": ["ESSG10006001"],
    "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477"
  },
  "pickup": {
    "address": {
      "city": "City",
      "company_name": "Test Plc.",
      "contact_email": "asd@asd.com",
      "contact_name": "Foo Bar",
      "contact_phone": "+852-1234-5678",
      "country_alpha2": "HK",
      "default_for": {
        "billing": false,
        "pickup": true,
        "return": true,
        "sender": true
      },
      "hk_district": {
        "area": "Admiralty",
        "district": "Central and Western",
        "id": 1,
        "zone": "Hong Kong Island"
      },
      "id": "01563646-58c1-4607-8fe0-cae3e33c0005",
      "line_1": "123 Test Street",
      "line_2": "Block 3",
      "postal_code": "ABC123",
      "state": "State",
      "validation": {
        "detail": "Address is not valid",
        "status": "invalid_address",
        "comparison": {
          "changes": "",
          "post": "",
          "pre": ""
        }
      }
    },
    "courier": {
      "id": "01563646-58c1-4607-8fe0-cae3e33c0001",
      "name": "USPS"
    },
    "easyship_pickup_id": "PHK10000001",
    "pickup_fee": 0,
    "pickup_reference_number": "string",
    "pickup_state": "pending-confirmation",
    "provider_name": "Standard Pickup",
    "selected_from_time": "2022-02-23T12:00",
    "selected_to_time": "2022-02-23T16:00",
    "shipments_count": 1,
    "total_actual_weight": 30.0
  }
}
"""

PickupUpdateResponse = """{
  "meta": {
    "available_balance": 0,
    "easyship_shipment_ids": ["ESSG10006001"],
    "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477"
  },
  "pickup": {
    "address": {
      "city": "City",
      "company_name": "Test Plc.",
      "contact_email": "asd@asd.com",
      "contact_name": "Foo Bar",
      "contact_phone": "+852-1234-5678",
      "country_alpha2": "HK",
      "default_for": {
        "billing": false,
        "pickup": true,
        "return": true,
        "sender": true
      },
      "hk_district": {
        "area": "Admiralty",
        "district": "Central and Western",
        "id": 1,
        "zone": "Hong Kong Island"
      },
      "id": "01563646-58c1-4607-8fe0-cae3e33c0005",
      "line_1": "123 Test Street",
      "line_2": "Block 3",
      "postal_code": "ABC123",
      "state": "State",
      "validation": {
        "detail": "Address is not valid",
        "status": "invalid_address",
        "comparison": {
          "changes": "",
          "post": "",
          "pre": ""
        }
      }
    },
    "courier": {
      "id": "01563646-58c1-4607-8fe0-cae3e33c0001",
      "name": "USPS"
    },
    "easyship_pickup_id": "PHK10000001",
    "pickup_fee": 0,
    "pickup_reference_number": "string",
    "pickup_state": "pending-confirmation",
    "provider_name": "Standard Pickup",
    "selected_from_time": "2022-02-23T12:00",
    "selected_to_time": "2022-02-23T16:00",
    "shipments_count": 1,
    "total_actual_weight": 30.0
  }
}
"""

PickupCancelResponse = """{
  "meta": {
    "request_id": "01563646-58c1-4607-8fe0-cae3e92c4477"
  },
  "success": {
    "message": "Pickup successfully cancelled"
  }
}
"""
