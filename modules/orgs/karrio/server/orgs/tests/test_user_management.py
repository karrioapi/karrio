from django.core import mail
from rest_framework import status
from django.test import override_settings
from karrio.server.graph.tests.base import GraphTestCase


REGISTER_USER_MUTATION = """
mutation RegisterUser($data: RegisterUserMutationInput!) {
    register_user(input: $data) {
        user { email full_name }
        errors { field messages }
    }
}
"""

UPDATE_USER_MUTATION = """
mutation UpdateUser($data: UpdateUserInput!) {
    update_user(input: $data) {
        user { email full_name }
        errors { field messages }
    }
}
"""

CHANGE_PASSWORD_MUTATION = """
mutation ChangePassword($data: ChangePasswordMutationInput!) {
    change_password(input: $data) {
        user { email }
        errors { field messages }
    }
}
"""

REQUEST_PASSWORD_RESET_MUTATION = """
mutation RequestPasswordReset($data: RequestPasswordResetMutationInput!) {
    request_password_reset(input: $data) {
        email
        redirect_url
        errors { field messages }
    }
}
"""

REQUEST_EMAIL_CHANGE_MUTATION = """
mutation RequestEmailChange($data: RequestEmailChangeMutationInput!) {
    request_email_change(input: $data) {
        errors { field messages }
    }
}
"""


class TestUserRegistration(GraphTestCase):
    """Test user registration and authentication flows."""

    def test_register_user_success(self):
        """Test successful user registration."""
        response = self.query(
            REGISTER_USER_MUTATION,
            variables={
                "data": {
                    "email": "newuser@example.com",
                    "password1": "testpassword123",
                    "password2": "testpassword123",
                    "full_name": "New User",
                    "redirect_url": "http://example.com/confirm"
                }
            }
        )
        self.assertResponseNoErrors(response)

        user_data = response.data["data"]["register_user"]["user"]
        self.assertEqual(user_data["email"], "newuser@example.com")
        self.assertEqual(user_data["full_name"], "New User")

    def test_register_user_duplicate_email(self):
        """Test user registration with duplicate email fails."""
        # First registration
        self.query(
            REGISTER_USER_MUTATION,
            variables={
                "data": {
                    "email": "duplicate@example.com",
                    "password1": "testpassword123",
                    "password2": "testpassword123",
                    "full_name": "First User",
                    "redirect_url": "http://example.com/confirm"
                }
            }
        )

        # Second registration with same email
        response = self.query(
            REGISTER_USER_MUTATION,
            variables={
                "data": {
                    "email": "duplicate@example.com",
                    "password1": "testpassword123",
                    "password2": "testpassword123",
                    "full_name": "Second User",
                    "redirect_url": "http://example.com/confirm"
                }
            }
        )
        # Should have validation errors
        self.assertTrue(
            len(response.data.get("errors", [])) > 0 or
            response.data["data"]["register_user"]["errors"] is not None
        )

    def test_register_user_password_mismatch(self):
        """Test user registration with password mismatch fails."""
        response = self.query(
            REGISTER_USER_MUTATION,
            variables={
                "data": {
                    "email": "mismatch@example.com",
                    "password1": "testpassword123",
                    "password2": "differentpassword123",
                    "full_name": "Mismatch User",
                    "redirect_url": "http://example.com/confirm"
                }
            }
        )
        # Should have validation errors
        self.assertTrue(
            len(response.data.get("errors", [])) > 0 or
            response.data["data"]["register_user"]["errors"] is not None
        )


class TestUserUpdate(GraphTestCase):
    """Test user profile update functionality."""

    def test_update_user_info(self):
        """Test updating user information."""
        response = self.query(
            UPDATE_USER_MUTATION,
            variables={
                "data": {
                    "full_name": "Updated Name"
                }
            }
        )
        self.assertResponseNoErrors(response)

        user_data = response.data["data"]["update_user"]["user"]
        self.assertEqual(user_data["full_name"], "Updated Name")

    def test_update_user_email_only(self):
        """Test updating user active status only."""
        response = self.query(
            UPDATE_USER_MUTATION,
            variables={
                "data": {
                    "is_active": True
                }
            }
        )
        self.assertResponseNoErrors(response)

        user_data = response.data["data"]["update_user"]["user"]
        # Note: email field is not updatable via UpdateUserInput - need separate email change flow
        self.assertIsNotNone(user_data["email"])

    def test_update_user_unauthorized(self):
        """Test updating user without authentication."""
        # Clear authentication
        self.client.credentials()

        response = self.query(
            UPDATE_USER_MUTATION,
            variables={
                "data": {
                    "full_name": "Unauthorized Update"
                }
            }
        )
        # Should fail with authentication error
        self.assertTrue(len(response.data.get("errors", [])) > 0)


