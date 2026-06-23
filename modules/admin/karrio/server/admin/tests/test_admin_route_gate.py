"""
Regression tests for SHIP2-1164.

The /admin/graphql endpoint must enforce staff-only access at the route level,
before any GraphQL resolver runs. Authorization is centralized on the route —
per-resolver decorators are not used — so adding a new query or mutation to
any admin schema cannot accidentally bypass the staff check.

These tests verify that:
1. A non-staff authenticated user receives HTTP 403 for any /admin/graphql
   request — including the queries that previously leaked.
2. An unauthenticated user receives HTTP 401.
3. A staff user is not blocked by the route-level gate.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from karrio.server.admin.tests.base import AdminGraphTestCase
from karrio.server.user.models import Token
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Queries that previously leaked cross-tenant data. The schema only contains
# the orgs admin types when karrio-insiders is installed; the gate must reject
# the request regardless of whether the field resolves so we use a query that
# is always present (rate_sheets) AND the previously-vulnerable ones.
PICKUPS_QUERY = "{ pickups { edges { node { id } } } }"
SHIPMENTS_QUERY = "{ shipments { edges { node { id } } } }"
TRACKERS_QUERY = "{ trackers { edges { node { id } } } }"
ORDERS_QUERY = "{ orders { edges { node { id } } } }"
RATE_SHEETS_QUERY = "{ rate_sheets { edges { node { id } } } }"


class TestAdminGraphQLRouteGate(APITestCase):
    """The /admin/graphql route rejects non-staff before the schema executes."""

    @classmethod
    def setUpTestData(cls):
        cls.regular_user = get_user_model().objects.create_user(email="regular-route@example.com", password="test")
        cls.regular_token = Token.objects.create(user=cls.regular_user, test_mode=False)

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.regular_token.key)
        self.url = reverse("karrio.server.admin:admin-graph")

    def _post(self, query: str):
        return self.client.post(self.url, {"query": query})

    def test_non_staff_pickups_query_is_rejected_at_route(self):
        """SHIP2-1164: pickups query must be blocked before the resolver runs."""
        response = self._post(PICKUPS_QUERY)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        body = response.json()
        self.assertIn("errors", body)
        self.assertNotIn("data", body)

    def test_non_staff_shipments_query_is_rejected_at_route(self):
        response = self._post(SHIPMENTS_QUERY)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("data", response.json())

    def test_non_staff_trackers_query_is_rejected_at_route(self):
        response = self._post(TRACKERS_QUERY)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("data", response.json())

    def test_non_staff_orders_query_is_rejected_at_route(self):
        response = self._post(ORDERS_QUERY)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("data", response.json())

    def test_non_staff_rate_sheets_query_is_rejected_at_route(self):
        """Even queries that were always decorated must now hit the route gate."""
        response = self._post(RATE_SHEETS_QUERY)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("data", response.json())

    def test_non_staff_mutation_is_rejected_at_route(self):
        response = self._post('mutation { create_rate_sheet(input: {name: "x", carrier_name: "ups"}) { id } }')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAdminGraphQLRouteGateUnauthenticated(APITestCase):
    """Unauthenticated requests to /admin/graphql receive HTTP 401."""

    def setUp(self):
        self.client = APIClient()  # no credentials
        self.url = reverse("karrio.server.admin:admin-graph")

    def test_unauthenticated_query_returns_401(self):
        response = self.client.post(self.url, {"query": PICKUPS_QUERY})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        body = response.json()
        self.assertIn("errors", body)


class TestAdminGraphQLRouteGateStaffPasses(AdminGraphTestCase):
    """The route-level gate must not block legitimate staff access."""

    def test_staff_can_query_rate_sheets(self):
        result = self.query(RATE_SHEETS_QUERY)
        # Either data resolves (200, no errors) or schema-level error — what
        # matters is the route gate did not return 401/403.
        self.assertNotIn(result.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
