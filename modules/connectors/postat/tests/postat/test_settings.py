"""PostAT connection settings tests (server_url is fixed / SSRF-safe)."""

import unittest

import karrio.sdk as karrio

SERVER_URL = "https://plc.post.at/Post.Webservice/ShippingService.svc/secure"


def build_gateway(config=None):
    return karrio.gateway["postat"].create(
        dict(
            id="carrier_id",
            test_mode=True,
            carrier_id="postat",
            client_id="-1",
            org_unit_id="1461448",
            org_unit_guid="cd96848d-6552-4653-a992-f0f411710fb4",
            config=config or {},
        )
    )


class TestPostATServerURL(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_server_url_is_the_fixed_endpoint(self):
        self.assertEqual(build_gateway().settings.server_url, SERVER_URL)

    def test_server_url_is_not_tamperable_via_config(self):
        # A tenant-supplied server_url must be ignored — no SSRF surface.
        for tampered in TAMPER_ATTEMPTS:
            with self.subTest(server_url=tampered):
                gateway = build_gateway(config=dict(server_url=tampered))
                self.assertEqual(gateway.settings.server_url, SERVER_URL)

    def test_server_url_is_not_an_advertised_config_option(self):
        from karrio.providers.postat.units import ConnectionConfig

        self.assertNotIn("server_url", ConnectionConfig.__members__)


TAMPER_ATTEMPTS = [
    "http://169.254.169.254/latest/meta-data/",  # cloud metadata
    "http://localhost/admin",  # loopback
    "https://10.0.0.1/internal",  # RFC-1918
    "file:///etc/passwd",  # non-http scheme
    "https://post.at.evil.com/",  # look-alike host
    "https://plc.post.at/Post.Webservice/ShippingService.svc/secure",  # even a valid-looking one
]


if __name__ == "__main__":
    unittest.main()
