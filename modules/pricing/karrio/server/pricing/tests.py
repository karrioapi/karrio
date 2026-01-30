"""
Tests for the Pricing module (Markup and Fee models).

These tests cover:
1. Markup application to shipping rates (amount and percentage types)
2. Fee capture after shipment label creation
3. Various filter combinations (carrier_codes, service_codes, connection_ids)
"""

import json
import logging
from unittest.mock import patch, ANY
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from karrio.core.models import RateDetails, ChargeDetails
from karrio.server.core.tests import APITestCase
import karrio.server.pricing.models as models
import karrio.server.pricing.signals as signals

logging.disable(logging.CRITICAL)


class TestMarkupApplication(APITestCase):
    """Test markup application to shipping rates."""

    def setUp(self) -> None:
        super().setUp()

        # Create a markup targeting specific carriers and services
        self.markup: models.Markup = models.Markup.objects.create(
            **{
                "amount": 1.0,
                "name": "brokerage",
                "carrier_codes": ["canadapost"],
                "service_codes": ["canadapost_priority", "canadapost_regular_parcel"],
            }
        )

    def test_apply_markup_amount_to_shipment_rates(self):
        """Test applying fixed amount markup to rates."""
        url = reverse("karrio.server.proxy:shipment-rates")
        data = RATING_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(f"{url}", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, RATING_RESPONSE)

    def test_apply_markup_percentage_to_shipment_rates(self):
        """Test applying percentage markup to rates."""
        self.markup.amount = 2.0
        self.markup.markup_type = "PERCENTAGE"
        self.markup.save()
        url = reverse("karrio.server.proxy:shipment-rates")
        data = RATING_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = RETURNED_VALUE
            response = self.client.post(f"{url}", data)
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertDictEqual(response_data, RATING_WITH_PERCENTAGE_RESPONSE)


class TestMarkupFilters(TestCase):
    """Test markup filter logic."""

    def test_carrier_codes_filter(self):
        """Test that markup only applies to specified carrier codes."""
        markup = models.Markup.objects.create(
            name="fedex_markup",
            amount=5.0,
            markup_type="AMOUNT",
            carrier_codes=["fedex"],
        )

        # Create mock rate for FedEx
        from karrio.server.core.datatypes import Rate, RateResponse

        fedex_rate = Rate(
            id="rate_1",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_ground",
            total_charge=10.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_123"},
        )

        ups_rate = Rate(
            id="rate_2",
            carrier_id="ups",
            carrier_name="ups",
            service="ups_ground",
            total_charge=12.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_456"},
        )

        response = RateResponse(
            rates=[fedex_rate, ups_rate],
            messages=[],
        )

        result = markup.apply_charge(response)

        # FedEx rate should have markup applied
        fedex_result = next(r for r in result.rates if r.carrier_name == "fedex")
        self.assertEqual(fedex_result.total_charge, 15.0)  # 10 + 5

        # UPS rate should NOT have markup applied
        ups_result = next(r for r in result.rates if r.carrier_name == "ups")
        self.assertEqual(ups_result.total_charge, 12.0)  # unchanged

    def test_service_codes_filter(self):
        """Test that markup only applies to specified service codes."""
        markup = models.Markup.objects.create(
            name="express_markup",
            amount=10.0,
            markup_type="PERCENTAGE",
            service_codes=["fedex_overnight"],
        )

        from karrio.server.core.datatypes import Rate, RateResponse

        overnight_rate = Rate(
            id="rate_1",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_overnight",
            total_charge=100.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_123"},
        )

        ground_rate = Rate(
            id="rate_2",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_ground",
            total_charge=50.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_123"},
        )

        response = RateResponse(
            rates=[overnight_rate, ground_rate],
            messages=[],
        )

        result = markup.apply_charge(response)

        # Overnight rate should have 10% markup applied
        overnight_result = next(r for r in result.rates if r.service == "fedex_overnight")
        self.assertEqual(overnight_result.total_charge, 110.0)  # 100 + 10%

        # Ground rate should NOT have markup applied
        ground_result = next(r for r in result.rates if r.service == "fedex_ground")
        self.assertEqual(ground_result.total_charge, 50.0)  # unchanged

    def test_connection_ids_filter(self):
        """Test that markup only applies to specified connection IDs."""
        markup = models.Markup.objects.create(
            name="specific_connection_markup",
            amount=3.0,
            markup_type="AMOUNT",
            connection_ids=["car_special_123"],
        )

        from karrio.server.core.datatypes import Rate, RateResponse

        special_rate = Rate(
            id="rate_1",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_ground",
            total_charge=25.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_special_123"},
        )

        regular_rate = Rate(
            id="rate_2",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_ground",
            total_charge=25.0,
            currency="USD",
            extra_charges=[],
            meta={"carrier_connection_id": "car_regular_456"},
        )

        response = RateResponse(
            rates=[special_rate, regular_rate],
            messages=[],
        )

        result = markup.apply_charge(response)

        # Rate with special connection should have markup
        special_result = next(
            r for r in result.rates
            if r.meta.get("carrier_connection_id") == "car_special_123"
        )
        self.assertEqual(special_result.total_charge, 28.0)  # 25 + 3

        # Rate with regular connection should NOT have markup
        regular_result = next(
            r for r in result.rates
            if r.meta.get("carrier_connection_id") == "car_regular_456"
        )
        self.assertEqual(regular_result.total_charge, 25.0)  # unchanged

    def test_empty_filters_apply_to_all(self):
        """Test that markup with no filters applies to all rates."""
        markup = models.Markup.objects.create(
            name="global_markup",
            amount=1.0,
            markup_type="AMOUNT",
            carrier_codes=[],
            service_codes=[],
            connection_ids=[],
        )

        from karrio.server.core.datatypes import Rate, RateResponse

        rate1 = Rate(
            id="rate_1",
            carrier_id="fedex",
            carrier_name="fedex",
            service="fedex_ground",
            total_charge=10.0,
            currency="USD",
            extra_charges=[],
            meta={},
        )

        rate2 = Rate(
            id="rate_2",
            carrier_id="ups",
            carrier_name="ups",
            service="ups_ground",
            total_charge=12.0,
            currency="USD",
            extra_charges=[],
            meta={},
        )

        response = RateResponse(
            rates=[rate1, rate2],
            messages=[],
        )

        result = markup.apply_charge(response)

        # Both rates should have markup applied
        for rate in result.rates:
            if rate.carrier_name == "fedex":
                self.assertEqual(rate.total_charge, 11.0)  # 10 + 1
            elif rate.carrier_name == "ups":
                self.assertEqual(rate.total_charge, 13.0)  # 12 + 1


