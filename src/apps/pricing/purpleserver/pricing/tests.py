import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from purplship.core.models import RateDetails, ChargeDetails
from purpleserver.core.tests import APITestCase
import purpleserver.pricing.models as models


class TestPricing(APITestCase):

    def setUp(self) -> None:
        super().setUp()

        self.charge: models.PricingCharge = models.PricingCharge.objects.create(**{
            "amount": 1.0,
            "carriers": ["canadapost"],
            "services": ["canadapost_priority", "canadapost_regular_parcel"],
            "freight_range": (None, 130.0),
            "user": self.user
        })

    def test_apply_charge_to_shipment_rates(self):
        url = reverse('purpleserver.proxy:shipment-rates')
        data = RATING_DATA

        with patch("purpleserver.core.gateway.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertDictEqual(response_data, RATING_RESPONSE)


RATING_DATA = {
    "shipper": {
        "postal_code": "V6M2V9",
        "city": "Vancouver",
        "country_code": "CA",
        "state_code": "BC",
        "residential": True,
        "address_line1": "5840 Oak St"
    },
    "recipient": {
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "country_code": "CA",
        "state_code": "NB",
        "residential": False,
        "address_line1": "125 Church St"
    },
    "parcels": [{
        "weight": 1,
        "packagePreset": "canadapost_corrugated_small_box"
    }],
    "services": [],
    "carrier_ids": ["canadapost"]
}

RETURNED_VALUE = [(
    [
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=7,
            service="canadapost_expedited_parcel",
            discount=-0.95,
            base_charge=29.64,
            total_charge=32.99,
            duties_and_taxes=4.3,
            extra_charges=[
                ChargeDetails(
                    amount=1.24,
                    currency="CAD",
                    name="Fuel surcharge"
                ),
                ChargeDetails(
                    amount=-2.19,
                    currency="CAD",
                    name="SMB Savings"
                )
            ]
        ),
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=2,
            service="canadapost_xpresspost",
            discount=-1.34,
            base_charge=75.82,
            total_charge=85.65,
            duties_and_taxes=11.17,
            extra_charges=[
                ChargeDetails(
                    amount=3.21,
                    currency="CAD",
                    name="Fuel surcharge"
                ),
                ChargeDetails(
                    amount=-4.55,
                    currency="CAD",
                    name="SMB Savings"
                )
            ]
        ),
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=2,
            service="canadapost_priority",
            discount=-2.76,
            base_charge=101.83,
            total_charge=113.93,
            duties_and_taxes=14.86,
            extra_charges=[
                ChargeDetails(
                    amount=4.27,
                    currency="CAD",
                    name="Fuel surcharge"
                ),
                ChargeDetails(
                    amount=-7.03,
                    currency="CAD",
                    name="SMB Savings"
                )
            ]
        )
    ],
    [],
)]

RATING_RESPONSE = {
  "messages": [],
  "rates": [
    {
      "base_charge": 29.64,
      "carrier_id": "canadapost",
      "carrier_name": "canadapost",
      "carrier_ref": ANY,
      "currency": "CAD",
      "discount": -0.95,
      "duties_and_taxes": 4.3,
      "extra_charges": [
        {
          "amount": 1.24,
          "currency": "CAD",
          "name": "Fuel surcharge"
        },
        {
          "amount": -2.19,
          "currency": "CAD",
          "name": "SMB Savings"
        }
      ],
      "id": ANY,
      "meta": None,
      "service": "canadapost_expedited_parcel",
      "total_charge": 32.99,
      "transit_days": 7,
      "test_mode": True
    },
    {
      "base_charge": 75.82,
      "carrier_id": "canadapost",
      "carrier_name": "canadapost",
      "carrier_ref": ANY,
      "currency": "CAD",
      "discount": -1.34,
      "duties_and_taxes": 11.17,
      "extra_charges": [
        {
          "amount": 3.21,
          "currency": "CAD",
          "name": "Fuel surcharge"
        },
        {
          "amount": -4.55,
          "currency": "CAD",
          "name": "SMB Savings"
        }
      ],
      "id": ANY,
      "meta": None,
      "service": "canadapost_xpresspost",
      "total_charge": 85.65,
      "transit_days": 2,
      "test_mode": True
    },
    {
      "base_charge": 101.83,
      "carrier_id": "canadapost",
      "carrier_name": "canadapost",
      "carrier_ref": ANY,
      "currency": "CAD",
      "discount": -2.76,
      "duties_and_taxes": 14.86,
      "extra_charges": [
        {
          "amount": 4.27,
          "currency": "CAD",
          "name": "Fuel surcharge"
        },
        {
          "amount": -7.03,
          "currency": "CAD",
          "name": "SMB Savings"
        },
        {
          "amount": 1.0,
          "currency": "CAD",
          "name": "Service charge"
        }
      ],
      "id": ANY,
      "meta": None,
      "service": "canadapost_priority",
      "total_charge": 114.93,
      "transit_days": 2,
      "test_mode": True
    }
  ]
}