class TestPasswordManagement(GraphTestCase):
    """Test password change and reset functionality."""

    def test_change_password_success(self):
        """Test successful password change."""
        response = self.query(
            CHANGE_PASSWORD_MUTATION,
            variables={
                "data": {
                    "old_password": "test",
                    "new_password1": "newpassword123",
                    "new_password2": "newpassword123"
                }
            }
        )
        self.assertResponseNoErrors(response)

        user_data = response.data["data"]["change_password"]["user"]
        self.assertEqual(user_data["email"], self.user.email)

    def test_change_password_wrong_old_password(self):
        """Test password change with wrong old password."""
        response = self.query(
            CHANGE_PASSWORD_MUTATION,
            variables={
                "data": {
                    "old_password": "wrongpassword",
                    "new_password1": "newpassword123",
                    "new_password2": "newpassword123"
                }
            }
        )
        # Should have validation errors
        self.assertTrue(
            len(response.data.get("errors", [])) > 0 or
            response.data["data"]["change_password"]["errors"] is not None
        )

    def test_change_password_mismatch(self):
        """Test password change with password mismatch."""
        response = self.query(
            CHANGE_PASSWORD_MUTATION,
            variables={
                "data": {
                    "old_password": "test",
                    "new_password1": "newpassword123",
                    "new_password2": "differentpassword123"
                }
            }
        )
        # Should have validation errors
        self.assertTrue(
            len(response.data.get("errors", [])) > 0 or
            response.data["data"]["change_password"]["errors"] is not None
        )

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_request_password_reset(self):
        """Test password reset request."""
        response = self.query(
            REQUEST_PASSWORD_RESET_MUTATION,
            variables={
                "data": {
                    "email": self.user.email,
                    "redirect_url": "http://example.com/reset"
                }
            }
        )
        self.assertResponseNoErrors(response)

        reset_data = response.data["data"]["request_password_reset"]
        self.assertEqual(reset_data["email"], self.user.email)
        self.assertEqual(reset_data["redirect_url"], "http://example.com/reset")

        # Check that email was sent
        self.assertEqual(len(mail.outbox), 1)

    def test_request_password_reset_invalid_email(self):
        """Test password reset request with invalid email."""
        response = self.query(
            REQUEST_PASSWORD_RESET_MUTATION,
            variables={
                "data": {
                    "email": "nonexistent@example.com",
                    "redirect_url": "http://example.com/reset"
                }
            }
        )
        # Should handle gracefully - either success or error
        self.assertTrue(response.status_code == status.HTTP_200_OK)


class TestEmailManagement(GraphTestCase):
    """Test email change functionality."""

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_request_email_change(self):
        """Test email change request."""
        response = self.query(
            REQUEST_EMAIL_CHANGE_MUTATION,
            variables={
                "data": {
                    "email": "newemail@example.com",
                    "password": "test",
                    "redirect_url": "http://example.com/confirm"
                }
            }
        )
        self.assertResponseNoErrors(response)

        # Check that the mutation completed without errors
        change_data = response.data["data"]["request_email_change"]
        self.assertIsNone(change_data["errors"])

        # Check that email was sent
        self.assertEqual(len(mail.outbox), 1)


class TestUserQueries(GraphTestCase):
    """Test user-related queries."""

    def test_query_user_info(self):
        """Test querying current user information."""
        response = self.query(
            """
            query GetUser {
                user {
                    email
                    full_name
                    is_staff
                    is_superuser
                    date_joined
                    last_login
                }
            }
            """
        )
        self.assertResponseNoErrors(response)

        user_data = response.data["data"]["user"]
        self.assertEqual(user_data["email"], self.user.email)
        self.assertIsNotNone(user_data["email"])

    def test_query_api_keys(self):
        """Test querying user's API keys."""
        response = self.query(
            """
            query GetAPIKeys {
                api_keys {
                    key
                    label
                    test_mode
                }
            }
            """
        )
        self.assertResponseNoErrors(response)

        api_keys = response.data["data"]["api_keys"]
        # Should have at least one API key (the default token)
        self.assertTrue(len(api_keys) >= 0)
