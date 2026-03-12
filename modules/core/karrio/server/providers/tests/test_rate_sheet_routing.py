from django.test import TestCase
from django.contrib.auth import get_user_model

import karrio.server.providers.models as providers


class TestRateSheetRouting(TestCase):
    """Coverage for ServiceLevel.rate_sheet routing behavior."""

    def setUp(self):
        self.user = get_user_model().objects.create_superuser("routes@example.com", "test")

        self.service = providers.ServiceLevel.objects.create(
            service_name="UPS Standard",
            service_code="ups_standard",
            carrier_service_code="11",
            currency="USD",
            active=True,
            zone_ids=["zone_1"],
            created_by=self.user,
        )

        self.account_rate_sheet = providers.RateSheet.objects.create(
            name="Account Rate Sheet",
            carrier_name="ups",
            slug="account-rate-sheet",
            zones=[{"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]}],
            surcharges=[],
            service_rates=[
                {
                    "service_id": self.service.id,
                    "zone_id": "zone_1",
                    "rate": 10.0,
                    "cost": 8.0,
                }
            ],
            created_by=self.user,
        )
        self.account_rate_sheet.services.add(self.service)

        self.system_rate_sheet = providers.SystemRateSheet.objects.create(
            id="rsys_test_001",
            name="System Rate Sheet",
            carrier_name="ups",
            slug="system-rate-sheet",
            zones=[{"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]}],
            surcharges=[],
            service_rates=[
                {
                    "service_id": self.service.id,
                    "zone_id": "zone_1",
                    "rate": 12.0,
                    "cost": 9.0,
                }
            ],
        )

    def test_service_prefers_account_rate_sheet_when_both_exist(self):
        """ServiceLevel.rate_sheet should prefer account sheet over system sheet."""
        self.system_rate_sheet.services.add(self.service)

        resolved = self.service.rate_sheet
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.id, self.account_rate_sheet.id)

    def test_service_uses_system_rate_sheet_when_no_account_sheet(self):
        """Fallback to system sheet when account sheet relation is absent."""
        # remove account relation
        self.account_rate_sheet.services.remove(self.service)
        self.system_rate_sheet.services.add(self.service)

        resolved = self.service.rate_sheet
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.id, self.system_rate_sheet.id)

    def test_service_has_no_rate_sheet_when_unlinked(self):
        """No relations should return None without crashing."""
        self.account_rate_sheet.services.remove(self.service)

        resolved = self.service.rate_sheet
        self.assertIsNone(resolved)
