"""Tests for carrier connection OAuth and Webhook APIs."""

import json
from unittest.mock import patch, ANY
from django.urls import reverse
from rest_framework import status
from karrio.core.models import (
    OAuthAuthorizeRequest,
    WebhookRegistrationDetails,
    ConfirmationDetails,
    Message,
)
from karrio.server.core.tests import APITestCase
import karrio.server.providers.models as providers


class TestConnectionOAuthAuthorize(APITestCase):
    """Tests for OAuth authorization flow endpoints."""

    def test_oauth_authorize(self):
        """Test POST /v1/connections/oauth/{carrier_name}/authorize."""
        url = reverse(
            "karrio.server.providers:connection-oauth-authorize",
            kwargs=dict(carrier_name="teleship"),
        )
        data = OAUTH_AUTHORIZE_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = OAUTH_AUTHORIZE_RETURNED_VALUE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, OAUTH_AUTHORIZE_RESPONSE)

    def test_oauth_authorize_error(self):
        """Test OAuth authorize with configuration error."""
        url = reverse(
            "karrio.server.providers:connection-oauth-authorize",
            kwargs=dict(carrier_name="teleship"),
        )
        data = {"state": "test_state", "options": {}}

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = OAUTH_AUTHORIZE_ERROR_RETURNED_VALUE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, OAUTH_AUTHORIZE_ERROR_RESPONSE)


class TestConnectionOAuthCallback(APITestCase):
    """Tests for OAuth callback handling."""

    def test_oauth_callback_get(self):
        """Test GET /v1/connections/oauth/{carrier_name}/callback with valid credentials."""
        url = reverse(
            "karrio.server.providers:connection-oauth-callback",
            kwargs=dict(carrier_name="teleship"),
        )
        query_params = (
            "?code=auth_code_12345"
            "&account_client_id=user_client_abc"
            "&account_client_secret=user_secret_xyz"
            "&state=eyJjb25uZWN0aW9uX2lkIjogIjEyMyJ9"
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = OAUTH_CALLBACK_RETURNED_VALUE
            response = self.client.get(f"{url}{query_params}")
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, OAUTH_CALLBACK_RESPONSE)

    def test_oauth_callback_post(self):
        """Test POST /v1/connections/oauth/{carrier_name}/callback with valid credentials."""
        url = reverse(
            "karrio.server.providers:connection-oauth-callback",
            kwargs=dict(carrier_name="teleship"),
        )
        query_params = (
            "?code=auth_code_12345"
            "&account_client_id=user_client_abc"
            "&account_client_secret=user_secret_xyz"
            "&state=eyJjb25uZWN0aW9uX2lkIjogIjEyMyJ9"
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = OAUTH_CALLBACK_RETURNED_VALUE
            response = self.client.post(f"{url}{query_params}", {}, format="json")
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, OAUTH_CALLBACK_RESPONSE)

    def test_oauth_callback_error(self):
        """Test OAuth callback with missing authorization code."""
        url = reverse(
            "karrio.server.providers:connection-oauth-callback",
            kwargs=dict(carrier_name="teleship"),
        )
        query_params = (
            "?account_client_id=user_client_abc"
            "&account_client_secret=user_secret_xyz"
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = OAUTH_CALLBACK_ERROR_RETURNED_VALUE
            response = self.client.get(f"{url}{query_params}")
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, OAUTH_CALLBACK_ERROR_RESPONSE)


class TestConnectionWebhookRegister(APITestCase):
    """Tests for webhook registration."""

    def setUp(self):
        super().setUp()
        url = reverse("karrio.server.providers:carrier-connection-list")
        response = self.client.post(url, TELESHIP_CONNECTION_DATA, format="json")
        self.teleship_carrier_pk = json.loads(response.content)["id"]

    def test_webhook_register(self):
        """Test POST /v1/connections/webhook/{pk}/register."""
        url = reverse(
            "karrio.server.providers:connection-webhook-register",
            kwargs=dict(pk=self.teleship_carrier_pk),
        )
        data = WEBHOOK_REGISTER_DATA

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = WEBHOOK_REGISTER_RETURNED_VALUE
            response = self.client.post(url, data)
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, WEBHOOK_REGISTER_RESPONSE)


