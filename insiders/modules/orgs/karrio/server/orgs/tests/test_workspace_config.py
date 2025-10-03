import json
from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework import status

from karrio.server.graph.tests.base import GraphTestCase
from karrio.server.user.models import Token
import karrio.server.orgs.models as models


CREATE_ORGANIZATION_MUTATION = """
mutation CreateOrganization($data: CreateOrganizationMutationInput!) {
    create_organization(input: $data) {
        organization { id name slug token }
        errors { field messages }
    }
}
"""

UPDATE_WORKSPACE_CONFIG_MUTATION = """
mutation UpdateWorkspaceConfig($data: WorkspaceConfigMutationInput!) {
    update_workspace_config(input: $data) {
        workspace_config {
            object_type
            default_currency
            default_weight_unit
            default_dimension_unit
            insured_by_default
            federal_tax_id
            state_tax_id
            default_country_code
        }
        errors { field messages }
    }
}
"""


class TestWorkspaceConfigOperations(GraphTestCase):
    """Test workspace configuration operations."""

    def setUp(self):
        super().setUp()
        # Create test organization using API
        org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Workspace Test Org"}},
        )
        self.assertResponseNoErrors(org_response)
        self.organization = org_response.data["data"]["create_organization"]["organization"]

    def test_query_workspace_config(self):
        """Test querying workspace configuration."""
        response = self.query(
            """
            query GetWorkspaceConfig {
                workspace_config {
                    object_type
                    default_currency
                    default_weight_unit
                    default_dimension_unit
                    insured_by_default
                }
            }
            """
        )
        self.assertResponseNoErrors(response)

        config_data = response.data["data"]["workspace_config"]
        if config_data:  # Config might be null initially
            self.assertIsNotNone(config_data["object_type"])
            self.assertIsInstance(config_data.get("default_currency"), (str, type(None)))

    def test_update_workspace_config_success(self):
        """Test successful workspace configuration update."""
        response = self.query(
            UPDATE_WORKSPACE_CONFIG_MUTATION,
            variables={
                "data": {
                    "default_currency": "USD",
                    "default_weight_unit": "LB",
                    "default_dimension_unit": "IN",
                    "insured_by_default": True
                }
            }
        )
        self.assertResponseNoErrors(response)

        config_data = response.data["data"]["update_workspace_config"]["workspace_config"]
        self.assertEqual(config_data["object_type"], "workspace-config")
        self.assertEqual(config_data["default_currency"], "USD")
        self.assertEqual(config_data["default_weight_unit"], "LB")
        self.assertEqual(config_data["default_dimension_unit"], "IN")
        self.assertEqual(config_data["insured_by_default"], True)

    def test_update_workspace_config_unauthorized(self):
        """Test workspace config update without authentication."""
        # Clear authentication
        self.client.credentials()

        response = self.query(
            UPDATE_WORKSPACE_CONFIG_MUTATION,
            variables={
                "data": {
                    "default_currency": "CAD"
                }
            }
        )
        # Should fail with authentication error
        self.assertTrue(len(response.data.get("errors", [])) > 0)


