"""Tests for rate sheet bulk operation optimizations.

Verifies that zone, surcharge, and service mutations use batched writes
instead of per-item saves.
"""

import karrio.server.providers.models as providers
from django.contrib.auth import get_user_model
from django.test import TestCase
from karrio.server.graph.serializers import _RateSheetSerializerMixin


class MockRateSheetSerializer(_RateSheetSerializerMixin):
    """Minimal mock to test the mixin methods in isolation."""

    def __init__(self, instance, context=None):
        self.instance = instance
        self.context = context or {}


class TestProcessZonesBulk(TestCase):
    """Test that process_zones batches all mutations into a single save."""

    def setUp(self):
        self.user = get_user_model().objects.create_superuser("testadmin@test.com", "testpassword")
        self.rate_sheet = providers.RateSheet.objects.create(
            name="Test Sheet",
            carrier_name="ups",
            slug="test_sheet",
            zones=[
                {"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]},
                {"id": "zone_2", "label": "Zone 2", "country_codes": ["CA"]},
            ],
            created_by=self.user,
        )
        self.serializer = MockRateSheetSerializer(self.rate_sheet)

    def test_update_multiple_zones_single_save(self):
        """Updating 5 zones should result in 1 UPDATE, not 5."""
        zones_data = [
            {"id": "zone_1", "label": "Updated Zone 1", "country_codes": ["US", "MX"]},
            {"id": "zone_2", "label": "Updated Zone 2", "country_codes": ["CA"]},
            {"id": None, "label": "Zone 3", "country_codes": ["GB"]},
            {"id": None, "label": "Zone 4", "country_codes": ["FR"]},
            {"id": None, "label": "Zone 5", "country_codes": ["DE"]},
        ]

        # Count queries: should be exactly 1 UPDATE
        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        with CaptureQueriesContext(connection) as ctx:
            self.serializer.process_zones(zones_data)

        # Should be 1 UPDATE query (not 5 separate saves)
        update_queries = [q for q in ctx.captured_queries if "UPDATE" in q["sql"]]
        self.assertEqual(len(update_queries), 1)

        # Verify all zones are saved
        self.rate_sheet.refresh_from_db()
        self.assertEqual(len(self.rate_sheet.zones), 5)
        self.assertEqual(self.rate_sheet.zones[0]["label"], "Updated Zone 1")

    def test_remove_missing_zones(self):
        """With remove_missing=True, only incoming zones should remain."""
        zones_data = [
            {"id": "zone_1", "label": "Keep This", "country_codes": ["US"]},
        ]

        self.serializer.process_zones(zones_data, remove_missing=True)

        self.rate_sheet.refresh_from_db()
        self.assertEqual(len(self.rate_sheet.zones), 1)
        self.assertEqual(self.rate_sheet.zones[0]["id"], "zone_1")

    def test_empty_zones_list(self):
        """Empty list should save empty zones."""
        self.serializer.process_zones([], remove_missing=True)

        self.rate_sheet.refresh_from_db()
        self.assertEqual(len(self.rate_sheet.zones), 0)


class TestProcessSurchargesBulk(TestCase):
    """Test that process_surcharges batches all mutations into a single save."""

    def setUp(self):
        self.user = get_user_model().objects.create_superuser("testadmin2@test.com", "testpassword")
        self.rate_sheet = providers.RateSheet.objects.create(
            name="Test Sheet 2",
            carrier_name="ups",
            slug="test_sheet_2",
            surcharges=[
                {"id": "surch_1", "name": "Fuel", "amount": 8.5, "surcharge_type": "percentage", "active": True},
            ],
            created_by=self.user,
        )
        self.serializer = MockRateSheetSerializer(self.rate_sheet)

    def test_update_multiple_surcharges_single_save(self):
        """Updating 3 surcharges should result in 1 UPDATE, not 3."""
        surcharges_data = [
            {"id": "surch_1", "name": "Updated Fuel", "amount": 10.0, "surcharge_type": "percentage"},
            {"id": None, "name": "Handling", "amount": 5.0},
            {"id": None, "name": "Peak Season", "amount": 15.0},
        ]

        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        with CaptureQueriesContext(connection) as ctx:
            self.serializer.process_surcharges(surcharges_data)

        update_queries = [q for q in ctx.captured_queries if "UPDATE" in q["sql"]]
        self.assertEqual(len(update_queries), 1)

        self.rate_sheet.refresh_from_db()
        self.assertEqual(len(self.rate_sheet.surcharges), 3)
        self.assertEqual(self.rate_sheet.surcharges[0]["name"], "Updated Fuel")


class TestUpdateServicesBulk(TestCase):
    """Test that update_services uses bulk operations."""

    def setUp(self):
        self.user = get_user_model().objects.create_superuser("testadmin3@test.com", "testpassword")
        self.rate_sheet = providers.RateSheet.objects.create(
            name="Test Sheet 3",
            carrier_name="ups",
            slug="test_sheet_3",
            created_by=self.user,
        )
        # Create existing services
        self.service1 = providers.ServiceLevel.objects.create(
            service_name="Standard",
            service_code="standard",
            currency="USD",
            active=True,
            created_by=self.user,
        )
        self.service2 = providers.ServiceLevel.objects.create(
            service_name="Express",
            service_code="express",
            currency="USD",
            active=True,
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service1, self.service2)
        self.serializer = MockRateSheetSerializer(self.rate_sheet, context={"user": self.user})

    def test_bulk_update_existing_services(self):
        """Updating multiple existing services should use bulk_update."""
        services_data = [
            {"id": self.service1.id, "service_name": "Updated Standard"},
            {"id": self.service2.id, "service_name": "Updated Express"},
        ]

        self.serializer.update_services(services_data)

        self.service1.refresh_from_db()
        self.service2.refresh_from_db()
        self.assertEqual(self.service1.service_name, "Updated Standard")
        self.assertEqual(self.service2.service_name, "Updated Express")

    def test_bulk_create_new_services(self):
        """Creating multiple new services should use bulk_create + single M2M add."""
        services_data = [
            {"service_name": "Economy", "service_code": "economy", "currency": "USD"},
            {"service_name": "Priority", "service_code": "priority", "currency": "USD"},
        ]

        self.serializer.update_services(services_data)

        self.assertEqual(self.rate_sheet.services.count(), 4)  # 2 existing + 2 new

    def test_remove_missing_services(self):
        """With remove_missing=True, unlisted services should be deleted."""
        services_data = [
            {"id": self.service1.id, "service_name": "Keep This"},
        ]

        self.serializer.update_services(services_data, remove_missing=True)

        self.assertEqual(self.rate_sheet.services.count(), 1)
        self.assertFalse(providers.ServiceLevel.objects.filter(id=self.service2.id).exists())

    def test_mixed_create_and_update(self):
        """Mix of new and existing services should work correctly."""
        services_data = [
            {"id": self.service1.id, "service_name": "Updated Standard"},
            {"service_name": "New Service", "service_code": "new_svc", "currency": "USD"},
        ]

        self.serializer.update_services(services_data)

        self.service1.refresh_from_db()
        self.assertEqual(self.service1.service_name, "Updated Standard")
        self.assertEqual(self.rate_sheet.services.count(), 3)


if __name__ == "__main__":
    import unittest

    unittest.main()
