"""Tests for ResourceAccessToken and /api/tokens endpoint."""

from unittest import mock
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from karrio.server.user.models import Token
from karrio.server.core.utils import ResourceAccessToken
from karrio.server.core.tests.base import APITestCase as KarrioAPITestCase


class TestResourceAccessTokenUnit(TestCase):
    """Unit tests for ResourceAccessToken class."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_create_token_for_single_resource(self):
        """Test creating a token for a single resource."""
        token = ResourceAccessToken.for_resource(
            user=self.user,
            resource_type="shipment",
            resource_ids=["shp_123"],
            access=["label"],
            format="pdf",
        )

        self.assertDictEqual(
            {
                "resource_type": token["resource_type"],
                "resource_ids": token["resource_ids"],
                "access": token["access"],
                "format": token["format"],
            },
            {
                "resource_type": "shipment",
                "resource_ids": ["shp_123"],
                "access": ["label"],
                "format": "pdf",
            },
        )

    def test_create_token_for_multiple_resources(self):
        """Test creating a token for multiple resources."""
        token = ResourceAccessToken.for_resource(
            user=self.user,
            resource_type="document",
            resource_ids=["shp_1", "shp_2", "shp_3"],
            access=["batch_labels"],
            format="pdf",
        )

        self.assertDictEqual(
            {
                "resource_type": token["resource_type"],
                "resource_ids": sorted(token["resource_ids"]),
                "access": token["access"],
            },
            {
                "resource_type": "document",
                "resource_ids": ["shp_1", "shp_2", "shp_3"],
                "access": ["batch_labels"],
            },
        )

    def test_decode_valid_token(self):
        """Test decoding a valid token."""
        token = ResourceAccessToken.for_resource(
            user=self.user,
            resource_type="manifest",
            resource_ids=["mnf_456"],
            access=["manifest"],
        )

        claims = ResourceAccessToken.decode(str(token))

        self.assertDictEqual(
            {
                "resource_type": claims["resource_type"],
                "resource_ids": claims["resource_ids"],
                "access": claims["access"],
            },
            {
                "resource_type": "manifest",
                "resource_ids": ["mnf_456"],
                "access": ["manifest"],
            },
        )

    def test_validate_access_success(self):
        """Test successful access validation."""
        token = ResourceAccessToken.for_resource(
            user=self.user,
            resource_type="shipment",
            resource_ids=["shp_123"],
            access=["label", "invoice"],
        )

        claims = ResourceAccessToken.validate_access(
            token_string=str(token),
            resource_type="shipment",
            resource_id="shp_123",
            access="label",
        )

        self.assertIsNotNone(claims)
        self.assertEqual(claims["resource_type"], "shipment")

    def test_validate_access_wrong_resource_type(self):
        """Test validation fails for wrong resource type."""
        token = ResourceAccessToken.for_resource(
            user=self.user,
            resource_type="shipment",
            resource_ids=["shp_123"],
            access=["label"],
        )

        with self.assertRaises(PermissionError) as context:
            ResourceAccessToken.validate_access(
                token_string=str(token),
                resource_type="manifest",
                resource_id="shp_123",
                access="label",
            )

        self.assertIn("resource type", str(context.exception).lower())

    def test_validate_access_wrong_resource_id(self):
        """Test validation fails for wrong resource ID."""
        token = ResourceAccessToken.for_resource(
            user=self.user,
            resource_type="shipment",
            resource_ids=["shp_123"],
            access=["label"],
        )

        with self.assertRaises(PermissionError) as context:
            ResourceAccessToken.validate_access(
                token_string=str(token),
                resource_type="shipment",
                resource_id="shp_999",
                access="label",
            )

        self.assertIn("resource", str(context.exception).lower())

    def test_validate_access_wrong_permission(self):
        """Test validation fails for wrong access permission."""
        token = ResourceAccessToken.for_resource(
            user=self.user,
            resource_type="shipment",
            resource_ids=["shp_123"],
            access=["label"],
        )

        with self.assertRaises(PermissionError) as context:
            ResourceAccessToken.validate_access(
                token_string=str(token),
                resource_type="shipment",
                resource_id="shp_123",
                access="invoice",
            )

        self.assertIn("access", str(context.exception).lower())

    def test_validate_batch_access_success(self):
        """Test successful batch access validation."""
        token = ResourceAccessToken.for_resource(
            user=self.user,
            resource_type="document",
            resource_ids=["shp_1", "shp_2", "shp_3"],
            access=["batch_labels"],
        )

        claims = ResourceAccessToken.validate_batch_access(
            token_string=str(token),
            resource_type="document",
            resource_ids=["shp_1", "shp_2"],
            access="batch_labels",
        )

        self.assertIsNotNone(claims)
        self.assertEqual(claims["resource_type"], "document")

    def test_validate_batch_access_missing_id(self):
        """Test batch validation fails when requesting ID not in token."""
        token = ResourceAccessToken.for_resource(
            user=self.user,
            resource_type="document",
            resource_ids=["shp_1", "shp_2"],
            access=["batch_labels"],
        )

        with self.assertRaises(PermissionError) as context:
            ResourceAccessToken.validate_batch_access(
                token_string=str(token),
                resource_type="document",
                resource_ids=["shp_1", "shp_2", "shp_3"],
                access="batch_labels",
            )

        self.assertIn("shp_3", str(context.exception))

    def test_token_with_org_id_and_test_mode(self):
        """Test token includes org_id and test_mode when provided."""
        token = ResourceAccessToken.for_resource(
            user=self.user,
            resource_type="shipment",
            resource_ids=["shp_123"],
            access=["label"],
            org_id="org_abc",
            test_mode=True,
        )

        claims = ResourceAccessToken.decode(str(token))

        self.assertDictEqual(
            {
                "org_id": claims["org_id"],
                "test_mode": claims["test_mode"],
            },
            {
                "org_id": "org_abc",
                "test_mode": True,
            },
        )


class TestResourceTokenAPI(APITestCase):
    """API tests for /api/tokens endpoint."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="api_test@example.com", password="testpass123"
        )
        self.token = Token.objects.create(user=self.user, test_mode=True)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_generate_shipment_label_token(self):
        """Test generating a token for shipment label access."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "shipment",
                "resource_ids": ["shp_123"],
                "access": ["label"],
                "format": "pdf",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            {
                "has_token": "token" in response.data,
                "has_expires_at": "expires_at" in response.data,
                "has_resource_urls": "resource_urls" in response.data,
                "has_shp_123_url": "shp_123" in response.data.get("resource_urls", {}),
            },
            {
                "has_token": True,
                "has_expires_at": True,
                "has_resource_urls": True,
                "has_shp_123_url": True,
            },
        )

    def test_generate_batch_labels_token(self):
        """Test generating a token for batch labels."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "document",
                "resource_ids": ["shp_1", "shp_2", "shp_3"],
                "access": ["batch_labels"],
                "format": "pdf",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("batch", response.data["resource_urls"])

    def test_generate_manifest_token(self):
        """Test generating a token for manifest access."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "manifest",
                "resource_ids": ["mnf_456"],
                "access": ["manifest"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("mnf_456", response.data["resource_urls"])

    def test_generate_template_token(self):
        """Test generating a token for template access."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "template",
                "resource_ids": ["tpl_789"],
                "access": ["render"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("tpl_789", response.data["resource_urls"])

    def test_unauthenticated_request_fails(self):
        """Test that unauthenticated requests are rejected."""
        self.client.credentials()
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "shipment",
                "resource_ids": ["shp_123"],
                "access": ["label"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_invalid_resource_type_fails(self):
        """Test that invalid resource type is rejected."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "invalid_type",
                "resource_ids": ["shp_123"],
                "access": ["label"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_access_type_fails(self):
        """Test that invalid access type is rejected."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "shipment",
                "resource_ids": ["shp_123"],
                "access": ["invalid_access"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_empty_resource_ids_fails(self):
        """Test that empty resource_ids is rejected."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "shipment",
                "resource_ids": [],
                "access": ["label"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_custom_expiration_success(self):
        """Test custom token expiration."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "shipment",
                "resource_ids": ["shp_123"],
                "access": ["label"],
                "expires_in": 600,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

    def test_response_has_no_cache_headers(self):
        """Test that token response includes cache prevention headers."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "shipment",
                "resource_ids": ["shp_123"],
                "access": ["label"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            {
                "cache_control": response.get("Cache-Control"),
                "cdn_cache_control": response.get("CDN-Cache-Control"),
            },
            {
                "cache_control": "no-store",
                "cdn_cache_control": "no-store",
            },
        )


class TestDocumentDownloadWithAPIToken(KarrioAPITestCase):
    """Test document download endpoints with API Token authentication.

    These tests verify that document download endpoints accept API Token
    authentication as an alternative to resource access tokens.
    """

    def setUp(self):
        super().setUp()
        from karrio.server.manager.models import Shipment, Manifest
        from karrio.server.core.utils import create_carrier_snapshot

        # Create test addresses (JSON data for embedded fields)
        self.shipper_data = {
            "id": "adr_shipper",
            "postal_code": "E1C4Z8",
            "city": "Moncton",
            "person_name": "John Doe",
            "country_code": "CA",
            "state_code": "NB",
            "address_line1": "125 Church St",
        }
        self.recipient_data = {
            "id": "adr_recipient",
            "postal_code": "V6M2V9",
            "city": "Vancouver",
            "person_name": "Jane Doe",
            "country_code": "CA",
            "state_code": "BC",
            "address_line1": "5840 Oak St",
        }

        # Create test parcel (JSON data for embedded field)
        self.parcel_data = {
            "id": "pcl_test",
            "weight": 1.0,
            "weight_unit": "KG",
        }

        # Create test shipment with label (using JSON fields)
        self.shipment = Shipment.objects.create(
            shipper=self.shipper_data,
            recipient=self.recipient_data,
            parcels=[self.parcel_data],
            created_by=self.user,
            test_mode=True,
            status="purchased",
            tracking_number="TEST123456",
            label="JVBERi0xLjQKMSAwIG9iago8PAovVGl0bGUgKP7/AFQAZQBzAHQpCj4+CmVuZG9iagoyIDAgb2JqCjw8Cj4+CmVuZG9iagozIDAgb2JqCjw8Cj4+CmVuZG9iagp4cmVmCjAgNAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTUgMDAwMDAgbiAKMDAwMDAwMDA2OCAwMDAwMCBuIAowMDAwMDAwMDg5IDAwMDAwIG4gCnRyYWlsZXIKPDwKL1NpemUgNAo+PgpzdGFydHhyZWYKMTEwCiUlRU9GCg==",  # Base64 encoded minimal PDF
            label_type="PDF",
        )

        # Create manifest address (JSON data for embedded field)
        self.manifest_address_data = {
            "id": "adr_manifest",
            "postal_code": "E1C4Z8",
            "city": "Moncton",
            "person_name": "Manifest Address",
            "country_code": "CA",
            "state_code": "NB",
            "address_line1": "125 Church St",
        }

        # Create test manifest with document (using JSON field)
        self.manifest = Manifest.objects.create(
            created_by=self.user,
            test_mode=True,
            address=self.manifest_address_data,
            manifest="JVBERi0xLjQKMSAwIG9iago8PAovVGl0bGUgKP7/AFQAZQBzAHQpCj4+CmVuZG9iagoyIDAgb2JqCjw8Cj4+CmVuZG9iagozIDAgb2JqCjw8Cj4+CmVuZG9iagp4cmVmCjAgNAowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTUgMDAwMDAgbiAKMDAwMDAwMDA2OCAwMDAwMCBuIAowMDAwMDAwMDg5IDAwMDAwIG4gCnRyYWlsZXIKPDwKL1NpemUgNAo+PgpzdGFydHhyZWYKMTEwCiUlRU9GCg==",  # Base64 encoded minimal PDF
            carrier=create_carrier_snapshot(self.carrier),
        )

    def test_shipment_label_download_with_api_token(self):
        """Test that shipment label can be downloaded with API Token auth."""
        # Request with API Token (no resource token needed)
        response = self.client.get(
            f"/v1/shipments/{self.shipment.pk}/label.pdf",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get("Content-Type", "").startswith("application/pdf"))

    def test_shipment_label_download_without_auth_fails(self):
        """Test that shipment label download fails without any authentication."""
        # Clear credentials
        self.client.credentials()

        response = self.client.get(
            f"/v1/shipments/{self.shipment.pk}/label.pdf",
        )

        self.assertEqual(response.status_code, 403)

    def test_shipment_label_download_with_resource_token(self):
        """Test that shipment label download still works with resource token."""
        # Clear API credentials
        self.client.credentials()

        # Generate resource token first (re-authenticate for this call)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        token_response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "shipment",
                "resource_ids": [self.shipment.pk],
                "access": ["label"],
                "format": "pdf",
            },
            format="json",
        )
        self.assertEqual(token_response.status_code, 201)
        resource_token = token_response.data["token"]

        # Clear credentials again and use resource token
        self.client.credentials()
        response = self.client.get(
            f"/v1/shipments/{self.shipment.pk}/label.pdf?token={resource_token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get("Content-Type", "").startswith("application/pdf"))

    def test_manifest_download_with_api_token(self):
        """Test that manifest document can be downloaded with API Token auth."""
        response = self.client.get(
            f"/v1/manifests/{self.manifest.pk}/manifest.pdf",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get("Content-Type", "").startswith("application/pdf"))

    def test_manifest_download_without_auth_fails(self):
        """Test that manifest download fails without any authentication."""
        self.client.credentials()

        response = self.client.get(
            f"/v1/manifests/{self.manifest.pk}/manifest.pdf",
        )

        self.assertEqual(response.status_code, 403)

    def test_manifest_download_with_resource_token(self):
        """Test that manifest download still works with resource token."""
        # Clear API credentials
        self.client.credentials()

        # Generate resource token first
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        token_response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "manifest",
                "resource_ids": [self.manifest.pk],
                "access": ["manifest"],
            },
            format="json",
        )
        self.assertEqual(token_response.status_code, 201)
        resource_token = token_response.data["token"]

        # Clear credentials and use resource token
        self.client.credentials()
        response = self.client.get(
            f"/v1/manifests/{self.manifest.pk}/manifest.pdf?token={resource_token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get("Content-Type", "").startswith("application/pdf"))

    def test_batch_labels_without_auth_fails(self):
        """Test that batch labels endpoint requires authentication."""
        # Clear credentials to test unauthenticated access
        self.client.credentials()

        response = self.client.get(
            f"/documents/shipments/label.pdf?shipments={self.shipment.pk}",
        )

        # Should return 403 (Forbidden) when no auth is provided
        self.assertEqual(response.status_code, 403)
