import karrio.lib as lib
from unittest.mock import ANY
import karrio.server.providers.models as providers
from karrio.server.graph.tests.base import GraphTestCase


class TestSystemConnections(GraphTestCase):
    def test_query_system_connections(self):
        response = self.query(
            """
            query get_system_connections {
              system_connections {
                edges {
                  node {
                    id
                    carrier_id
                    carrier_name
                    active
                    test_mode
                  }
                }
              }
            }
            """,
            operation_name="get_system_connections",
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response_data),
            SYSTEM_CONNECTIONS,
        )


class TestUserConnections(GraphTestCase):
    def test_query_user_connections(self):
        providers.CarrierConnection.objects.create(
            carrier_code="generic",
            carrier_id="custom_carrier",
            test_mode=False,
            created_by=self.user,
            credentials=dict(
                custom_carrier_name="Custom Carrier",
                display_name="Custom Carrier Display",
            ),
            capabilities=["rating", "shipping"],
        )
        response = self.query(
            """
            query get_user_connections {
                user_connections {
                edges {
                  node {
                    id
                    carrier_id
                    carrier_name
                    active
                    test_mode
                    credentials
                    custom_carrier_name
                  }
                }
              }
            }
            """,
            operation_name="get_user_connections",
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response_data),
            USER_CONNECTIONS,
        )

    def test_create_user_connection(self):
        response = self.query(
            """
            mutation create_connection($data: CreateCarrierConnectionMutationInput!) {
              create_carrier_connection(input: $data) {
                connection {
                    id
                    carrier_id
                    carrier_name
                    active
                    test_mode
                    credentials
                }
              }
            }
            """,
            operation_name="create_connection",
            variables=CONNECTION_DATA,
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(response_data, CONNECTION_RESPONSE)

    def test_update_user_connection(self):
        response = self.query(
            """
            mutation update_connection($data: UpdateCarrierConnectionMutationInput!) {
              update_carrier_connection(input: $data) {
                connection {
                    carrier_id
                    credentials
                }
              }
            }
            """,
            operation_name="update_connection",
            variables={
                "data": {
                    "id": self.carrier.id,
                    **CONNECTION_UPDATE_DATA["data"],
                },
            },
        )
        response_data = response.data

        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            lib.to_dict(response_data),
            lib.to_dict(CONNECTION_UPDATE_RESPONSE),
        )


