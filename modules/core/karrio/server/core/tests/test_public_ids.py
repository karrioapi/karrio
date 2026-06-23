"""Tests for karrio.server.core.public_ids."""

import time
from unittest import mock

from django.test import TestCase, override_settings
from karrio.server.core import public_ids


class TestEncryptId(TestCase):
    """Deterministic encrypted ids (AES-SIV)."""

    def test_round_trip(self):
        token = public_ids.encrypt_id("car_abc123", "scn")
        self.assertEqual(public_ids.decrypt_id(token, "scn"), "car_abc123")

    def test_is_deterministic(self):
        a = public_ids.encrypt_id("car_abc123", "scn")
        b = public_ids.encrypt_id("car_abc123", "scn")
        self.assertEqual(a, b, "AES-SIV must produce stable ciphertext for stable ids")

    def test_namespace_isolation(self):
        token = public_ids.encrypt_id("car_abc123", "scn")
        self.assertIsNone(
            public_ids.decrypt_id(token, "bcn"),
            "decrypt with wrong namespace must fail closed",
        )

    def test_tampered_token_returns_none(self):
        token = public_ids.encrypt_id("car_abc123", "scn")
        tampered = token[:-2] + ("AB" if not token.endswith("AB") else "CD")
        self.assertIsNone(public_ids.decrypt_id(tampered, "scn"))

    def test_unknown_prefix_returns_none(self):
        self.assertIsNone(public_ids.decrypt_id("not_a_token", "scn"))
        self.assertIsNone(public_ids.decrypt_id("", "scn"))

    def test_empty_plaintext_is_passthrough(self):
        self.assertEqual(public_ids.encrypt_id("", "scn"), "")

    def test_passthrough_helpers_are_idempotent(self):
        raw = "car_abc123"
        once = public_ids.encrypt_id_or_passthrough(raw, "scn")
        twice = public_ids.encrypt_id_or_passthrough(once, "scn")
        self.assertEqual(once, twice)
        self.assertEqual(public_ids.decrypt_id(once, "scn"), raw)

    def test_decrypt_or_passthrough_accepts_legacy_raw(self):
        # During rollout, clients may still send the raw id. The boundary
        # helper must accept both forms and return the plaintext id.
        raw = "car_legacy_id"
        self.assertEqual(public_ids.decrypt_id_or_passthrough(raw, "scn"), raw)
        encrypted = public_ids.encrypt_id(raw, "scn")
        self.assertEqual(public_ids.decrypt_id_or_passthrough(encrypted, "scn"), raw)


class TestEncryptIdRotation(TestCase):
    """Multi-key rotation: tokens minted under an old key must still decrypt."""

    def test_decrypts_with_rotated_secret(self):
        with override_settings(SECRET_KEY="old-key-aaaaaaaaaaaaaaaa"):
            old_token = public_ids.encrypt_id("car_rotated", "scn")

        with override_settings(
            SECRET_KEY="new-key-bbbbbbbbbbbbbbbb",
            PUBLIC_ID_ROTATION_KEYS=["old-key-aaaaaaaaaaaaaaaa"],
        ):
            self.assertEqual(public_ids.decrypt_id(old_token, "scn"), "car_rotated")
            # New mints use the new key:
            new_token = public_ids.encrypt_id("car_rotated", "scn")
            self.assertNotEqual(new_token, old_token)
            self.assertEqual(public_ids.decrypt_id(new_token, "scn"), "car_rotated")


class TestEncryptToken(TestCase):
    """Ephemeral AES-GCM tokens with TTL."""

    def test_round_trip(self):
        token = public_ids.encrypt_token({"cid": "car_abc", "kind": "system"}, "rate")
        decoded = public_ids.decrypt_token(token, "rate")
        self.assertEqual(decoded, {"cid": "car_abc", "kind": "system"})

    def test_tokens_are_unique_per_call(self):
        a = public_ids.encrypt_token({"cid": "car_abc"}, "rate")
        b = public_ids.encrypt_token({"cid": "car_abc"}, "rate")
        self.assertNotEqual(a, b, "AES-GCM uses a random nonce per call")

    def test_expired_token_returns_none(self):
        token = public_ids.encrypt_token({"cid": "car_abc"}, "rate", ttl_seconds=60)
        future = time.time() + 120
        with mock.patch("karrio.server.core.public_ids.time.time", return_value=future):
            self.assertIsNone(public_ids.decrypt_token(token, "rate"))

    def test_namespace_isolation(self):
        token = public_ids.encrypt_token({"cid": "car_abc"}, "rate")
        self.assertIsNone(public_ids.decrypt_token(token, "scn"))

    def test_tampered_token_returns_none(self):
        token = public_ids.encrypt_token({"cid": "car_abc"}, "rate")
        tampered = token[:-2] + ("AB" if not token.endswith("AB") else "CD")
        self.assertIsNone(public_ids.decrypt_token(tampered, "rate"))

    def test_invalid_inputs(self):
        self.assertIsNone(public_ids.decrypt_token("", "rate"))
        self.assertIsNone(public_ids.decrypt_token("garbage", "rate"))
        with self.assertRaises(ValueError):
            public_ids.encrypt_token({"x": 1}, "rate", ttl_seconds=0)
        with self.assertRaises(ValueError):
            public_ids.encrypt_token({"x": 1}, "rate", ttl_seconds=10**9)


