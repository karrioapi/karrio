"""Tests for telemetry_scrubbing: deterministic regex + structural default-deny
PII/credential redaction (issue #641 — replaced the Presidio/spaCy NER scrubber).

The scrubber's input is carrier HTTP request/response bodies + URLs (JSON/XML).
These tests assert: value-shaped PII is redacted field-agnostically; names are
redacted structurally by default-deny (any key, known or unknown, plus free-text);
operational data survives; and — the key safety property — PII never leaks even
under field names we've never seen. No Presidio/spaCy dependency, so this runs in
CI and locally.
"""

import json
import logging
import unittest
from unittest import mock

import karrio.server.core.telemetry_scrubbing as telemetry_scrubbing
from karrio.server.core.tests._logging_helpers import capture_records

# Names that must never survive scrubbing, in any context.
PII_NAMES = ["Hans Müller", "Anna Schmidt", "John Smith", "Greta Bauer", "Lena Fischer", "Koch"]
# Carrier field names the OLD field-name list did NOT cover (the gaps that leaked).
GAP_NAME_KEYS = [
    "givenName",
    "familyName",
    "receiverName",
    "psCustomerFirstName",
    "psCustomerLastName",
    "middlename",
    "remitToName",
    "signedBy",
    "signatureName",
    "pickupName",
    "authorizerName",
    # plus carrier-unknown / foreign keys — must still be caught by default-deny
    "kundenname",
    "empfaenger",
    "destinataire",
    "consignatario",
    "x_custom_name",
]


class TestValueShapedPII(unittest.TestCase):
    """Email / phone / IBAN / tokens are redacted by VALUE — regardless of key."""

    def setUp(self):
        self.maxDiff = None
        self.mod = telemetry_scrubbing

    def test_email_redacted_any_key(self):
        for key in ("email", "mail", "notificationEmail", "totallyUnknownKey"):
            out = self.mod.scrub_text(json.dumps({key: "hans.mueller@example.de"}))
            self.assertNotIn("hans.mueller@example.de", out, msg=key)
            self.assertIn("REDACTED_EMAIL", out, msg=key)

    def test_phone_redacted_any_key(self):
        for key in ("phone", "phone1", "EmergencyPhone", "whatever"):
            out = self.mod.scrub_text(json.dumps({key: "+49 151 12345678"}))
            self.assertNotIn("+49 151 12345678", out, msg=key)

    def test_iban_and_tokens_redacted(self):
        out = self.mod.scrub_text(json.dumps({"bankAccount": "DE89370400440532013000"}))
        self.assertNotIn("DE89370400440532013000", out)
        out = self.mod.scrub_text('{"Authorization":"Bearer eyJhbGciOiJSUzI1NiJ9.abc123def456ghi789jkl"}')
        self.assertNotIn("eyJhbGciOiJSUzI1NiJ9", out)
        self.assertIn("REDACTED_CREDENTIAL", out)


class TestStructuralNames(unittest.TestCase):
    """Names redacted structurally by default-deny — known AND unknown keys."""

    def setUp(self):
        self.maxDiff = None
        self.mod = telemetry_scrubbing

    def test_known_and_gap_name_keys_redacted(self):
        for key in GAP_NAME_KEYS + ["recipientName", "shipperName", "name1", "firstname"]:
            out = self.mod.scrub_text(json.dumps({key: "Hans Müller"}))
            self.assertNotIn("Hans Müller", out, msg=f"name leaked under key={key}")
            self.assertIn("REDACTED_PII", out, msg=key)

    def test_split_name_surname_only(self):
        out = self.mod.scrub_text('{"name1":"", "name2":"Koch", "name3":""}')
        self.assertNotIn("Koch", out)

    def test_free_text_field_with_name(self):
        out = self.mod.scrub_text('{"eventDescription":"Signed by John Smith at 14:30"}')
        self.assertNotIn("John Smith", out)

    def test_xml_contact_name(self):
        out = self.mod.scrub_text("<shipment><contact-name>John Smith</contact-name></shipment>")
        self.assertNotIn("John Smith", out)


