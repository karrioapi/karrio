"""Tests for plugin shipment advisors (metadata, registry, runner, invocation)."""

import unittest
from unittest.mock import patch, MagicMock
import karrio.lib as lib
import karrio.references as references
import karrio.core.metadata as metadata
import karrio.core.models as models

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


if __name__ == "__main__":
    unittest.main()