class TestConnectionWebhookDeregister(APITestCase):
    """Tests for webhook deregistration."""

    def setUp(self):
        super().setUp()
        url = reverse("karrio.server.providers:carrier-connection-list")
        response = self.client.post(
            url, TELESHIP_CONNECTION_WITH_WEBHOOK_DATA, format="json"
        )
        self.teleship_carrier_pk = json.loads(response.content)["id"]

    def test_webhook_deregister(self):
        """Test POST /v1/connections/webhook/{pk}/deregister."""
        url = reverse(
            "karrio.server.providers:connection-webhook-deregister",
            kwargs=dict(pk=self.teleship_carrier_pk),
        )

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = WEBHOOK_DEREGISTER_RETURNED_VALUE
            response = self.client.post(url, {})
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, WEBHOOK_DEREGISTER_RESPONSE)


class TestConnectionWebhookDisconnect(APITestCase):
    """Tests for force disconnecting webhook (local only)."""

    def setUp(self):
        super().setUp()
        url = reverse("karrio.server.providers:carrier-connection-list")
        response = self.client.post(
            url, TELESHIP_CONNECTION_WITH_WEBHOOK_DATA, format="json"
        )
        self.teleship_carrier_pk = json.loads(response.content)["id"]

    def test_webhook_disconnect(self):
        """Test POST /v1/connections/webhook/{pk}/disconnect."""
        url = reverse(
            "karrio.server.providers:connection-webhook-disconnect",
            kwargs=dict(pk=self.teleship_carrier_pk),
        )

        response = self.client.post(url, {})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, WEBHOOK_DISCONNECT_RESPONSE)

        # Verify the webhook config was cleared
        detail_url = reverse(
            "karrio.server.providers:carrier-connection-details",
            kwargs=dict(pk=self.teleship_carrier_pk),
        )
        detail_response = self.client.get(detail_url)
        detail_data = json.loads(detail_response.content)
        self.assertIsNone(detail_data["config"].get("webhook_id"))
        self.assertIsNone(detail_data["config"].get("webhook_secret"))


class TestConnectionWebhookEvent(APITestCase):
    """Tests for inbound webhook event processing."""

    def setUp(self):
        super().setUp()
        url = reverse("karrio.server.providers:carrier-connection-list")
        response = self.client.post(
            url, TELESHIP_CONNECTION_WITH_WEBHOOK_DATA, format="json"
        )
        self.teleship_carrier_pk = json.loads(response.content)["id"]

    def test_webhook_event(self):
        """Test POST /v1/connections/webhook/{pk}/events with valid event."""
        url = reverse(
            "karrio.server.providers:connection-webhook-event",
            kwargs=dict(pk=self.teleship_carrier_pk),
        )

        from karrio.server.core import datatypes

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = (
                datatypes.WebhookEventDetails(
                    carrier_name="teleship",
                    carrier_id="teleship_connection",
                    tracking_number="TELESHIP12345678901",
                    shipment_identifier="shp-12345",
                    tracking=None,
                ),
                [],
            )
            client = self.client_class()
            response = client.post(url, WEBHOOK_EVENT_DATA, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_webhook_event_not_found(self):
        """Test webhook event with non-existent connection."""
        url = reverse(
            "karrio.server.providers:connection-webhook-event",
            kwargs=dict(pk="non-existent-pk"),
        )

        client = self.client_class()
        response = client.post(url, WEBHOOK_EVENT_DATA, format="json")
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response_data, WEBHOOK_EVENT_NOT_FOUND_RESPONSE)

    def test_webhook_event_signature_error(self):
        """Test webhook event with invalid signature."""
        url = reverse(
            "karrio.server.providers:connection-webhook-event",
            kwargs=dict(pk=self.teleship_carrier_pk),
        )

        from karrio.server.core import datatypes

        with patch("karrio.server.core.gateway.utils.identity") as mock:
            mock.return_value = (
                None,
                [
                    datatypes.Message(
                        carrier_name="teleship",
                        carrier_id="teleship_connection",
                        code="SIGNATURE_INVALID",
                        message="Webhook signature verification failed",
                    )
                ],
            )
            client = self.client_class()
            response = client.post(
                url,
                WEBHOOK_EVENT_DATA,
                format="json",
                HTTP_X_TELESHIP_SIGNATURE="invalid_signature",
            )
            response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_data, WEBHOOK_EVENT_SIGNATURE_ERROR_RESPONSE)


