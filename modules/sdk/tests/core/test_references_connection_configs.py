import typing
import unittest
from unittest import mock

import karrio.lib as lib
import karrio.references as references
import karrio.core.metadata as metadata


class NotificationChannel(lib.StrEnum):
    sms = "sms"
    email = "email"
    letter = "letter"


class LabelType(lib.StrEnum):
    PDF = "PDF"
    ZPL = "ZPL"


class ConnectionConfig(lib.Enum):
    default_notification = lib.OptionEnum(
        "default_notification",
        typing.List[NotificationChannel],
        default=["sms", "email"],
    )
    notification_tags = lib.OptionEnum("notification_tags", typing.List[str])
    label_type = lib.OptionEnum("label_type", LabelType)
    shipping_options = lib.OptionEnum("shipping_options", list)


class ShippingOption(lib.Enum):
    notification_channels = lib.OptionEnum(
        "notification_channels", typing.List[NotificationChannel]
    )


class TestReferencesConnectionConfigs(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def collect(self) -> dict:
        provider = metadata.PluginMetadata(
            id="fake_carrier",
            label="Fake Carrier",
            connection_configs=ConnectionConfig,
            options=ShippingOption,
        )

        with mock.patch.multiple(
            references,
            PROVIDERS={"fake_carrier": provider},
            LSP_PLUGINS={},
            PLUGIN_METADATA={},
            FAILED_IMPORTS={},
            REFERENCES={},
        ):
            return references.collect_references(
                plugin_registry={"ENABLE_ALL_PLUGINS_BY_DEFAULT": True}
            )

    def test_publish_enum_list_connection_configs(self):
        refs = self.collect()

        self.assertDictEqual(
            refs["connection_configs"]["fake_carrier"],
            {
                "default_notification": {
                    "name": "default_notification",
                    "code": "default_notification",
                    "required": False,
                    "type": "list",
                    "default": ["sms", "email"],
                    "enum": ["sms", "email", "letter"],
                },
                "notification_tags": {
                    "name": "notification_tags",
                    "code": "notification_tags",
                    "required": False,
                    "type": "list",
                },
                "label_type": {
                    "name": "label_type",
                    "code": "label_type",
                    "required": False,
                    "type": "string",
                    "enum": ["PDF", "ZPL"],
                },
                "shipping_options": {
                    "name": "shipping_options",
                    "code": "shipping_options",
                    "required": False,
                    "type": "list",
                },
            },
        )

    def test_publish_enum_list_shipping_options(self):
        refs = self.collect()

        self.assertDictEqual(
            refs["options"]["fake_carrier"]["notification_channels"],
            {
                "code": "notification_channels",
                "type": "list",
                "enum": ["sms", "email", "letter"],
                "meta": {"configurable": True},
            },
        )

    def test_parse_type_lists_before_enum(self):
        self.assertListEqual(
            [
                references.parse_type(typing.List[NotificationChannel]),
                references.parse_type(list),
                references.parse_type(NotificationChannel),
            ],
            ["list", "list", "string"],
        )

    def test_extract_list_item_enum(self):
        self.assertListEqual(
            [
                references.extract_list_item_enum(typing.List[NotificationChannel]),
                references.extract_list_item_enum(typing.List[str]),
                references.extract_list_item_enum(list),
                references.extract_list_item_enum(NotificationChannel),
            ],
            [["sms", "email", "letter"], None, None, None],
        )


if __name__ == "__main__":
    unittest.main()
