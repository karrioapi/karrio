"""
Regression tests for #926: production ran with PASSWORD_HASHERS = [MD5] only,
so any password stored with a non-MD5 algorithm (PBKDF2, the Django default)
silently failed verification — it looked like "my password reset itself".

These drive the real login endpoint (POST /api/token) under the *production*
hasher list to prove:
  1. a PBKDF2-hashed account can authenticate (the lockout is gone), and
  2. a legacy MD5-hashed account authenticates AND is auto-upgraded to PBKDF2
     on that login (Django's transparent migration), so MD5 can be dropped
     later without stranding anyone.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

# Mirror of the production PASSWORD_HASHERS in settings/base.py: PBKDF2 preferred,
# MD5 retained only as a trailing fallback for the migration window.
PROD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# DRF throttling hits the cache on every /api/token request; locmem avoids the
# default Redis backend (unavailable in unit tests).
_TEST_SETTINGS = dict(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
)

PASSWORD = "correct-horse-battery-staple"


@override_settings(PASSWORD_HASHERS=PROD_HASHERS, **_TEST_SETTINGS)
class TestPasswordHasherLogin(APITestCase):
    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()
        self.url = reverse("jwt-obtain-pair")

    def _make_user(self, email: str, algorithm: str):
        User = get_user_model()
        user = User.objects.create_user(email=email, password="placeholder")
        # Force a specific stored hash, independent of the active preferred hasher.
        user.password = make_password(PASSWORD, hasher=algorithm)
        user.save(update_fields=["password"])
        return user

    def test_pbkdf2_account_can_log_in(self):
        """A pre-#926 PBKDF2 password verifies — would 401 under the old MD5-only config."""
        self._make_user("pbkdf2-user@example.com", "pbkdf2_sha256")

        response = self.client.post(self.url, {"email": "pbkdf2-user@example.com", "password": PASSWORD})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)

    def test_md5_account_logs_in_and_upgrades_to_pbkdf2(self):
        """A legacy MD5 password still verifies and is re-hashed as PBKDF2 on login."""
        user = self._make_user("md5-user@example.com", "md5")
        self.assertTrue(user.password.startswith("md5$"))

        response = self.client.post(self.url, {"email": "md5-user@example.com", "password": PASSWORD})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user.refresh_from_db()
        self.assertTrue(
            user.password.startswith("pbkdf2_"),
            f"expected auto-upgrade to pbkdf2, still {user.password.split('$')[0]}",
        )

    def test_wrong_password_is_rejected(self):
        self._make_user("pbkdf2-reject@example.com", "pbkdf2_sha256")

        response = self.client.post(self.url, {"email": "pbkdf2-reject@example.com", "password": "wrong"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
