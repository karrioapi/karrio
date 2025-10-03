from unittest.mock import patch, MagicMock
from karrio.server.graph.tests.base import GraphTestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserRegistration(GraphTestCase):
    
    @patch('karrio.server.conf.settings.ALLOW_SIGNUP', True)
    @patch('karrio.server.conf.settings.EMAIL_ENABLED', False)
    def test_register_user_mutation(self):
        """Test successful user registration"""
        # Ensure user doesn't exist
        User.objects.filter(email="newuser@example.com").delete()
        
        response = self.query(
            """
            mutation register_user($data: RegisterUserMutationInput!) {
              register_user(input: $data) {
                user {
                  email
                  full_name
                  is_active
                }
              }
            }
            """,
            operation_name="register_user",
            variables={
                "data": {
                    "email": "newuser@example.com",
                    "full_name": "New Test User",
                    "password1": "TestPassword123!",
                    "password2": "TestPassword123!",
                    "redirect_url": "http://localhost:3000/email"
                }
            }
        )
        
        self.assertResponseNoErrors(response)
        self.assertIsNotNone(response.data['data']['register_user']['user'])
        self.assertEqual(response.data['data']['register_user']['user']['email'], "newuser@example.com")
        self.assertEqual(response.data['data']['register_user']['user']['full_name'], "New Test User")
        
        # Verify user was created in database
        user = User.objects.get(email="newuser@example.com")
        self.assertEqual(user.full_name, "New Test User")
    
    @patch('karrio.server.conf.settings.ALLOW_SIGNUP', True)
    def test_register_user_password_mismatch(self):
        """Test registration fails with mismatched passwords"""
        response = self.query(
            """
            mutation register_user($data: RegisterUserMutationInput!) {
              register_user(input: $data) {
                user {
                  email
                }
              }
            }
            """,
            operation_name="register_user",
            variables={
                "data": {
                    "email": "mismatch@example.com",
                    "full_name": "Mismatch User",
                    "password1": "TestPassword123!",
                    "password2": "DifferentPassword123!",
                    "redirect_url": "http://localhost:3000/email"
                }
            }
        )
        
        # Should have errors
        self.assertIsNotNone(response.data.get('errors'))
        self.assertIn("password", str(response.data['errors'][0]))
    
    @patch('karrio.server.conf.settings.ALLOW_SIGNUP', True)
    def test_register_user_duplicate_email(self):
        """Test registration fails with duplicate email"""
        # First create a user
        User.objects.create_user(
            email="existing@example.com",
            password="ExistingPass123!",
            full_name="Existing User"
        )
        
        response = self.query(
            """
            mutation register_user($data: RegisterUserMutationInput!) {
              register_user(input: $data) {
                user {
                  email
                }
              }
            }
            """,
            operation_name="register_user",
            variables={
                "data": {
                    "email": "existing@example.com",
                    "full_name": "Duplicate User",
                    "password1": "TestPassword123!",
                    "password2": "TestPassword123!",
                    "redirect_url": "http://localhost:3000/email"
                }
            }
        )
        
        # Should have errors about duplicate email
        self.assertIsNotNone(response.data.get('errors'))
    
    @patch('karrio.server.conf.settings.ALLOW_SIGNUP', False)
    def test_register_user_signup_disabled(self):
        """Test registration fails when signup is disabled"""
        response = self.query(
            """
            mutation register_user($data: RegisterUserMutationInput!) {
              register_user(input: $data) {
                user {
                  email
                }
              }
            }
            """,
            operation_name="register_user",
            variables={
                "data": {
                    "email": "disabled@example.com",
                    "full_name": "Disabled User",
                    "password1": "TestPassword123!",
                    "password2": "TestPassword123!",
                    "redirect_url": "http://localhost:3000/email"
                }
            }
        )
        
        # Should have errors about signup not allowed
        self.assertIsNotNone(response.data.get('errors'))
        self.assertIn("Signup is not allowed", str(response.data['errors'][0]))


class TestPasswordReset(GraphTestCase):
    
    def setUp(self):
        super().setUp()
        # Create a test user for password reset
        self.reset_user = User.objects.create_user(
            email="resetuser@example.com",
            password="OldPassword123!",
            full_name="Reset User"
        )
    
    @patch('django.core.mail.send_mail')
    def test_request_password_reset(self, mock_send_mail):
        """Test requesting a password reset"""
        response = self.query(
            """
            mutation request_password_reset($data: RequestPasswordResetMutationInput!) {
              request_password_reset(input: $data) {
                email
                redirect_url
              }
            }
            """,
            operation_name="request_password_reset",
            variables={
                "data": {
                    "email": "resetuser@example.com",
                    "redirect_url": "http://localhost:3000/password/reset"
                }
            }
        )
        
        self.assertResponseNoErrors(response)
        self.assertEqual(response.data['data']['request_password_reset']['email'], "resetuser@example.com")


class TestEmailConfirmation(GraphTestCase):
    
    @patch('karrio.server.graph.schemas.base.mutations.email_verification.verify_token')
    def test_confirm_email(self, mock_verify):
        """Test email confirmation"""
        mock_verify.return_value = (True, None)
        
        response = self.query(
            """
            mutation confirm_email($data: ConfirmEmailMutationInput!) {
              confirm_email(input: $data) {
                success
              }
            }
            """,
            operation_name="confirm_email",
            variables={
                "data": {
                    "token": "test-confirmation-token"
                }
            }
        )
        
        self.assertResponseNoErrors(response)
        self.assertTrue(response.data['data']['confirm_email']['success'])
        mock_verify.assert_called_once_with("test-confirmation-token")