import typing
import unittest

import karrio.lib as lib


class NotificationChannel(lib.StrEnum):
    sms = "sms"
    email = "email"
    letter = "letter"


class ConnectionConfig(lib.Enum):
    default_notification = lib.OptionEnum(
        "default_notification", typing.List[NotificationChannel]
    )
    shipping_options = lib.OptionEnum("shipping_options", list)


class TestOptionEnumListCoercion(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.typed = lib.OptionEnum(
            "default_notification", typing.List[NotificationChannel]
        )
        self.bare = lib.OptionEnum("shipping_options", list)

    def test_none_stays_none(self):
        self.assertListEqual(
            [self.typed(None).state, self.bare(None).state],
            [None, None],
        )

    def test_string_becomes_one_item_list(self):
        self.assertListEqual(
            [self.typed("sms").state, self.bare("fedex_ground").state],
            [["sms"], ["fedex_ground"]],
        )

    def test_scalar_becomes_one_item_list(self):
        self.assertListEqual(
            [self.typed(3).state, self.bare(3).state],
            [[3], [3]],
        )

    def test_list_and_tuple_are_copied_in_order(self):
        value = ["letter", "sms"]
        state = self.typed(value).state

        self.assertListEqual(
            [state, self.bare(("email", "sms")).state, state is value],
            [["letter", "sms"], ["email", "sms"], False],
        )

    def test_items_are_not_validated(self):
        self.assertListEqual(
            self.typed(["sms", "pigeon"]).state,
            ["sms", "pigeon"],
        )

    def test_default_applies_when_value_is_none(self):
        option = lib.OptionEnum(
            "default_notification",
            typing.List[NotificationChannel],
            default=["email"],
        )

        self.assertListEqual(option(None).state, ["email"])

    def test_connection_config_coerces_list_values(self):
        config = lib.to_connection_config(
            dict(default_notification="sms", shipping_options="signature"),
            option_type=ConnectionConfig,
        )

        self.assertListEqual(
            [config.default_notification.state, config.shipping_options.state],
            [["sms"], ["signature"]],
        )


if __name__ == "__main__":
    unittest.main()
