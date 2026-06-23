"""Tests for StatusView — the stripped /status/ health endpoint (issue #581).

Verifies that the endpoint:
  - returns a bare 200 with body "OK" when all checks pass
  - never leaks infra detail in any response (including ?format=json)
  - returns 500 with body "unavailable" when any check reports an error
"""

import socket
import unittest.mock

from django.test import TestCase
from django.urls import reverse
from karrio.server.core.views.health import StatusView


class _FakeResult:
    """Stub check result with no error (healthy)."""

    error = None


class _FakeCheck:
    """Stub health check that always passes."""

    async def get_result(self):
        return _FakeResult()


class TestHealthStatus(TestCase):
    """Tests for the /status/ endpoint served by StatusView."""

    def setUp(self):
        self.maxDiff = None
        self.url = reverse("karrio.server.core:health_check")

    def test_status_healthy_returns_bare_200(self):
        """All checks pass → 200, body == "OK"."""
        with unittest.mock.patch.object(StatusView, "get_checks", return_value=[_FakeCheck()]):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "OK")
        self.assertIn("text/plain", response["Content-Type"])

    def test_status_body_leaks_no_infra_detail(self):
        """Body must contain none of the known-leaky strings from django-health-check.

        This is a regression guard for issue #581. Also explicitly verifies that
        hitting /status/?format=json still returns the bare plain-text "OK" — not
        JSON with infra detail.
        """
        leak_strings = [
            socket.gethostname(),
            "Database",
            "Cache",
            "Redis",
            "Disk",
            "Memory",
            "time_taken",
            "working",
            "/app",
            "path=",
            "alias=",
            "hostname=",
        ]

        for url in [self.url, self.url + "?format=json", self.url + "?format=text"]:
            with unittest.mock.patch.object(StatusView, "get_checks", return_value=[_FakeCheck()]):
                response = self.client.get(url)
            body = response.content.decode()

            self.assertEqual(response.status_code, 200, msg=f"Expected 200 for {url}")
            for leak in leak_strings:
                self.assertNotIn(
                    leak,
                    body,
                    msg=f"Infra detail '{leak}' leaked in response for {url}",
                )

    def test_status_unhealthy_returns_500(self):
        """When any check has a truthy .error → 500, body "unavailable", no infra detail."""

        class _FailingResult:
            error = "something went wrong"

        class _FailingCheck:
            async def get_result(self):
                return _FailingResult()

        with unittest.mock.patch.object(StatusView, "get_checks", return_value=[_FailingCheck()]):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content.decode(), "unavailable")
        self.assertIn("text/plain", response["Content-Type"])
        # Must not contain any infra detail even in unhealthy path
        self.assertNotIn("Database", response.content.decode())
        self.assertNotIn("Redis", response.content.decode())
