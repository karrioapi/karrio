import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDHLExpressPickup(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.PickupRequest = PickupRequest(**PickupPayload)
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
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.schedule(self.PickupRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_update_pickup(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.update(self.PickupUpdateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_pickup_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = PickupResponse
            parsed_response = (
                karrio.Pickup.schedule(self.PickupRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedPickupResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.mydhl.proxy.lib.request") as mock:
            mock.return_value = ""
            parsed_response = (
                karrio.Pickup.cancel(self.PickupCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelPickupResponse
            )


if __name__ == "__main__":
    unittest.main()


PickupPayload = {}

PickupUpdatePayload = {}

PickupCancelPayload = {"confirmation_number": "0074698052"}

ParsedPickupResponse = []

ParsedCancelPickupResponse = []


PickupRequest = {
    "plannedPickupDateAndTime": "2022-11-20T09:19:40 GMT+08:00",
    "closeTime": "18:00",
    "location": "reception",
    "locationType": "business",
    "accounts": [{"typeCode": "shipper", "number": "123456789"}],
    "specialInstructions": [{"value": "please ring front desk", "typeCode": "TBD"}],
    "remark": "two parcels required pickup",
    "customerDetails": {
        "shipperDetails": {
            "postalAddress": {
                "postalCode": "B24 8DW",
                "cityName": "BIRMINGHAM",
                "countryCode": "GB",
                "addressLine1": "498 Bromford Gate",
                "addressLine2": "Bromford Lane",
                "addressLine3": "Erdington",
            },
            "contactInformation": {
                "email": "that@before.gb",
                "phone": "+1123456789",
                "mobilePhone": "+60112345678",
                "companyName": "Company Name",
                "fullName": "Adam Spencer",
            },
        },
        "receiverDetails": {
            "postalAddress": {
                "postalCode": "14800",
                "cityName": "Prague",
                "countryCode": "CZ",
                "provinceCode": "CZ",
                "addressLine1": "V Parku 2308/10",
                "addressLine2": "addres2",
                "addressLine3": "addres3",
                "countyName": "Central Bohemia",
            },
            "contactInformation": {
                "email": "that@before.de",
                "phone": "+1123456789",
                "mobilePhone": "+60112345678",
                "companyName": "Company Name",
                "fullName": "John Brew",
            },
        },
    },
    "shipmentDetails": [
        {
            "accounts": [{"typeCode": "shipper", "number": "123456789"}],
            "packages": [
                {
                    "typeCode": "3BX",
                    "weight": 10.5,
                    "dimensions": {"length": 25, "width": 35, "height": 15},
                }
            ],
            "productCode": "P",
            "declaredValue": 50,
            "unitOfMeasurement": "metric",
            "valueAddedServices": [
                {"serviceCode": "II", "value": 100, "currency": "GBP"}
            ],
            "isCustomsDeclarable": True,
            "declaredValueCurrency": "EUR",
        }
    ],
}

PickupUpdateRequest = {
    "dispatchConfirmationNumber": "CBJ201220123456",
    "originalShipperAccountNumber": "123456789",
    "plannedPickupDateAndTime": "2019-08-04T14:00:31GMT+01:00",
    "closeTime": "18:00",
    "location": "reception",
    "locationType": "residence",
    "accounts": [{"typeCode": "shipper", "number": "123456789"}],
    "specialInstructions": [{"value": "please ring door bell", "typeCode": "TBD"}],
    "remark": "string",
    "customerDetails": {
        "shipperDetails": {
            "postalAddress": {
                "postalCode": "14800",
                "cityName": "Prague",
                "countryCode": "CZ",
                "provinceCode": "CZ",
                "addressLine1": "V Parku 2308/10",
                "addressLine2": "addres2",
                "addressLine3": "addres3",
                "countyName": "Central Bohemia",
            },
            "contactInformation": {
                "email": "that@before.de",
                "phone": "+1123456789",
                "mobilePhone": "+60112345678",
                "companyName": "Company Name",
                "fullName": "John Brew",
            },
        },
        "receiverDetails": {
            "postalAddress": {
                "postalCode": "14800",
                "cityName": "Prague",
                "countryCode": "CZ",
                "provinceCode": "CZ",
                "addressLine1": "V Parku 2308/10",
                "addressLine2": "addres2",
                "addressLine3": "addres3",
                "countyName": "Central Bohemia",
            },
            "contactInformation": {
                "email": "that@before.de",
                "phone": "+1123456789",
                "mobilePhone": "+60112345678",
                "companyName": "Company Name",
                "fullName": "John Brew",
            },
        },
        "bookingRequestorDetails": {
            "postalAddress": {
                "postalCode": "14800",
                "cityName": "Prague",
                "countryCode": "CZ",
                "provinceCode": "CZ",
                "addressLine1": "V Parku 2308/10",
                "addressLine2": "addres2",
                "addressLine3": "addres3",
                "countyName": "Central Bohemia",
            },
            "contactInformation": {
                "email": "that@before.de",
                "phone": "+1123456789",
                "mobilePhone": "+60112345678",
                "companyName": "Company Name",
                "fullName": "John Brew",
            },
        },
        "pickupDetails": {
            "postalAddress": {
                "postalCode": "14800",
                "cityName": "Prague",
                "countryCode": "CZ",
                "provinceCode": "CZ",
                "addressLine1": "V Parku 2308/10",
                "addressLine2": "addres2",
                "addressLine3": "addres3",
                "countyName": "Central Bohemia",
            },
            "contactInformation": {
                "email": "that@before.de",
                "phone": "+1123456789",
                "mobilePhone": "+60112345678",
                "companyName": "Company Name",
                "fullName": "John Brew",
            },
        },
    },
    "shipmentDetails": [
        {
            "productCode": "D",
            "localProductCode": "D",
            "accounts": [{"typeCode": "shipper", "number": "123456789"}],
            "valueAddedServices": [
                {
                    "serviceCode": "II",
                    "localServiceCode": "II",
                    "value": 100,
                    "currency": "GBP",
                    "method": "cash",
                }
            ],
            "isCustomsDeclarable": True,
            "declaredValue": 150,
            "declaredValueCurrency": "CZK",
            "unitOfMeasurement": "metric",
            "shipmentTrackingNumber": "123456790",
            "packages": [
                {
                    "typeCode": "3BX",
                    "weight": 10.5,
                    "dimensions": {"length": 25, "width": 35, "height": 15},
                }
            ],
        }
    ],
}

PickupCancelRequest = {"requestorName": "John Doe", "confirmationNumber": "reason"}


PickupResponse = """{
  "dispatchConfirmationNumbers": ["PRG221222000062"]
}
"""

PickupUpdateResponse = """{
  "dispatchConfirmationNumber": "PRG201220123456",
  "readyByTime": "10:00",
  "nextPickupDate": "2020-06-01",
  "warnings": ["Pickup has been updated but something went wrong"]
}
"""

PickupCancelResponse = """
"""
