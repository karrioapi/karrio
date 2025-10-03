from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings

from karrio.server.graph.tests.base import GraphTestCase
import karrio.server.orgs.models as models


CREATE_ORGANIZATION_MUTATION = """
mutation CreateOrganization($data: CreateOrganizationMutationInput!) {
    create_organization(input: $data) {
        organization { id name is_active created modified token }
        errors { field messages }
    }
}
"""

UPDATE_ORGANIZATION_MUTATION = """
mutation UpdateOrganization($data: UpdateOrganizationMutationInput!) {
    update_organization(input: $data) {
        organization { id name }
        errors { field messages }
    }
}
"""

DELETE_ORGANIZATION_MUTATION = """
mutation DeleteOrganization($data: DeleteOrganizationMutationInput!) {
    delete_organization(input: $data) {
        organization { id name }
        errors { field messages }
    }
}
"""

SEND_ORGANIZATION_INVITES_MUTATION = """
mutation SendOrganizationInvites($data: SendOrganizationInvitesMutationInput!) {
    send_organization_invites(input: $data) {
        organization {
            id
            name
        }
        errors { field messages }
    }
}
"""

ACCEPT_ORGANIZATION_INVITATION_MUTATION = """
mutation AcceptOrganizationInvitation($data: AcceptOrganizationInvitationMutationInput!) {
    accept_organization_invitation(input: $data) {
        organization {
            id
            name
            current_user { email is_admin }
        }
        errors { field messages }
    }
}
"""

REMOVE_ORGANIZATION_MEMBER_MUTATION = """
mutation RemoveOrganizationMember($data: RemoveOrganizationMemberMutationInput!) {
    remove_organization_member(input: $data) {
        organization {
            id
            name
            members {
                email
                is_admin
                is_owner
            }
        }
        errors { field messages }
    }
}
"""

UPDATE_MEMBER_STATUS_MUTATION = """
mutation UpdateMemberStatus($data: UpdateMemberStatusMutationInput!) {
    update_member_status(input: $data) {
        organization {
            id
            name
            members {
                email
                is_admin
                is_owner
            }
        }
        errors { field messages }
    }
}
"""

RESEND_ORGANIZATION_INVITE_MUTATION = """
mutation ResendOrganizationInvite($data: ResendOrganizationInviteMutationInput!) {
    resend_organization_invite(input: $data) {
        invitation {
            id
            invitee_identifier
        }
        errors { field messages }
    }
}
"""


class TestOrganizationCreation(GraphTestCase):
    """Test organization creation functionality."""

    @override_settings(MULTI_ORGANIZATIONS=True)
    def test_create_organization_success(self):
        """Test successful organization creation."""
        response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "New Test Organization"}},
        )
        self.assertResponseNoErrors(response)

        organization = response.data["data"]["create_organization"]["organization"]
        self.assertEqual(organization["name"], "New Test Organization")
        self.assertTrue(organization["is_active"])
        self.assertIsNotNone(organization["created"])
        self.assertIsNotNone(organization["token"])
        self.assertIsNotNone(organization["id"])

    # @override_settings(ALLOW_MULTI_ACCOUNT=False)
    # def test_create_organization_multi_org_disabled(self):
    #     """Test organization creation when multi-org is disabled."""
    #     print(f"Before test_create_organization_multi_org_disabled")
    #     response = self.query(
    #         CREATE_ORGANIZATION_MUTATION,
    #         variables={
    #             "data": {
    #                 "name": "Should Fail"
    #             }
    #         }
    #     )
    #     print(f"Multi-org disabled response: {response.data}")
    #     # Should fail when multi-org is disabled
    #     self.assertTrue(len(response.data.get("errors", [])) > 0)


