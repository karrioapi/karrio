"""The carrier OAuth callback only redirects to a configured frontend, never
reflects markup into its result page, and is never cached or leaked by Referer.

The callback needs a signed-in browser (the carrier's redirect carries no
Authorization header, so it works with the dashboard's HttpOnly JWT cookie or a
session). A signed-in victim following a crafted link is the case tested here.
"""
import base64
import json
import re
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from django.test import Client, override_settings
from django.urls import reverse

from karrio.server.core.tests import APITestCase

BROWSER_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
DASHBOARD = "https://dashboard.example"
SHOP = "https://shop.example.org:8443"
CONFIGURED = dict(DASHBOARD_URL=DASHBOARD, EMAIL_LINK_ALLOWED_ORIGINS=[SHOP])
CREDS = dict(
    code="c0de",
    account_client_id="VICTIM_CLIENT_ID",
    account_client_secret="VICTIM_CLIENT_SECRET",
)
CREDENTIALS = dict(client_id="VICTIM_CLIENT_ID", client_secret="VICTIM_CLIENT_SECRET")
SCRIPT = "</script><script>window.__pwned=1</script>"


def state_of(frontend_url) -> str:
    return base64.b64encode(json.dumps(dict(frontend_url=frontend_url)).encode()).decode()


class OAuthCallbackCase(APITestCase):
    def url(self, **query):
        base = reverse(
            "karrio.server.providers:connection-oauth-callback",
            kwargs=dict(carrier_name="teleship"),
        )
        return base + ("?" + "&".join(f"{k}={v}" for k, v in query.items()) if query else "")

    def session_client(self):
        client = Client()
        client.force_login(self.user)
        return client

    def jwt_client(self):
        """A browser signed in the way the dashboard signs in (HttpOnly JWT cookie)."""
        client = Client()
        response = client.post(
            "/api/token",
            dict(email="admin@example.com", password="test"),
            content_type="application/json",
        )
        self.assertIn(response.status_code, (200, 201))
        self.assertTrue(client.cookies["karrio_access_token"]["httponly"])
        return client

    def get(self, client, state=None, accept=BROWSER_ACCEPT, extra=None, **headers):
        query = dict(CREDS, **(extra or {}))
        if state is not None:
            query["state"] = state
        return client.get(self.url(**query), HTTP_ACCEPT=accept, **headers)

    def result_json(self, response):
        """The result the page embeds, read back from its json_script element."""
        match = re.search(
            r'<script id="oauth-result" type="application/json">(.*?)</script>',
            response.content.decode(),
            re.S,
        )
        self.assertIsNotNone(match, "result page has no json_script element")
        return json.loads(match.group(1))


