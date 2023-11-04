import json
import logging
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import RateDetails, ChargeDetails
from karrio.server.core.tests import APITestCase
import karrio.server.pricing.models as models

logging.disable(logging.CRITICAL)


class TestPricing(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.charge: models.Surcharge = models.Surcharge.objects.create(
            **{
                "amount": 1.0,
                "name": "brokerage",
                "carriers": ["canadapost"],
                "services": ["canadapost_priority", "canadapost_regular_parcel"],
            }
        )

    def test_apply_surcharge_amount_to_shipment_rates(self):
        url = reverse("karrio.server.proxy:shipment-rates")
        data = RATING_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(f"{url}", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, RATING_RESPONSE)

    def test_apply_surcharge_percentage_to_shipment_rates(self):
        self.charge.amount = 2.0
        self.charge.surcharge_type = "PERCENTAGE"
        self.charge.save()
        url = reverse("karrio.server.proxy:shipment-rates")
        data = RATING_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(f"{url}", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, RATING_WITH_PERCENTAGE_RESPONSE)


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
            "packagePreset": "canadapost_corrugated_small_box",
        }
    ],
    "services": [],
    "carrier_ids": ["canadapost"],
}

RETURNED_VALUE = (
    [
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=7,
            service="canadapost_expedited_parcel",
            total_charge=32.99,
            extra_charges=[
                ChargeDetails(amount=29.64, currency="CAD", name="Base charge"),
                ChargeDetails(amount=1.24, currency="CAD", name="Fuel surcharge"),
                ChargeDetails(amount=-2.19, currency="CAD", name="SMB Savings"),
                ChargeDetails(amount=4.3, currency="CAD", name="Duty and taxes"),
                ChargeDetails(amount=-0.95, currency="CAD", name="Discount"),
            ],
        ),
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=2,
            service="canadapost_xpresspost",
            total_charge=85.65,
            extra_charges=[
                ChargeDetails(amount=75.82, currency="CAD", name="Base charge"),
                ChargeDetails(amount=3.21, currency="CAD", name="Fuel surcharge"),
                ChargeDetails(amount=-4.55, currency="CAD", name="SMB Savings"),
                ChargeDetails(amount=4.3, currency="CAD", name="Duty and taxes"),
                ChargeDetails(amount=11.17, currency="CAD", name="Discount"),
            ],
        ),
        RateDetails(
            carrier_id="canadapost",
            carrier_name="canadapost",
            currency="CAD",
            transit_days=2,
            service="canadapost_priority",
            total_charge=113.93,
            extra_charges=[
                ChargeDetails(amount=101.83, currency="CAD", name="Base charge"),
                ChargeDetails(amount=4.27, currency="CAD", name="Fuel surcharge"),
                ChargeDetails(amount=-7.03, currency="CAD", name="SMB Savings"),
                ChargeDetails(amount=14.86, currency="CAD", name="Duties and taxes"),
                ChargeDetails(amount=-2.76, currency="CAD", name="Discount"),
            ],
        ),
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
            "service": "canadapost_expedited_parcel",
            "total_charge": 32.99,
            "transit_days": 7,
            "extra_charges": [
                {"name": "Base charge", "amount": 29.64, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 1.24, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -2.19, "currency": "CAD"},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD"},
                {"name": "Discount", "amount": -0.95, "currency": "CAD"},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST EXPEDITED PARCEL",
                "carrier_connection_id": ANY,
            },
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_xpresspost",
            "total_charge": 85.65,
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base charge", "amount": 75.82, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 3.21, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -4.55, "currency": "CAD"},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD"},
                {"name": "Discount", "amount": 11.17, "currency": "CAD"},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST XPRESSPOST",
                "carrier_connection_id": ANY,
            },
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_priority",
            "total_charge": 114.93,
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base charge", "amount": 101.83, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 4.27, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -7.03, "currency": "CAD"},
                {"name": "Duties and taxes", "amount": 14.86, "currency": "CAD"},
                {"name": "Discount", "amount": -2.76, "currency": "CAD"},
                {"name": "brokerage", "amount": 1.0, "currency": "CAD"},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "carrier_connection_id": ANY,
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
            },
            "test_mode": True,
        },
    ],
}

RATING_WITH_PERCENTAGE_RESPONSE = {
    "messages": [],
    "rates": [
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_expedited_parcel",
            "total_charge": 32.99,
            "transit_days": 7,
            "extra_charges": [
                {"name": "Base charge", "amount": 29.64, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 1.24, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -2.19, "currency": "CAD"},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD"},
                {"name": "Discount", "amount": -0.95, "currency": "CAD"},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST EXPEDITED PARCEL",
                "carrier_connection_id": ANY,
            },
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_xpresspost",
            "total_charge": 85.65,
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base charge", "amount": 75.82, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 3.21, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -4.55, "currency": "CAD"},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD"},
                {"name": "Discount", "amount": 11.17, "currency": "CAD"},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST XPRESSPOST",
                "carrier_connection_id": ANY,
            },
            "test_mode": True,
        },
        {
            "id": ANY,
            "object_type": "rate",
            "carrier_name": "canadapost",
            "carrier_id": "canadapost",
            "currency": "CAD",
            "estimated_delivery": ANY,
            "service": "canadapost_priority",
            "total_charge": 116.21,
            "transit_days": 2,
            "extra_charges": [
                {"name": "Base charge", "amount": 101.83, "currency": "CAD"},
                {"name": "Fuel surcharge", "amount": 4.27, "currency": "CAD"},
                {"name": "SMB Savings", "amount": -7.03, "currency": "CAD"},
                {"name": "Duties and taxes", "amount": 14.86, "currency": "CAD"},
                {"name": "Discount", "amount": -2.76, "currency": "CAD"},
                {"name": "brokerage", "amount": 2.28, "currency": "CAD"},
            ],
            "meta": {
                "ext": "canadapost",
                "carrier": "canadapost",
                "carrier_connection_id": ANY,
                "rate_provider": "canadapost",
                "service_name": "CANADAPOST PRIORITY",
            },
            "test_mode": True,
        },
    ],
}
