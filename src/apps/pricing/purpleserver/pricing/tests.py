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
        "postalCode": "V6M2V9",
        "city": "Vancouver",
        "countryCode": "CA",
        "stateCode": "BC",
        "residential": True,
        "addressLine1": "5840 Oak St"
    },
    "recipient": {
        "postalCode": "E1C4Z8",
        "city": "Moncton",
        "countryCode": "CA",
        "stateCode": "NB",
        "residential": False,
        "addressLine1": "125 Church St"
    },
    "parcels": [{
        "weight": 1,
        "packagePreset": "canadapost_corrugated_small_box"
    }],
    "services": [],
    "carrierIds": ["canadapost"]
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
  "rates": [
    {
      "baseCharge": 29.64,
      "carrierId": "canadapost",
      "carrierName": "canadapost",
      "carrierRef": ANY,
      "currency": "CAD",
      "discount": -0.95,
      "dutiesAndTaxes": 4.3,
      "extraCharges": [
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
      "service": "canadapost_expedited_parcel",
      "totalCharge": 32.99,
      "transitDays": 7,
      "testMode": True
    },
    {
      "baseCharge": 75.82,
      "carrierId": "canadapost",
      "carrierName": "canadapost",
      "carrierRef": ANY,
      "currency": "CAD",
      "discount": -1.34,
      "dutiesAndTaxes": 11.17,
      "extraCharges": [
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
      "service": "canadapost_xpresspost",
      "totalCharge": 85.65,
      "transitDays": 2,
      "testMode": True
    },
    {
      "baseCharge": 101.83,
      "carrierId": "canadapost",
      "carrierName": "canadapost",
      "carrierRef": ANY,
      "currency": "CAD",
      "discount": -2.76,
      "dutiesAndTaxes": 14.86,
      "extraCharges": [
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
      "service": "canadapost_priority",
      "totalCharge": 114.93,
      "transitDays": 2,
      "testMode": True
    }
  ]
}