@override_settings(**CONFIGURED)
class TestOAuthCallbackRedirect(OAuthCallbackCase):
    def test_a_crafted_state_cannot_redirect_credentials_to_another_host(self):
        targets = [
            "https://attacker.example/collect",
            "http://attacker.example:8080/x",
            "//attacker.example/x",
            "https://dashboard.example@attacker.example/",  # userinfo trick
            "https://dashboard.example.attacker.example/",  # suffix trick
            "http://dashboard.example/oauth/callback",  # not the configured scheme
            "https://dashboard.example:8443/oauth/callback",  # not the configured port
            "javascript:alert(1)",
        ]
        for name, client in (("session", self.session_client()), ("jwt", self.jwt_client())):
            for target in targets:
                response = self.get(client, state_of(target))
                self.assertEqual(response.status_code, 200, (name, target))
                self.assertNotIn("Location", response, (name, target))
                self.assertNotIn("attacker", response.get("Location", ""), (name, target))
                # the escaped result page is rendered instead
                self.assertIn("providers/oauth_callback.html", [t.name for t in response.templates])
                self.assertEqual(self.result_json(response)["credentials"], CREDENTIALS)

    def test_a_missing_or_unparsable_frontend_renders_the_result_page(self):
        client = self.session_client()
        for state in (None, "not-base64!!", state_of(None), state_of(""), state_of(["x"])):
            response = self.get(client, state)
            self.assertEqual(response.status_code, 200, state)
            self.assertNotIn("Location", response, state)
            self.assertEqual(self.result_json(response)["success"], True)

    @override_settings(DASHBOARD_URL=None, EMAIL_LINK_ALLOWED_ORIGINS=[])
    def test_nothing_configured_means_no_redirect_at_all(self):
        response = self.get(self.session_client(), state_of("https://dashboard.example/cb"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Location", response)

    @override_settings(DASHBOARD_URL="https://dashboard.example/?next=x", EMAIL_LINK_ALLOWED_ORIGINS=[])
    def test_a_configured_value_with_a_query_authorises_nothing(self):
        response = self.get(self.session_client(), state_of("https://dashboard.example/cb"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Location", response)

    def test_a_configured_frontend_still_receives_the_result(self):
        for name, client in (("session", self.session_client()), ("jwt", self.jwt_client())):
            for frontend, origin in (
                (f"{DASHBOARD}/oauth/callback", DASHBOARD),
                (f"{DASHBOARD}:443/oauth/callback", DASHBOARD),  # default port is the same origin
                ("HTTPS://Dashboard.Example/oauth/callback", DASHBOARD),
                (f"{SHOP}/oauth/callback", SHOP),  # EMAIL_LINK_ALLOWED_ORIGINS
            ):
                response = self.get(client, state_of(frontend))
                self.assertEqual(response.status_code, 302, (name, frontend))
                location = urlsplit(response["Location"])
                self.assertEqual(
                    f"{location.scheme}://{location.netloc}{location.path}",
                    f"{origin}/oauth/callback",
                )
                result = json.loads(base64.b64decode(parse_qs(location.query)["oauth_result"][0]))
                self.assertEqual(result["success"], True)
                self.assertEqual(result["credentials"], CREDENTIALS)

    def test_a_frontend_with_a_query_or_fragment_is_not_redirected_to(self):
        for frontend in (f"{DASHBOARD}/cb?x=1", f"{DASHBOARD}/cb#frag"):
            response = self.get(self.session_client(), state_of(frontend))
            self.assertEqual(response.status_code, 200, frontend)
            self.assertNotIn("Location", response, frontend)

    def test_json_callers_still_get_the_result_as_json(self):
        response = self.get(
            self.session_client(), state_of("https://attacker.example/x"), accept="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["credentials"], CREDENTIALS)


@override_settings(**CONFIGURED)
class TestOAuthCallbackResultPage(OAuthCallbackCase):
    def test_markup_in_the_callback_is_not_reflected_into_the_script(self):
        client = self.session_client()
        for response in (
            self.get(client, extra=dict(account_client_id=SCRIPT)),
            self.get(client, state=SCRIPT),
            self.get(client, extra=dict(account_client_id=SCRIPT), state=state_of("https://attacker.example/")),
        ):
            body = response.content.decode()
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(SCRIPT, body)
            self.assertNotIn("<script>window.__pwned", body)
            # only the page's own two script blocks: the json data and the logic
            self.assertEqual(body.count("<script"), 2)
            self.assertEqual(body.count("</script>"), 2)
            self.assertNotIn("|safe", body)

        # the value survives, as data, through the json_script element
        response = self.get(client, extra=dict(account_client_id=SCRIPT))
        self.assertEqual(self.result_json(response)["credentials"]["client_id"], SCRIPT)
        self.assertIn("\\u003C/script\\u003E", response.content.decode())

    def test_an_error_message_is_escaped(self):
        response = self.get(self.session_client(), extra=dict(code="", account_client_id=""))
        body = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.result_json(response)["success"], False)
        self.assertEqual(body.count("<script"), 2)


@override_settings(**CONFIGURED)
class TestOAuthCallbackHeaders(OAuthCallbackCase):
    def assert_private(self, response, label):
        self.assertEqual(response["Cache-Control"], "no-store", label)
        self.assertEqual(response["Referrer-Policy"], "no-referrer", label)

    def test_every_response_of_the_callback_is_private(self):
        client = self.session_client()
        redirect = self.get(client, state_of(f"{DASHBOARD}/oauth/callback"))
        self.assertEqual(redirect.status_code, 302)
        page = self.get(client, state_of("https://attacker.example/"))
        self.assertEqual(page.status_code, 200)
        data = self.get(client, accept="application/json")
        self.assertEqual(data.status_code, 200)
        post = client.post(
            self.url(), dict(CREDS), content_type="application/json", HTTP_ACCEPT="application/json"
        )
        self.assertEqual(post.status_code, 200)

        for label, response in (("302", redirect), ("html", page), ("json", data), ("post", post)):
            self.assert_private(response, label)

    def test_a_refused_request_is_private_too(self):
        response = self.get(Client(), state_of(f"{DASHBOARD}/oauth/callback"))
        self.assertIn(response.status_code, (401, 403))
        self.assert_private(response, "unauthenticated")


@override_settings(**CONFIGURED)
class TestOAuthCallbackAuthentication(OAuthCallbackCase):
    def test_an_unauthenticated_call_is_still_refused(self):
        for state in (state_of(f"{DASHBOARD}/oauth/callback"), state_of("https://attacker.example/"), None):
            response = self.get(Client(), state)
            self.assertIn(response.status_code, (401, 403), state)
            self.assertNotIn("Location", response, state)
            self.assertNotIn("VICTIM_CLIENT_SECRET", response.content.decode())


@override_settings(**CONFIGURED)
class TestOAuthCallbackLogging(OAuthCallbackCase):
    def test_the_sdk_does_not_log_the_callback_payload(self):
        client = self.jwt_client()
        with patch("karrio.api.interface.logger") as log:
            self.get(
                client,
                state_of(f"{DASHBOARD}/oauth/callback"),
                HTTP_AUTHORIZATION="Bearer bearer-marker",
            )

        logged = repr(log.debug.call_args_list)
        self.assertIn("Processing OAuth callback", logged)
        self.assertIn("/v1/connections/oauth/teleship/callback", logged)  # the URL is still logged
        for leaked in ("VICTIM_CLIENT_SECRET", "VICTIM_CLIENT_ID", "karrio_access_token", "bearer-marker", "c0de"):
            self.assertNotIn(leaked, logged)