class TestOrganizationUpdate(GraphTestCase):
    """Test organization update functionality."""

    def setUp(self):
        super().setUp()
        # Create test organization using API
        org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Test Organization"}},
        )
        self.assertResponseNoErrors(org_response)
        self.organization = org_response.data["data"]["create_organization"][
            "organization"
        ]

    def test_update_organization_success(self):
        """Test successful organization update."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        response = self.query(
            UPDATE_ORGANIZATION_MUTATION,
            variables={
                "data": {
                    "id": self.organization["id"],
                    "name": "Updated Organization Name",
                }
            },
        )
        self.assertResponseNoErrors(response)

        updated_org = response.data["data"]["update_organization"]["organization"]
        self.assertEqual(updated_org["name"], "Updated Organization Name")
        self.assertEqual(updated_org["id"], self.organization["id"])

    def test_update_organization_unauthorized(self):
        """Test updating organization without proper permissions."""
        # Create another user and organization
        other_user = get_user_model().objects.create_user(
            email="other@example.com", password="test123"
        )
        other_user_jwt = self.getJWTToken(email="other@example.com", password="test123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {other_user_jwt}")

        # Create organization for other user
        other_org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Other User Org"}},
        )
        self.assertResponseNoErrors(other_org_response)
        other_organization = other_org_response.data["data"]["create_organization"][
            "organization"
        ]

        # Try to update original organization using other user's organization token
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {other_organization['token']}"
        )

        response = self.query(
            UPDATE_ORGANIZATION_MUTATION,
            variables={
                "data": {"id": self.organization["id"], "name": "Unauthorized Update"}
            },
        )
        # Should fail with permission error
        self.assertTrue(len(response.data.get("errors", [])) > 0)


class TestOrganizationDeletion(GraphTestCase):
    """Test organization deletion functionality."""

    def setUp(self):
        super().setUp()
        # Create test organization using API
        org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "To Delete Org"}},
        )
        self.assertResponseNoErrors(org_response)
        self.organization = org_response.data["data"]["create_organization"][
            "organization"
        ]

    def test_delete_organization_success(self):
        """Test successful organization deletion."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        response = self.query(
            DELETE_ORGANIZATION_MUTATION,
            variables={
                "data": {
                    "id": self.organization["id"],
                    "password": "test",
                }
            },
        )
        self.assertResponseNoErrors(response)

        deleted_org = response.data["data"]["delete_organization"]["organization"]
        self.assertEqual(deleted_org["id"], self.organization["id"])

    def test_delete_organization_wrong_password(self):
        """Test organization deletion with wrong password."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        response = self.query(
            DELETE_ORGANIZATION_MUTATION,
            variables={
                "data": {"id": self.organization["id"], "password": "wrong_password"}
            },
        )
        # Should fail with authentication error
        self.assertTrue(len(response.data.get("errors", [])) > 0)


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_FROM_ADDRESS="test@example.com",
    EMAIL_ENABLED=True,
)
class TestOrganizationInvitations(GraphTestCase):
    """Test organization invitation functionality."""

    def setUp(self):
        super().setUp()
        # Create test organization using API
        org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Invitation Org"}},
        )
        self.assertResponseNoErrors(org_response)
        self.organization = org_response.data["data"]["create_organization"][
            "organization"
        ]

    def test_send_organization_invites_success(self):
        """Test sending organization invitations."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        response = self.query(
            SEND_ORGANIZATION_INVITES_MUTATION,
            variables={
                "data": {
                    "org_id": self.organization["id"],
                    "emails": ["invite1@example.com", "invite2@example.com"],
                    "redirect_url": "http://example.com/accept",
                    "roles": ["member"],
                }
            },
        )
        self.assertResponseNoErrors(response)

        organization = response.data["data"]["send_organization_invites"][
            "organization"
        ]
        self.assertEqual(organization["name"], "Invitation Org")

        # Verify invitations were created by checking the database
        invitations = models.OrganizationInvitation.objects.filter(
            organization_id=organization["id"]
        )
        self.assertEqual(invitations.count(), 2)

        # Check that emails were sent
        self.assertEqual(len(mail.outbox), 2)


