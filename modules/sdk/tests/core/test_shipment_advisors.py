"""Tests for plugin shipment advisors (metadata, registry, runner, invocation)."""

import attr
import unittest
from unittest.mock import patch, MagicMock
import karrio.lib as lib
import karrio.references as references
import karrio.core.advisors as advisors
import karrio.core.metadata as metadata
import karrio.core.models as models
import karrio.core.settings as settings

import logging

logging.disable(logging.CRITICAL)


def country_advisor(request, context):
    return [
        models.Message(
            carrier_name=context.carrier_name,
            carrier_id=context.carrier_id,
            code="country_advice",
            level="warning",
            message=f"shipper country {request.shipper.country_code}",
        )
    ]


def carrier_integration_metadata(**kwargs) -> metadata.PluginMetadata:
    return metadata.PluginMetadata(
        id="advised_carrier",
        label="Advised Carrier",
        Mapper=MagicMock(),
        Proxy=MagicMock(),
        Settings=MagicMock(),
        **kwargs,
    )


class TestPluginMetadataAdvisors(unittest.TestCase):
    def test_advisor_only_plugin_is_typed_advisor(self):
        plugin = metadata.PluginMetadata(
            id="conventions",
            label="Conventions",
            shipment_advisors=[country_advisor],
        )

        self.assertEqual(plugin.plugin_type, "advisor")
        self.assertListEqual(plugin.plugin_types, ["advisor"])

    def test_carrier_plugin_with_advisors_reports_both_types(self):
        plugin = carrier_integration_metadata(shipment_advisors=[country_advisor])

        self.assertEqual(plugin.plugin_type, "carrier")
        self.assertListEqual(plugin.plugin_types, ["carrier", "advisor"])

    def test_plugins_without_advisors_keep_their_types(self):
        carrier = carrier_integration_metadata()
        bare = metadata.PluginMetadata(id="bare", label="Bare")

        self.assertListEqual(carrier.shipment_advisors, [])
        self.assertListEqual(carrier.plugin_types, ["carrier"])
        self.assertEqual(bare.plugin_type, "unknown")
        self.assertListEqual(bare.plugin_types, ["unknown"])

    def test_advisor_lists_are_not_shared_between_instances(self):
        first = metadata.PluginMetadata(id="first", label="First")
        second = metadata.PluginMetadata(id="second", label="Second")

        first.shipment_advisors.append(country_advisor)

        self.assertListEqual(second.shipment_advisors, [])


def entrypoint_plugins(*plugins: metadata.PluginMetadata) -> dict:
    return {plugin.id: {"entrypoint": {plugin.id: plugin}} for plugin in plugins}


class TestAdvisorRegistry(unittest.TestCase):
    def setUp(self):
        self.advisor_only = metadata.PluginMetadata(
            id="conventions",
            label="Conventions",
            shipment_advisors=[country_advisor],
        )

    def tearDown(self):
        references.import_extensions()

    def import_with(self, *plugins: metadata.PluginMetadata):
        with patch(
            "karrio.core.plugins.discover_entrypoint_plugins",
            return_value=entrypoint_plugins(*plugins),
        ):
            references.import_extensions()

    def test_advisors_are_collected_from_advisor_only_plugins(self):
        self.import_with(self.advisor_only)

        self.assertIn(("conventions", country_advisor), references.get_advisors())
        self.assertNotIn("conventions", references.PROVIDERS)
        self.assertNotIn("conventions", references.LSP_PLUGINS)

    def test_advisors_are_reset_on_reimport(self):
        self.import_with(self.advisor_only)
        self.import_with()

        self.assertNotIn(("conventions", country_advisor), references.get_advisors())

    def test_advisor_only_plugin_is_not_unknown_in_references(self):
        self.import_with(self.advisor_only)

        plugin = references.collect_references(plugin_registry={})["plugins"][
            "conventions"
        ]

        self.assertEqual(plugin["type"], "advisor")
        self.assertListEqual(plugin["types"], ["advisor"])


@attr.s(auto_attribs=True)
class CredentialSettings(settings.Settings):
    api_key: str = None
    secret: str = None

    @property
    def carrier_name(self):
        return "advised_carrier"


def credential_settings() -> CredentialSettings:
    return CredentialSettings(
        carrier_id="advised_carrier_se",
        account_country_code="SE",
        test_mode=True,
        api_key="API-KEY-VALUE",
        secret="SECRET-VALUE",
        metadata={"token": "METADATA-VALUE"},
        config={"label_type": "PDF", "nested": {"flag": True}},
        id="CONNECTION-ID-VALUE",
    )


RatePayload = {
    "shipper": {"postal_code": "11122", "country_code": "SE"},
    "recipient": {"postal_code": "0150", "country_code": "NO"},
    "parcels": [{"weight": 1.0, "weight_unit": "KG"}],
}


