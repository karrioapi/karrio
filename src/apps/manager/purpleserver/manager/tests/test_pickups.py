import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from purplship.core.models import PickupDetails, ConfirmationDetails, ChargeDetails
from purpleserver.manager.tests.test_shipments import TestShipmentFixture
import purpleserver.manager.models as models


class TestFixture(TestShipmentFixture):
    def setUp(self) -> None:
        super().setUp()

        self.address: models.Address = models.Address.objects.create(**{
            "postal_code": "E1C4Z8",
            "city": "Moncton",
            "federal_tax_id": None,
            "state_tax_id": None,
            "person_name": "John Poop",
            "company_name": "A corp.",
            "country_code": "CA",
            "email": "john@a.com",
            "phone_number": "514 000 0000",
            "state_code": "NB",
            "suburb": None,
            "residential": False,
            "address_line1": "125 Church St",
            "address_line2": None,
            "user": self.user
        })
        self.shipment.tracking_number = "123456789012"
        self.shipment.selected_rate_carrier = self.carrier
        self.shipment.save()


class TestPickupSchedule(TestFixture):

    def test_schedule_pickup(self):
        url = reverse(
            'purpleserver.manager:shipment-pickup-request',
            kwargs=dict(carrier_name="canadapost")
        )

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = SCHEDULE_RETURNED_VALUE
            response = self.client.post(f"{url}?test", PICKUP_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertDictEqual(response_data, PICKUP_RESPONSE)


class TestPickupDetails(TestFixture):
    def setUp(self) -> None:
        super().setUp()
        self.pickup: models.Pickup = models.Pickup.objects.create(
            address=self.address,
            pickup_carrier=self.carrier,
            user=self.user,
            test_mode=True,
            pickup_date="2020-10-25",
            ready_time="13:00",
            closing_time="17:00",
            instruction="Should not be folded",
            package_location="At the main entrance hall",
            confirmation_number="00110215",
            pickup_charge={
                "name": "Pickup fees",
                "amount": 0.0,
                "currency": "CAD"
            },
        )
        self.pickup.shipments.set([self.shipment])

    def test_udpate_pickup(self):
        url = reverse(
            'purpleserver.manager:shipment-pickup-details',
            kwargs=dict(pk=self.pickup.pk)
        )

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = UPDATE_RETURNED_VALUE
            response = self.client.patch(url, PICKUP_UPDATE_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, PICKUP_UPDATE_RESPONSE)

    def test_cancel_pickup(self):
        url = reverse(
            'purpleserver.manager:shipment-pickup-cancel',
            kwargs=dict(pk=self.pickup.pk)
        )

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = CANCEL_RETURNED_VALUE
            response = self.client.post(url, PICKUP_CANCEL_DATA)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, PICKUP_CANCEL_RESPONSE)


PICKUP_DATA = {
    "pickupDate": "2020-10-25",
    "readyTime": "13:00",
    "closingTime": "17:00",
    "instruction": "Should not be folded",
    "packageLocation": "At the main entrance hall",
    "address": {
        "addressLine1": "125 Church St",
        "personName": "John Doe",
        "companyName": "A corp.",
        "phoneNumber": "514 000 0000",
        "city": "Moncton",
        "countryCode": "CA",
        "postalCode": "E1C4Z8",
        "residential": False,
        "stateCode": "NB",
        "email": "john@a.com"
    },
    "tracking_numbers": [
        "123456789012"
    ]
}

PICKUP_UPDATE_DATA = {
    "readyTime": "14:00",
    "packageLocation": "At the main entrance hall next to the distributor",
    "address": {
        "personName": "Janet Jackson"
    }
}

PICKUP_CANCEL_DATA = {}


SCHEDULE_RETURNED_VALUE = (
    PickupDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        confirmation_number="27241",
        pickup_date="2020-10-25",
        pickup_charge=ChargeDetails(
            name="Pickup fees",
            amount=0.0,
            currency="CAD"
        ),
        ready_time="13:00",
        closing_time="17:00"
    ),
    [],
)

UPDATE_RETURNED_VALUE = (
    PickupDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        confirmation_number="27241",
        pickup_date="2020-10-23",
        ready_time="14:00",
        closing_time="17:00"
    ),
    [],
)

CANCEL_RETURNED_VALUE = (
    ConfirmationDetails(
        carrier_id="canadapost",
        carrier_name="canadapost",
        operation="Cancel Pickup",
        success=True
    ),
    []
)


PICKUP_RESPONSE = {
  "id": ANY,
  "carrierName": "canadapost",
  "carrierId": "canadapost",
  "confirmationNumber": "27241",
  "pickupDate": "2020-10-25",
  "pickupCharge": {
    "name": "Pickup fees",
    "amount": 0.0,
    "currency": "CAD"
  },
  "readyTime": "13:00",
  "closingTime": "17:00",
  "testMode": True,
  "address": {
    "id": ANY,
    "postalCode": "E1C4Z8",
    "city": "Moncton",
    "federalTaxId": None,
    "stateTaxId": None,
    "personName": "John Doe",
    "companyName": "A corp.",
    "countryCode": "CA",
    "email": "john@a.com",
    "phoneNumber": "514 000 0000",
    "stateCode": "NB",
    "suburb": None,
    "residential": False,
    "addressLine1": "125 Church St",
    "addressLine2": None
  },
  "parcels": [
    {
      "id": ANY,
      "weight": 1.0,
      "width": None,
      "height": None,
      "length": None,
      "packagingType": None,
      "packagePreset": "canadapost_corrugated_small_box",
      "description": None,
      "content": None,
      "isDocument": False,
      "weightUnit": None,
      "dimensionUnit": None
    }
  ],
  "instruction": "Should not be folded",
  "packageLocation": "At the main entrance hall",
  "options": {}
}

PICKUP_UPDATE_RESPONSE = {
  "id": ANY,
  "carrierName": "canadapost",
  "carrierId": "canadapost",
  "confirmationNumber": "00110215",
  "pickupDate": "2020-10-25",
  "pickupCharge": {
    "name": "Pickup fees",
    "amount": 0.0,
    "currency": "CAD"
  },
  "readyTime": "14:00",
  "closingTime": "17:00",
  "testMode": True,
  "address": {
    "id": ANY,
    "postalCode": "E1C4Z8",
    "city": "Moncton",
    "federalTaxId": None,
    "stateTaxId": None,
    "personName": "Janet Jackson",
    "companyName": "A corp.",
    "countryCode": "CA",
    "email": "john@a.com",
    "phoneNumber": "514 000 0000",
    "stateCode": "NB",
    "suburb": None,
    "residential": False,
    "addressLine1": "125 Church St",
    "addressLine2": None
  },
  "parcels": [
    {
      "id": ANY,
      "weight": 1.0,
      "width": None,
      "height": None,
      "length": None,
      "packagingType": None,
      "packagePreset": "canadapost_corrugated_small_box",
      "description": None,
      "content": None,
      "isDocument": False,
      "weightUnit": None,
      "dimensionUnit": None
    }
  ],
  "instruction": "Should not be folded",
  "packageLocation": "At the main entrance hall next to the distributor",
  "options": {}
}

PICKUP_CANCEL_RESPONSE = {
  "carrierName": "canadapost",
  "carrierId": "canadapost",
  "operation": "Cancel Pickup",
  "success": True
}
