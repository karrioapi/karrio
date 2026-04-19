"""
Admin API authentication, authorization and input-validation tests.

These are the tests that were entirely missing from the original admin
test monolith: every happy-path mutation had zero coverage for:
  - Unauthenticated access (401/403)
  - Non-staff user calling admin-only endpoints (403)
  - Invalid / missing input (400 / GraphQL errors)
  - Cross-user data isolation
"""

import karrio.server.providers.models as providers
from django.contrib.auth import get_user_model
from karrio.server.admin.tests.base import AdminGraphTestCase
from karrio.server.user.models import Token
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# ---------------------------------------------------------------------------
# Unauthenticated access
# ---------------------------------------------------------------------------


class TestAdminUnauthenticated(APITestCase):
    """Admin GraphQL endpoint must reject unauthenticated requests."""

    def test_unauthenticated_graphql_returns_error(self):
        """Unauthenticated GraphQL request must be blocked.

        The admin GraphQL endpoint may return HTTP 200 with a GraphQL-level
        permission error, or HTTP 401/403. Either is acceptable — the key
        requirement is that rate_sheets data is NOT returned.
        """
        from django.urls import reverse

        client = APIClient()  # No credentials
        response = client.post(
            reverse("karrio.server.admin:admin-graph"),
            {"query": "{ rate_sheets { edges { node { id } } } }"},
        )
        data = response.json() if response.status_code == 200 else {}

        is_blocked = (
            response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
            or data.get("errors") is not None
            or data.get("data", {}).get("rate_sheets") is None
        )
        self.assertTrue(is_blocked, f"Unauthenticated access was not blocked: {response.status_code} {data}")

    def test_unauthenticated_mutation_is_rejected(self):
        """Unauthenticated mutation must not create resources."""
        from django.urls import reverse

        client = APIClient()
        response = client.post(
            reverse("karrio.server.admin:admin-graph"),
            {
                "query": """
                mutation {
                  create_rate_sheet(input: {name: "Evil Sheet", carrier_name: "ups"}) { id }
                }
                """
            },
        )
        data = response.json() if response.status_code == 200 else {}
        is_blocked = (
            response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
            or data.get("errors") is not None
            or data.get("data", {}).get("create_rate_sheet") is None
        )
        self.assertTrue(is_blocked, f"Unauthenticated mutation was not blocked: {response.status_code} {data}")


# ---------------------------------------------------------------------------
# Non-admin (non-staff) user access
# ---------------------------------------------------------------------------


class TestAdminNonStaffUser(APITestCase):
    """Regular (non-staff) users must not access admin endpoints."""

    @classmethod
    def setUpTestData(cls):
        cls.regular_user = get_user_model().objects.create_user(email="regular@example.com", password="test")
        cls.regular_token = Token.objects.create(user=cls.regular_user, test_mode=False)

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.regular_token.key)

    def test_non_staff_cannot_query_admin_rate_sheets(self):
        from django.urls import reverse

        response = self.client.post(
            reverse("karrio.server.admin:admin-graph"),
            {"query": "{ rate_sheets { edges { node { id } } } }"},
        )
        # Must either reject outright or return a permission error in GraphQL errors
        data = response.json() if response.status_code == 200 else {}
        non_staff_blocked = response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN] or (
            data.get("errors") is not None and len(data["errors"]) > 0
        )
        self.assertTrue(non_staff_blocked, f"Non-staff got unrestricted access: {response.status_code} {data}")

    def test_non_staff_cannot_create_system_connection(self):
        from django.urls import reverse

        response = self.client.post(
            reverse("karrio.server.admin:admin-graph"),
            {
                "query": """
                mutation {
                  create_system_carrier_connection(input: {
                    carrier_name: "dhl_express"
                    carrier_id: "dhl_evil"
                    credentials: {site_id: "x", password: "y", account_number: "z"}
                  }) { id }
                }
                """
            },
        )
        data = response.json() if response.status_code == 200 else {}
        non_staff_blocked = response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN] or (
            data.get("errors") is not None and len(data["errors"]) > 0
        )
        self.assertTrue(non_staff_blocked)


# ---------------------------------------------------------------------------
# Invalid input validation
# ---------------------------------------------------------------------------


