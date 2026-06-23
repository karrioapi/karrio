"""Admin create_user mutation regression tests.

Covers the regression where admin create_user failed with
"Signup is not allowed" whenever the public ALLOW_SIGNUP setting
was False — the gate belongs at the tenant RegisterUserMutation,
not in the shared SignUpForm.
"""

from unittest.mock import patch

from django.contrib.auth import get_user_model
from karrio.server.admin.tests.base import AdminGraphTestCase

CREATE_USER_MUTATION = """
mutation create_user($data: CreateUserMutationInput!) {
  create_user(input: $data) {
    user {
      id
      email
      full_name
      is_staff
      is_active
      is_superuser
    }
    errors {
      field
      messages
    }
  }
}
"""


class TestAdminCreateUser(AdminGraphTestCase):
    @patch("karrio.server.conf.settings.ALLOW_SIGNUP", False)
    def test_create_staff_user_succeeds_when_public_signup_disabled(self):
        """Admin create_user must work even when ALLOW_SIGNUP is False.

        Regression: the SignUpForm.save() ALLOW_SIGNUP gate was inherited by
        the admin CreateUserForm and rejected staff creation. The gate now
        lives only at the tenant RegisterUserMutation layer.
        """
        result = self.query(
            CREATE_USER_MUTATION,
            operation_name="create_user",
            variables={
                "data": {
                    "email": "new-staff@example.com",
                    "full_name": "New Staff",
                    "password1": "TestPassword123!",
                    "password2": "TestPassword123!",
                    "is_staff": True,
                    "is_active": True,
                }
            },
        )

        self.assertResponseNoErrors(result)
        user = result.data["data"]["create_user"]["user"]
        self.assertEqual(user["email"], "new-staff@example.com")
        self.assertTrue(user["is_staff"])
        self.assertTrue(user["is_active"])

        created = get_user_model().objects.get(email="new-staff@example.com")
        self.assertTrue(created.is_staff)
        self.assertTrue(created.is_active)
