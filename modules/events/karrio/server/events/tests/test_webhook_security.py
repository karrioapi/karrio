from unittest.mock import patch

from django.test import override_settings
from django.urls import reverse
from requests import Response
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from karrio.server.events.webhook_http import resolve_destination, post_webhook
from karrio.server.events.task_definitions.base.webhook import update_notified_webhooks

from karrio.server.core.tests import APITestCase
from karrio.server.graph.tests.base import GraphTestCase
from karrio.server.events.models import Webhook
from karrio.server.events.task_definitions.base.webhook import notify_subscribers


class TestWebhookDestinationSecurity(APITestCase):
    def test_private_destination_create(self):
        response = self.client.post(
            reverse("karrio.server.events:webhook-list"),
            dict(url="http://127.0.0.1/internal", enabled_events=["all"]),
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Webhook.objects.exists())

    def test_model_save_blocks_private_destination(self):
        with self.assertRaises(ValidationError):
            Webhook.objects.create(url="http://127.0.0.1/internal", test_mode=True)

    def test_legacy_private_destination_not_sent(self):
        hook = Webhook(url="http://169.254.169.254/latest", test_mode=True)
        response = Response()
        response.status_code = 200
        with patch("requests.post", return_value=response) as post:
            results = notify_subscribers([hook], {"event": "test"})
        post.assert_not_called()
        self.assertFalse(results[0][1].ok)

    @patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))])
    def test_owner_create_update_and_private_update(self, dns):
        url = reverse("karrio.server.events:webhook-list")
        response = self.client.post(
            url, dict(url="https://example.com/hook", enabled_events=["all"])
        )
        self.assertEqual(response.status_code, 201)
        hook = Webhook.objects.get()
        detail = reverse(
            "karrio.server.events:webhook-details", kwargs=dict(pk=hook.pk)
        )
        self.assertEqual(
            self.client.patch(detail, dict(url="https://example.com/new")).status_code,
            200,
        )
        dns.return_value = [(2, 1, 6, "", ("10.0.0.2", 80))]
        self.assertEqual(
            self.client.patch(
                detail, dict(url="http://internal.example/private")
            ).status_code,
            400,
        )
        hook.refresh_from_db()
        self.assertEqual(hook.url, "https://example.com/new")

    @patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))])
    def test_dns_change_at_delivery_updates_failure_counter(self, dns):
        hook = Webhook.objects.create(
            url="https://example.com/hook", test_mode=True, created_by=self.user
        )
        dns.return_value = [(2, 1, 6, "", ("127.0.0.1", 443))]
        with (
            patch("urllib3.HTTPSConnectionPool") as pool,
            patch("requests.post") as post,
        ):
            results = notify_subscribers([hook], {"event": "test"})
        pool.assert_not_called()
        post.assert_not_called()
        update_notified_webhooks([hook], results, timezone.now())
        hook.refresh_from_db()
        self.assertEqual(hook.failure_streak_count, 1)