class TestOrganizationQueries(GraphTestCase):
    """Test organization query functionality."""

    def setUp(self):
        super().setUp()
        # Create test organization using API
        org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Query Test Org"}},
        )
        self.assertResponseNoErrors(org_response)
        self.organization = org_response.data["data"]["create_organization"][
            "organization"
        ]

    def test_query_organization_details(self):
        """Test querying organization details."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        response = self.query(
            """
            query GetOrganization($id: String!) {
                organization(id: $id) {
                    id
                    name
                    is_active
                    created
                    modified
                    current_user {
                        email
                        is_admin
                        is_owner
                    }
                    members {
                        email
                        is_admin
                        is_owner
                    }
                }
            }
            """,
            variables={"id": self.organization["id"]},
        )
        self.assertResponseNoErrors(response)

        org_data = response.data["data"]["organization"]
        self.assertEqual(org_data["id"], self.organization["id"])
        self.assertEqual(org_data["name"], "Query Test Org")
        self.assertIsNotNone(org_data["current_user"])
        self.assertTrue(len(org_data["members"]) >= 1)

    def test_query_organizations_list(self):
        """Test querying list of organizations."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        # Create additional organization using the same user
        second_org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Second Org"}},
        )
        self.assertResponseNoErrors(second_org_response)

        response = self.query(
            """
            query GetOrganizations {
                organizations {
                    edges {
                        node {
                            id
                            name
                            is_active
                            current_user {
                                email
                                is_admin
                                is_owner
                            }
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)

        organizations = response.data["data"]["organizations"]["edges"]
        self.assertTrue(len(organizations) >= 2)

        org_names = [org["node"]["name"] for org in organizations]
        self.assertIn("Query Test Org", org_names)
        self.assertIn("Second Org", org_names)


class TestOrganizationMemberManagement(GraphTestCase):
    """Test organization member management functionality."""

    def setUp(self):
        super().setUp()
        # Create test organization using API
        org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Member Management Org"}},
        )
        self.assertResponseNoErrors(org_response)
        self.organization = org_response.data["data"]["create_organization"][
            "organization"
        ]

        # Create additional test user to manage
        self.test_member = get_user_model().objects.create_user(
            email="member@example.com", password="test123"
        )

        # Add the test member to the organization using API approach
        org_obj = models.Organization.objects.get(id=self.organization["id"])
        org_obj.add_user(self.test_member)

        # Store string IDs for GraphQL
        self.test_member_id = str(self.test_member.id)
        self.owner_user_id = str(self.user.id)

    def test_remove_organization_member_success(self):
        """Test successful removal of organization member."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        response = self.query(
            REMOVE_ORGANIZATION_MEMBER_MUTATION,
            variables={
                "data": {
                    "org_id": self.organization["id"],
                    "user_id": self.test_member_id,
                }
            },
        )
        self.assertResponseNoErrors(response)

        organization = response.data["data"]["remove_organization_member"][
            "organization"
        ]
        self.assertEqual(organization["id"], self.organization["id"])

        # Verify member was removed from organization
        org_obj = models.Organization.objects.get(id=self.organization["id"])
        self.assertFalse(org_obj.users.filter(id=self.test_member.id).exists())

    def test_remove_organization_member_cannot_remove_owner(self):
        """Test that organization owner cannot be removed."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        # Try to remove the organization owner (the user who created it)
        response = self.query(
            REMOVE_ORGANIZATION_MEMBER_MUTATION,
            variables={
                "data": {
                    "org_id": self.organization["id"],
                    "user_id": self.owner_user_id,  # Owner user
                }
            },
        )
        # Should fail with validation error
        self.assertTrue(len(response.data.get("errors", [])) > 0)

    def test_remove_organization_member_cannot_remove_self(self):
        """Test that user cannot remove themselves."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        # Try to remove self
        response = self.query(
            REMOVE_ORGANIZATION_MEMBER_MUTATION,
            variables={
                "data": {
                    "org_id": self.organization["id"],
                    "user_id": self.owner_user_id,  # Self
                }
            },
        )
        # Should fail with validation error
        self.assertTrue(len(response.data.get("errors", [])) > 0)

    def test_update_member_status_suspend_success(self):
        """Test successful suspension of organization member."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        response = self.query(
            UPDATE_MEMBER_STATUS_MUTATION,
            variables={
                "data": {
                    "org_id": self.organization["id"],
                    "user_id": self.test_member_id,
                    "is_active": False,
                }
            },
        )
        self.assertResponseNoErrors(response)

        organization = response.data["data"]["update_member_status"]["organization"]
        self.assertEqual(organization["id"], self.organization["id"])

        # Verify member was suspended
        self.test_member.refresh_from_db()
        self.assertFalse(self.test_member.is_active)

    def test_update_member_status_activate_success(self):
        """Test successful activation of suspended organization member."""
        # First suspend the member
        self.test_member.is_active = False
        self.test_member.save()

        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        response = self.query(
            UPDATE_MEMBER_STATUS_MUTATION,
            variables={
                "data": {
                    "org_id": self.organization["id"],
                    "user_id": self.test_member_id,
                    "is_active": True,
                }
            },
        )
        self.assertResponseNoErrors(response)

        organization = response.data["data"]["update_member_status"]["organization"]
        self.assertEqual(organization["id"], self.organization["id"])

        # Verify member was activated
        self.test_member.refresh_from_db()
        self.assertTrue(self.test_member.is_active)

    def test_update_member_status_cannot_suspend_owner(self):
        """Test that organization owner cannot be suspended."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        # Try to suspend the organization owner
        response = self.query(
            UPDATE_MEMBER_STATUS_MUTATION,
            variables={
                "data": {
                    "org_id": self.organization["id"],
                    "user_id": self.owner_user_id,  # Owner user
                    "is_active": False,
                }
            },
        )
        # Should fail with validation error
        self.assertTrue(len(response.data.get("errors", [])) > 0)

    def test_update_member_status_cannot_suspend_self(self):
        """Test that user cannot suspend themselves."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        # Try to suspend self
        response = self.query(
            UPDATE_MEMBER_STATUS_MUTATION,
            variables={
                "data": {
                    "org_id": self.organization["id"],
                    "user_id": self.owner_user_id,  # Self
                    "is_active": False,
                }
            },
        )
        # Should fail with validation error
        self.assertTrue(len(response.data.get("errors", [])) > 0)


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    EMAIL_FROM_ADDRESS="test@example.com",
    EMAIL_ENABLED=True,
)
class TestOrganizationInvitationManagement(GraphTestCase):
    """Test organization invitation management functionality."""

    def setUp(self):
        super().setUp()
        # Create test organization using API
        org_response = self.query(
            CREATE_ORGANIZATION_MUTATION,
            variables={"data": {"name": "Invitation Management Org"}},
        )
        self.assertResponseNoErrors(org_response)
        self.organization = org_response.data["data"]["create_organization"][
            "organization"
        ]

        # Create test invitation using API approach
        org_obj = models.Organization.objects.get(id=self.organization["id"])
        self.invitation = models.OrganizationInvitation.objects.create(
            organization=org_obj,
            invitee_identifier="invitee@example.com",
            invited_by=self.user,
            roles=["member"],
        )

        # Store string ID for GraphQL
        self.invitation_id = str(self.invitation.id)

    def test_resend_organization_invite_success(self):
        """Test successful resending of organization invitation."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        response = self.query(
            RESEND_ORGANIZATION_INVITE_MUTATION,
            variables={
                "data": {
                    "invitation_id": self.invitation_id,
                    "redirect_url": "http://example.com/accept",
                }
            },
        )
        self.assertResponseNoErrors(response)

        invitation = response.data["data"]["resend_organization_invite"]["invitation"]
        self.assertEqual(invitation["id"], self.invitation_id)
        self.assertEqual(invitation["invitee_identifier"], "invitee@example.com")

    def test_resend_organization_invite_invalid_invitation(self):
        """Test resending invitation with invalid invitation ID."""
        # Use organization token for proper scoping
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.organization['token']}"
        )

        response = self.query(
            RESEND_ORGANIZATION_INVITE_MUTATION,
            variables={
                "data": {
                    "invitation_id": "invalid_id",
                    "redirect_url": "http://example.com/accept",
                }
            },
        )
        # Should fail with error
        self.assertTrue(len(response.data.get("errors", [])) > 0)
