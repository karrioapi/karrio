"""
Test API Token and APIKey management with organization-specific functionality.
"""
from django.contrib.auth import get_user_model
import karrio.server.user.models as auth
from karrio.server.graph.tests.base import GraphTestCase
import karrio.server.iam.permissions as iam

CREATE_ORGANIZATION_MUTATION = """
mutation CreateOrganization($data: CreateOrganizationMutationInput!) {
    create_organization(input: $data) {
        organization { id name slug token }
        errors { field messages }
    }
}
"""

REGISTER_USER_MUTATION = """
mutation RegisterUser($data: RegisterUserMutationInput!) {
    register_user(input: $data) {
        user { id email full_name }
        errors { field messages }
    }
}
"""

MUTATE_TOKEN_MUTATION = """
mutation MutateToken($data: TokenMutationInput!) {
    mutate_token(input: $data) {
        token { key label test_mode }
        errors { field messages }
    }
}
"""

CREATE_API_KEY_MUTATION = """
mutation CreateAPIKey($data: CreateAPIKeyMutationInput!) {
    create_api_key(input: $data) {
        api_key { key label permissions }
        errors { field messages }
    }
}
"""

GET_ORGANIZATION_QUERY = """
query GetOrganization {
    organization {
        id
        token
    }
}
"""


class TestAPITokenManagement(GraphTestCase):
    """Test API token management functionality."""

    def setUp(self):

        super().setUp()
        # Create organization using API
        org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Test Organization"}},
        )
        self.assertResponseNoErrors(org_response)
        self.organization = org_response.data["data"]["create_organization"]["organization"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.organization['token']}")

    def test_query_api_keys_list(self):
        """Test querying API keys list."""
        # Create an API key first
        api_key_response = self.query(
            CREATE_API_KEY_MUTATION,
            variables={
                "data": {
                    "label": "Test API Key",
                    "password": "test"
                }
            }
        )
        self.assertResponseNoErrors(api_key_response)

        response = self.query(
            """
            query GetAPIKeys {
                api_keys {
                    key
                    label
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        api_keys = response.data["data"]["api_keys"]
        self.assertTrue(len(api_keys) >= 1)

    def test_mutate_token_retrieve_existing(self):
        """Test retrieving existing token."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.organization['token']}")
        response = self.query(
            MUTATE_TOKEN_MUTATION,
            variables={
                "data": {
                    "key": self.organization['token'],
                    "password": "test"
                }
            }
        )
        self.assertResponseNoErrors(response)
        token_data = response.data["data"]["mutate_token"]["token"]
        self.assertEqual(token_data["key"], self.organization['token'])

    def test_mutate_token_refresh_success(self):
        """Test successful token refresh."""
        response = self.query(
            MUTATE_TOKEN_MUTATION,
            variables={
                "data": {
                    "key": self.organization['token'],
                    "refresh": True,
                    "password": "test"
                }
            }
        )
        self.assertResponseNoErrors(response)
        token_data = response.data["data"]["mutate_token"]["token"]
        self.assertNotEqual(token_data["key"], self.organization['token'])

    def test_mutate_token_refresh_wrong_password(self):
        """Test token refresh with wrong password."""
        response = self.query(
            MUTATE_TOKEN_MUTATION,
            variables={
                "data": {
                    "key": self.organization['token'],
                    "refresh": True,
                    "password": "wrong_password"
                }
            }
        )
        self.assertTrue(len(response.data.get("errors", [])) > 0)


