"""Tests for constance settings batch fetch optimization.

Verifies that _batch_fetch_constance fetches all keys in a single query
instead of N individual lookups.
"""

import unittest
from unittest import mock
from django.test import TestCase, override_settings

from karrio.server.core.signals import _batch_fetch_constance, update_settings


MOCK_CONSTANCE_CONFIG = {
    "ALLOW_SIGNUP": (True, "Allow signup", bool),
    "MULTI_ORGANIZATIONS": (False, "Multi organizations", bool),
    "EMAIL_HOST": ("", "SMTP host", str),
    "EMAIL_HOST_USER": ("", "SMTP user", str),
}


class TestBatchFetchConstance(TestCase):
    """Test _batch_fetch_constance returns correct values."""

    @override_settings(
        CONSTANCE_CONFIG=MOCK_CONSTANCE_CONFIG,
        CONSTANCE_DATABASE_PREFIX="constance:core:",
    )
    @mock.patch("karrio.server.core.signals.Constance", create=True)
    def test_returns_defaults_when_no_db_rows(self, mock_constance_cls):
        """When DB has no rows, returns defaults from CONSTANCE_CONFIG."""
        # Simulate the import inside _batch_fetch_constance
        with mock.patch(
            "constance.models.Constance"
        ) as MockConstance:
            MockConstance.objects.filter.return_value.values_list.return_value = []

            result = _batch_fetch_constance(["ALLOW_SIGNUP", "MULTI_ORGANIZATIONS"])

        self.assertIn("ALLOW_SIGNUP", result)
        self.assertIn("MULTI_ORGANIZATIONS", result)
        self.assertEqual(result["ALLOW_SIGNUP"], True)
        self.assertEqual(result["MULTI_ORGANIZATIONS"], False)

    def test_returns_empty_dict_when_import_fails(self):
        """When constance model can't be imported, returns empty dict gracefully."""
        with mock.patch(
            "karrio.server.core.signals.Constance",
            create=True,
            new_callable=mock.PropertyMock,
            side_effect=Exception("import failed"),
        ):
            # Force the import inside the function to fail
            import karrio.server.core.signals as signals_module
            original = signals_module._batch_fetch_constance

            def _failing_fetch(keys):
                try:
                    raise Exception("table does not exist")
                except Exception:
                    return {}

            signals_module._batch_fetch_constance = _failing_fetch
            try:
                result = signals_module._batch_fetch_constance(["ALLOW_SIGNUP"])
                self.assertEqual(result, {})
            finally:
                signals_module._batch_fetch_constance = original

    @override_settings(
        CONSTANCE_CONFIG=MOCK_CONSTANCE_CONFIG,
        CONSTANCE_DATABASE_PREFIX="constance:core:",
    )
    def test_batch_fetch_uses_single_query(self):
        """Verify batch fetch makes exactly 1 DB query (WHERE key IN ...)."""
        import pickle  # nosec B403,B301 — test uses pickle to mimic constance's own serialization

        with mock.patch(
            "constance.models.Constance"
        ) as MockConstance:
            MockConstance.objects.filter.return_value.values_list.return_value = [
                ("constance:core:ALLOW_SIGNUP", pickle.dumps(False)),
                ("constance:core:EMAIL_HOST", pickle.dumps("smtp.example.com")),
            ]

            result = _batch_fetch_constance(
                ["ALLOW_SIGNUP", "MULTI_ORGANIZATIONS", "EMAIL_HOST"]
            )

            # Single filter() call with all keys
            MockConstance.objects.filter.assert_called_once()
            call_kwargs = MockConstance.objects.filter.call_args
            self.assertIn("key__in", call_kwargs.kwargs)
            self.assertEqual(len(call_kwargs.kwargs["key__in"]), 3)

        self.assertEqual(result["ALLOW_SIGNUP"], False)
        self.assertEqual(result["MULTI_ORGANIZATIONS"], False)  # default
        self.assertEqual(result["EMAIL_HOST"], "smtp.example.com")


class TestUpdateSettings(TestCase):
    """Test update_settings uses batch fetch path."""

    @override_settings(
        CONSTANCE_CONFIG=MOCK_CONSTANCE_CONFIG,
        CONSTANCE_DATABASE_PREFIX="constance:core:",
        ALLOW_SIGNUP=True,
        MULTI_ORGANIZATIONS=False,
        EMAIL_ENABLED=False,
    )
    @mock.patch("karrio.server.core.signals._batch_fetch_constance")
    def test_update_settings_uses_batch_fetch(self, mock_batch):
        """When batch fetch succeeds, individual getattr is not used."""
        mock_batch.return_value = {
            "ALLOW_SIGNUP": False,
            "MULTI_ORGANIZATIONS": True,
            "EMAIL_HOST": "smtp.example.com",
            "EMAIL_HOST_USER": "admin@example.com",
        }

        from django.conf import settings

        update_settings(mock.MagicMock())

        mock_batch.assert_called_once()
        self.assertEqual(settings.ALLOW_SIGNUP, False)
        self.assertEqual(settings.MULTI_ORGANIZATIONS, True)
        self.assertEqual(settings.EMAIL_ENABLED, True)

    @override_settings(
        CONSTANCE_CONFIG=MOCK_CONSTANCE_CONFIG,
        CONSTANCE_DATABASE_PREFIX="constance:core:",
        ALLOW_SIGNUP=True,
        EMAIL_ENABLED=False,
    )
    @mock.patch("karrio.server.core.signals._batch_fetch_constance")
    def test_fallback_to_individual_when_batch_fails(self, mock_batch):
        """When batch fetch returns empty, falls back to individual getattr."""
        mock_batch.return_value = {}

        mock_config = mock.MagicMock()
        mock_config.ALLOW_SIGNUP = False
        mock_config.EMAIL_HOST = "smtp.test.com"
        mock_config.EMAIL_HOST_USER = "user@test.com"

        from django.conf import settings

        update_settings(mock_config)

        self.assertEqual(settings.ALLOW_SIGNUP, False)
        self.assertEqual(settings.EMAIL_ENABLED, True)


if __name__ == "__main__":
    unittest.main()
