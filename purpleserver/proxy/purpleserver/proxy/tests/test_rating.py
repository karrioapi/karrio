import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from purplship.core.models import RateDetails, ChargeDetails
from purpleserver.core.tests import APITestCase


class TestRating(APITestCase):

    def test_fetch_shipment_rates(self):
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
    "parcel": {
        "weight": 1,
        "packagePreset": "canadapost_corrugated_small_box"
    },
    "services": ["canadapost_priority"],
    "carrierIds": ["canadapost"]
}

RETURNED_VALUE = [[
    [
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=2,
            service="canadapost_priority",
            discount=-9.04,
            base_charge=101.83,
            total_charge=106.71,
            duties_and_taxes=13.92,
            extra_charges=[
                ChargeDetails(
                    amount=2.7,
                    currency="CAD",
                    name="Fuel surcharge"
                ),
                ChargeDetails(
                    amount=-11.74,
                    currency="CAD",
                    name="SMB Savings"
                )
            ]
        )
    ],
    [],
]]

RATING_RESPONSE = {
    "rates": [
        {
            "id": ANY,
            "carrierRef": ANY,
            "baseCharge": 101.83,
            "carrierId": "canadapost",
            "carrierName": "canadapost",
            "currency": "CAD",
            "discount": -9.04,
            "dutiesAndTaxes": 13.92,
            "extraCharges": [
                {
                    "amount": 2.7,
                    "currency": "CAD",
                    "name": "Fuel surcharge"
                },
                {
                    "amount": -11.74,
                    "currency": "CAD",
                    "name": "SMB Savings"
                }
            ],
            "service": "canadapost_priority",
            "totalCharge": 106.71,
            "transitDays": 2
        }
    ]
}