class TestAPIKeyManagement(GraphTestCase):
    """Test API key management functionality."""

    def setUp(self):
        iam.setup_groups()
        super().setUp()
        # Create organization using API
        org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Test Organization"}},
        )
        self.assertResponseNoErrors(org_response)
        self.organization = org_response.data["data"]["create_organization"]["organization"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.organization['token']}")

    def test_create_api_key_basic(self):
        """Test basic API key creation."""
        response = self.query(
            CREATE_API_KEY_MUTATION,
            variables={
                "data": {
                    "label": "Test API Key",
                    "password": "test"
                }
            }
        )
        self.assertResponseNoErrors(response)
        api_key = response.data["data"]["create_api_key"]["api_key"]
        self.assertEqual(api_key["label"], "Test API Key")

    def test_create_api_key_with_permissions(self):
        """Test API key creation with specific permissions."""
        response = self.query(
            CREATE_API_KEY_MUTATION,
            variables={
                "data": {
                    "label": "Limited API Key",
                    "password": "test",
                    "permissions": ["manage_carriers"]
                }
            }
        )
        self.assertResponseNoErrors(response)
        api_key = response.data["data"]["create_api_key"]["api_key"]
        self.assertEqual(api_key["label"], "Limited API Key")
        self.assertListEqual(api_key["permissions"], ["manage_carriers"])

    def test_create_api_key_wrong_password(self):
        """Test API key creation with wrong password."""
        response = self.query(
            CREATE_API_KEY_MUTATION,
            variables={
                "data": {
                    "label": "Test API Key",
                    "password": "wrong_password"
                }
            }
        )
        self.assertTrue(len(response.data.get("errors", [])) > 0)

    def test_delete_api_key_success(self):
        """Test successful API key deletion."""
        # First create an API key
        create_response = self.query(
            CREATE_API_KEY_MUTATION,
            variables={
                "data": {
                    "label": "To Delete",
                    "password": "test"
                }
            }
        )
        self.assertResponseNoErrors(create_response)
        api_key = create_response.data["data"]["create_api_key"]["api_key"]["key"]

        # Then delete it
        delete_response = self.query(
            """
            mutation DeleteAPIKey($data: DeleteAPIKeyMutationInput!) {
                delete_api_key(input: $data) {
                    errors { field messages }
                }
            }
            """,
            variables={
                "data": {
                    "key": api_key,
                    "password": "test"
                }
            }
        )
        self.assertResponseNoErrors(delete_response)


class TestOrganizationSpecificTokens(GraphTestCase):
    """Test organization-specific token behavior."""

    def setUp(self):
        super().setUp()
        # Create two organizations

        ## retrieve first default first organization
        org1_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Organization 1"}},
        )
        self.assertResponseNoErrors(org1_response)
        self.org1 = org1_response.data["data"]["create_organization"]["organization"]
        self.token1 = auth.Token.objects.get(key=self.org1['token'])

        # Create second user and organization
        self.user2 = get_user_model().objects.create_user(
            email="user2@example.com", password="test123"
        )
        user2_access_token = self.getJWTToken(email="user2@example.com", password="test123")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_access_token}")
        org2_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Organization 2"}},
        )
        self.assertResponseNoErrors(org2_response)
        self.org2 = org2_response.data["data"]["create_organization"]["organization"]
        self.token2 = auth.Token.objects.get(key=self.org2['token'])

        # Switch back to first user
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

    def test_token_retrieval_by_org_id(self):
        """Test token retrieval with organization context."""
        # Switch to second organization
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")
        response = self.query(
            """
            query GetOrganization {
                organization {
                    id
                    token
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        org_data = response.data["data"]["organization"]
        self.assertDictEqual(org_data, dict(
            id=self.org1["id"],
            token=self.token1.key,
        ))

    def test_api_keys_filtered_by_organization(self):
        """Test that API keys are filtered by organization."""
        response = self.query(
            """
            query GetAPIKeys {
                api_keys {
                    key
                    label
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        # Should only see API keys for current organization

    def test_token_isolation_between_organizations(self):
        """Test that tokens are isolated between organizations."""
        # Switch to second organization
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")

        response = self.query(
            """
            query GetOrganization {
                organization {
                    id
                    token
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        org_data = response.data["data"]["organization"]
        self.assertDictEqual(org_data, dict(
            id=self.org2["id"],
            token=self.token2.key,
        ))