class TestConnectionList(APITestCase):
    """Tests for listing carrier connections (GET /v1/connections)."""

    def setUp(self):
        super().setUp()
        # Create a SystemConnection (admin-managed platform connection)
        self.system_connection = providers.SystemConnection.objects.create(
            carrier_code="usps",
            carrier_id="usps_system",
            test_mode=True,
            active=True,
            credentials=dict(
                client_id="system_client",
                client_secret="system_secret",
            ),
        )
        # Create a BrokeredConnection (user enablement of the system connection)
        self.brokered_connection = providers.BrokeredConnection.objects.create(
            system_connection=self.system_connection,
            is_enabled=True,
            created_by=self.user,
        )

    def test_list_connections(self):
        """Test GET /v1/connections returns user and system connections."""
        url = reverse("karrio.server.providers:carrier-connection-list")

        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response_data)
        carrier_ids = [c["carrier_id"] for c in response_data["results"]]
        self.assertIn("canadapost", carrier_ids)
        self.assertIn("ups_package", carrier_ids)
        self.assertIn("fedex_express", carrier_ids)
        self.assertIn("usps_system", carrier_ids)

    def test_list_connections_filter_by_carrier_name(self):
        """Test filtering connections by carrier_name."""
        url = reverse("karrio.server.providers:carrier-connection-list")

        response = self.client.get(f"{url}?carrier_name=canadapost")
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data["results"]), 1)
        self.assertEqual(response_data["results"][0]["carrier_name"], "canadapost")

    def test_list_connections_filter_by_active(self):
        """Test filtering connections by active status."""
        list_url = reverse("karrio.server.providers:carrier-connection-list")
        self.client.post(list_url, INACTIVE_CONNECTION_DATA, format="json")

        response = self.client.get(f"{list_url}?active=true")
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for connection in response_data["results"]:
            self.assertTrue(connection["active"])

    def test_credentials_are_write_only(self):
        """Test that credentials are write-only and never exposed in API responses.

        Note: Credentials can be created/updated via POST/PATCH but are never
        returned in GET responses for security reasons.
        """
        url = reverse("karrio.server.providers:carrier-connection-list")

        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that credentials are not returned for any connection type
        for connection in response_data["results"]:
            self.assertNotIn(
                "credentials",
                connection,
                f"Credentials should not be exposed for connection {connection.get('id')}",
            )


class TestConnectionCreate(APITestCase):
    """Tests for creating carrier connections (POST /v1/connections)."""

    def test_create_connection(self):
        """Test POST /v1/connections creates a new connection."""
        url = reverse("karrio.server.providers:carrier-connection-list")

        response = self.client.post(url, SENDLE_CONNECTION_DATA, format="json")
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, SENDLE_CONNECTION_RESPONSE)

    def test_create_connection_with_config(self):
        """Test creating connection with additional config."""
        url = reverse("karrio.server.providers:carrier-connection-list")

        response = self.client.post(
            url, SENDLE_CONNECTION_WITH_CONFIG_DATA, format="json"
        )
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response_data, SENDLE_CONNECTION_WITH_CONFIG_RESPONSE)

    def test_create_connection_invalid_carrier(self):
        """Test creating connection with invalid carrier name."""
        url = reverse("karrio.server.providers:carrier-connection-list")

        response = self.client.post(url, INVALID_CONNECTION_DATA, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestConnectionDetail(APITestCase):
    """Tests for retrieving, updating, and deleting carrier connections."""

    def test_retrieve_connection(self):
        """Test GET /v1/connections/{pk} retrieves connection details."""
        url = reverse(
            "karrio.server.providers:carrier-connection-details",
            kwargs=dict(pk=self.carrier.pk),
        )

        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["carrier_name"], "canadapost")
        self.assertEqual(response_data["carrier_id"], "canadapost")

    def test_update_connection(self):
        """Test PATCH /v1/connections/{pk} updates connection."""
        url = reverse(
            "karrio.server.providers:carrier-connection-details",
            kwargs=dict(pk=self.carrier.pk),
        )

        response = self.client.patch(url, CONNECTION_UPDATE_DATA, format="json")
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["carrier_id"], "canadapost_updated")
        self.assertFalse(response_data["active"])

    def test_update_connection_credentials(self):
        """Test updating connection credentials.

        Note: Credentials are write-only - they can be updated via PATCH
        but are not returned in the response. We verify the update by
        checking the database directly.
        """
        url = reverse(
            "karrio.server.providers:carrier-connection-details",
            kwargs=dict(pk=self.carrier.pk),
        )

        response = self.client.patch(url, CREDENTIALS_UPDATE_DATA, format="json")
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Credentials are write-only - verify they're not in response
        self.assertNotIn("credentials", response_data)

        # Verify credentials were actually updated in the database
        self.carrier.refresh_from_db()
        self.assertEqual(self.carrier.credentials["username"], "new_username")
        self.assertEqual(self.carrier.credentials["password"], "new_password")

    def test_delete_connection(self):
        """Test DELETE /v1/connections/{pk} removes connection."""
        list_url = reverse("karrio.server.providers:carrier-connection-list")
        create_response = self.client.post(
            list_url, SENDLE_TO_DELETE_DATA, format="json"
        )
        connection_pk = json.loads(create_response.content)["id"]

        url = reverse(
            "karrio.server.providers:carrier-connection-details",
            kwargs=dict(pk=connection_pk),
        )

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_can_delete_any_connection(self):
        """Test that superuser can delete any connection."""
        from django.contrib.auth import get_user_model

        other_user = get_user_model().objects.create_user(
            "other@example.com", "password456"
        )
        other_connection = providers.CarrierConnection.objects.create(
            carrier_code="sendle",
            carrier_id="other_user_sendle",
            test_mode=True,
            active=True,
            created_by=other_user,
            credentials=dict(sendle_id="test", api_key="test"),
        )
        url = reverse(
            "karrio.server.providers:carrier-connection-details",
            kwargs=dict(pk=other_connection.pk),
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            providers.CarrierConnection.objects.filter(pk=other_connection.pk).exists()
        )


