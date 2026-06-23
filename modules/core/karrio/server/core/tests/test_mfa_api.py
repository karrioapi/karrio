"""
Tests for /api/mfa/* TOTP enrollment endpoints (karrio.server.urls.mfa).

Login + OTP verification (/api/token, /api/token/verified) are covered
elsewhere; these tests focus on the four new enrollment views.
"""

import json
import unittest

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django_otp.oath import totp
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


def _generate_valid_token(device: TOTPDevice) -> str:
    """Compute the 6-digit code an authenticator app would currently show."""
    return f"{totp(device.bin_key, device.step, device.t0, device.digits):0{device.digits}d}"


def _auth_cookies(client: APIClient, user, *, is_verified: bool = True) -> None:
    """Mint a JWT pair for `user` and attach them as the JWTAuthentication cookies."""
    refresh = RefreshToken.for_user(user)
    refresh["is_verified"] = is_verified
    client.cookies["karrio_access_token"] = str(refresh.access_token)
    client.cookies["karrio_refresh_token"] = str(refresh)


# Test-only overrides:
#  • STORAGES: admin templates reference admin/css/base.css which Whitenoise's
#    manifest backend can't resolve without a built manifest.
#  • CACHES: DRF throttling hits the cache on every request; the default Redis
#    backend isn't available in unit tests.
_TEST_SETTINGS = dict(
    STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}},
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
)


@override_settings(**_TEST_SETTINGS)
class MFAAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.staff = User.objects.create_user(
            email="mfa-staff@example.com",
            password="x",
            is_staff=True,
        )
        cls.other = User.objects.create_user(
            email="mfa-other@example.com",
            password="x",
        )

    def setUp(self):
        self.maxDiff = None
        self.client = APIClient()