class TestLabelTemplatePersistence(GraphTestCase):
    """Reproduce the dashboard label template editor save not persisting.

    The redesigned Connections page (packages/core/modules/Connections/index.tsx
    handleEditLabelTemplate) saves a partial credentials delta through the
    update_carrier_connection graph mutation:

        {id, credentials: {label_template: <modal template object>}}

    The modal (packages/ui/core/modals/label-template-edit-modal.tsx) submits
    its whole template state object, shaped by DEFAULT_LABEL_TEMPLATE_CONTENT
    plus user edits.
    """

    def setUp(self):
        super().setUp()
        self.generic_carrier = providers.CarrierConnection.objects.create(
            carrier_code="generic",
            carrier_id="custom_carrier",
            test_mode=False,
            created_by=self.user,
            credentials=dict(
                custom_carrier_name="Custom Carrier",
                display_name="Custom Carrier Display",
            ),
            capabilities=["rating", "shipping"],
        )

    def test_update_generic_connection_label_template(self):
        response = self.query(
            """
            mutation update_connection($data: UpdateCarrierConnectionMutationInput!) {
              update_carrier_connection(input: $data) {
                connection {
                    id
                    credentials
                }
              }
            }
            """,
            operation_name="update_connection",
            variables={
                "data": {
                    "id": self.generic_carrier.id,
                    **LABEL_TEMPLATE_UPDATE_DATA["data"],
                },
            },
        )

        self.assertResponseNoErrors(response)
        print("mutation response credentials:", response.data)

        connection = providers.CarrierConnection.objects.get(
            id=self.generic_carrier.id
        )
        print("reloaded raw credentials:", connection.credentials)
        self.assertIn("label_template", connection.credentials)
        self.assertEqual(
            connection.credentials["label_template"],
            LABEL_TEMPLATE_UPDATE_DATA["data"]["credentials"]["label_template"],
        )

    def test_update_generic_connection_label_template_legacy_toplevel(self):
        """The pre-redesign UI (packages/ui/core/forms/user-carrier-list.tsx)
        sent label_template as a top-level mutation input key. Document what
        the graph layer does with that unknown key."""
        response = self.query(
            """
            mutation update_connection($data: UpdateCarrierConnectionMutationInput!) {
              update_carrier_connection(input: $data) {
                connection {
                    id
                    credentials
                }
              }
            }
            """,
            operation_name="update_connection",
            variables={
                "data": {
                    "id": self.generic_carrier.id,
                    "label_template": LABEL_TEMPLATE_UPDATE_DATA["data"][
                        "credentials"
                    ]["label_template"],
                },
            },
        )

        print("legacy-shape response:", response.data)

        if response.data.get("errors") is None:
            connection = providers.CarrierConnection.objects.get(
                id=self.generic_carrier.id
            )
            print("legacy-shape reloaded credentials:", connection.credentials)

    def test_create_generic_connection_with_blank_label_template(self):
        """Reproduce the connection create failure introduced by mapping
        object-typed credential descriptors to PlainDictField.

        When a NEW connection's carrier is selected, the dialog seeds every
        connection_fields key with `field.default || ""`
        (packages/ui/components/carrier-connection-dialog.tsx defaultCredentials
        builder). label_template has no default, so the create payload carries
        it as a blank string, and the blank value must be treated as absent
        instead of failing validation with not_a_dict.
        """
        response = self.query(
            """
            mutation create_connection($data: CreateCarrierConnectionMutationInput!) {
              create_carrier_connection(input: $data) {
                connection {
                    id
                    carrier_id
                    carrier_name
                    active
                    test_mode
                    credentials
                }
              }
            }
            """,
            operation_name="create_connection",
            variables=DIALOG_CREATE_DATA,
        )

        self.assertResponseNoErrors(response)

        connection = providers.CarrierConnection.objects.get(
            carrier_id="new-custom-carrier"
        )
        self.assertNotIn("label_template", connection.credentials)
        self.assertEqual(
            connection.credentials["display_name"], "New Custom Carrier"
        )
        self.assertEqual(
            connection.credentials["custom_carrier_name"], "new_custom_carrier"
        )

    def test_generic_connection_serializer_keeps_label_template(self):
        """Bisect the drop: feed the merged credentials dict directly to the
        generated generic connection serializer that
        CarrierConnectionModelSerializer.update re-serializes through
        (modules/core/karrio/server/providers/serializers/base.py:250-260)."""
        from karrio.server.providers.serializers.base import (
            CONNECTION_SERIALIZERS,
        )

        merged = lib.to_dict(
            {
                **self.generic_carrier.credentials,
                **LABEL_TEMPLATE_UPDATE_DATA["data"]["credentials"],
            }
        )
        result = CONNECTION_SERIALIZERS["generic"].map(data=merged).data
        print("generic serializer fields:", list(result.keys()))
        self.assertIn("label_template", result)


DIALOG_CREATE_DATA = {
    "data": {
        # Shape assembled by useCarrierConnectionForm.handleSubmit
        # (packages/hooks/user-connection.ts) for a new connection, with the
        # credentials dict the dialog's defaultCredentials builder produces
        # for generic: every connection_fields key set to `field.default || ""`,
        # display_name/custom_carrier_name filled in by the user.
        "carrier_name": "generic",
        "carrier_id": "new-custom-carrier",
        "active": True,
        "credentials": {
            "display_name": "New Custom Carrier",
            "custom_carrier_name": "new_custom_carrier",
            "account_country_code": "",
            "account_number": "",
            "metadata": {},
            "config": {},
            "label_template": "",
        },
        "config": {},
        "metadata": {},
    }
}


LABEL_TEMPLATE_UPDATE_DATA = {
    "data": {
        "credentials": {
            # Exact object the modal's onSubmit receives and the Connections
            # page nests under credentials: DEFAULT_LABEL_TEMPLATE_CONTENT
            # with the slug filled and the template body edited. Untouched
            # width/height remain the numeric defaults; shipment_sample
            # stays the initial empty object.
            "label_template": {
                "slug": "ucc_128",
                "width": 4,
                "height": 6,
                "template_type": "SVG",
                "template": (
                    "<svg xmlns='http://www.w3.org/2000/svg' width='4in' "
                    "height='6in'></svg>"
                ),
                "shipment_sample": {},
            },
        },
    }
}


