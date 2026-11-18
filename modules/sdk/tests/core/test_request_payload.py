import unittest
from types import SimpleNamespace
from unittest.mock import patch

import karrio.core.models as models
import karrio.api.interface as interface


class TestRequestPayloadRawBody(unittest.TestCase):
    def test_raw_body_is_optional_and_defaults_to_none(self):
        payload = models.RequestPayload(url="https://example.com/hook")

        self.assertIsNone(payload.raw_body)
        self.assertEqual(payload.body, {})
        self.assertEqual(
            models.RequestPayload(url="u", body={"a": 1}, raw_body=b'{"a": 1}').raw_body,
            b'{"a": 1}',
        )

    def test_hooks_pass_raw_bytes_untouched_to_the_connector(self):
        received = []
        gateway = SimpleNamespace(
            check=lambda *args, **kwargs: [],
            hooks=SimpleNamespace(
                on_webhook_event=lambda payload: received.append(payload) or ("ok", [])
            ),
        )
        raw = b'{"b":1,\n "a":"\xc3\xa9"}'

        result = interface.Hooks.on_webhook_event(
            dict(url="u", body={"b": 1, "a": "é"}, headers={"X-A": "1"}, raw_body=raw)
        ).from_(gateway).parse()

        self.assertEqual(result, ("ok", []))
        self.assertEqual(received[0].raw_body, raw)
        self.assertEqual(received[0].body, {"a": "é", "b": 1})
        self.assertEqual(received[0].headers, {"X-A": "1"})

    def test_hooks_accept_a_payload_object_and_raw_body_is_optional(self):
        received = []
        gateway = SimpleNamespace(
            check=lambda *args, **kwargs: [],
            hooks=SimpleNamespace(
                on_webhook_event=lambda payload: received.append(payload) or ("ok", [])
            ),
        )

        interface.Hooks.on_webhook_event(
            models.RequestPayload(url="u", raw_body=b"{}")
        ).from_(gateway).parse()
        interface.Hooks.on_webhook_event(dict(url="u")).from_(gateway).parse()

        self.assertEqual([_.raw_body for _ in received], [b"{}", None])

    def test_hooks_do_not_write_request_headers_or_body_to_the_log(self):
        gateway = SimpleNamespace(
            check=lambda *args, **kwargs: [],
            hooks=SimpleNamespace(on_webhook_event=lambda payload: (None, [])),
        )

        with patch.object(interface, "logger") as logger:
            interface.Hooks.on_webhook_event(
                dict(
                    url="https://example.com/hook",
                    body={"secret-body": "body-marker"},
                    headers={"x-teleship-signature": "signature-marker"},
                    query={"token": "query-marker"},
                    raw_body=b"raw-marker",
                )
            ).from_(gateway).parse()

        logged = repr(logger.mock_calls)
        for marker in ["signature-marker", "body-marker", "query-marker", "raw-marker"]:
            self.assertNotIn(marker, logged)


if __name__ == "__main__":
    unittest.main()
