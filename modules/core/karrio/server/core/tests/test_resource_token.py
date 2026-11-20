"""Tests for ResourceAccessToken and /api/tokens endpoint."""

from unittest import mock
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from karrio.server.user.models import Token
from karrio.server.core.middleware import CreatorAccess
from karrio.server.core.utils import ResourceAccessToken
from karrio.server.core.tests.base import APITestCase as KarrioAPITestCase
from karrio.server.documents.models import DocumentTemplate
from karrio.server.manager.models import Manifest, Shipment
from karrio.server.orders.models import Order

MANIFEST_ADDRESS = {"postal_code": "10115", "city": "Berlin", "country_code": "DE", "address_line1": "Sample Str. 1"}


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
        # Tokens are only minted for resources the caller can see, so the ids are real rows.
        self.shipments = [
            Shipment.objects.create(created_by=self.user, test_mode=True, tracking_number=f"TRK{i}")
            for i in range(3)
        ]
        self.shipment = self.shipments[0]
        self.manifest = Manifest.objects.create(created_by=self.user, test_mode=True, address=MANIFEST_ADDRESS)
        self.template = DocumentTemplate.objects.create(
            name="tpl", slug="tpl", template="{{ x }}", related_object="shipment", created_by=self.user
        )

    def test_generate_shipment_label_token(self):
        """Test generating a token for shipment label access."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "shipment",
                "resource_ids": [self.shipment.id],
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
                "has_shp_123_url": self.shipment.id in response.data.get("resource_urls", {}),
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
                "resource_ids": [s.id for s in self.shipments],
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
                "resource_ids": [self.manifest.id],
                "access": ["manifest"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn(self.manifest.id, response.data["resource_urls"])

    def test_generate_template_token(self):
        """Test generating a token for template access."""
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "template",
                "resource_ids": [self.template.id],
                "access": ["render"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn(self.template.id, response.data["resource_urls"])

    def test_unauthenticated_request_fails(self):
        """Test that unauthenticated requests are rejected."""
        self.client.credentials()
        response = self.client.post(
            "/api/tokens",
            {
                "resource_type": "shipment",
                "resource_ids": [self.shipment.id],
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
                "resource_ids": [self.shipment.id],
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
                "resource_ids": [self.shipment.id],
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
                "resource_ids": [self.shipment.id],
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
                "resource_ids": [self.shipment.id],
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
            status="created",
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


class TestResourceTokenTenantScoping(APITestCase):
    """A token is only minted for resources the caller can see. The test default filter
    (`WideAccess`) filters nothing, so a per-owner filter is patched in."""

    def setUp(self):
        self.victim = get_user_model().objects.create_user(email="victim@example.com", password="test")
        self.intruder = get_user_model().objects.create_user(email="intruder@example.com", password="test")
        self.victim_rows = self._rows(self.victim)
        self.own_rows = self._rows(self.intruder)
        self.client = APIClient()
        self._authenticate(self.intruder)
        access = mock.patch("karrio.server.core.models.base.get_access_filter", CreatorAccess())
        access.start()
        self.addCleanup(access.stop)

    @staticmethod
    def _rows(user) -> dict:
        shipment = Shipment.objects.create(created_by=user, test_mode=True, tracking_number=f"TRK-{user.pk}")
        return {
            "shipment": shipment,
            "manifest": Manifest.objects.create(created_by=user, test_mode=True, address=MANIFEST_ADDRESS),
            "order": Order.objects.create(order_id=f"ORD-{user.pk}", test_mode=True, created_by=user),
            "template": DocumentTemplate.objects.create(
                name=f"t{user.pk}", slug=f"t{user.pk}", template="x", related_object="shipment", created_by=user
            ),
        }

    def _authenticate(self, user, test_mode: bool = True) -> None:
        token = Token.objects.create(user=user, test_mode=test_mode)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def _mint(self, resource_type: str, ids: list, access: list):
        return self.client.post(
            "/api/tokens",
            {"resource_type": resource_type, "resource_ids": ids, "access": access},
            format="json",
        )

    def _cases(self, rows: dict) -> list:
        return [
            ("shipment", rows["shipment"].id, "label"),
            ("shipment", rows["shipment"].id, "invoice"),
            ("manifest", rows["manifest"].id, "manifest"),
            ("order", rows["order"].id, "batch_labels"),
            ("order", rows["order"].id, "batch_invoices"),
            ("template", rows["template"].id, "render"),
            ("document", rows["shipment"].id, "batch_labels"),
            ("document", rows["shipment"].id, "batch_invoices"),
            ("document", rows["manifest"].id, "batch_manifests"),
        ]

    def test_another_tenants_resource_is_refused_for_every_type(self):
        for resource_type, resource_id, access in self._cases(self.victim_rows):
            with self.subTest(resource_type=resource_type, access=access):
                self.assertEqual(self._mint(resource_type, [resource_id], [access]).status_code, 404)

    def test_own_resources_are_minted_for_every_type(self):
        for resource_type, resource_id, access in self._cases(self.own_rows):
            with self.subTest(resource_type=resource_type, access=access):
                self.assertEqual(self._mint(resource_type, [resource_id], [access]).status_code, 201)

    def test_a_missing_id_answers_exactly_like_a_foreign_one(self):
        missing = self._mint("shipment", ["shp_does_not_exist"], ["label"])
        foreign = self._mint("shipment", [self.victim_rows["shipment"].id], ["label"])

        self.assertEqual((missing.status_code, missing.data), (foreign.status_code, foreign.data))
        self.assertEqual(foreign.status_code, 404)

    def test_one_foreign_id_among_own_ids_refuses_the_whole_token(self):
        response = self._mint(
            "document", [self.own_rows["shipment"].id, self.victim_rows["shipment"].id], ["batch_labels"]
        )

        self.assertEqual(response.status_code, 404)

    def test_a_live_mode_caller_cannot_mint_for_a_test_mode_row(self):
        self._authenticate(self.intruder, test_mode=False)

        response = self._mint("shipment", [self.own_rows["shipment"].id], ["label"])

        self.assertEqual(response.status_code, 404)

    def test_access_served_by_another_model_is_rejected(self):
        for resource_type, access in [
            ("document", ["batch_labels", "batch_manifests"]),
            ("shipment", ["manifest"]),
            ("manifest", ["label"]),
        ]:
            with self.subTest(resource_type=resource_type, access=access):
                response = self._mint(resource_type, [self.own_rows["shipment"].id], access)
                self.assertEqual(response.status_code, 400)
