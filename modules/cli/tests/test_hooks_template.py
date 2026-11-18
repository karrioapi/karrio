"""The scaffolded webhook hook must fail closed, like the Teleship connector."""

import sys
import hmac
import json
import types
import hashlib
import unittest
from unittest.mock import patch

import karrio.lib as lib
import karrio.core.models as models
from karrio_cli.templates import hooks
from karrio_cli.templates import sdk as sdk_templates

SECRET = "whsec_template_secret"


def load_generated_hooks():
    """Render the scaffold for a carrier "acme" and import it with stub siblings."""
    source = hooks.HOOKS_EVENT_TEMPLATE.render(name="Acme", id="acme")
    stubs = {
        "karrio.providers": types.ModuleType("karrio.providers"),
        "karrio.providers.acme": types.ModuleType("karrio.providers.acme"),
        "karrio.providers.acme.error": types.SimpleNamespace(
            parse_error_response=lambda body, settings: []
        ),
        "karrio.providers.acme.utils": types.SimpleNamespace(Settings=object),
        "karrio.providers.acme.units": types.ModuleType("units"),
        "karrio.providers.acme.tracking": types.SimpleNamespace(
            _extract_details=lambda *args, **kwargs: None
        ),
    }
    module = types.ModuleType("generated_acme_event")
    with patch.dict(sys.modules, stubs):
        exec(compile(source, "hooks/event.py", "exec"), module.__dict__)
    return source, module


class ConnectionConfig(lib.Enum):
    webhook_secret = lib.OptionEnum("webhook_secret", str)


class Settings:
    carrier_id = "acme"
    carrier_name = "acme"

    def __init__(self, secret=None):
        self.connection_config = lib.to_connection_config(
            {"webhook_secret": secret} if secret is not None else {},
            option_type=ConnectionConfig,
        )


def compact(body):
    return json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode()


def sign(raw, secret=SECRET):
    return hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()


BODY = {"eventName": "shipment.updated", "objectType": "shipment", "objectId": "1", "data": {}}


class TestHooksEventTemplate(unittest.TestCase):
    def setUp(self):
        self.source, self.module = load_generated_hooks()

    def payload(self, headers=None, raw_body=None, body=None):
        return models.RequestPayload(
            url="https://example.com/hook",
            body=BODY if body is None else body,
            headers=headers or {},
            raw_body=raw_body,
        )

    def codes(self, payload, settings):
        details, messages = self.module.on_webhook_event(payload, settings)
        return details, [_.code for _ in messages]

    def test_scaffold_has_no_fail_open_branch(self):
        self.assertNotIn("return True", self.source)
        self.assertNotIn("skip verification", self.source)
        self.assertIn("compare_digest", self.source)
        self.assertIn("raw_body", self.source)

    def test_missing_header_is_rejected(self):
        details, codes = self.codes(self.payload(raw_body=compact(BODY)), Settings(SECRET))
        self.assertIsNone(details)
        self.assertEqual(codes, ["webhook_signature_missing"])

    def test_wrong_signature_is_rejected(self):
        raw = compact(BODY)
        for signature in ["deadbeef", sign(raw, "other"), "sïg"]:
            details, codes = self.codes(
                self.payload({"x-acme-signature": signature}, raw), Settings(SECRET)
            )
            self.assertIsNone(details)
            self.assertEqual(codes, ["invalid_signature"])

    def test_no_secret_is_rejected(self):
        raw = compact(BODY)
        for settings in [Settings(), Settings("")]:
            details, codes = self.codes(
                self.payload({"x-acme-signature": sign(raw)}, raw), settings
            )
            self.assertIsNone(details)
            self.assertEqual(codes, ["webhook_secret_not_configured"])

    def test_signed_event_is_accepted(self):
        raw = compact(BODY)
        details, codes = self.codes(
            self.payload({"X-Acme-Signature": sign(raw)}, raw), Settings(SECRET)
        )
        self.assertEqual(codes, [])
        self.assertIsNotNone(details)

    def test_compact_form_of_a_reformatted_body_is_accepted_old_form_is_not(self):
        indented = json.dumps(BODY, indent=4).encode()
        ok = self.codes(
            self.payload({"x-acme-signature": sign(compact(BODY))}, indented), Settings(SECRET)
        )
        old = self.codes(
            self.payload({"x-acme-signature": sign(lib.to_json(BODY).encode())}, compact(BODY)),
            Settings(SECRET),
        )
        self.assertEqual(ok[1], [])
        self.assertEqual(old[1], ["invalid_signature"])

    def test_unencodable_compact_form_does_not_break_verification(self):
        raw = json.dumps({**BODY, "extension": "\ud800"}).encode()
        body = json.loads(raw)
        self.assertEqual(self.module.signed_payloads(self.payload(body=body, raw_body=raw)), [raw])

        details, codes = self.codes(
            self.payload({"x-acme-signature": sign(raw)}, raw, body), Settings(SECRET)
        )
        self.assertEqual(codes, [])
        self.assertIsNotNone(details)

        details, codes = self.codes(
            self.payload({"x-acme-signature": "deadbeef"}, raw, body), Settings(SECRET)
        )
        self.assertIsNone(details)
        self.assertEqual(codes, ["invalid_signature"])

    def test_generated_connection_config_declares_the_secret(self):
        with_webhook = sdk_templates.PROVIDER_UNITS_TEMPLATE.render(
            name="Acme", id="acme", features=["webhook"]
        )
        without = sdk_templates.PROVIDER_UNITS_TEMPLATE.render(
            name="Acme", id="acme", features=["rating"]
        )
        self.assertIn('webhook_secret = lib.OptionEnum("webhook_secret", str)', with_webhook)
        self.assertNotIn("webhook_secret", without)

    def test_generated_tests_cover_three_rejections_and_one_acceptance(self):
        source = hooks.TEST_HOOKS_EVENT_TEMPLATE.render(
            name="Acme", id="acme", compact_name="Acme"
        )
        compile(source, "test_hooks.py", "exec")
        for name in [
            "test_on_webhook_event_rejects_a_missing_signature_header",
            "test_on_webhook_event_rejects_a_wrong_signature",
            "test_on_webhook_event_rejects_when_no_secret_is_stored",
            "test_on_webhook_event_accepts_a_signed_event",
        ]:
            self.assertIn(name, source)


if __name__ == "__main__":
    unittest.main()
