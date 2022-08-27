import unittest
from unittest.mock import patch
from tests.ups_freight.fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestUPSFreightPickup(unittest.TestCase):
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
        requests = request.serialize()

        self.assertEqual(requests["cancel"].serialize(), PickupCancelRequest)
        self.assertEqual(requests["create"].serialize(), PickupRequest)

    def test_create_cancel_pickup_request(self):
        request = gateway.mapper.create_cancel_pickup_request(self.PickupCancelRequest)

        self.assertEqual(request.serialize(), PickupCancelRequest)

    def test_create_pickup(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/ship/v1/freight/pickups",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mocks:
            mocks.side_effect = [PickupCancelResponse, "{}"]
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            rate_call, create_call = mocks.call_args_list
            self.assertEqual(
                rate_call[1]["url"],
                f"{gateway.settings.server_url}/ship/v1/freight/pickups",
            )
            self.assertEqual(
                create_call[1]["url"],
                f"{gateway.settings.server_url}/ship/v1/freight/pickups",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/ship/v1/freight/pickups",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.ups_freight.proxy.lib.request") as mock:
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
    "pickup_date": "2015-01-28",
    "address": {
        "company_name": "Jim Duggan",
        "address_line1": "2271 Herring Cove",
        "city": "Halifax",
        "postal_code": "B3L2C2",
        "country_code": "CA",
        "person_name": "John Doe",
        "phone_number": "1 514 5555555",
        "state_code": "NS",
        "residential": True,
        "email": "john.doe@canadapost.ca",
    },
    "parcels": [
        {
            "height": 4,
            "length": 9,
            "width": 5,
            "weight": 150,
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "packaging_type": "pallet",
            "options": {"freight_class": "60"},
        }
    ],
    "instruction": "Door at Back",
    "ready_time": "08:00",
    "closing_time": "16:00",
    "options": {
        "ups_freight_freezable_protection_indicator": True,
        "ups_freight_limited_access_pickup_indicator": True,
        "ups_freight_limited_access_delivery_indicator": True,
        "ups_freight_extreme_length_indicator": True,
    },
}

PickupUpdatePayload = {
    "confirmation_number": "0074698052",
    "pickup_date": "2015-01-28",
    "address": {
        "company_name": "Jim Duggan",
        "address_line1": "2271 Herring Cove",
        "city": "Halifax",
        "postal_code": "B3L2C2",
        "country_code": "CA",
        "person_name": "John Doe",
        "phone_number": "1 514 5555555",
        "state_code": "NS",
        "residential": True,
        "email": "john.doe@canadapost.ca",
    },
    "parcels": [
        {
            "height": 4,
            "length": 9,
            "width": 5,
            "weight": 150,
            "weight_unit": "LB",
            "dimension_unit": "IN",
            "packaging_type": "pallet",
            "options": {"freight_class": "60"},
        }
    ],
    "instruction": "Door at Back",
    "ready_time": "08:00",
    "closing_time": "16:00",
    "options": {
        "ups_freight_freezable_protection_indicator": True,
        "ups_freight_limited_access_pickup_indicator": True,
        "ups_freight_limited_access_delivery_indicator": True,
        "ups_freight_extreme_length_indicator": True,
    },
}

PickupCancelPayload = {
    "confirmation_number": "0074698052",
}

ParsedPickupResponse = [
    {
        "carrier_id": "ups_freight",
        "carrier_name": "ups_freight",
        "confirmation_number": "WBU4776818",
    },
    [
        {
            "carrier_id": "ups_freight",
            "carrier_name": "ups_freight",
            "code": "9369054",
            "message": "User is not registered for freight processing.",
        },
        {
            "carrier_id": "ups_freight",
            "carrier_name": "ups_freight",
            "code": "9369055",
            "message": "User is not eligible for contract rates.",
        },
    ],
]

ParsedCancelPickupResponse = [
    {
        "carrier_id": "ups_freight",
        "carrier_name": "ups_freight",
        "operation": "Cancel Pickup",
        "success": True,
    },
    [
        {
            "carrier_id": "ups_freight",
            "carrier_name": "ups_freight",
            "code": "9369054",
            "message": "User is not registered for freight processing.",
        },
        {
            "carrier_id": "ups_freight",
            "carrier_name": "ups_freight",
            "code": "9369055",
            "message": "User is not eligible for contract rates.",
        },
    ],
]


PickupRequest = {
    "FreightPickupRequest": {
        "DestinationCountryCode": "CA",
        "EarliestTimeReady": "0800",
        "LatestTimeReady": "1600",
        "PickupDate": "20150128",
        "Request": {"TransactionReference": {"CustomerContext": "Pickup transactions"}},
        "Requester": {
            "AttentionName": "John Doe",
            "EMailAddress": "john.doe@canadapost.ca",
            "Name": "Jim Duggan",
            "Phone": {"Number": "1 514 5555555"},
        },
        "ShipFrom": {
            "Address": {
                "AddressLine": "2271 Herring Cove",
                "City": "Halifax",
                "CountryCode": "CA",
                "PostalCode": "B3L2C2",
                "StateProvinceCode": "NS",
            },
            "AttentionName": "John Doe",
            "EMailAddress": "john.doe@canadapost.ca",
            "Name": "Jim Duggan",
            "Phone": {"Number": "1 514 5555555"},
        },
        "ShipmentDetail": {
            "NumberOfPieces": 1,
            "PackagingType": {"Code": "Pallet"},
            "Weight": {"UnitOfMeasurement": {"Code": "LBS"}, "Value": 150.0},
        },
        "ShipmentServiceOptions": {
            "ExtremeLengthIndicator": True,
            "FreezableProtectionIndicator": True,
            "LimitedAccessDeliveryIndicator": True,
            "LimitedAccessPickupIndicator": True,
        },
        "SpecialInstructions": "Door at Back",
    }
}

PickupCancelRequest = {
    "PickupRequestConfirmationNumber": "0074698052",
}


PickupResponse = """{
  "FreightPickupResponse": {
    "Response": {
      "ResponseStatus": {
        "Code": "1",
        "Description": "Success"
      },
      "Alert": [
        {
          "Code": "9369054",
          "Description": "User is not registered for freight processing."
        },
        {
          "Code": "9369055",
          "Description": "User is not eligible for contract rates."
        }
      ],
      "TransactionReference": {
        "CustomerContext": "GG",
        "TransactionIdentifier": "xwsspta112t8kjVgt0C6Fd"
      }
    },
    "PickupRequestConfirmationNumber": "WBU4776818"
  }
}
"""

PickupCancelResponse = """{
  "FreightCancelPickupResponse": {
    "Response": {
      "ResponseStatus": "1",
      "Alert": [
        {
          "Code": "9369054",
          "Description": "User is not registered for freight processing."
        },
        {
          "Code": "9369055",
          "Description": "User is not eligible for contract rates."
        }
      ],
      "TransactionReference": {
        "CustomerContext": "CC",
        "TransactionIdentifier": "xwsspta112t8rws7vKJcFB"
      }
    },
    "FreightCancelStatus": "1"
  }
}
"""