def rate_request() -> models.RateRequest:
    return lib.to_object(models.RateRequest, RatePayload)


class TestAdvisorContext(unittest.TestCase):
    def test_context_exposes_only_allowlisted_fields(self):
        context = advisors.AdvisorContext.from_settings(
            credential_settings(), "rating"
        )

        self.assertDictEqual(
            attr.asdict(context),
            {
                "carrier_name": "advised_carrier",
                "carrier_id": "advised_carrier_se",
                "account_country_code": "SE",
                "test_mode": True,
                "operation": "rating",
                "config": {"label_type": "PDF", "nested": {"flag": True}},
            },
        )
        self.assertFalse(
            any(
                hasattr(context, name)
                for name in ["api_key", "secret", "metadata", "id", "settings"]
            )
        )

    def test_context_config_is_a_deep_copy(self):
        connection = credential_settings()
        context = advisors.AdvisorContext.from_settings(connection, "shipping")

        context.config["nested"]["flag"] = False

        self.assertTrue(connection.config["nested"]["flag"])

    def test_context_is_immutable(self):
        context = advisors.AdvisorContext.from_settings(
            credential_settings(), "rating"
        )

        with self.assertRaises(attr.exceptions.FrozenInstanceError):
            context.carrier_id = "other"


def message_advisor(**kwargs):
    return lambda request, context: [models.Message(**{**dict(carrier_name=None, carrier_id=None), **kwargs})]


def failing_advisor(request, context):
    raise ValueError("advisor exploded")


def mutating_advisor(request, context):
    request.shipper.country_code = "DK"
    return []


class TestRunAdvisors(unittest.TestCase):
    def run_with(self, *registered, request=None, operation="rating"):
        with patch.object(references, "ADVISORS", list(registered)):
            return advisors.run_advisors(
                request or rate_request(), credential_settings(), operation
            )

    def test_no_advisors_returns_no_messages(self):
        self.assertListEqual(self.run_with(), [])

    def test_levels_above_warning_are_downgraded(self):
        messages = self.run_with(
            ("p1", message_advisor(code="a", level="error", message="A")),
            ("p2", message_advisor(code="b", level="info", message="B")),
            ("p3", message_advisor(code="c", level="warning", message="C")),
            ("p4", message_advisor(code="d", message="D")),
        )

        self.assertListEqual(
            [(m.code, m.level) for m in messages],
            [("a", "warning"), ("b", "info"), ("c", "warning"), ("d", "warning")],
        )

    def test_mutating_advisor_leaves_request_unchanged(self):
        request = rate_request()
        seen = []

        self.run_with(
            ("mutator", mutating_advisor),
            ("observer", lambda req, ctx: seen.append(req.shipper.country_code) or []),
            request=request,
        )

        self.assertEqual(request.shipper.country_code, "SE")
        self.assertListEqual(seen, ["SE"])

    def test_failing_advisor_is_reported_and_others_still_run(self):
        messages = self.run_with(
            ("broken_plugin", failing_advisor),
            ("conventions", country_advisor),
        )

        self.assertListEqual(
            lib.to_dict(messages),
            [
                {
                    "carrier_name": "advised_carrier",
                    "carrier_id": "advised_carrier_se",
                    "code": "shipment_advisor_failed",
                    "level": "warning",
                    "message": "Shipment advisor from plugin 'broken_plugin' failed",
                    "details": {
                        "plugin": "broken_plugin",
                        "error": "advisor exploded",
                    },
                },
                {
                    "carrier_name": "advised_carrier",
                    "carrier_id": "advised_carrier_se",
                    "code": "country_advice",
                    "level": "warning",
                    "message": "shipper country SE",
                },
            ],
        )

    def test_invalid_advisor_output_is_reported_as_failure(self):
        messages = self.run_with(("garbage", lambda req, ctx: [object()]))

        self.assertListEqual(
            [(m.code, m.details["plugin"]) for m in messages],
            [("shipment_advisor_failed", "garbage")],
        )

    def test_message_identity_is_filled_from_context(self):
        messages = self.run_with(
            ("p1", message_advisor(code="a", level="warning")),
            (
                "p2",
                message_advisor(
                    carrier_name="explicit",
                    carrier_id="explicit_id",
                    code="b",
                    level="warning",
                ),
            ),
        )

        self.assertListEqual(
            [(m.carrier_name, m.carrier_id) for m in messages],
            [("advised_carrier", "advised_carrier_se"), ("explicit", "explicit_id")],
        )

    def test_advisor_receives_operation_in_context(self):
        seen = []

        self.run_with(
            ("p1", lambda req, ctx: seen.append(ctx.operation) or []),
            operation="shipping",
        )

        self.assertListEqual(seen, ["shipping"])


if __name__ == "__main__":
    unittest.main()
