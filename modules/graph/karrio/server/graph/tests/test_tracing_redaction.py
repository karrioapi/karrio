"""Tenant-side `tracing_records` query must not surface SystemConnection PKs.

`TracingRecord.meta.carrier_account_id` is stamped by the SDK settings layer
with the live gateway connection PK (see `karrio.core.settings.Settings.trace`).
For brokered/system carriers that PK is server-internal — the same kind of
value the rate-meta redaction helpers strip elsewhere. Without an exclusion
filter on the tenant graph, a merchant could read it via the top-level
`tracing_records` query even though `LogType.records` already hides those rows.
"""

import json
import time

import karrio.server.tracing.models as tracing
from django.contrib.auth import get_user_model
from karrio.server.graph.tests.base import GraphTestCase
from karrio.server.user.models import Token
from rest_framework.test import APIClient

_RECORDS_QUERY = """
query TracingRecords {
    tracing_records(filter: { offset: 0, first: 50 }) {
        edges {
            node {
                id
                meta
            }
        }
    }
}
"""

_RECORD_QUERY = """
query TracingRecord($id: String!) {
    tracing_record(id: $id) {
        id
        meta
    }
}
"""


class TestTracingRecordRedaction(GraphTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        # Non-staff merchant user — the audience this filter protects.
        cls.merchant_user = get_user_model().objects.create_user(
            email="merchant@example.com",
            password="test",
            is_staff=False,
        )
        cls.merchant_token = Token.objects.create(user=cls.merchant_user, test_mode=False)

        from django.conf import settings as django_settings

        if django_settings.MULTI_ORGANIZATIONS:
            from karrio.server.orgs.models import TokenLink

            cls.organization.add_user(cls.merchant_user, is_admin=False)
            TokenLink.objects.create(item=cls.merchant_token, org=cls.organization)

        # Two tracing records owned by the merchant — one points at a
        # SystemConnection PK (must be hidden from non-staff), one points
        # at the merchant's own CarrierConnection PK (must remain visible).
        cls.system_record = tracing.TracingRecord.objects.create(
            key="ship_request",
            record={"data": "system carrier request"},
            timestamp=time.time(),
            test_mode=False,
            created_by=cls.merchant_user,
            meta={
                "carrier_account_id": cls.dhl_system_connection.id,
                "carrier_id": cls.dhl_system_connection.carrier_id,
                "carrier_name": cls.dhl_system_connection.carrier_code,
            },
        )
        cls.account_record = tracing.TracingRecord.objects.create(
            key="ship_request",
            record={"data": "merchant carrier request"},
            timestamp=time.time(),
            test_mode=False,
            created_by=cls.merchant_user,
            meta={
                "carrier_account_id": cls.carrier.id,
                "carrier_id": cls.carrier.carrier_id,
                "carrier_name": cls.carrier.carrier_code,
            },
        )
        # A third record owned by the staff admin user, also pointing at a
        # SystemConnection PK — used to assert that staff queries are NOT
        # filtered (admins debug carrier integrations against system carriers).
        cls.staff_owned_system_record = tracing.TracingRecord.objects.create(
            key="ship_request",
            record={"data": "admin trace against system carrier"},
            timestamp=time.time(),
            test_mode=False,
            created_by=cls.user,
            meta={
                "carrier_account_id": cls.dhl_system_connection.id,
                "carrier_id": cls.dhl_system_connection.carrier_id,
                "carrier_name": cls.dhl_system_connection.carrier_code,
            },
        )

        if django_settings.MULTI_ORGANIZATIONS:
            from karrio.server.serializers import bulk_link_org
            from karrio.server.serializers.abstract import Context

            # Link records to the org so access_by() picks them up regardless
            # of which user runs the query.
            ctx = Context(user=cls.user, org=cls.organization, test_mode=False)
            bulk_link_org(
                [cls.system_record, cls.account_record, cls.staff_owned_system_record],
                ctx,
            )

    def _merchant_client(self) -> APIClient:
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + self.merchant_token.key)
        return client

    def _post(self, client: APIClient, *, query: str, variables: dict | None = None) -> dict:
        from django.urls import reverse

        response = client.post(
            reverse("karrio.server.graph:graphql"),
            dict(query=query, variables=variables, operation_name=None),
        )
        return json.loads(response.content)

    # ── Non-staff merchant ──────────────────────────────────────────────

    def test_merchant_cannot_list_system_connection_traces(self):
        """`tracing_records` excludes records whose `carrier_account_id`
        is a SystemConnection PK for non-staff users."""
        client = self._merchant_client()
        result = self._post(client, query=_RECORDS_QUERY)
        self.assertIsNone(result.get("errors"))

        ids = {edge["node"]["id"] for edge in result["data"]["tracing_records"]["edges"]}
        self.assertIn(self.account_record.id, ids)
        self.assertNotIn(self.system_record.id, ids)

    def test_merchant_cannot_fetch_system_connection_trace_by_id(self):
        """`tracing_record(id: ...)` returns null for system-connection
        records even when the merchant owns the row."""
        client = self._merchant_client()
        result = self._post(
            client,
            query=_RECORD_QUERY,
            variables={"id": self.system_record.id},
        )
        self.assertIsNone(result.get("errors"))
        self.assertIsNone(result["data"]["tracing_record"])

    # ── Staff admin ─────────────────────────────────────────────────────

    def test_staff_sees_system_connection_traces(self):
        """Admin tooling (`/admin/graphql` is staff-gated at the route;
        the base graph still serves staff users) must keep the full view
        — admins need this to debug carrier integrations."""
        result = self._post(self.client, query=_RECORDS_QUERY)
        self.assertIsNone(result.get("errors"))

        ids = {edge["node"]["id"] for edge in result["data"]["tracing_records"]["edges"]}
        # The staff-owned record points at a SystemConnection PK; the staff
        # branch in the filter leaves it in the result.
        self.assertIn(self.staff_owned_system_record.id, ids)
