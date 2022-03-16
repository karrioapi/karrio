import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import RateDetails, ChargeDetails
from karrio.server.core.tests import APITestCase


class TestRating(APITestCase):
    def test_fetch_shipment_rates(self):
        url = reverse("karrio.server.proxy:shipment-rates")
        data = RATING_DATA

        with patch("karrio.server.core.gateway.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(f"{url}?test", data)
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
        "address_line1": "5840 Oak St",
    },
    "recipient": {
        "postal_code": "E1C4Z8",
        "city": "Moncton",
        "country_code": "CA",
        "state_code": "NB",
        "residential": False,
        "address_line1": "125 Church St",
    },
    "parcels": [
        {
            "weight": 1,
            "weight_unit": "KG",
            "package_preset": "canadapost_corrugated_small_box",
        }
    ],
    "services": ["canadapost_priority"],
    "carrier_ids": ["canadapost"],
}

RETURNED_VALUE = (
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
                ChargeDetails(amount=2.7, currency="CAD", name="Fuel surcharge"),
                ChargeDetails(amount=-11.74, currency="CAD", name="SMB Savings"),
            ],
        )
    ],
    [],
)

RATING_RESPONSE = {
    "messages": [],
    "rates": [
        {
            "id": ANY,
            "object_type": "rate",
            "meta": None,
            "base_charge": 101.83,
            "carrier_id": "canadapost",
            "carrier_name": "canadapost",
            "currency": "CAD",
            "discount": -9.04,
            "duties_and_taxes": 13.92,
            "extra_charges": [
                {"amount": 2.7, "currency": "CAD", "name": "Fuel surcharge"},
                {"amount": -11.74, "currency": "CAD", "name": "SMB Savings"},
            ],
            "test_mode": True,
            "service": "canadapost_priority",
            "total_charge": 106.71,
            "transit_days": 2,
            "meta": {
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
                        "carrier_connection_id": ANY,
            },
        }
    ],
}