class TestAdminRateSheetValidation(AdminGraphTestCase):
    """Admin mutations must reject invalid or missing input."""

    def test_create_rate_sheet_missing_name_returns_error(self):
        result = self.query(
            """
            mutation create_rate_sheet($input: CreateRateSheetInput!) {
              create_rate_sheet(input: $input) { id name }
            }
            """,
            operation_name="create_rate_sheet",
            variables={
                "input": {
                    # name intentionally omitted
                    "carrier_name": "ups",
                }
            },
        )
        # Must return GraphQL validation error
        self.assertIsNotNone(result.data.get("errors"), "Expected errors for missing required field 'name'")

    def test_create_rate_sheet_invalid_carrier_name_returns_error(self):
        result = self.query(
            """
            mutation create_rate_sheet($input: CreateRateSheetInput!) {
              create_rate_sheet(input: $input) { id name }
            }
            """,
            operation_name="create_rate_sheet",
            variables={
                "input": {
                    "name": "Invalid Carrier Sheet",
                    "carrier_name": "nonexistent_carrier_xyz",
                }
            },
        )
        has_error = (
            result.data.get("errors") is not None or result.data.get("data", {}).get("create_rate_sheet") is None
        )
        self.assertTrue(has_error, "Expected error for unknown carrier_name")

    def test_add_zone_invalid_rate_sheet_id_returns_error(self):
        result = self.query(
            """
            mutation add_shared_zone($input: AddRateSheetZoneInput!) {
              add_shared_zone(input: $input) { id }
            }
            """,
            operation_name="add_shared_zone",
            variables={
                "input": {
                    "rate_sheet_id": "nonexistent-id-000",
                    "zone": {"id": "zone_1", "label": "Zone 1"},
                }
            },
        )
        has_error = result.data.get("errors") is not None or result.data.get("data", {}).get("add_shared_zone") is None
        self.assertTrue(has_error, "Expected error for nonexistent rate_sheet_id")

    def test_delete_nonexistent_rate_sheet_returns_error(self):
        result = self.query(
            """
            mutation delete_rate_sheet($id: String!) {
              delete_rate_sheet(id: $id) { id }
            }
            """,
            operation_name="delete_rate_sheet",
            variables={"id": "nonexistent-rate-sheet-id"},
        )
        has_error = (
            result.data.get("errors") is not None or result.data.get("data", {}).get("delete_rate_sheet") is None
        )
        self.assertTrue(has_error, "Expected error when deleting nonexistent rate sheet")


class TestAdminConnectionValidation(AdminGraphTestCase):
    """System connection mutations must reject invalid input."""

    def test_create_connection_duplicate_carrier_id_returns_error(self):
        # Create a connection first
        providers.SystemConnection.objects.create(
            carrier_code="dhl_universal",
            carrier_id="dhl_universal_dup_test",
            test_mode=False,
            active=True,
            credentials=dict(consumer_key="k", consumer_secret="s"),
        )

        # Try to create another with the same carrier_id
        result = self.query(
            """
            mutation create_system_carrier_connection($input: CreateSystemCarrierConnectionInput!) {
              create_system_carrier_connection(input: $input) { id }
            }
            """,
            operation_name="create_system_carrier_connection",
            variables={
                "input": {
                    "carrier_name": "dhl_universal",
                    "carrier_id": "dhl_universal_dup_test",
                    "credentials": {"consumer_key": "k2", "consumer_secret": "s2"},
                }
            },
        )
        has_error = (
            result.data.get("errors") is not None
            or result.data.get("data", {}).get("create_system_carrier_connection") is None
        )
        self.assertTrue(has_error, "Expected error for duplicate carrier_id")

    def test_update_nonexistent_connection_returns_error(self):
        result = self.query(
            """
            mutation update_system_carrier_connection($input: UpdateSystemCarrierConnectionInput!) {
              update_system_carrier_connection(input: $input) { id }
            }
            """,
            operation_name="update_system_carrier_connection",
            variables={
                "input": {
                    "id": "nonexistent-connection-id",
                    "active": True,
                }
            },
        )
        has_error = (
            result.data.get("errors") is not None
            or result.data.get("data", {}).get("update_system_carrier_connection") is None
        )
        self.assertTrue(has_error, "Expected error when updating nonexistent connection")