SYSTEM_CONNECTIONS = {
    "data": {
        "system_connections": {
            "edges": [
                {
                    "node": {
                        "active": True,
                        "carrier_id": "dhl_universal",
                        "carrier_name": "dhl_universal",
                        "id": ANY,
                        "test_mode": False,
                    }
                },
                {
                    "node": {
                        "active": True,
                        "carrier_id": "fedex_express",
                        "carrier_name": "fedex",
                        "id": ANY,
                        "test_mode": False,
                    }
                },
            ]
        }
    }
}

USER_CONNECTIONS = {
    "data": {
        "user_connections": {
            "edges": [
                {
                    "node": {
                        "active": True,
                        "carrier_id": "custom_carrier",
                        "carrier_name": "generic",
                        "credentials": {
                            "custom_carrier_name": "Custom Carrier",
                            "display_name": "Custom Carrier Display",
                        },
                        "custom_carrier_name": "Custom Carrier",
                        "id": ANY,
                        "test_mode": False,
                    }
                },
                {
                    "node": {
                        "active": True,
                        "carrier_id": "dhl_universal",
                        "carrier_name": "dhl_universal",
                        "credentials": {
                            "consumer_key": "test",
                            "consumer_secret": "password",
                        },
                        "id": ANY,
                        "test_mode": False,
                    }
                },
                {
                    "node": {
                        "active": True,
                        "carrier_id": "fedex_express",
                        "carrier_name": "fedex",
                        "credentials": {
                            "account_number": "000000",
                            "api_key": "test",
                            "secret_key": "password",
                            "track_api_key": "test",
                            "track_secret_key": "password",
                        },
                        "id": ANY,
                        "test_mode": False,
                    }
                },
                {
                    "node": {
                        "active": True,
                        "carrier_id": "ups_package",
                        "carrier_name": "ups",
                        "credentials": {
                            "account_number": "000000",
                            "client_id": "test",
                            "client_secret": "test",
                        },
                        "id": ANY,
                        "test_mode": False,
                    }
                },
                {
                    "node": {
                        "active": True,
                        "carrier_id": "canadapost",
                        "carrier_name": "canadapost",
                        "credentials": {
                            "contract_id": "42708517",
                            "customer_number": "2004381",
                            "password": "0bfa9fcb9853d1f51ee57a",
                            "username": "6e93d53968881714",
                        },
                        "id": ANY,
                        "test_mode": False,
                    }
                },
            ]
        }
    }
}

CONNECTION_DATA = {
    "data": {
        "carrier_name": "sendle",
        "carrier_id": "sendle",
        "credentials": {
            "sendle_id": "test_sendle_id",
            "api_key": "test_api_key",
        },
    }
}

CONNECTION_RESPONSE = {
    "data": {
        "create_carrier_connection": {
            "connection": {
                "id": ANY,
                "active": True,
                "carrier_id": "sendle",
                "carrier_name": "sendle",
                "test_mode": False,
                "credentials": {
                    "api_key": "test_api_key",
                    "sendle_id": "test_sendle_id",
                    "account_country_code": None,
                },
            }
        }
    }
}

CONNECTION_UPDATE_DATA = {
    "data": {
        "carrier_id": "canadapost_updated",
        "credentials": {
            "username": "6e93d53968881714_updated",
            "customer_number": "2004381_updated",
            "contract_id": "42708517_updated",
            "password": "0bfa9fcb9853d1f51ee57a_updated",
        },
    }
}

CONNECTION_UPDATE_RESPONSE = {
    "data": {
        "update_carrier_connection": {
            "connection": {
                "carrier_id": "canadapost_updated",
                "credentials": {
                    "account_country_code": "CA",
                    "contract_id": "42708517_updated",
                    "customer_number": "2004381_updated",
                    "password": "0bfa9fcb9853d1f51ee57a_updated",
                    "username": "6e93d53968881714_updated",
                },
            }
        }
    }
}
