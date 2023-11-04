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

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(f"{url}", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
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
            total_charge=106.71,
            extra_charges=[
                ChargeDetails(amount=101.83, currency="CAD", name="Base charge"),
                ChargeDetails(amount=2.7, currency="CAD", name="Fuel surcharge"),
                ChargeDetails(amount=-11.74, currency="CAD", name="SMB Savings"),
                ChargeDetails(amount=-9.04, currency="CAD", name="Discount"),
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
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_priority",
            "total_charge": 106.71,
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base charge", "amount": 101.83, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 2.7, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -11.74, "currency": "CAD"},
                {"name": "Discount", "amount": -9.04, "currency": "CAD"},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
                "carrier_connection_id": ANY,
            },
            "test_mode": True,
        }
    ],
}
