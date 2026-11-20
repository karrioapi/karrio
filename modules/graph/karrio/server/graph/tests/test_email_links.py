import time
from django.core import mail
from django.test import override_settings
from django.contrib.auth import get_user_model

import karrio.server.core.links as links
import karrio.server.admin.forms as admin_forms
from karrio.server.graph.tests.base import GraphTestCase

User = get_user_model()
DASHBOARD = "https://dash.example.com"

RESET = """
    mutation reset($data: RequestPasswordResetMutationInput!) {
      request_password_reset(input: $data) { email }
    }
"""
REGISTER = """
    mutation register($data: RegisterUserMutationInput!) {
      register_user(input: $data) { user { email } }
    }
"""
EMAIL_CHANGE = """
    mutation change($data: RequestEmailChangeMutationInput!) {
      request_email_change(input: $data) { user { email } }
    }
"""

# Each of these must be refused although it mentions the allowed host.
CONFUSING_URLS = {
    "userinfo": "https://dash.example.com@evil.com/password/reset",
    "suffix host": "https://dash.example.com.evil.com/password/reset",
    "scheme relative": "//evil.com/password/reset",
    "backslash": "https://evil.com\\@dash.example.com/password/reset",
    "backslash authority": "https:\\\\evil.com/password/reset",
    "other port": "https://dash.example.com:8443/password/reset",
    "other scheme": "http://dash.example.com/password/reset",
    "javascript": "javascript:alert(1)//dash.example.com",
    "query": "https://dash.example.com/password/reset?next=https://evil.com",
    "fragment": "https://dash.example.com/password/reset#x",
    "whitespace": " https://dash.example.com/password/reset",
    "control character": "https://dash.example.com/password/reset\n",
    "other host": "https://evil.com/password/reset",
    "unclosed ipv6 bracket": "https://[dash.example.com/password/reset",
    "bracketed non-ip": "https://[not-ip]/password/reset",
    "fullwidth slash in authority": "https://dash.example.com\uff0fevil.com/password/reset",
}
# Spellings of the allowed origin that must still be accepted.
EQUIVALENT_URLS = [
    "HTTPS://DASH.Example.COM/password/reset",
    "https://dash.example.com:443/password/reset",
    "https://dash.example.com./password/reset",
]


def _wait_for_mail(count: int = 1, timeout: float = 2.0):
    """Sign-up confirmation mail is sent from a thread."""
    deadline = time.monotonic() + timeout
    while len(mail.outbox) < count and time.monotonic() < deadline:
        time.sleep(0.02)