class TestConnectionPagination(APITestCase):
    """Tests for connection list pagination."""

    def setUp(self):
        super().setUp()
        list_url = reverse("karrio.server.providers:carrier-connection-list")
        for i in range(25):
            self.client.post(
                list_url,
                {
                    "carrier_name": "sendle",
                    "carrier_id": f"sendle_paginated_{i}",
                    "credentials": {"sendle_id": f"test_{i}", "api_key": f"key_{i}"},
                },
                format="json",
            )

    def test_default_pagination(self):
        """Test that connections are paginated by default."""
        url = reverse("karrio.server.providers:carrier-connection-list")

        response = self.client.get(url)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response_data)
        self.assertIn("results", response_data)
        self.assertLessEqual(len(response_data["results"]), 20)

    def test_custom_limit(self):
        """Test custom pagination limit."""
        url = reverse("karrio.server.providers:carrier-connection-list")

        response = self.client.get(f"{url}?limit=5")
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data["results"]), 5)

    def test_pagination_offset(self):
        """Test pagination with offset."""
        url = reverse("karrio.server.providers:carrier-connection-list")

        response1 = self.client.get(f"{url}?limit=5")
        data1 = json.loads(response1.content)

        response2 = self.client.get(f"{url}?limit=5&offset=5")
        data2 = json.loads(response2.content)

        ids1 = {c["id"] for c in data1["results"]}
        ids2 = {c["id"] for c in data2["results"]}
        self.assertEqual(len(ids1.intersection(ids2)), 0)


if __name__ == "__main__":
    import unittest

    unittest.main()


# =============================================================================
# TEST FIXTURES
# =============================================================================

# OAuth Authorize
OAUTH_AUTHORIZE_DATA = {
    "state": "eyJjb25uZWN0aW9uX2lkIjogIjEyMyJ9",
    "options": {"scope": "read_accounts"},
    "frontend_url": "https://app.karrio.io/oauth/callback",
}

OAUTH_AUTHORIZE_RETURNED_VALUE = (
    OAuthAuthorizeRequest(
        carrier_name="teleship",
        authorization_url="https://api.teleship.com/oauth/authorize?clientId=test&redirectUri=https%3A%2F%2Fapi.karrio.io%2Fv1%2Fconnections%2Foauth%2Fteleship%2Fcallback&state=eyJjb25uZWN0aW9uX2lkIjogIjEyMyJ9",
        meta={"scope": "read_accounts"},
    ),
    [],
)