class TestWorkspaceConfigDataIsolation(GraphTestCase):
    """Test workspace configuration data isolation between organizations."""

    def setUp(self):
        super().setUp()
        # Create first organization
        org1_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Config Org 1"}},
        )
        self.assertResponseNoErrors(org1_response)
        self.org1 = org1_response.data["data"]["create_organization"]["organization"]

        # Create second user and organization
        self.user2 = get_user_model().objects.create_user(
            email="user2@example.com",
            password="test123"
        )
        self.token2 = Token.objects.create(user=self.user2, test_mode=False)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        org2_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Config Org 2"}},
        )
        self.assertResponseNoErrors(org2_response)
        self.org2 = org2_response.data["data"]["create_organization"]["organization"]

        # Switch back to first user
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_workspace_config_isolation_with_token(self):
        """Test that workspace configs are isolated between organizations using tokens."""
        # Set config for org1
        response1_update = self.query(
            UPDATE_WORKSPACE_CONFIG_MUTATION,
            variables={"data": {"default_currency": "USD", "insured_by_default": True}}
        )
        self.assertResponseNoErrors(response1_update)

        # Switch to org2 and set different config
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response2_update = self.query(
            UPDATE_WORKSPACE_CONFIG_MUTATION,
            variables={"data": {"default_currency": "CAD", "insured_by_default": False}}
        )
        self.assertResponseNoErrors(response2_update)

        # Verify org2 config
        response2 = self.query(
            """
            query GetWorkspaceConfig {
                workspace_config {
                    default_currency
                    insured_by_default
                }
            }
            """
        )
        self.assertResponseNoErrors(response2)
        if response2.data["data"]["workspace_config"]:
            self.assertEqual(response2.data["data"]["workspace_config"]["default_currency"], "CAD")
            self.assertEqual(response2.data["data"]["workspace_config"]["insured_by_default"], False)

        # Switch back to org1 and verify isolation
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response1 = self.query(
            """
            query GetWorkspaceConfig {
                workspace_config {
                    default_currency
                    insured_by_default
                }
            }
            """
        )
        self.assertResponseNoErrors(response1)
        if response1.data["data"]["workspace_config"]:
            self.assertEqual(response1.data["data"]["workspace_config"]["default_currency"], "USD")
            self.assertEqual(response1.data["data"]["workspace_config"]["insured_by_default"], True)

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_workspace_config_update_isolation(self):
        """Test that workspace config updates are isolated between organizations."""
        # Set initial config for org1
        initial_response = self.query(
            UPDATE_WORKSPACE_CONFIG_MUTATION,
            variables={"data": {"default_weight_unit": "KG", "default_dimension_unit": "CM"}}
        )
        self.assertResponseNoErrors(initial_response)

        # Update config for org1
        response = self.query(
            UPDATE_WORKSPACE_CONFIG_MUTATION,
            variables={"data": {"default_weight_unit": "LB", "default_dimension_unit": "IN"}}
        )
        self.assertResponseNoErrors(response)

        # Verify org2 doesn't see org1's config
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        response2 = self.query(
            """
            query GetWorkspaceConfig {
                workspace_config {
                    default_weight_unit
                    default_dimension_unit
                }
            }
            """
        )
        self.assertResponseNoErrors(response2)
        # Org2 should have empty/default config or null
        config2 = response2.data["data"]["workspace_config"]
        if config2:
            # Org2 should not have the same config as org1
            self.assertNotEqual(config2.get("default_weight_unit"), "LB")
            self.assertNotEqual(config2.get("default_dimension_unit"), "IN")


class TestWorkspaceConfigMultiOrgJWT(GraphTestCase):
    """Test workspace configuration with organization-specific tokens."""

    def setUp(self):
        super().setUp()
        # Create first organization with first user
        org1_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "JWT Org 1"}},
        )
        self.assertResponseNoErrors(org1_response)
        self.org1 = org1_response.data["data"]["create_organization"]["organization"]

        # Create second user and organization
        self.user2 = get_user_model().objects.create_user(
            email="user2jwt@example.com", password="test123"
        )
        user2_access_token = self.getJWTToken(email="user2jwt@example.com", password="test123")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_access_token}")
        org2_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "JWT Org 2"}},
        )
        self.assertResponseNoErrors(org2_response)
        self.org2 = org2_response.data["data"]["create_organization"]["organization"]

        # Switch back to first user
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_workspace_config_with_org_token(self):
        """Test workspace config operations with organization-specific token."""
        # Set config for org1 using organization token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.org1['token']}")

        response = self.query(
            UPDATE_WORKSPACE_CONFIG_MUTATION,
            variables={"data": {"default_country_code": "US", "state_tax_id": "12345"}}
        )
        self.assertResponseNoErrors(response)

        # Verify config was set for org1
        response = self.query(
            """
            query GetWorkspaceConfig {
                workspace_config {
                    default_country_code
                    state_tax_id
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        if response.data["data"]["workspace_config"]:
            self.assertEqual(response.data["data"]["workspace_config"]["default_country_code"], "US")
            self.assertEqual(response.data["data"]["workspace_config"]["state_tax_id"], "12345")

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_workspace_config_switch_organization(self):
        """Test switching between organizations using organization-specific tokens."""
        # Set config for org1 using its token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.org1['token']}")
        response1_update = self.query(
            UPDATE_WORKSPACE_CONFIG_MUTATION,
            variables={"data": {"federal_tax_id": "111111111"}}
        )
        self.assertResponseNoErrors(response1_update)

        # Switch to org2 using its token and set different config
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.org2['token']}")
        response2_update = self.query(
            UPDATE_WORKSPACE_CONFIG_MUTATION,
            variables={"data": {"federal_tax_id": "222222222"}}
        )
        self.assertResponseNoErrors(response2_update)

        # Verify org2 config
        response2 = self.query(
            """
            query GetWorkspaceConfig {
                workspace_config {
                    federal_tax_id
                }
            }
            """
        )
        self.assertResponseNoErrors(response2)
        if response2.data["data"]["workspace_config"]:
            self.assertEqual(response2.data["data"]["workspace_config"]["federal_tax_id"], "222222222")

        # Switch back to org1 using its token and verify different config
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.org1['token']}")
        response1 = self.query(
            """
            query GetWorkspaceConfig {
                workspace_config {
                    federal_tax_id
                }
            }
            """
        )
        self.assertResponseNoErrors(response1)
        if response1.data["data"]["workspace_config"]:
            self.assertEqual(response1.data["data"]["workspace_config"]["federal_tax_id"], "111111111")