class TestFeeCapture(TestCase):
    """Test fee capture after shipment creation."""

    def setUp(self):
        """Set up test data."""
        # Create a markup
        self.markup = models.Markup.objects.create(
            name="test_markup",
            amount=5.0,
            markup_type="AMOUNT",
        )

    def test_capture_fees_from_shipment(self):
        """Test that fees are captured from shipment's selected_rate via signal.

        When a shipment is saved with status='purchased' and a selected_rate,
        the fee capture signal should automatically capture fees.
        """
        from django.contrib.auth import get_user_model
        import karrio.server.manager.models as manager

        User = get_user_model()
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

        # Create a shipment with markup in extra_charges
        # The signal should automatically capture fees on save
        shipment = manager.Shipment.objects.create(
            status="purchased",
            test_mode=True,
            shipper={"city": "Montreal"},
            recipient={"city": "Toronto"},
            parcels=[{"weight": 1}],
            selected_rate={
                "carrier_name": "fedex",
                "carrier_id": "fedex",
                "service": "fedex_ground",
                "total_charge": 15.0,
                "currency": "USD",
                "extra_charges": [
                    {"id": self.markup.id, "name": "test_markup", "amount": 5.0, "currency": "USD"},
                ],
                "meta": {
                    "carrier_code": "fedex",
                    "carrier_connection_id": "car_123",
                },
            },
            created_by=user,
        )

        # Verify fee was captured by the signal (don't call manually)
        fees = models.Fee.objects.filter(shipment_id=shipment.id)
        self.assertEqual(fees.count(), 1)

        fee = fees.first()
        self.assertEqual(fee.markup_id, self.markup.id)
        self.assertEqual(fee.name, "test_markup")
        self.assertEqual(fee.amount, 5.0)
        self.assertEqual(fee.currency, "USD")
        self.assertEqual(fee.carrier_code, "fedex")
        self.assertEqual(fee.service_code, "fedex_ground")
        self.assertEqual(fee.connection_id, "car_123")
        self.assertEqual(fee.test_mode, True)

    def test_capture_fees_function_directly(self):
        """Test the capture_fees_for_shipment function in isolation.

        Create shipment with status='created' (so signal won't fire),
        then manually call capture function.
        """
        from django.contrib.auth import get_user_model
        import karrio.server.manager.models as manager

        User = get_user_model()
        user = User.objects.create_user(
            email="test_direct@example.com",
            password="testpass123",
        )

        # Create shipment with status that won't trigger signal
        shipment = manager.Shipment.objects.create(
            status="created",  # Signal won't fire for this status
            test_mode=True,
            shipper={"city": "Montreal"},
            recipient={"city": "Toronto"},
            parcels=[{"weight": 1}],
            selected_rate={
                "carrier_name": "fedex",
                "carrier_id": "fedex",
                "service": "fedex_ground",
                "total_charge": 15.0,
                "currency": "USD",
                "extra_charges": [
                    {"id": self.markup.id, "name": "test_markup", "amount": 5.0, "currency": "USD"},
                ],
                "meta": {
                    "carrier_code": "fedex",
                    "carrier_connection_id": "car_123",
                },
            },
            created_by=user,
        )

        # No fees should exist yet
        self.assertEqual(models.Fee.objects.filter(shipment_id=shipment.id).count(), 0)

        # Manually capture fees
        signals.capture_fees_for_shipment(shipment)

        # Verify fee was captured
        fees = models.Fee.objects.filter(shipment_id=shipment.id)
        self.assertEqual(fees.count(), 1)

        fee = fees.first()
        self.assertEqual(fee.markup_id, self.markup.id)
        self.assertEqual(fee.amount, 5.0)

    def test_no_duplicate_fee_capture(self):
        """Test that fees are not captured twice for the same shipment.

        Signal should check if fees exist before capturing.
        """
        from django.contrib.auth import get_user_model
        import karrio.server.manager.models as manager

        User = get_user_model()
        user = User.objects.create_user(
            email="test2@example.com",
            password="testpass123",
        )

        # Create shipment - signal will capture fee
        shipment = manager.Shipment.objects.create(
            status="purchased",
            test_mode=True,
            shipper={"city": "Montreal"},
            recipient={"city": "Toronto"},
            parcels=[{"weight": 1}],
            selected_rate={
                "carrier_name": "fedex",
                "carrier_id": "fedex",
                "service": "fedex_ground",
                "total_charge": 15.0,
                "currency": "USD",
                "extra_charges": [
                    {"id": self.markup.id, "name": "test_markup", "amount": 5.0, "currency": "USD"},
                ],
                "meta": {"carrier_connection_id": "car_123"},
            },
            created_by=user,
        )

        # Fee should already exist from signal
        fees = models.Fee.objects.filter(shipment_id=shipment.id)
        self.assertEqual(fees.count(), 1)

        # Save again - signal should not create duplicate
        shipment.save()

        # Still only one fee
        fees = models.Fee.objects.filter(shipment_id=shipment.id)
        self.assertEqual(fees.count(), 1)


