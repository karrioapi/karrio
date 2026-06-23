"""
Tests that the Django admin site enforces OTP verification.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django_otp import DEVICE_ID_SESSION_KEY
from django_otp.plugins.otp_email.models import EmailDevice
from two_factor.admin import AdminSiteOTPRequiredMixin

# Test settings override so admin's static-file references don't require a
# pre-built manifest. The default Whitenoise CompressedManifestStaticFilesStorage
# is not populated under `karrio test`.
TEST_STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


class TestAdminSiteMixin(TestCase):
    def test_admin_site_has_otp_mixin(self):
        # admin.site is a DefaultAdminSite LazyObject; isinstance proxies through.
        self.assertIsInstance(admin.site, AdminSiteOTPRequiredMixin)


@override_settings(STORAGES=TEST_STORAGES)
class TestAdminMFAGate(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.staff = User.objects.create_user(
            email="staff@example.com",
            password="t0pSecret!",
            is_staff=True,
            is_active=True,
        )
        cls.regular = User.objects.create_user(
            email="user@example.com",
            password="t0pSecret!",
            is_active=True,
        )
        cls.device = EmailDevice.objects.create(
            user=cls.staff,
            name="default",
            confirmed=True,
        )

    def setUp(self):
        self.maxDiff = None
        self.client = Client()

    def test_anonymous_redirects_to_login(self):
        response = self.client.get("/admin/", follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_non_staff_redirects_to_login(self):
        self.client.force_login(self.regular)
        response = self.client.get("/admin/", follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_staff_without_otp_verified_redirects(self):
        # force_login bypasses two_factor wizard — session has no OTP device key
        self.client.force_login(self.staff)
        response = self.client.get("/admin/", follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_staff_with_otp_verified_session_admitted(self):
        self.client.force_login(self.staff)
        # Simulate a completed OTP challenge by writing the device id to session
        session = self.client.session
        session[DEVICE_ID_SESSION_KEY] = self.device.persistent_id
        session.save()

        response = self.client.get("/admin/", follow=False)
        self.assertEqual(response.status_code, 200)

    def test_setup_wizard_reachable_when_authenticated(self):
        # `self.regular` has no OTP device, so the wizard is the right starting page.
        # `self.staff` already has a confirmed device — the wizard would redirect
        # them to setup_complete, which is correct stock library behavior we don't
        # need to assert.
        self.client.force_login(self.regular)
        response = self.client.get("/account/two_factor/setup/", follow=False)
        self.assertEqual(response.status_code, 200)

    def test_setup_wizard_requires_login(self):
        response = self.client.get("/account/two_factor/setup/", follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])