class TestWebhookHTTP(SimpleTestCase):
    def test_blocked_addresses(self):
        for ip in [
            "127.0.0.1",
            "10.0.0.1",
            "172.16.0.1",
            "192.168.1.1",
            "169.254.169.254",
            "0.0.0.0",
            "224.0.0.1",
            "::1",
            "fe80::1",
            "fc00::1",
            "::ffff:127.0.0.1",
        ]:
            with (
                self.subTest(ip=ip),
                patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", (ip, 80))]),
            ):
                with self.assertRaises(ValidationError):
                    resolve_destination("http://example.com/hook")

    def test_mixed_dns_and_failure(self):
        for answers in [
            [],
            [(2, 1, 6, "", ("93.184.216.34", 80)), (2, 1, 6, "", ("10.1.1.1", 80))],
        ]:
            with (
                patch("socket.getaddrinfo", return_value=answers),
                self.assertRaises(ValidationError),
            ):
                resolve_destination("http://example.com")
        with (
            patch("socket.getaddrinfo", side_effect=OSError),
            self.assertRaises(ValidationError),
        ):
            resolve_destination("http://example.com")

    def test_invalid_urls(self):
        for url in [
            "file:///etc/passwd",
            "ftp://example.com",
            "http://user:secret@example.com",
            "http://example.com:bad",
            "http://example.com/#fragment",
            "http://example.com/\nfoo",
        ]:
            with self.subTest(url=url), self.assertRaises(ValidationError):
                resolve_destination(url)

    @override_settings(
        WEBHOOK_ALLOWED_DESTINATIONS=[
            "internal.example",
            "10.0.0.0/8",
            "0.0.0.0/0",
            "::/0",
        ]
    )
    def test_operator_exceptions_never_allow_metadata(self):
        with patch(
            "socket.getaddrinfo", return_value=[(2, 1, 6, "", ("10.1.1.1", 80))]
        ):
            self.assertEqual(
                resolve_destination("http://internal.example")[1], "10.1.1.1"
            )
        for ip in [
            "169.254.169.254",
            "fd00:ec2::254",
            "fd20:ce::254",
            "::ffff:169.254.169.254",
            "100.100.100.200",
        ]:
            with (
                patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", (ip, 80))]),
                self.assertRaises(ValidationError),
            ):
                resolve_destination("http://internal.example")

    @patch("requests.utils.get_environ_proxies", return_value={})
    @patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))])
    def test_direct_pins_ip_and_preserves_tls_hostname(self, dns, proxies):
        with patch("urllib3.HTTPSConnectionPool") as pool:
            pool.return_value.urlopen.return_value.status = 200
            result = post_webhook(
                "https://example.com:443/hook?q=1", {"event": "test"}, {}
            )
            self.assertTrue(result.ok)
            self.assertEqual(pool.call_args.args, ("93.184.216.34",))
            self.assertEqual(pool.call_args.kwargs["server_hostname"], "example.com")
            self.assertEqual(pool.call_args.kwargs["assert_hostname"], "example.com")
            kwargs = pool.return_value.urlopen.call_args.kwargs
            self.assertEqual(kwargs["headers"]["Host"], "example.com:443")
            self.assertFalse(kwargs["redirect"])
            self.assertFalse(kwargs["retries"])
            dns.assert_called_once()
            pool.return_value.urlopen.return_value.status = 302
            self.assertFalse(post_webhook("https://example.com", {}, {}).ok)

    @patch(
        "requests.utils.get_environ_proxies",
        return_value={"https": "http://proxy.example:8080"},
    )
    @patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))])
    def test_proxy_validated_and_redirects_disabled(self, dns, proxies):
        response = Response()
        response.status_code = 302
        response._content_consumed = True
        with patch("requests.post", return_value=response) as post:
            self.assertFalse(post_webhook("https://example.com", {}, {}).ok)
            self.assertFalse(post.call_args.kwargs["allow_redirects"])
            self.assertEqual(post.call_args.kwargs["timeout"], (5, 15))
            dns.return_value = [(2, 1, 6, "", ("127.0.0.1", 443))]
            with self.assertRaises(ValidationError):
                post_webhook("https://example.com", {}, {})
            post.assert_called_once()