class TestNoLeakGuard(unittest.TestCase):
    """The core safety property: a name under ANY field — including keys we've
    never seen — must be redacted. This is what the field-name/NER approaches
    failed and default-deny passes deterministically."""

    def setUp(self):
        self.maxDiff = None
        self.mod = telemetry_scrubbing

    def test_names_under_unknown_keys_never_leak(self):
        leaks = []
        for name in PII_NAMES:
            for key in GAP_NAME_KEYS:
                out = self.mod.scrub_text(json.dumps({key: name, "service": "std", "weight": 3}))
                if name in out:
                    leaks.append((key, name))
        self.assertEqual(leaks, [], f"PII leaked under keys: {leaks}")

    def test_nested_and_listed_names_redacted(self):
        body = json.dumps({"shipment": {"parcels": [{"toName": "Hans Müller"}, {"toName": "Anna Schmidt"}]}})
        out = self.mod.scrub_text(body)
        self.assertNotIn("Hans Müller", out)
        self.assertNotIn("Anna Schmidt", out)


class TestOperationalPreserved(unittest.TestCase):
    """Non-PII operational data survives so telemetry stays useful."""

    def setUp(self):
        self.maxDiff = None
        self.mod = telemetry_scrubbing

    def test_codes_numbers_dates_currencies_kept(self):
        body = json.dumps(
            {
                "service": "express",
                "status": "in_transit",
                "weight": 2.5,
                "pieces": 3,
                "currency": "EUR",
                "country": "DE",
                "trackingNumber": "1Z999AA10123456784",
                "serviceCode": "V01PAK",
                "createdAt": "2026-06-16T10:00:00Z",
                "delivered": False,
            }
        )
        out = self.mod.scrub_text(body)
        for kept in (
            "express",
            "in_transit",
            "2.5",
            "3",
            "EUR",
            "DE",
            "1Z999AA10123456784",
            "V01PAK",
            "2026-06-16T10:00:00Z",
            "false",
        ):
            self.assertIn(kept, out, msg=f"operational value lost: {kept}")
        self.assertNotIn("REDACTED", out)