class TestMFAStatus(MFAAPITestCase):
    def test_unauthenticated_is_rejected(self):
        response = self.client.get(reverse("mfa-status"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_device_returns_false(self):
        _auth_cookies(self.client, self.staff)
        response = self.client.get(reverse("mfa-status"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            json.loads(response.content),
            {"enrolled": False, "confirmed": False},
        )

    def test_unconfirmed_device_reports_enrolled_not_confirmed(self):
        TOTPDevice.objects.create(user=self.staff, name="default", confirmed=False)
        _auth_cookies(self.client, self.staff)
        response = self.client.get(reverse("mfa-status"))
        self.assertDictEqual(
            json.loads(response.content),
            {"enrolled": True, "confirmed": False},
        )

    def test_confirmed_device_reports_both_true(self):
        TOTPDevice.objects.create(user=self.staff, name="default", confirmed=True)
        _auth_cookies(self.client, self.staff)
        response = self.client.get(reverse("mfa-status"))
        self.assertDictEqual(
            json.loads(response.content),
            {"enrolled": True, "confirmed": True},
        )

    def test_status_is_per_user(self):
        TOTPDevice.objects.create(user=self.other, name="default", confirmed=True)
        _auth_cookies(self.client, self.staff)
        response = self.client.get(reverse("mfa-status"))
        self.assertDictEqual(
            json.loads(response.content),
            {"enrolled": False, "confirmed": False},
        )


class TestTOTPInit(MFAAPITestCase):
    def test_unauthenticated_is_rejected(self):
        response = self.client.post(reverse("mfa-totp-init"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creates_unconfirmed_device_and_returns_uri(self):
        _auth_cookies(self.client, self.staff)
        response = self.client.post(reverse("mfa-totp-init"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = json.loads(response.content)
        self.assertIn("provisioning_uri", body)
        self.assertIn("secret", body)
        self.assertTrue(body["provisioning_uri"].startswith("otpauth://totp/"))
        self.assertEqual(TOTPDevice.objects.filter(user=self.staff, confirmed=False).count(), 1)

    def test_idempotent_for_pending_enrollment(self):
        _auth_cookies(self.client, self.staff)
        r1 = self.client.post(reverse("mfa-totp-init"))
        r2 = self.client.post(reverse("mfa-totp-init"))
        self.assertEqual(r1.status_code, status.HTTP_200_OK)
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        # Same device → same secret (no silent rotation)
        self.assertEqual(json.loads(r1.content)["secret"], json.loads(r2.content)["secret"])
        self.assertEqual(TOTPDevice.objects.filter(user=self.staff).count(), 1)

    def test_refuses_when_already_confirmed(self):
        TOTPDevice.objects.create(user=self.staff, name="default", confirmed=True)
        _auth_cookies(self.client, self.staff)
        response = self.client.post(reverse("mfa-totp-init"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("TOTP is already enrolled", json.dumps(response.json()))

    def test_recovers_from_duplicate_unconfirmed_devices(self):
        # Simulate a race or an aborted prior enrollment that left multiple
        # unconfirmed devices behind. Plain `get_or_create` would raise
        # MultipleObjectsReturned here; init must self-heal.
        TOTPDevice.objects.create(user=self.staff, name="old", confirmed=False)
        TOTPDevice.objects.create(user=self.staff, name="newer", confirmed=False)
        TOTPDevice.objects.create(user=self.staff, name="newest", confirmed=False)

        _auth_cookies(self.client, self.staff)
        response = self.client.post(reverse("mfa-totp-init"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("provisioning_uri", json.loads(response.content))
        # Exactly one unconfirmed device should remain.
        self.assertEqual(TOTPDevice.objects.filter(user=self.staff, confirmed=False).count(), 1)


class TestTOTPConfirm(MFAAPITestCase):
    def test_unauthenticated_is_rejected(self):
        response = self.client.post(
            reverse("mfa-totp-confirm"),
            {"otp_token": "123456"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_otp_token_is_400(self):
        _auth_cookies(self.client, self.staff)
        response = self.client.post(reverse("mfa-totp-confirm"), {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_pending_device_is_400(self):
        _auth_cookies(self.client, self.staff)
        response = self.client.post(
            reverse("mfa-totp-confirm"),
            {"otp_token": "123456"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No pending TOTP enrollment", json.dumps(response.json()))

    def test_invalid_otp_token_is_400(self):
        TOTPDevice.objects.create(user=self.staff, name="default", confirmed=False)
        _auth_cookies(self.client, self.staff)
        response = self.client.post(
            reverse("mfa-totp-confirm"),
            {"otp_token": "000000"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid or expired OTP token", json.dumps(response.json()))
        # Device stays unconfirmed
        self.assertFalse(TOTPDevice.objects.filter(user=self.staff, confirmed=True).exists())

    def test_valid_otp_token_marks_device_confirmed(self):
        device = TOTPDevice.objects.create(user=self.staff, name="default", confirmed=False)
        _auth_cookies(self.client, self.staff)
        valid_token = _generate_valid_token(device)
        response = self.client.post(
            reverse("mfa-totp-confirm"),
            {"otp_token": valid_token},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(json.loads(response.content), {"confirmed": True})
        device.refresh_from_db()
        self.assertTrue(device.confirmed)


class TestTOTPDisable(MFAAPITestCase):
    def test_unauthenticated_is_rejected(self):
        response = self.client.post(reverse("mfa-totp-disable"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unverified_session_is_rejected(self):
        # JWT carries is_verified=False — JWTAuthentication should reject before
        # the view runs.
        TOTPDevice.objects.create(user=self.staff, name="default", confirmed=True)
        _auth_cookies(self.client, self.staff, is_verified=False)
        response = self.client.post(reverse("mfa-totp-disable"), {"otp_token": "123456"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Device must survive
        self.assertTrue(TOTPDevice.objects.filter(user=self.staff, confirmed=True).exists())

    def test_missing_otp_token_is_400(self):
        # Step-up: an OTP-verified session alone is not sufficient — the body
        # must carry a fresh OTP code.
        TOTPDevice.objects.create(user=self.staff, name="default", confirmed=True)
        _auth_cookies(self.client, self.staff, is_verified=True)
        response = self.client.post(reverse("mfa-totp-disable"), {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Device must survive
        self.assertTrue(TOTPDevice.objects.filter(user=self.staff, confirmed=True).exists())

    def test_invalid_otp_token_is_400(self):
        TOTPDevice.objects.create(user=self.staff, name="default", confirmed=True)
        _auth_cookies(self.client, self.staff, is_verified=True)
        response = self.client.post(
            reverse("mfa-totp-disable"),
            {"otp_token": "000000"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid or expired OTP token", json.dumps(response.json()))
        # Device must survive
        self.assertTrue(TOTPDevice.objects.filter(user=self.staff, confirmed=True).exists())

    def test_no_confirmed_device_is_400(self):
        # Edge case: caller hits disable while only having an unconfirmed
        # device (shouldn't happen if /init/confirm flow is followed, but
        # defensive).
        TOTPDevice.objects.create(user=self.staff, name="default", confirmed=False)
        _auth_cookies(self.client, self.staff, is_verified=True)
        response = self.client.post(
            reverse("mfa-totp-disable"),
            {"otp_token": "123456"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No confirmed TOTP device to disable", json.dumps(response.json()))

    def test_valid_otp_token_deletes_all_devices(self):
        device = TOTPDevice.objects.create(user=self.staff, name="default", confirmed=True)
        TOTPDevice.objects.create(user=self.staff, name="extra", confirmed=False)
        _auth_cookies(self.client, self.staff, is_verified=True)
        valid_token = _generate_valid_token(device)
        response = self.client.post(
            reverse("mfa-totp-disable"),
            {"otp_token": valid_token},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(json.loads(response.content), {"disabled": True})
        # Wipes BOTH confirmed and unconfirmed devices for the user.
        self.assertFalse(TOTPDevice.objects.filter(user=self.staff).exists())

    def test_disable_is_per_user(self):
        # Other user's device must survive a successful disable on staff.
        other_device = TOTPDevice.objects.create(user=self.other, name="default", confirmed=True)
        staff_device = TOTPDevice.objects.create(user=self.staff, name="default", confirmed=True)
        _auth_cookies(self.client, self.staff, is_verified=True)
        self.client.post(
            reverse("mfa-totp-disable"),
            {"otp_token": _generate_valid_token(staff_device)},
            format="json",
        )
        self.assertTrue(TOTPDevice.objects.filter(pk=other_device.pk, confirmed=True).exists())


class TestTokenObtainPairExposesIsVerified(MFAAPITestCase):
    """`POST /api/token` must surface the is_verified flag in the response body."""

    def test_user_without_device_gets_is_verified_true(self):
        response = self.client.post(
            "/api/token",
            {"email": "mfa-staff@example.com", "password": "x"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = json.loads(response.content)
        self.assertIn("is_verified", body)
        self.assertTrue(body["is_verified"])

    def test_user_with_confirmed_device_gets_is_verified_false(self):
        TOTPDevice.objects.create(user=self.staff, name="default", confirmed=True)
        response = self.client.post(
            "/api/token",
            {"email": "mfa-staff@example.com", "password": "x"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = json.loads(response.content)
        self.assertFalse(body["is_verified"])


class TestF1JwtStaffMFABypass(MFAAPITestCase):
    """
    Tripwire for follow-up **F1** in ``PRDs/MFA_DJANGO_ADMIN.md``.

    Today, a staff user who has NOT yet enrolled an OTP device receives a JWT
    with ``is_verified=True`` from ``POST /api/token`` (see
    ``TokenObtainPairSerializer.get_token`` —
    ``token["is_verified"] = not default_device(user)``). The session-based
    ``/admin/`` gate doesn't catch this, so the staff user can call
    ``/admin/graphql`` and any other JWT-protected endpoint without ever
    completing MFA. The Django admin gate is therefore cosmetic for any JWT
    client until F1 lands.

    When F1 is implemented (enforce enrolled MFA for staff JWT issuance),
    the assertions below — written for the *desired* future state — will
    naturally start passing. ``unittest`` will then flag the test as an
    *unexpected success*, signalling that the ``@expectedFailure`` decorator
    can be removed in the same PR that closes F1.

    DO NOT delete this test class — it's the only code-level marker for F1.
    """

    @unittest.expectedFailure
    def test_staff_without_device_should_get_is_verified_false(self):
        """When F1 lands, staff users will be forced to enroll before
        getting a verified JWT — even on first login. Until then,
        ``is_verified=True`` is the buggy default."""
        response = self.client.post(
            "/api/token",
            {"email": "mfa-staff@example.com", "password": "x"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        body = json.loads(response.content)
        # Desired post-F1 behavior:
        self.assertFalse(
            body["is_verified"],
            "F1 follow-up not implemented yet — staff without MFA still get verified JWTs",
        )

    @unittest.expectedFailure
    def test_unverified_token_should_be_accepted_by_totp_init(self):
        """
        SPA-enrollment-path tripwire (couples to F1).

        Today F1's bug masks this: a staff user with no device gets
        ``is_verified=True``, so the JWT auth check at
        ``JWTAuthentication.authenticate`` (line 232-233) admits them and
        ``TOTPInitView`` runs.

        When F1 lands (unenrolled staff → ``is_verified=False``), the JWT
        auth check rejects unverified tokens with ``otp_not_verified`` BEFORE
        the view runs. First-time SPA enrollment would 401 — chicken-and-egg
        because the user can't enroll without first being verified.

        The F1 fix must therefore also relax the per-view auth on
        ``TOTPInitView`` / ``TOTPConfirmView`` to accept JWT-but-unverified
        tokens (the user is authenticated; they just haven't completed OTP
        yet, which is exactly what these endpoints exist to fix).

        This test pins the desired post-F1 behavior. Today it fails because
        ``JWTAuthentication`` blocks the unverified token at line 232-233.
        When F1 ships with the relaxed per-view auth, this test flips to
        passing and ``unittest`` flags it as an unexpected success.
        """
        # Mint an UNverified JWT pair, as a future post-F1 /api/token would.
        refresh = RefreshToken.for_user(self.staff)
        refresh["is_verified"] = False
        self.client.cookies["karrio_access_token"] = str(refresh.access_token)
        self.client.cookies["karrio_refresh_token"] = str(refresh)

        response = self.client.post(reverse("mfa-totp-init"))

        # Desired post-F1 behavior: init must accept unverified tokens.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