class TestWebhookReviewRegressions(APITestCase):
    @patch(
        "requests.utils.get_environ_proxies",
        return_value={
            "http": "http://proxy.example:8080",
            "https": "http://proxy.example:8080",
        },
    )
    @patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 80))])
    def test_proxy_parser_differential_rejected_at_validation_and_send(
        self, dns, proxies
    ):
        for url in [
            "http://10.0.0.5\\x.attacker.test/hook",
            "https://169.254.169.254\\x.attacker.test/hook",
            "http://example.com/illegal|path",
            "http://example.com/illegal{path}",
            "http://example.com/%zz",
        ]:
            for action in [
                resolve_destination,
                lambda value: post_webhook(value, {}, {}),
            ]:
                with (
                    self.subTest(url=url, action=action),
                    patch("requests.post") as post,
                ):
                    post.return_value.status_code = 200
                    with self.assertRaises(ValidationError):
                        action(url)
                    post.assert_not_called()

    def test_ipv4_transition_ranges_blocked_in_literals_and_dns(self):
        for ip in ["64:ff9b::a00:5", "::a9fe:a9fe", "2002:0a00:0005::1"]:
            for host in [f"[{ip}]", "example.com"]:
                with (
                    self.subTest(ip=ip, host=host),
                    patch(
                        "socket.getaddrinfo", return_value=[(10, 1, 6, "", (ip, 80))]
                    ),
                    self.assertRaises(ValidationError),
                ):
                    resolve_destination(f"http://{host}/hook")

    @override_settings(WEBHOOK_ALLOWED_DESTINATIONS=["::/0", "0.0.0.0/0"])
    def test_ipv4_transition_ranges_cannot_override_metadata(self):
        with patch(
            "socket.getaddrinfo",
            return_value=[(10, 1, 6, "", ("64:ff9b::a9fe:a9fe", 80))],
        ):
            with self.assertRaises(ValidationError):
                resolve_destination("http://example.com")

    @patch("requests.utils.get_environ_proxies", return_value={})
    @patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))])
    def test_idna_host_and_sni_and_canonical_proxy_url(self, dns, proxies):
        with patch("urllib3.HTTPSConnectionPool") as pool:
            pool.return_value.urlopen.return_value.status = 200
            self.assertTrue(post_webhook("https://例え.test/hook", {}, {}).ok)
            self.assertEqual(
                pool.call_args.kwargs["server_hostname"], "xn--r8jz45g.test"
            )
            self.assertEqual(
                pool.call_args.kwargs["assert_hostname"], "xn--r8jz45g.test"
            )
            self.assertEqual(
                pool.return_value.urlopen.call_args.kwargs["headers"]["Host"],
                "xn--r8jz45g.test",
            )
            self.assertEqual(dns.call_args.args[0], "xn--r8jz45g.test")
        proxies.return_value = {"https": "http://proxy.example:8080"}
        response = Response()
        response.status_code = 200
        response._content_consumed = True
        with patch("requests.post", return_value=response) as post:
            post_webhook("https://bücher.test/hook", {}, {})
            self.assertEqual(post.call_args.args[0], "https://xn--bcher-kva.test/hook")

    @patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))])
    def test_delivery_value_error_is_per_webhook_and_records_failure(self, dns):
        hooks = [
            Webhook.objects.create(
                url="https://example.com", test_mode=True, created_by=self.user
            )
            for _ in range(2)
        ]
        response = Response()
        response.status_code = 200
        with (
            patch(
                "karrio.server.events.task_definitions.base.webhook.post_webhook",
                side_effect=[
                    UnicodeEncodeError("latin-1", "例", 0, 1, "unsupported"),
                    response,
                ],
            ),
            patch(
                "karrio.server.events.task_definitions.base.webhook.logger.warning"
            ) as warning,
        ):
            results = notify_subscribers(hooks, {})
            warning.assert_called_once_with(
                "Webhook delivery blocked or failed", webhook_id=hooks[0].id
            )
        self.assertEqual([result.status_code for _, result in results], [502, 200])
        update_notified_webhooks(hooks, results, timezone.now())
        for hook, expected in zip(hooks, [1, 0]):
            hook.refresh_from_db()
            self.assertEqual(hook.failure_streak_count, expected)

    @patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))])
    def test_legacy_url_and_dns_failure_allow_unrelated_edits(self, dns):
        hook = Webhook.objects.create(
            url="https://example.com", test_mode=True, created_by=self.user
        )
        Webhook.objects.filter(pk=hook.pk).update(url="http://169.254.169.254/latest")
        detail = reverse(
            "karrio.server.events:webhook-details", kwargs=dict(pk=hook.pk)
        )
        dns.side_effect = OSError("DNS unavailable")
        self.assertEqual(self.client.patch(detail, {"disabled": True}).status_code, 200)
        hook.refresh_from_db()
        self.assertTrue(hook.disabled)
        hook.description = "editable"
        hook.save()
        self.assertEqual(
            self.client.patch(detail, {"url": "https://changed.test"}).status_code, 400
        )
        hook.refresh_from_db()
        self.assertEqual(hook.url, "http://169.254.169.254/latest")

    @patch("socket.getaddrinfo", return_value=[(2, 1, 6, "", ("93.184.216.34", 443))])
    def test_dns_failure_between_serializer_validation_and_save_returns_400(self, dns):
        dns.side_effect = [
            [(2, 1, 6, "", ("93.184.216.34", 443))],
            OSError("DNS unavailable"),
        ]
        response = self.client.post(
            reverse("karrio.server.events:webhook-list"),
            dict(url="https://example.com", enabled_events=["all"]),
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Webhook.objects.exists())

    @override_settings(WEBHOOK_ALLOWED_DESTINATIONS=["xn--r8jz45g.test"])
    @patch("requests.utils.get_environ_proxies", return_value={})
    def test_idna_host_over_local_socket(self, proxies):
        import threading
        from http.server import BaseHTTPRequestHandler, HTTPServer

        received = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                received.append(self.headers["Host"])
                self.send_response(204)
                self.end_headers()

            def log_message(self, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            port = server.server_port
            with patch(
                "socket.getaddrinfo", return_value=[(2, 1, 6, "", ("127.0.0.1", port))]
            ):
                self.assertTrue(
                    post_webhook(f"http://例え.test:{port}/hook", {}, {}).ok
                )
            self.assertEqual(received, [f"xn--r8jz45g.test:{port}"])
        finally:
            server.shutdown()
            worker.join()
            server.server_close()


FULLWIDTH_PERCENT_URL = "http://y\uff05" + "40x.attacker.test/hook"
PUBLIC_DNS = [(2, 1, 6, "", ("93.184.216.34", 80))]


class TestWebhookHostCanonicalPolicy(APITestCase):
    """The host is validated after IDNA canonicalisation, not before."""

    @patch("socket.getaddrinfo", return_value=PUBLIC_DNS)
    def test_fullwidth_percent_host_refused_over_rest(self, dns):
        # IDNA folds U+FF05 into "%", which an earlier "%" check never saw.
        response = self.client.post(
            reverse("karrio.server.events:webhook-list"),
            dict(url=FULLWIDTH_PERCENT_URL, enabled_events=["all"]),
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Webhook.objects.exists())

    @patch("socket.getaddrinfo", return_value=PUBLIC_DNS)
    def test_fullwidth_percent_host_refused_over_update(self, dns):
        hook = Webhook.objects.create(
            url="https://example.com/hook", test_mode=True, created_by=self.user
        )
        detail = reverse(
            "karrio.server.events:webhook-details", kwargs=dict(pk=hook.pk)
        )
        response = self.client.patch(detail, dict(url=FULLWIDTH_PERCENT_URL))
        self.assertEqual(response.status_code, 400)
        hook.refresh_from_db()
        self.assertEqual(hook.url, "https://example.com/hook")

    @patch("socket.getaddrinfo", return_value=PUBLIC_DNS)
    def test_host_characters_after_canonicalisation(self, dns):
        for url in [
            FULLWIDTH_PERCENT_URL,
            "http://y%40x.attacker.test/hook",
            "http://under_score.test/hook",
            "http://exa$mple.test/hook",
            "http://exa!mple.test/hook",
            "http://" + "a" * 64 + ".test/hook",
            "http://" + ".".join(["a" * 63] * 3 + ["b" * 62]) + "/hook",  # 254
            "http://" + ".".join(["a" * 50] * 6) + "/hook",
            "http://a..test/hook",
            "http://.test/hook",
            "http://[fe80::1%25eth0]/hook",
        ]:
            with self.subTest(url=url), self.assertRaises(ValidationError):
                resolve_destination(url)

    @patch("socket.getaddrinfo", return_value=PUBLIC_DNS)
    def test_ordinary_hosts_still_accepted(self, dns):
        for url in [
            "http://example.com/hook",
            "https://a-b.example.com:8443/hook?x=1",
            "http://" + "a" * 63 + ".test/hook",
            "http://" + ".".join(["a" * 63] * 3 + ["b" * 61]) + "/hook",  # 253
            "http://EXAMPLE.com./hook",
            "https://例え.test/hook",
            "http://93.184.216.34/hook",
        ]:
            with self.subTest(url=url):
                self.assertEqual(resolve_destination(url)[1], "93.184.216.34")
        with patch("socket.getaddrinfo", return_value=[(10, 1, 6, "", ("2606:4700::1111", 80))]):
            self.assertEqual(
                resolve_destination("http://[2606:4700::1111]/hook")[1], "2606:4700::1111"
            )

    @patch(
        "requests.utils.get_environ_proxies",
        return_value={"http": "http://proxy.example:8080"},
    )
    def test_stored_fullwidth_percent_host_is_not_sent(self, proxies):
        # A row stored by the earlier release, which accepted the full-width sign.
        hook = Webhook(url=FULLWIDTH_PERCENT_URL, test_mode=True)
        response = Response()
        response.status_code = 200
        response._content_consumed = True
        with (
            patch("socket.getaddrinfo", return_value=PUBLIC_DNS),
            patch("requests.post", return_value=response) as post,
        ):
            results = notify_subscribers([hook], {"event": "test"})
        post.assert_not_called()
        self.assertEqual(results[0][1].status_code, 502)


class TestWebhookDeliveryIsolation(APITestCase):
    """One failing webhook never stops the others in the batch."""

    @patch("socket.getaddrinfo", return_value=PUBLIC_DNS)
    def make_hooks(self, dns, count=3):
        return [
            Webhook.objects.create(
                url=f"https://example.com/{i}", test_mode=True, created_by=self.user
            )
            for i in range(count)
        ]

    def test_unexpected_exception_is_a_counted_failed_delivery(self):
        hooks = self.make_hooks()
        ok = Response()
        ok.status_code = 200
        with (
            patch(
                "karrio.server.events.task_definitions.base.webhook.post_webhook",
                side_effect=[AssertionError("http.client rejected the host"), ok, ok],
            ),
            patch(
                "karrio.server.events.task_definitions.base.webhook.logger"
            ) as log,
        ):
            results = notify_subscribers(hooks, {"event": "secret-payload"})
        self.assertEqual(sorted(r.status_code for _, r in results), [200, 200, 502])
        failed = [wid for wid, r in results if r.status_code == 502]
        self.assertEqual(len(failed), 1)
        # Only the webhook id is logged: no URL, no payload, no error text.
        logged = [str(call) for call in log.method_calls]
        self.assertTrue(logged)
        for entry in logged:
            self.assertNotIn("example.com", entry)
            self.assertNotIn("secret-payload", entry)
            self.assertNotIn("http.client", entry)
        self.assertIn(failed[0], "".join(logged))
        update_notified_webhooks(hooks, results, timezone.now())
        for hook in hooks:
            hook.refresh_from_db()
            self.assertEqual(hook.failure_streak_count, 1 if hook.id == failed[0] else 0)

    def test_repeated_unexpected_failure_auto_disables_only_that_webhook(self):
        hooks = self.make_hooks(count=2)
        ok = Response()
        ok.status_code = 200

        def deliver(url, payload, headers):
            if url.endswith("/0"):
                raise AssertionError("boom")
            return ok

        with patch(
            "karrio.server.events.task_definitions.base.webhook.post_webhook",
            side_effect=deliver,
        ):
            for _ in range(6):
                results = notify_subscribers(hooks, {})
                update_notified_webhooks(hooks, results, timezone.now())
        for hook in hooks:
            hook.refresh_from_db()
        self.assertTrue(next(h for h in hooks if h.url.endswith("/0")).disabled)
        healthy = next(h for h in hooks if h.url.endswith("/1"))
        self.assertFalse(healthy.disabled)
        self.assertEqual(healthy.failure_streak_count, 0)


class TestWebhookIPv6GlobalUnicast(APITestCase):
    REFUSED = [
        ("::ffff:0:0:0/96", "::ffff:0:a9fe:a9fe"),
        ("::ffff:0:0:0/96 (loopback)", "::ffff:0:7f00:1"),
        ("64:ff9b::/96", "64:ff9b::a9fe:a9fe"),
        ("64:ff9b:1::/48", "64:ff9b:1::a9fe:a9fe"),
        ("::/96", "::a9fe:a9fe"),
        ("6to4 2002::/16", "2002:a9fe:a9fe::1"),
        ("Teredo 2001::/32", "2001:0:4136:e378:8000:63bf:3fff:fdd2"),
        ("site-local fec0::/10", "fec0::1"),
        ("outside 2000::/3", "1000::1"),
        ("outside 2000::/3 (unassigned)", "4000::1"),
        ("unique local fc00::/7", "fd12:3456:789a::1"),
        ("link-local fe80::/10", "fe80::1"),
        ("loopback", "::1"),
        ("documentation 2001:db8::/32", "2001:db8::1"),
    ]

    def test_refused_in_dns_answers_and_literals(self):
        for name, ip in self.REFUSED:
            for host in ["example.com", f"[{ip}]"]:
                with (
                    self.subTest(range=name, ip=ip, host=host),
                    patch("socket.getaddrinfo", return_value=[(10, 1, 6, "", (ip, 80))]),
                    self.assertRaises(ValidationError),
                ):
                    resolve_destination(f"http://{host}/hook")

    def test_ordinary_global_address_is_accepted(self):
        for ip in ["2606:4700:4700::1111", "2a00:1450:4001:81b::200e"]:
            for host in ["example.com", f"[{ip}]"]:
                with (
                    self.subTest(ip=ip, host=host),
                    patch("socket.getaddrinfo", return_value=[(10, 1, 6, "", (ip, 80))]),
                ):
                    self.assertEqual(resolve_destination(f"http://{host}/hook")[1], ip)

    @override_settings(WEBHOOK_ALLOWED_DESTINATIONS=["::/0", "0.0.0.0/0"])
    def test_embedding_ranges_are_refused_even_with_operator_exceptions(self):
        for ip in ["::ffff:0:a9fe:a9fe", "::ffff:0:a00:5"]:
            with (
                self.subTest(ip=ip),
                patch("socket.getaddrinfo", return_value=[(10, 1, 6, "", (ip, 80))]),
                self.assertRaises(ValidationError),
            ):
                resolve_destination("http://example.com")


class TestWebhookTeredoAndIsatap(APITestCase):
    """Teredo and ISATAP destinations are refused, operator exception or not.

    Mock DNS only: nothing here claims that a tunnel is configured or reachable.
    """

    TEREDO = [
        "2001:0:4136:e378:8000:63bf:3fff:fdd2",
        "2001:0:c000:204:0:0:a9fe:a9fe",
    ]
    # RFC 5214 section 6.1: 0000:5efe or 0200:5efe in bits 64-95, any /64.
    ISATAP = [
        ("2606:4700:1234:5678:0:5efe:a9fe:a9fe", "0000:5efe, 2606:4700:1234:5678::/64"),
        ("2606:4700:1234:5678:200:5efe:a9fe:a9fe", "0200:5efe, 2606:4700:1234:5678::/64"),
        ("2a00:1450:abcd:1234:0:5efe:808:808", "0000:5efe, 2a00:1450:abcd:1234::/64"),
        ("2a00:1450:abcd:1234:200:5efe:808:808", "0200:5efe, 2a00:1450:abcd:1234::/64"),
        ("2606:4700::5efe:a9fe:a9fe", "0000:5efe, 2606:4700::/64"),
    ]
    EXCEPTIONS = [[], ["::/0"], ["::/0", "0.0.0.0/0"], ["example.com"]]

    def refused(self, ip, host):
        with (
            patch("socket.getaddrinfo", return_value=[(10, 1, 6, "", (ip, 80))]),
            self.assertRaises(ValidationError),
        ):
            resolve_destination(f"http://{host}/hook")

    def test_teredo_refused_without_and_with_operator_exception(self):
        for exceptions in self.EXCEPTIONS:
            for ip in self.TEREDO:
                for host in ["example.com", f"[{ip}]"]:
                    with (
                        self.subTest(exceptions=exceptions, ip=ip, host=host),
                        override_settings(WEBHOOK_ALLOWED_DESTINATIONS=exceptions),
                    ):
                        self.refused(ip, host)

    def test_isatap_refused_without_and_with_operator_exception(self):
        for exceptions in self.EXCEPTIONS:
            for ip, name in self.ISATAP:
                for host in ["example.com", f"[{ip}]"]:
                    with (
                        self.subTest(exceptions=exceptions, marker=name, host=host),
                        override_settings(WEBHOOK_ALLOWED_DESTINATIONS=exceptions),
                    ):
                        self.refused(ip, host)

    @override_settings(WEBHOOK_ALLOWED_DESTINATIONS=["::/0"])
    def test_delivery_is_refused_before_any_connection(self):
        for ip in [self.TEREDO[0], self.ISATAP[0][0], self.ISATAP[1][0]]:
            with (
                self.subTest(ip=ip),
                patch("socket.getaddrinfo", return_value=[(10, 1, 6, "", (ip, 80))]),
                patch("requests.utils.get_environ_proxies", return_value={}),
                patch("urllib3.HTTPConnectionPool") as pool,
                self.assertRaises(ValidationError),
            ):
                post_webhook("http://example.com/hook", {}, {})
            pool.assert_not_called()

    def test_ordinary_global_addresses_are_still_accepted(self):
        ordinary = [
            "2606:4700:4700::1111",
            "2a00:1450:4001:81b::200e",
            "2001:4860:4860::8888",  # next to, but outside, 2001::/32
            "2606:4700:1234:5678:100:5efe:a9fe:a9fe",  # 0100:5efe is not a marker
            "2606:4700:1234:5678:5efe:0:a9fe:a9fe",  # 5efe outside bits 64-95
            "2606:4700::5efe:a9fe",  # 5efe in the low 32 bits only
        ]
        for exceptions in [[], ["::/0"]]:
            for ip in ordinary:
                for host in ["example.com", f"[{ip}]"]:
                    with (
                        self.subTest(exceptions=exceptions, ip=ip, host=host),
                        override_settings(WEBHOOK_ALLOWED_DESTINATIONS=exceptions),
                        patch(
                            "socket.getaddrinfo",
                            return_value=[(10, 1, 6, "", (ip, 80))],
                        ),
                    ):
                        self.assertEqual(
                            resolve_destination(f"http://{host}/hook")[1], ip
                        )

    def test_network_specific_nat64_prefix_is_accepted_by_design(self):
        # RFC 6052 section 2.2: a network-specific prefix cannot be told apart
        # from an ordinary global address, and no heuristic on the low 32 bits
        # is applied. An operator whose network translates such a prefix must
        # block webhook delivery to it at the network. Expected, not refused.
        for ip in ["2606:4700:1234::a9fe:a9fe", "2a00:1450:abcd::a9fe:a9fe"]:
            with (
                self.subTest(ip=ip),
                patch("socket.getaddrinfo", return_value=[(10, 1, 6, "", (ip, 80))]),
            ):
                self.assertEqual(resolve_destination("http://example.com/hook")[1], ip)


class TestWebhookGraphQLHostPolicy(GraphTestCase):
    @patch("socket.getaddrinfo", return_value=PUBLIC_DNS)
    def test_fullwidth_percent_host_refused_over_graphql(self, dns):
        response = self.query(
            """
            mutation create_webhook($data: CreateWebhookMutationInput!) {
              create_webhook(input: $data) {
                webhook { id url }
                errors { field messages }
              }
            }
            """,
            variables={"data": {"url": FULLWIDTH_PERCENT_URL, "enabled_events": ["all"]}},
        )
        self.assertFalse(Webhook.objects.exists(), response.data)
        self.assertTrue(
            response.data.get("errors")
            or (response.data["data"]["create_webhook"] or {}).get("errors"),
            response.data,
        )