# Test data fixtures

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
                {"name": "Base charge", "amount": 29.64, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 1.24, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -2.19, "currency": "CAD", "id": None},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": -0.95, "currency": "CAD", "id": None},
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
                {"name": "Base charge", "amount": 75.82, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 3.21, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -4.55, "currency": "CAD", "id": None},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": 11.17, "currency": "CAD", "id": None},
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
                {"name": "Base charge", "amount": 101.83, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 4.27, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -7.03, "currency": "CAD", "id": None},
                {"name": "Duties and taxes", "amount": 14.86, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": -2.76, "currency": "CAD", "id": None},
                {"name": "brokerage", "amount": 1.0, "currency": "CAD", "id": ANY},
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
                {"name": "Base charge", "amount": 29.64, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 1.24, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -2.19, "currency": "CAD", "id": None},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": -0.95, "currency": "CAD", "id": None},
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
                {"name": "Base charge", "amount": 75.82, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 3.21, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -4.55, "currency": "CAD", "id": None},
                {"name": "Duty and taxes", "amount": 4.3, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": 11.17, "currency": "CAD", "id": None},
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
                {"name": "Base charge", "amount": 101.83, "currency": "CAD", "id": None},
                {"name": "Fuel surcharge", "amount": 4.27, "currency": "CAD", "id": None},
                {"name": "SMB Savings", "amount": -7.03, "currency": "CAD", "id": None},
                {"name": "Duties and taxes", "amount": 14.86, "currency": "CAD", "id": None},
                {"name": "Discount", "amount": -2.76, "currency": "CAD", "id": None},
                {"name": "brokerage", "amount": 2.28, "currency": "CAD", "id": ANY},
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
