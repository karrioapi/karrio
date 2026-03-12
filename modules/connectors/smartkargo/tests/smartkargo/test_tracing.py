"""SmartKargo Sentry tracing context propagation tests.

Verifies that _urlopen_with_span (not plain urlopen) is called when
lib.request() runs inside exec_async worker threads, and that the
Sentry span context is available in those threads.
"""

import unittest
from unittest.mock import patch, MagicMock, call
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestSmartKargoTracingContext(unittest.TestCase):
    """Assert that Sentry tracing context propagates through exec_async."""

    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(
            tracking_numbers=["yogi045"],
        )
        self.RateRequest = models.RateRequest(
            shipper={
                "address_line1": "1 Broadway",
                "city": "Boston",
                "postal_code": "02142",
                "country_code": "US",
                "state_code": "MA",
                "person_name": "TESTER TEST",
                "company_name": "Test Company",
                "phone_number": "19999999999",
                "email": "test@test.com",
            },
            recipient={
                "address_line1": "124 Main St",
                "city": "Los Angeles",
                "postal_code": "98148",
                "country_code": "US",
                "state_code": "CA",
                "person_name": "Tester Tester",
                "phone_number": "8888347867",
                "email": "test2@test.com",
            },
            parcels=[
                {
                    "weight": 10.0,
                    "width": 20.0,
                    "height": 20.0,
                    "length": 20.0,
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                }
            ],
        )

    def test_urlopen_with_span_called_in_tracking(self):
        """_urlopen_with_span must be called (not bypassed) when tracking
        goes through exec_async."""
        with patch(
            "karrio.core.utils.helpers._urlopen_with_span"
        ) as mock_span_open:
            mock_resp = MagicMock()
            mock_resp.read.return_value = b"[]"
            mock_resp.status = 200
            mock_resp.headers = {}
            mock_resp.__enter__ = MagicMock(return_value=mock_resp)
            mock_resp.__exit__ = MagicMock(return_value=False)
            mock_span_open.return_value = mock_resp

            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertTrue(
                mock_span_open.called,
                "_urlopen_with_span was not called — Sentry spans will be missing",
            )

    def test_urlopen_with_span_called_in_rating(self):
        """_urlopen_with_span must be called (not bypassed) when rating
        goes through exec_async."""
        with patch(
            "karrio.core.utils.helpers._urlopen_with_span"
        ) as mock_span_open:
            mock_resp = MagicMock()
            mock_resp.read.return_value = b"{}"
            mock_resp.status = 200
            mock_resp.headers = {}
            mock_resp.__enter__ = MagicMock(return_value=mock_resp)
            mock_resp.__exit__ = MagicMock(return_value=False)
            mock_span_open.return_value = mock_resp

            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertTrue(
                mock_span_open.called,
                "_urlopen_with_span was not called — Sentry spans will be missing",
            )

    def test_sentry_scope_propagated_into_exec_async(self):
        """When a Sentry isolation scope exists, exec_async must propagate it
        into worker threads via new_scope + update_from_scope."""
        mock_scope = MagicMock()
        mock_new_scope_cm = MagicMock()
        mock_new_scope_cm.__enter__ = MagicMock(return_value=mock_scope)
        mock_new_scope_cm.__exit__ = MagicMock(return_value=False)

        with patch.dict("sys.modules", {"sentry_sdk": MagicMock()}) as _:
            import sys

            mock_sentry = sys.modules["sentry_sdk"]
            mock_sentry.get_isolation_scope.return_value = MagicMock()
            mock_sentry.new_scope.return_value = mock_new_scope_cm

            results = lib.run_asynchronously(lambda x: x * 2, [1, 2, 3])

            self.assertTrue(
                mock_sentry.get_isolation_scope.called,
                "get_isolation_scope was not called — scope not captured",
            )
            self.assertTrue(
                mock_sentry.new_scope.called,
                "new_scope was not called — scope not propagated to workers",
            )
            self.assertEqual(sorted(results), [2, 4, 6])


if __name__ == "__main__":
    unittest.main()