class TestRedactRateMeta(TestCase):
    """Tenant-facing redaction of rate.meta."""

    def test_account_passthrough(self):
        meta = {
            "connection_kind": "account",
            "carrier_connection_id": "car_owner",
            "ext": "dhl_express",
        }
        out = public_ids.redact_rate_meta_for_tenant(meta)
        self.assertEqual(out["carrier_connection_id"], "car_owner")
        self.assertEqual(out["connection_kind"], "account")
        # Input not mutated:
        self.assertEqual(meta["carrier_connection_id"], "car_owner")

    def test_system_kind_redacted(self):
        meta = {
            "connection_kind": "system",
            "carrier_connection_id": "car_system_pk",
            "ext": "dhl_express",
        }
        out = public_ids.redact_rate_meta_for_tenant(meta)
        self.assertNotIn("carrier_connection_id", out)
        self.assertEqual(out["connection_kind"], "system")
        self.assertIn("rate_ref", out)
        self.assertEqual(out["ext"], "dhl_express")

    def test_brokered_kind_redacted(self):
        meta = {"connection_kind": "brokered", "carrier_connection_id": "car_sys_pk"}
        out = public_ids.redact_rate_meta_for_tenant(meta)
        self.assertNotIn("carrier_connection_id", out)
        self.assertIn("rate_ref", out)

    def test_redaction_handles_empty(self):
        self.assertIsNone(public_ids.redact_rate_meta_for_tenant(None))
        self.assertEqual(public_ids.redact_rate_meta_for_tenant({}), {})

    def test_redaction_without_kind_passes_through(self):
        # If kind is missing we treat it as account (legacy rates pre-PR).
        # Redaction-without-kind would lose the PK irrecoverably, which
        # would break older clients during the rollout window.
        meta = {"carrier_connection_id": "car_legacy"}
        out = public_ids.redact_rate_meta_for_tenant(meta)
        self.assertEqual(out["carrier_connection_id"], "car_legacy")


class TestResolveRateRef(TestCase):
    """Reverse of redact_rate_meta_for_tenant, used by buy-label."""

    def test_resolves_account_directly(self):
        meta = {"connection_kind": "account", "carrier_connection_id": "car_owner"}
        self.assertEqual(
            public_ids.resolve_rate_ref(meta),
            {"connection_id": "car_owner", "connection_type": "account"},
        )

    def test_resolves_via_rate_ref(self):
        original = {
            "connection_kind": "system",
            "carrier_connection_id": "car_system_pk",
        }
        redacted = public_ids.redact_rate_meta_for_tenant(original)
        self.assertEqual(
            public_ids.resolve_rate_ref(redacted),
            {"connection_id": "car_system_pk", "connection_type": "system"},
        )

    def test_brokered_round_trip(self):
        original = {"connection_kind": "brokered", "carrier_connection_id": "car_sys"}
        redacted = public_ids.redact_rate_meta_for_tenant(original)
        self.assertEqual(
            public_ids.resolve_rate_ref(redacted),
            {"connection_id": "car_sys", "connection_type": "brokered"},
        )

    def test_legacy_no_kind(self):
        meta = {"carrier_connection_id": "car_legacy"}
        self.assertEqual(
            public_ids.resolve_rate_ref(meta),
            {"connection_id": "car_legacy", "connection_type": "account"},
        )

    def test_returns_none_when_no_ref(self):
        self.assertIsNone(public_ids.resolve_rate_ref({}))
        self.assertIsNone(public_ids.resolve_rate_ref(None))
        self.assertIsNone(public_ids.resolve_rate_ref({"ext": "dhl"}))

    def test_invalid_rate_ref_falls_back_to_carrier_connection_id(self):
        # Defense-in-depth: a tampered rate_ref shouldn't silently fail.
        # Caller gets the legacy fallback so the request isn't bricked,
        # and access control downstream will catch unauthorized ids.
        meta = {
            "connection_kind": "system",
            "rate_ref": "rate_v1_garbagegarbagegarbage",
            "carrier_connection_id": "car_legacy_pk",
        }
        self.assertEqual(
            public_ids.resolve_rate_ref(meta),
            {"connection_id": "car_legacy_pk", "connection_type": "system"},
        )