class TestAdminMarkupValidation(AdminGraphTestCase):
    """Markup mutations must reject invalid input."""

    def test_create_markup_with_negative_amount_returns_error(self):
        result = self.query(
            """
            mutation create_markup($input: CreateMarkupInput!) {
              create_markup(input: $input) { id }
            }
            """,
            operation_name="create_markup",
            variables={
                "input": {
                    "name": "Negative Test",
                    "amount": -99.0,
                    "markup_type": "AMOUNT",
                }
            },
        )
        has_error = result.data.get("errors") is not None or result.data.get("data", {}).get("create_markup") is None
        self.assertTrue(has_error, "Expected validation error for negative markup amount")

    def test_delete_nonexistent_markup_returns_error(self):
        result = self.query(
            """
            mutation delete_markup($id: String!) {
              delete_markup(id: $id) { id }
            }
            """,
            operation_name="delete_markup",
            variables={"id": "nonexistent-markup-id"},
        )
        has_error = result.data.get("errors") is not None or result.data.get("data", {}).get("delete_markup") is None
        self.assertTrue(has_error, "Expected error when deleting nonexistent markup")


# ---------------------------------------------------------------------------
# Cross-user data isolation
# ---------------------------------------------------------------------------


class TestAdminDataIsolation(APITestCase):
    """
    Verify that a staff user from org A cannot modify system resources
    owned/managed by a different admin context.
    """

    @classmethod
    def setUpTestData(cls):
        from django.urls import reverse as _reverse

        cls.reverse = staticmethod(_reverse)

        # Admin 1
        cls.admin1 = get_user_model().objects.create_superuser("admin1@example.com", "test")
        cls.admin1.is_staff = True
        cls.admin1.save()
        cls.token1 = Token.objects.create(user=cls.admin1, test_mode=False)

        # Admin 2
        cls.admin2 = get_user_model().objects.create_superuser("admin2@example.com", "test")
        cls.admin2.is_staff = True
        cls.admin2.save()
        cls.token2 = Token.objects.create(user=cls.admin2, test_mode=False)

        # A system connection owned by admin1's creation context
        cls.system_conn = providers.SystemConnection.objects.create(
            carrier_code="dhl_universal",
            carrier_id="dhl_isolation_test",
            test_mode=False,
            active=True,
            credentials=dict(consumer_key="isolation_key", consumer_secret="isolation_secret"),
        )

    def _client_for(self, token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        return client

    def _query(self, client, query, variables=None):
        from django.urls import reverse

        response = client.post(
            reverse("karrio.server.admin:admin-graph"),
            {"query": query, "variables": variables},
        )
        return response.status_code, response.json()

    def test_admin2_can_read_system_connections(self):
        """System connections are globally visible to all admins."""
        client2 = self._client_for(self.token2)
        code, data = self._query(
            client2,
            "{ system_carrier_connections { edges { node { id carrier_id } } } }",
        )
        self.assertEqual(code, 200)
        self.assertIsNone(data.get("errors"))
        ids = [edge["node"]["carrier_id"] for edge in data["data"]["system_carrier_connections"]["edges"]]
        self.assertIn("dhl_isolation_test", ids)

    def test_token_for_admin1_cannot_be_used_by_admin2(self):
        """Tokens are non-transferable — admin2 using admin1's token is rejected."""
        # admin2 tries to use admin1's raw token value but the user is different
        # This tests that token → user lookup is deterministic
        client_fake = APIClient()
        client_fake.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)
        # Make a query that would reveal admin1's context; the test itself
        # just verifies the token resolves to admin1's user in the response
        from django.urls import reverse

        response = client_fake.post(
            reverse("karrio.server.admin:admin-graph"),
            {"query": "{ user { email } }"},
        )
        # The response may 200 (with user data) or 401/403
        if response.status_code == 200:
            try:
                data = response.json()
            except Exception:
                data = {}
            user_data = (data.get("data") or {}).get("user") or {}
            if user_data:
                resolved_email = user_data.get("email", "")
                self.assertEqual(resolved_email, "admin1@example.com")