class TestEmailLinkOrigins(GraphTestCase):
    """Password-reset, sign-up and email-change emails carry a one-time token.
    The page their link opens may be chosen by the client (redirect_url), but
    only on a frontend the operator configured; otherwise the token would be
    delivered to whoever the caller names."""

    def setUp(self):
        super().setUp()
        self.victim = User.objects.create_user(
            email="victim@example.com", password="OldPassword123!"
        )
        mail.outbox = []

    def _reset(self, **data):
        return self.query(
            RESET,
            operation_name="reset",
            variables={"data": {"email": self.victim.email, **data}},
        )

    def _refused(self, response, reason: str = "redirect_url"):
        self.assertIsNotNone(response.data.get("errors"), response.data)
        self.assertIn(reason, str(response.data["errors"]))
        self.assertEqual(mail.outbox, [])

    # Password reset ------------------------------------------------------

    @override_settings(DASHBOARD_URL=DASHBOARD)
    def test_reset_link_on_the_dashboard_is_sent(self):
        response = self._reset(redirect_url=f"{DASHBOARD}/password/reset")

        self.assertResponseNoErrors(response)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(f"{DASHBOARD}/password/reset?uidb64=", mail.outbox[0].body)

    @override_settings(DASHBOARD_URL=DASHBOARD)
    def test_reset_without_redirect_url_links_to_the_dashboard(self):
        response = self._reset()

        self.assertResponseNoErrors(response)
        self.assertIn(f"{DASHBOARD}/password/reset?uidb64=", mail.outbox[0].body)

    @override_settings(
        DASHBOARD_URL=DASHBOARD,
        EMAIL_LINK_ALLOWED_ORIGINS=["https://shop.example.org:8443"],
    )
    def test_reset_link_on_an_extra_allowed_origin_is_sent(self):
        response = self._reset(redirect_url="https://shop.example.org:8443/base/password/reset")

        self.assertResponseNoErrors(response)
        self.assertIn(
            "https://shop.example.org:8443/base/password/reset?uidb64=",
            mail.outbox[0].body,
        )

    @override_settings(DASHBOARD_URL=DASHBOARD)
    def test_reset_link_to_another_host_is_refused(self):
        for label, url in CONFUSING_URLS.items():
            with self.subTest(label):
                mail.outbox = []
                self._refused(self._reset(redirect_url=url))

    @override_settings(DASHBOARD_URL=DASHBOARD)
    def test_equivalent_spellings_of_the_dashboard_are_accepted(self):
        for url in EQUIVALENT_URLS:
            with self.subTest(url):
                mail.outbox = []
                response = self._reset(redirect_url=url)

                self.assertResponseNoErrors(response)
                self.assertIn(f"{DASHBOARD}/password/reset?uidb64=", mail.outbox[0].body)

    @override_settings(DASHBOARD_URL=None, EMAIL_LINK_ALLOWED_ORIGINS=[])
    def test_reset_is_refused_when_no_frontend_is_configured(self):
        for data in [dict(redirect_url=f"{DASHBOARD}/password/reset"), dict()]:
            with self.subTest(data):
                response = self._reset(**data)

                self._refused(response, reason="DASHBOARD_URL")

    def test_a_dashboard_url_with_query_or_fragment_is_not_used(self):
        """The email appends its own query/token to the base URL. Such a
        DASHBOARD_URL counts as not configured, with or without redirect_url:
        it must not authorise its origin either."""
        for dashboard in [f"{DASHBOARD}/?next=x", f"{DASHBOARD}/#x"]:
            for data in [dict(), dict(redirect_url=f"{DASHBOARD}/password/reset")]:
                with self.subTest(dashboard=dashboard, data=data), override_settings(
                    DASHBOARD_URL=dashboard, EMAIL_LINK_ALLOWED_ORIGINS=[]
                ):
                    mail.outbox = []
                    self._refused(self._reset(**data), reason="DASHBOARD_URL")

    def test_an_invalid_allowed_origin_entry_authorises_nothing(self):
        with override_settings(
            DASHBOARD_URL=None,
            EMAIL_LINK_ALLOWED_ORIGINS=["https://shop.example.org/?next=x"],
        ):
            self._refused(
                self._reset(redirect_url="https://shop.example.org/password/reset"),
                reason="DASHBOARD_URL",
            )

    @override_settings(DASHBOARD_URL=DASHBOARD, ALLOW_SIGNUP=True, EMAIL_ENABLED=True)
    def test_a_refusal_is_logged_once_as_a_warning(self):
        from unittest.mock import patch
        import karrio.server.graph.views as views
        import karrio.server.graph.schemas.base.mutations as mutations

        flows = {
            "reset": lambda: self._reset(redirect_url="https://evil.com/password/reset"),
            "signup": lambda: self._register("w@example.com", redirect_url="https://evil.com/email"),
            "email change": lambda: self._change(redirect_url="https://evil.com/email/change"),
        }
        for label, flow in flows.items():
            with self.subTest(label), patch.object(links.logger, "warning") as warning, patch.object(
                mutations.logger, "exception"
            ) as exception, patch.object(views.logger, "error") as error:
                self._refused(flow())

                warning.assert_called_once()
                exception.assert_not_called()
                error.assert_not_called()

        # The same, capturing every record (karrio logger and intercepted
        # standard logging): one warning, no stack trace, no email address.
        for label, flow in flows.items():
            records = []
            sink = links.logger.add(lambda m: records.append(m.record), level="WARNING")
            try:
                with self.subTest(f"{label} (all records)"):
                    self._refused(flow())
            finally:
                links.logger.remove(sink)

            self.assertEqual(
                [(r["level"].name, r["message"]) for r in records],
                [("WARNING", "Email link refused")],
                label,
            )
            self.assertIsNone(records[0]["exception"])
            self.assertNotIn("@example.com", str(records[0]))

    # Sign-up confirmation -------------------------------------------------

    def _register(self, email: str, **data):
        return self.query(
            REGISTER,
            operation_name="register",
            variables={
                "data": {
                    "email": email,
                    "password1": "TestPassword123!",
                    "password2": "TestPassword123!",
                    **data,
                }
            },
        )

    @override_settings(DASHBOARD_URL=DASHBOARD, ALLOW_SIGNUP=True, EMAIL_ENABLED=True)
    def test_signup_confirmation_links_to_the_dashboard(self):
        response = self._register("new@example.com", redirect_url=f"{DASHBOARD}/email")
        _wait_for_mail()

        self.assertResponseNoErrors(response)
        self.assertTrue(User.objects.filter(email="new@example.com").exists())
        self.assertIn(f"{DASHBOARD}/email/", mail.outbox[0].body)

    @override_settings(DASHBOARD_URL=DASHBOARD, ALLOW_SIGNUP=True, EMAIL_ENABLED=True)
    def test_signup_with_a_foreign_link_creates_nothing(self):
        response = self._register("squat@example.com", redirect_url="https://evil.com/email")
        _wait_for_mail()

        self._refused(response)
        self.assertFalse(User.objects.filter(email="squat@example.com").exists())

    @override_settings(DASHBOARD_URL=None, ALLOW_SIGNUP=True, EMAIL_ENABLED=False)
    def test_signup_without_email_needs_no_link(self):
        response = self._register("plain@example.com", redirect_url="https://evil.com/email")

        self.assertResponseNoErrors(response)
        self.assertTrue(User.objects.filter(email="plain@example.com").exists())
        self.assertEqual(mail.outbox, [])

    # Email change ---------------------------------------------------------

    def _change(self, **data):
        return self.query(
            EMAIL_CHANGE,
            operation_name="change",
            variables={"data": {"email": "next@example.com", "password": "test", **data}},
        )

    @override_settings(DASHBOARD_URL=DASHBOARD, EMAIL_ENABLED=True)
    def test_email_change_links_to_the_dashboard(self):
        response = self._change(redirect_url=f"{DASHBOARD}/email/change")

        self.assertResponseNoErrors(response)
        self.assertIn(f"{DASHBOARD}/email/change?token=", mail.outbox[0].body)

    @override_settings(DASHBOARD_URL=DASHBOARD, EMAIL_ENABLED=True)
    def test_email_change_with_a_foreign_link_is_refused(self):
        self._refused(self._change(redirect_url="https://evil.com/email/change"))

    # Admin-created user ---------------------------------------------------

    @override_settings(DASHBOARD_URL=DASHBOARD, EMAIL_ENABLED=True)
    def test_a_refused_admin_create_user_is_logged_once_without_pii(self):
        """Every log record emitted while the request runs is captured (the
        karrio logger and intercepted standard logging): exactly one warning,
        no error, no email address, no stack trace."""
        from django.urls import reverse
        from karrio.server.core.logging import logger

        records = []
        sink = logger.add(lambda message: records.append(message.record), level="WARNING")
        try:
            response = self.client.post(
                reverse("karrio.server.admin:admin-graph"),
                dict(
                    query="""
                        mutation create_user($input: CreateUserMutationInput!) {
                          create_user(input: $input) { user { email } }
                        }
                    """,
                    operation_name="create_user",
                    variables={
                        "input": {
                            "email": "pii-canary@example.com",
                            "password1": "TestPassword123!",
                            "password2": "TestPassword123!",
                            "redirect_url": "https://evil.com/email",
                        }
                    },
                ),
                format="json",
            )
        finally:
            logger.remove(sink)

        self.assertIn("redirect_url", response.content.decode())
        self.assertFalse(User.objects.filter(email="pii-canary@example.com").exists())
        self.assertEqual(
            [(r["level"].name, r["message"]) for r in records],
            [("WARNING", "Email link refused")],
        )
        self.assertIsNone(records[0]["exception"])
        self.assertNotIn("pii-canary", str(records[0]))

    @override_settings(DASHBOARD_URL=DASHBOARD, EMAIL_ENABLED=True)
    def test_admin_created_user_with_a_foreign_link_is_refused(self):
        data = dict(
            email="staffmade@example.com",
            password1="TestPassword123!",
            password2="TestPassword123!",
        )
        refused = admin_forms.CreateUserForm(dict(data, redirect_url="https://evil.com/email"))
        allowed = admin_forms.CreateUserForm(dict(data, redirect_url=f"{DASHBOARD}/email"))

        self.assertFalse(refused.is_valid())
        self.assertIn("redirect_url", refused.errors)
        self.assertTrue(allowed.is_valid(), allowed.errors)
        self.assertEqual(allowed.cleaned_data["redirect_url"], f"{DASHBOARD}/email")


class TestNormalizeOrigin(GraphTestCase):
    def test_origins(self):
        cases = {
            "https://Dash.Example.com/x": "https://dash.example.com",
            "https://dash.example.com:443": "https://dash.example.com",
            "http://dash.example.com:8080/": "http://dash.example.com:8080",
            "http://[::1]:3002/x": "http://[::1]:3002",
            "https://dash.example.com:99999": None,
            "https://user@dash.example.com": None,
            "dash.example.com/x": None,
            "": None,
            None: None,
        }
        for url, origin in cases.items():
            with self.subTest(url):
                self.assertEqual(links.normalize_origin(url), origin)