OAUTH_AUTHORIZE_RESPONSE = {
    "operation": "OAuth authorize",
    "request": {
        "carrier_name": "teleship",
        "authorization_url": "https://api.teleship.com/oauth/authorize?clientId=test&redirectUri=https%3A%2F%2Fapi.karrio.io%2Fv1%2Fconnections%2Foauth%2Fteleship%2Fcallback&state=eyJjb25uZWN0aW9uX2lkIjogIjEyMyJ9",
        "meta": {"scope": "read_accounts"},
    },
    "frontend_url": "https://app.karrio.io/oauth/callback",
    "messages": [],
}

OAUTH_AUTHORIZE_ERROR_RETURNED_VALUE = (
    OAuthAuthorizeRequest(
        carrier_name="teleship",
        authorization_url="",
        meta={},
    ),
    [
        Message(
            carrier_name="teleship",
            carrier_id="teleship",
            code="OAUTH_CONFIG_ERROR",
            message="OAuth not configured. Please set TELESHIP_OAUTH_CLIENT_ID environment variable.",
        )
    ],
)

OAUTH_AUTHORIZE_ERROR_RESPONSE = {
    "operation": "OAuth authorize",
    "request": {
        "carrier_name": "teleship",
        "meta": {},
    },
    "frontend_url": None,
    "messages": [
        {
            "carrier_name": "teleship",
            "carrier_id": "teleship",
            "code": "OAUTH_CONFIG_ERROR",
            "message": "OAuth not configured. Please set TELESHIP_OAUTH_CLIENT_ID environment variable.",
        }
    ],
}

# OAuth Callback
OAUTH_CALLBACK_RETURNED_VALUE = (
    {"client_id": "user_client_abc", "client_secret": "user_secret_xyz"},
    [],
)

OAUTH_CALLBACK_RESPONSE = {
    "type": "oauth_callback",
    "success": True,
    "carrier_name": "teleship",
    "credentials": {"client_id": "user_client_abc", "client_secret": "user_secret_xyz"},
    "state": "eyJjb25uZWN0aW9uX2lkIjogIjEyMyJ9",
    "messages": [],
}

OAUTH_CALLBACK_ERROR_RETURNED_VALUE = (
    None,
    [
        Message(
            carrier_name="teleship",
            carrier_id="teleship",
            code="OAUTH_CALLBACK_ERROR",
            message="Missing authorization code in callback",
        )
    ],
)

OAUTH_CALLBACK_ERROR_RESPONSE = {
    "type": "oauth_callback",
    "success": False,
    "carrier_name": "teleship",
    "credentials": None,
    "state": None,
    "messages": [
        {
            "carrier_name": "teleship",
            "carrier_id": "teleship",
            "code": "OAUTH_CALLBACK_ERROR",
            "message": "Missing authorization code in callback",
        }
    ],
}

# Teleship Connection Data
TELESHIP_CONNECTION_DATA = {
    "carrier_name": "teleship",
    "carrier_id": "teleship_connection",
    "credentials": {
        "client_id": "test_client",
        "client_secret": "test_secret",
    },
}

TELESHIP_CONNECTION_WITH_WEBHOOK_DATA = {
    "carrier_name": "teleship",
    "carrier_id": "teleship_connection",
    "credentials": {
        "client_id": "test_client",
        "client_secret": "test_secret",
    },
    "config": {
        "webhook_id": "WHK-12345",
        "webhook_secret": "whsec_abc123xyz789",
        "webhook_url": "https://api.karrio.io/v1/connections/webhook/test/events",
    },
}

# Webhook Register
WEBHOOK_REGISTER_DATA = {
    "webhook_url": "https://api.karrio.io/v1/connections/webhook/test/events",
    "description": "Karrio webhook for tracking updates",
}

WEBHOOK_REGISTER_RETURNED_VALUE = (
    WebhookRegistrationDetails(
        carrier_id="teleship_connection",
        carrier_name="teleship",
        webhook_identifier="WHK-12345",
        secret="whsec_abc123xyz789",
        meta={
            "url": "https://api.karrio.io/v1/connections/webhook/test/events",
            "enabledEvents": ["shipment.created", "shipment.updated"],
        },
    ),
    [],
)

WEBHOOK_REGISTER_RESPONSE = {
    "operation": "Webhook registration",
    "success": True,
    "carrier_name": "teleship",
    "carrier_id": "teleship_connection",
}

