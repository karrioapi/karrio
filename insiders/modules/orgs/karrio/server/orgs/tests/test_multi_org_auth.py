from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework.test import APIClient
from rest_framework import status

from karrio.server.graph.tests.base import GraphTestCase
from karrio.server.user.models import Token
import karrio.server.orgs.models as models
import karrio.server.providers.models as providers


CREATE_ORGANIZATION_MUTATION = """
mutation CreateOrganization($data: CreateOrganizationMutationInput!) {
    create_organization(input: $data) {
        organization { id name slug token }
        errors { field messages }
    }
}
"""

GET_ORGANIZATION_QUERY = """
query GetOrganization {
    organization { id name slug token }
}
"""

CREATE_CARRIER_CONNECTION_MUTATION = """
mutation CreateCarrierConnection($data: CreateCarrierConnectionMutationInput!) {
    create_carrier_connection(input: $data) {
        connection { id carrier_id carrier_name }
        errors { field messages }
    }
}
"""


class TestMultiOrgJWTAuthentication(GraphTestCase):
    """Test multi-organization authentication with organization-specific tokens."""

    def setUp(self):
        super().setUp()

        # Create first organization with default user
        org1_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Auth Org 1"}},
        )
        self.assertResponseNoErrors(org1_response)
        self.org1 = org1_response.data["data"]["create_organization"]["organization"]

        # Create second user and organization
        self.multi_org_user = get_user_model().objects.create_user(
            email="multiorg@example.com", password="test123", is_staff=True
        )
        user2_jwt = self.getJWTToken(email="multiorg@example.com", password="test123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_jwt}")

        org2_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Auth Org 2"}},
        )
        self.assertResponseNoErrors(org2_response)
        self.org2 = org2_response.data["data"]["create_organization"]["organization"]

        # Create third user and organization
        self.other_user = get_user_model().objects.create_user(
            email="other@example.com", password="test123", is_staff=True
        )
        user3_jwt = self.getJWTToken(email="other@example.com", password="test123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user3_jwt}")

        org3_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Auth Org 3"}},
        )
        self.assertResponseNoErrors(org3_response)
        self.org3 = org3_response.data["data"]["create_organization"]["organization"]

        # Reset to default user
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_organization_token_switching(self):
        """Test organization access using organization-specific tokens."""

        # Test access to org1 using its token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.org1['token']}")
        response = self.query(
            """
            query GetOrganization {
                organization {
                    id
                    name
                    current_user {
                        email
                        is_owner
                        is_admin
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        org_data = response.data["data"]["organization"]
        self.assertEqual(org_data["id"], self.org1["id"])
        self.assertEqual(org_data["name"], "Auth Org 1")
        self.assertTrue(
            org_data["current_user"]["is_owner"]
        )  # Owner since created by this user

        # Test access to org2 using its token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.org2['token']}")
        response = self.query(
            """
            query GetOrganization {
                organization {
                    id
                    name
                    current_user {
                        email
                        is_owner
                        is_admin
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        org_data = response.data["data"]["organization"]
        self.assertEqual(org_data["id"], self.org2["id"])
        self.assertEqual(org_data["name"], "Auth Org 2")
        self.assertTrue(
            org_data["current_user"]["is_owner"]
        )  # Owner since created by this user

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_invalid_token_authentication(self):
        """Test authentication with invalid token."""

        # Use an invalid token
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid_token_12345")

        response = self.query(
            """
            query GetOrganization {
                organization {
                    id
                    name
                }
            }
            """
        )

        # Should return authentication errors
        self.assertTrue(len(response.data.get("errors", [])) > 0)

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_organization_access_isolation(self):
        """Test that organizations can only access their own data using tokens."""

        # Access org1 using org1 token - should work
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.org1['token']}")
        response1 = self.query(
            """
            query GetOrganization {
                organization {
                    id
                    name
                }
            }
            """
        )
        self.assertResponseNoErrors(response1)
        org_data = response1.data["data"]["organization"]
        self.assertEqual(org_data["id"], self.org1["id"])
        self.assertEqual(org_data["name"], "Auth Org 1")

        # Access org3 using org3 token - should work
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.org3['token']}")
        response3 = self.query(
            """
            query GetOrganization {
                organization {
                    id
                    name
                }
            }
            """
        )
        self.assertResponseNoErrors(response3)
        org_data = response3.data["data"]["organization"]
        self.assertEqual(org_data["id"], self.org3["id"])
        self.assertEqual(org_data["name"], "Auth Org 3")
        # Should NOT be the same as org1
        self.assertNotEqual(org_data["id"], self.org1["id"])

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_organizations_list_filtering(self):
        """Test that organizations list only shows user's organizations."""

        # Use org2 token (multi_org_user's organization)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.org2['token']}")

        response = self.query(
            """
            query GetOrganizations {
                organizations {
                    edges {
                        node {
                            id
                            name
                            current_user {
                                email
                                is_admin
                            }
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        orgs = response.data["data"]["organizations"]["edges"]

        # Should see org2 (owned by multi_org_user)
        org_ids = [org["node"]["id"] for org in orgs]
        self.assertIn(self.org2["id"], org_ids)
        # Should NOT see org3 (owned by different user)
        self.assertNotIn(self.org3["id"], org_ids)

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_organization_mutations_with_tokens(self):
        """Test organization mutations work correctly with organization tokens."""

        # Update org2 using org2 token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.org2['token']}")

        response = self.query(
            """
            mutation UpdateOrganization($data: UpdateOrganizationMutationInput!) {
                update_organization(input: $data) {
                    organization {
                        id
                        name
                    }
                    errors {
                        field
                        messages
                    }
                }
            }
            """,
            variables={"data": {"id": self.org2["id"], "name": "Updated Auth Org 2"}},
        )
        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data["data"]["update_organization"]["organization"]["name"],
            "Updated Auth Org 2",
        )

        # Verify database was updated
        updated_org = models.Organization.objects.get(id=self.org2["id"])
        self.assertEqual(updated_org.name, "Updated Auth Org 2")


class TestMultiOrgTokenAuthentication(GraphTestCase):
    """Test multi-organization authentication with API tokens."""

    def setUp(self):
        super().setUp()

        # Create organizations using API instead of direct model access
        # Create first organization with default user
        org1_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Alpha Org"}},
        )
        self.assertResponseNoErrors(org1_response)
        self.alpha_org = org1_response.data["data"]["create_organization"][
            "organization"
        ]
        self.alpha_token = Token.objects.get(key=self.alpha_org["token"])

        # Create second user and organization
        self.user2 = get_user_model().objects.create_user(
            email="user2@example.com", password="test"
        )
        user2_jwt = self.getJWTToken(email="user2@example.com", password="test")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_jwt}")

        org2_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Beta Org"}},
        )
        self.assertResponseNoErrors(org2_response)
        self.beta_org = org2_response.data["data"]["create_organization"][
            "organization"
        ]
        self.beta_token = Token.objects.get(key=self.beta_org["token"])

        # Create carriers for each org using API
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.alpha_token.key}")
        carrier_alpha_response = self.query(
            CREATE_CARRIER_CONNECTION_MUTATION,
            variables={
                "data": {
                    "carrier_name": "sendle",
                    "carrier_id": "alpha_carrier",
                    "credentials": {"sendle_id": "test_alpha", "api_key": "test_alpha"},
                }
            },
        )
        self.assertResponseNoErrors(carrier_alpha_response)
        self.alpha_carrier = carrier_alpha_response.data["data"][
            "create_carrier_connection"
        ]["connection"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.beta_token.key}")
        carrier_beta_response = self.query(
            CREATE_CARRIER_CONNECTION_MUTATION,
            variables={
                "data": {
                    "carrier_name": "canadapost",
                    "carrier_id": "beta_carrier",
                    "credentials": {
                        "username": "test_beta",
                        "password": "test_beta",
                        "customer_number": "test_beta",
                        "contract_id": "test_beta",
                    },
                }
            },
        )
        self.assertResponseNoErrors(carrier_beta_response)
        self.beta_carrier = carrier_beta_response.data["data"][
            "create_carrier_connection"
        ]["connection"]

        # Reset to default user
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_token_organization_scoping(self):
        """Test that tokens are properly scoped to organizations."""
        # Use alpha token
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.alpha_token.key)

        response = self.query(
            """
            query GetOrganization {
                organization {
                    id
                    name
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        org_data = response.data["data"]["organization"]

        # Should get alpha org
        self.assertEqual(org_data["id"], self.alpha_org["id"])
        self.assertEqual(org_data["name"], "Alpha Org")

        # Switch to beta token
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.beta_token.key)

        response = self.query(
            """
            query GetOrganization {
                organization {
                    id
                    name
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        org_data = response.data["data"]["organization"]

        # Should get beta org
        self.assertEqual(org_data["id"], self.beta_org["id"])
        self.assertEqual(org_data["name"], "Beta Org")

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_token_cross_org_isolation(self):
        """Test that tokens cannot access other organizations' data."""

        # Use alpha token to query carriers
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.alpha_token.key)

        response = self.query(
            """
            query GetCarrierConnections {
                carrier_connections {
                    edges {
                        node {
                            id
                            carrier_id
                            carrier_name
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        carriers = response.data["data"]["carrier_connections"]["edges"]
        carrier_ids = [edge["node"]["carrier_id"] for edge in carriers]

        # Should see alpha_carrier but not beta_carrier
        self.assertIn("alpha_carrier", carrier_ids)
        self.assertNotIn("beta_carrier", carrier_ids)

        # Now check beta org with beta token
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.beta_token.key)

        response = self.query(
            """
            query GetCarrierConnections {
                carrier_connections {
                    edges {
                        node {
                            id
                            carrier_id
                            carrier_name
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        carriers = response.data["data"]["carrier_connections"]["edges"]
        carrier_ids = [edge["node"]["carrier_id"] for edge in carriers]

        # Should see beta_carrier but not alpha_carrier
        self.assertIn("beta_carrier", carrier_ids)
        self.assertNotIn("alpha_carrier", carrier_ids)

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_token_with_org_header_ignored(self):
        """Test that x-org-id header is ignored when using organization-scoped tokens."""
        # Use alpha token but try to access beta org via header
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.alpha_token.key,
            HTTP_X_ORG_ID=self.beta_org["id"],  # This should be ignored
        )

        response = self.query(
            """
            query GetOrganization {
                organization {
                    id
                    name
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        org_data = response.data["data"]["organization"]

        # Should still get alpha org (token takes precedence over header)
        self.assertEqual(org_data["id"], self.alpha_org["id"])
        self.assertEqual(org_data["name"], "Alpha Org")