class TestUrl(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.mod = telemetry_scrubbing

    def test_url_query_credentials_redacted(self):
        out = self.mod.scrub_text("https://api.dhl.com/ship?apikey=SECRET12345&ref=abc123")
        self.assertNotIn("SECRET12345", out)
        self.assertIn("ref=abc123", out)  # non-sensitive param kept


class TestFallbackAndCaps(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.mod = telemetry_scrubbing

    def test_truncated_json_redacts_complete_pairs(self):
        # 16KB cap can cut JSON mid-object; complete "key":"value" pairs still scrub.
        out = self.mod.scrub_text('{"recipientName":"Hans Müller","weight":2.5,"note":"call befo')
        self.assertNotIn("Hans Müller", out)

    def test_non_json_value_pii_fallback(self):
        out = self.mod.scrub_text("plain text contact hans@example.de here")
        self.assertNotIn("hans@example.de", out)

    def test_oversized_body_dropped(self):
        out = self.mod.scrub_text("x" * (self.mod._MAX_SCRUB_CHARS + 1))
        self.assertEqual(out, self.mod.R_OVERSIZED)

    def test_non_string_and_empty_passthrough(self):
        self.assertEqual(self.mod.scrub_text(123), 123)
        self.assertIsNone(self.mod.scrub_text(None))
        self.assertEqual(self.mod.scrub_text(""), "")


class TestScrubSpanData(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.mod = telemetry_scrubbing

    def test_only_scrub_keys_touched(self):
        data = {
            "http.request.body": '{"recipientName":"Hans Müller"}',
            "http.status_code": 200,
            "db.statement": "SELECT 1",
        }
        result = self.mod.scrub_span_data(data)
        self.assertNotIn("Hans Müller", result["http.request.body"])
        self.assertEqual(result["http.status_code"], 200)
        self.assertEqual(result["db.statement"], "SELECT 1")

    def test_all_scrub_keys_routed(self):
        for key in ["http.request.body", "request.body", "http.response.body", "response.body"]:
            result = self.mod.scrub_span_data({key: '{"name":"Hans Müller"}'})
            self.assertNotIn("Hans Müller", result[key], msg=key)

    def test_none_returns_empty_dict(self):
        self.assertEqual(self.mod.scrub_span_data(None), {})

    def test_per_key_failure_fails_closed_and_warns(self):
        # On an unexpected scrub error the field must be REDACTED, not passed
        # through raw — a scrub failure can never leak a raw payload to Sentry.
        records = capture_records(self, "karrio.server.core.telemetry_scrubbing", level=logging.WARNING)
        data = {"http.request.body": "some pii data"}
        with mock.patch.object(self.mod, "scrub_text", side_effect=RuntimeError("boom")):
            result = self.mod.scrub_span_data(data)
        self.assertNotIn("some pii data", result["http.request.body"])
        self.assertEqual(result["http.request.body"], self.mod.R_SCRUB_FAILED)
        self.assertTrue(any("http.request.body" in r.getMessage() for r in records))


class TestRegressionAndEdges(unittest.TestCase):
    """Leaks found during scenario review (must stay fixed) + structural edges."""

    def setUp(self):
        self.maxDiff = None
        self.mod = telemetry_scrubbing

    # ── numeric PII: pure-digit account/phone/id must NOT be kept as "a number" ──
    def test_long_pure_digit_strings_redacted(self):
        for body, tok in [
            ('{"accountNo":"1234567890"}', "1234567890"),  # account
            ('{"phone":"01511234567"}', "01511234567"),  # national phone, no +
            ('{"ssn":"123456789"}', "123456789"),  # national id
            ('{"customerNumber":"998877"}', "998877"),  # 6-digit
        ]:
            self.assertNotIn(tok, self.mod.scrub_text(body), msg=body)

    def test_short_numbers_and_keyed_numerics_kept(self):
        out = self.mod.scrub_text('{"pieces":3,"weight":"150000","zip":"12345"}')
        self.assertIn("3", out)
        self.assertIn("150000", out)  # kept via _SAFE_KEYS (weight)
        self.assertIn("12345", out)  # 5-digit zip kept by shape

    # ── short all-caps must not be mistaken for currency/country ──
    def test_short_all_caps_name_redacted(self):
        for tok in ["LEE", "WU", "NG", "OTT"]:
            self.assertNotIn(tok, self.mod.scrub_text(f'{{"lastName":"{tok}"}}'), msg=tok)

    def test_currency_country_kept_via_key(self):
        out = self.mod.scrub_text('{"currency":"EUR","country":"DE","countryCode":"US"}')
        for tok in ("EUR", "DE", "US"):
            self.assertIn(tok, out, msg=tok)

    # ── credentials / ids by value shape ──
    def test_high_entropy_token_redacted_any_key(self):
        out = self.mod.scrub_text('{"randomField":"aB3xK9mQ7wL2pR5tZ8vN1cD4fG6hJ0sUeYt"}')
        self.assertNotIn("aB3xK9mQ7wL2pR5tZ8vN1cD4fG6hJ0sUeYt", out)
        self.assertIn("REDACTED_CREDENTIAL", out)

    def test_uuid_preserved_as_correlation_id(self):
        u = "550e8400-e29b-41d4-a716-446655440000"
        self.assertIn(u, self.mod.scrub_text(f'{{"shipmentId":"{u}"}}'))

    def test_alphanumeric_code_kept(self):
        for tok in ["V01PAK", "1Z999AA10123456784"]:
            self.assertIn(tok, self.mod.scrub_text(f'{{"code":"{tok}"}}'), msg=tok)

    # ── XML edges ──
    def test_xml_attribute_pii_redacted(self):
        self.assertNotIn("John Smith", self.mod.scrub_text('<addr name="John Smith"/>'))

    def test_namespaced_xml_name_redacted(self):
        body = '<ns:s xmlns:ns="http://x.test"><ns:contact-name>John Smith</ns:contact-name></ns:s>'
        self.assertNotIn("John Smith", self.mod.scrub_text(body))

    def test_invalid_xml_falls_back_to_value_pii(self):
        # Not valid XML/JSON → freeform fallback still catches value-shaped PII.
        self.assertNotIn("a@b.de", self.mod.scrub_text("<broken contact a@b.de"))

    def test_xml_with_dtd_not_dom_parsed(self):
        # DTD/entity-bearing XML ("billion laughs"/XXE vector) must NOT be
        # DOM-parsed — it falls back to freeform (returns fast, no expansion).
        bomb = (
            '<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol">'
            '<!ENTITY lol2 "&lol;&lol;&lol;">]><contact>&lol2; a@b.de</contact>'
        )
        out = self.mod.scrub_text(bomb)
        self.assertIsInstance(out, str)  # returned fast, no entity expansion
        self.assertNotIn("a@b.de", out)  # value-PII still applied via freeform

    # ── URL edges ──
    def test_url_sensitive_params_redacted(self):
        for body, secret in [
            ("https://x/y?token=ABCDEF123456&q=1", "ABCDEF123456"),
            ("https://x/y?password=hunter2zz9&q=1", "hunter2zz9"),
            ("https://x/y?clientSecret=s3cr3tvalue&q=1", "s3cr3tvalue"),
        ]:
            out = self.mod.scrub_text(body)
            self.assertNotIn(secret, out, msg=body)
            self.assertIn("q=1", out)  # non-sensitive param kept

    def test_email_in_url_redacted(self):
        self.assertNotIn("a@b.de", self.mod.scrub_text("https://x/y?notify=a@b.de"))

    # ── top-level + nesting structure edges ──
    def test_top_level_json_array(self):
        out = self.mod.scrub_text('[{"recipientName":"Hans Müller"},{"pieces":2}]')
        self.assertNotIn("Hans Müller", out)
        self.assertIn("2", out)

    def test_top_level_scalar_number_kept(self):
        self.assertEqual(self.mod.scrub_text("123"), "123")

    def test_deeply_nested_name_redacted(self):
        out = self.mod.scrub_text('{"a":{"b":[{"c":{"toName":"Anna Schmidt"}}]}}')
        self.assertNotIn("Anna Schmidt", out)

    # ── scrub_span_data edges ──
    def test_http_url_key_routed(self):
        result = self.mod.scrub_span_data({"http.url": "https://x/y?apikey=SECRET123456&q=1"})
        self.assertNotIn("SECRET123456", result["http.url"])

    def test_scrub_span_data_non_dict_passthrough(self):
        self.assertEqual(self.mod.scrub_span_data("notadict"), "notadict")

    def test_whitespace_value_kept(self):
        out = self.mod.scrub_text('{"note":"   "}')
        self.assertNotIn("REDACTED", out)

    # ── form-urlencoded bodies (OAuth token requests + some carrier APIs) ──
    def test_form_urlencoded_name_and_secret_redacted(self):
        out = self.mod.scrub_text("recipientName=Hans+M%C3%BCller&email=a@b.de&weight=2.5")
        self.assertNotIn("Hans", out)
        self.assertNotIn("a@b.de", out)
        self.assertIn("weight=2.5", out)  # operational kept

    def test_form_oauth_credentials_redacted(self):
        out = self.mod.scrub_text("grant_type=client_credentials&client_id=myid123&client_secret=topsecret9")
        self.assertNotIn("myid123", out)
        self.assertNotIn("topsecret9", out)

    # ── short secrets/accounts under sensitive keys (shape looks safe) ──
    def test_short_secret_and_account_by_key_redacted(self):
        for body, tok in [
            ('{"client_secret":"SEKRET123"}', "SEKRET123"),  # looks like an alnum code
            ('{"apiKey":"AB12CD"}', "AB12CD"),
            ('{"siteId":"AB12CD"}', "AB12CD"),  # FedEx auth credential, alnum (audit gap)
            ('{"accountNumber":"998877"}', "998877"),  # 6-digit account
            ('{"phoneNumber":"5551234"}', "5551234"),
            ('{"meterNumber":"123456789"}', "123456789"),  # long numeric → default-deny
        ]:
            self.assertNotIn(tok, self.mod.scrub_text(body), msg=body)


if __name__ == "__main__":
    unittest.main()