# Webhook Deregister
WEBHOOK_DEREGISTER_RETURNED_VALUE = (
    ConfirmationDetails(
        carrier_id="teleship_connection",
        carrier_name="teleship",
        success=True,
        operation="webhook_deregistration",
    ),
    [],
)

WEBHOOK_DEREGISTER_RESPONSE = {
    "operation": "Webhook deregistration",
    "success": True,
    "carrier_name": "teleship",
    "carrier_id": "teleship_connection",
}

# Webhook Disconnect
WEBHOOK_DISCONNECT_RESPONSE = {
    "operation": "Webhook disconnect",
    "success": True,
    "carrier_name": "teleship",
    "carrier_id": ANY,
}

# Webhook Event
WEBHOOK_EVENT_DATA = {
    "eventName": "shipment.updated",
    "objectType": "shipment",
    "objectId": "shp-12345",
    "data": {
        "trackingNumber": "TELESHIP12345678901",
        "shipmentId": "shp-12345",
        "events": [
            {
                "timestamp": "2025-01-17T14:30:00.000Z",
                "code": "IN_TRANSIT",
                "description": "Package in transit",
                "location": "Chicago, IL",
            }
        ],
    },
}


WEBHOOK_EVENT_NOT_FOUND_RESPONSE = {
    "operation": "Webhook event",
    "success": False,
    "messages": [
        {
            "message": "Connection not found: non-existent-pk",
        }
    ],
}


WEBHOOK_EVENT_SIGNATURE_ERROR_RESPONSE = {
    "operation": "Webhook event",
    "success": False,
    "carrier_name": "teleship",
    "carrier_id": "teleship_connection",
    "messages": [
        {
            "carrier_name": "teleship",
            "carrier_id": "teleship_connection",
            "code": "SIGNATURE_INVALID",
            "message": "Webhook signature verification failed",
        }
    ],
}

WEBHOOK_EVENT_SUCCESS_RESPONSE = {
    "operation": "Webhook event",
    "success": True,
}

# Connection CRUD
SENDLE_CONNECTION_DATA = {
    "carrier_name": "sendle",
    "carrier_id": "my_sendle_connection",
    "credentials": {
        "sendle_id": "test_sendle_id",
        "api_key": "test_api_key",
    },
}

SENDLE_CONNECTION_RESPONSE = {
    "id": ANY,
    "object_type": "carrier-connection",
    "carrier_name": "sendle",
    "display_name": "Sendle",
    "carrier_id": "my_sendle_connection",
    # Note: credentials are write-only and not returned in responses
    "config": {},
    "metadata": {},
    "active": True,
    "test_mode": True,
    "capabilities": ANY,
    "is_system": False,
}

SENDLE_CONNECTION_WITH_CONFIG_DATA = {
    "carrier_name": "sendle",
    "carrier_id": "sendle_with_config",
    "credentials": {
        "sendle_id": "test_sendle_id",
        "api_key": "test_api_key",
    },
    "config": {
        "shipping_options": ["signature_required"],
    },
}

SENDLE_CONNECTION_WITH_CONFIG_RESPONSE = {
    "id": ANY,
    "object_type": "carrier-connection",
    "carrier_name": "sendle",
    "display_name": "Sendle",
    "carrier_id": "sendle_with_config",
    # Note: credentials are write-only and not returned in responses
    "config": {
        "shipping_options": ["signature_required"],
    },
    "metadata": {},
    "active": True,
    "test_mode": True,
    "capabilities": ANY,
    "is_system": False,
}

INVALID_CONNECTION_DATA = {
    "carrier_name": "invalid_carrier",
    "carrier_id": "test",
    "credentials": {},
}

INACTIVE_CONNECTION_DATA = {
    "carrier_name": "purolator",
    "carrier_id": "purolator_inactive",
    "active": False,
    "credentials": {
        "username": "test",
        "password": "test",
        "account_number": "test",
        "user_token": "test",
    },
}

CONNECTION_UPDATE_DATA = {
    "carrier_id": "canadapost_updated",
    "active": False,
}

CREDENTIALS_UPDATE_DATA = {
    "credentials": {
        "username": "new_username",
        "customer_number": "2004381",
        "contract_id": "42708517",
        "password": "new_password",
    },
}

SENDLE_TO_DELETE_DATA = {
    "carrier_name": "sendle",
    "carrier_id": "sendle_to_delete",
    "credentials": {
        "sendle_id": "test",
        "api_key": "test",
    },
}
