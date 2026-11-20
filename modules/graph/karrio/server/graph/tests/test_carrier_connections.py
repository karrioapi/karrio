import karrio.lib as lib
from unittest.mock import ANY
from karrio.server.graph.tests.base import GraphTestCase
import karrio.server.providers.models as providers


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



class TestCarrierCredentialsAreWriteOnly(GraphTestCase):
    """Any member of an organisation can read its connections, so a password,
    API key or client secret returned here reaches every member's browser.
    Secrets are accepted on write and never returned; account identifiers
    are still returned so a connection can be edited."""

    QUERY = """
        query get_connection($id: String!) {
          carrier_connection(id: $id) { id credentials }
        }
    """
    UPDATE = """
        mutation update_connection($data: UpdateCarrierConnectionMutationInput!) {
          update_carrier_connection(input: $data) { connection { credentials } }
        }
    """
    SECRETS = ["0bfa9fcb9853d1f51ee57a", "password"]

    def _credentials(self, connection):
        response = self.query(
            self.QUERY,
            operation_name="get_connection",
            variables={"id": connection.id},
        )
        self.assertResponseNoErrors(response)
        return response.data["data"]["carrier_connection"]["credentials"]

    def test_no_secret_is_returned_for_any_connection(self):
        connections = [self.carrier, self.ups_carrier, self.fedex_carrier, self.dhl_carrier]
        returned = {c.carrier_id: self._credentials(c) for c in connections}

        self.assertDictEqual(
            returned,
            {
                "canadapost": {
                    "username": "6e93d53968881714",
                    "customer_number": "2004381",
                    "contract_id": "42708517",
                },
                "ups_package": {"client_id": "test", "account_number": "000000"},
                "fedex_express": {"account_number": "000000"},
                "dhl_universal": {},
            },
        )

    def test_list_and_mutation_payloads_return_no_secret(self):
        listed = self.query(
            "query { user_connections { edges { node { credentials } } } }"
        )
        updated = self.query(
            self.UPDATE,
            operation_name="update_connection",
            variables={"data": {"id": self.carrier.id, "credentials": {"username": "new"}}},
        )

        self.assertResponseNoErrors(listed)
        self.assertResponseNoErrors(updated)
        for secret in self.SECRETS:
            self.assertNotIn(secret, str(listed.data))
            self.assertNotIn(secret, str(updated.data))

    def test_an_unlisted_credential_key_is_withheld_by_default(self):
        """A connector whose secret field is not marked sensitive, or has a
        name nobody anticipated, must not leak it."""
        self.dhl_carrier.credentials = dict(consumer_key="k", some_future_token="t")
        self.dhl_carrier.save()

        self.assertDictEqual(self._credentials(self.dhl_carrier), {})

    def test_update_without_the_secret_keeps_the_stored_one(self):
        response = self.query(
            self.UPDATE,
            operation_name="update_connection",
            variables={"data": {"id": self.carrier.id, "credentials": {"username": "new_user"}}},
        )
        self.assertResponseNoErrors(response)
        self.carrier.refresh_from_db()

        self.assertEqual(self.carrier.credentials["username"], "new_user")
        self.assertEqual(self.carrier.credentials["password"], "0bfa9fcb9853d1f51ee57a")

    def test_update_with_a_blank_or_null_secret_keeps_the_stored_one(self):
        """The edit form gets no secret back, so it sends one blank."""
        for blank in ["", None]:
            with self.subTest(blank=blank):
                response = self.query(
                    self.UPDATE,
                    operation_name="update_connection",
                    variables={
                        "data": {
                            "id": self.carrier.id,
                            "credentials": {"username": "edited", "password": blank},
                        }
                    },
                )
                self.assertResponseNoErrors(response)
                self.carrier.refresh_from_db()

                self.assertEqual(self.carrier.credentials["username"], "edited")
                self.assertEqual(self.carrier.credentials["password"], "0bfa9fcb9853d1f51ee57a")
                self.assertNotIn("0bfa9fcb9853d1f51ee57a", str(response.data))

    def test_a_blank_identifier_still_clears_it(self):
        """Only withheld secrets are kept on blank; a visible field is edited as sent."""
        response = self.query(
            self.UPDATE,
            operation_name="update_connection",
            variables={"data": {"id": self.carrier.id, "credentials": {"contract_id": ""}}},
        )
        self.assertResponseNoErrors(response)
        self.carrier.refresh_from_db()

        self.assertIsNone(self.carrier.credentials.get("contract_id"))

    def test_update_with_a_new_secret_replaces_it(self):
        response = self.query(
            self.UPDATE,
            operation_name="update_connection",
            variables={"data": {"id": self.carrier.id, "credentials": {"password": "rotated"}}},
        )
        self.assertResponseNoErrors(response)
        self.carrier.refresh_from_db()

        self.assertEqual(self.carrier.credentials["password"], "rotated")
        self.assertNotIn("rotated", str(response.data))


class TestConnectionConfigSecretsAreWriteOnly(GraphTestCase):
    """Connection ``config`` holds secrets too: SmartKargo sends
    partner_tracking_api_code as its auth header, webhook_secret verifies
    carrier webhooks. They are accepted on write and never returned to
    non-staff callers (tenant GraphQL, REST, brokered system connections);
    settings and identifiers still are, so a connection can be edited."""

    CONFIG = dict(
        primary_id="PRIMARY",
        site_id="SITE",
        partner_tracking_url="https://tracking.example.com",
        partner_tracking_api_code="partner-code-canary",
        webhook_id="wh_123",
        webhook_url="https://api.example.com/v1/connections/webhook/x/events",
        webhook_secret="webhook-secret-canary",
        some_future_token="future-canary",
        shipping_services=["smartkargo_express"],
    )
    PUBLIC = dict(
        primary_id="PRIMARY",
        site_id="SITE",
        partner_tracking_url="https://tracking.example.com",
        webhook_id="wh_123",
        webhook_url="https://api.example.com/v1/connections/webhook/x/events",
        shipping_services=["smartkargo_express"],
    )
    SECRETS = ["partner-code-canary", "webhook-secret-canary", "future-canary"]
    QUERY = """
        query get_connection($id: String!) {
          carrier_connection(id: $id) { id config }
        }
    """
    UPDATE = """
        mutation update_connection($data: UpdateCarrierConnectionMutationInput!) {
          update_carrier_connection(input: $data) { connection { config } }
        }
    """

    def setUp(self):
        super().setUp()
        from django.contrib.auth import get_user_model
        from karrio.server.user.models import Token

        # A plain member: no staff or superuser rights.
        self.member = get_user_model().objects.create_user(
            "member@example.com", "test"
        )
        self.member_token = Token.objects.create(user=self.member, test_mode=False)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.member_token.key)
        self.smartkargo = providers.CarrierConnection.objects.create(
            carrier_code="smartkargo",
            carrier_id="smartkargo",
            test_mode=False,
            created_by=self.member,
            credentials=dict(api_key="api-key-canary"),
            config=dict(self.CONFIG),
        )

    def _config(self):
        response = self.query(
            self.QUERY,
            operation_name="get_connection",
            variables={"id": self.smartkargo.id},
        )
        self.assertResponseNoErrors(response)
        return response.data["data"]["carrier_connection"]["config"]

    def _update(self, config: dict):
        response = self.query(
            self.UPDATE,
            operation_name="update_connection",
            variables={"data": {"id": self.smartkargo.id, "config": config}},
        )
        self.assertResponseNoErrors(response)
        self.smartkargo.refresh_from_db()
        return response

    def test_graphql_returns_config_settings_only(self):
        listed = self.query("query { user_connections { edges { node { config } } } }")

        self.assertDictEqual(self._config(), self.PUBLIC)
        self.assertResponseNoErrors(listed)
        for secret in self.SECRETS:
            self.assertNotIn(secret, str(listed.data))

    def test_rest_returns_config_settings_only(self):
        from django.urls import reverse

        detail = self.client.get(
            reverse(
                "karrio.server.providers:carrier-connection-details",
                kwargs=dict(pk=self.smartkargo.id),
            )
        )
        listed = self.client.get(
            reverse("karrio.server.providers:carrier-connection-list")
        )

        self.assertEqual(detail.status_code, 200)
        self.assertDictEqual(detail.json()["config"], self.PUBLIC)
        self.assertEqual(listed.status_code, 200)
        for secret in self.SECRETS:
            self.assertNotIn(secret, str(listed.json()))

    def test_brokered_system_connection_hides_platform_and_own_config_secrets(self):
        system = providers.SystemConnection.objects.create(
            carrier_code="smartkargo",
            carrier_id="smartkargo_system",
            test_mode=False,
            active=True,
            credentials=dict(api_key="system-api-key"),
            config=dict(primary_id="SYSTEM", partner_tracking_api_code="platform-code-canary"),
        )
        providers.BrokeredConnection.objects.create(
            system_connection=system,
            created_by=self.member,
            config_overrides=dict(site_id="MINE", webhook_secret="own-secret-canary"),
        )

        response = self.query(
            "query { system_connections { edges { node { carrier_id config } } } }"
        )

        self.assertResponseNoErrors(response)
        configs = {
            edge["node"]["carrier_id"]: edge["node"]["config"]
            for edge in response.data["data"]["system_connections"]["edges"]
        }
        self.assertDictEqual(
            configs["smartkargo_system"], dict(primary_id="SYSTEM", site_id="MINE")
        )
        self.assertNotIn("platform-code-canary", str(response.data))
        self.assertNotIn("own-secret-canary", str(response.data))

    def test_update_with_a_blank_config_secret_keeps_the_stored_one(self):
        """The edit form gets no secret back, so it sends it blank."""
        response = self._update(
            dict(partner_tracking_api_code="", webhook_secret="", site_id="EDITED")
        )

        self.assertEqual(self.smartkargo.config["partner_tracking_api_code"], "partner-code-canary")
        self.assertEqual(self.smartkargo.config["webhook_secret"], "webhook-secret-canary")
        self.assertEqual(self.smartkargo.config["site_id"], "EDITED")
        for secret in self.SECRETS:
            self.assertNotIn(secret, str(response.data))

    def test_update_with_a_new_config_secret_replaces_it_and_null_removes_it(self):
        self._update(dict(partner_tracking_api_code="rotated"))
        self.assertEqual(self.smartkargo.config["partner_tracking_api_code"], "rotated")

        self._update(dict(partner_tracking_api_code=None))
        self.assertNotIn("partner_tracking_api_code", self.smartkargo.config)

    def test_a_blank_config_setting_still_clears_it(self):
        self._update(dict(site_id=""))

        self.assertNotIn("site_id", self.smartkargo.config)

    def test_webhook_disconnect_still_clears_the_webhook_secret(self):
        from django.urls import reverse

        response = self.client.post(
            reverse(
                "karrio.server.providers:connection-webhook-disconnect",
                kwargs=dict(pk=self.smartkargo.id),
            )
        )
        self.smartkargo.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("webhook_secret", self.smartkargo.config)
        self.assertNotIn("webhook_id", self.smartkargo.config)

    def test_a_blank_brokered_override_secret_keeps_the_stored_one(self):
        system = providers.SystemConnection.objects.create(
            carrier_code="smartkargo",
            carrier_id="smartkargo_system",
            test_mode=False,
            active=True,
            credentials=dict(api_key="system-api-key"),
            config=dict(partner_tracking_api_code="platform-code-canary"),
        )
        brokered = providers.BrokeredConnection.objects.create(
            system_connection=system,
            created_by=self.member,
            config_overrides=dict(partner_tracking_api_code="own-code"),
        )

        response = self.query(
            """
            mutation update($data: SystemCarrierMutationInput!) {
              mutate_system_connection(input: $data) { carrier { id } }
            }
            """,
            operation_name="update",
            variables={"data": {"id": system.id, "config": {"partner_tracking_api_code": ""}}},
        )
        self.assertResponseNoErrors(response)
        brokered.refresh_from_db()

        self.assertEqual(brokered.config_overrides["partner_tracking_api_code"], "own-code")


class TestConnectionConfigClassification(GraphTestCase):
    """PUBLIC_CONFIG_FIELDS is an allowlist: a config option missing from it
    is never returned, so the connection editor would show a default and a
    save could overwrite the stored value. Every option a connector declares
    must therefore be classified on purpose, as public or as secret."""

    def test_every_declared_config_option_is_public_or_secret(self):
        import karrio.references as references
        import karrio.core.units as sdk_units

        declared = {
            "sdk": {option.name for option in sdk_units.ConnectionConfigOption},
            **{
                carrier: {option.name for option in metadata["connection_configs"]}
                for carrier, metadata in references.PROVIDERS.items()
                if metadata.get("connection_configs") is not None
            },
        }
        misclassified = {
            carrier: sorted(
                key
                for key in keys
                if (key in providers.PUBLIC_CONFIG_FIELDS)
                == (key in providers.SECRET_CONFIG_FIELDS)
            )
            for carrier, keys in declared.items()
        }

        self.assertGreater(len(declared), 20)
        self.assertEqual(
            {carrier: keys for carrier, keys in misclassified.items() if keys}, {}
        )
        self.assertEqual(providers.PUBLIC_CONFIG_FIELDS & providers.SECRET_CONFIG_FIELDS, set())
        self.assertIn("partner_tracking_api_code", declared["smartkargo"])
        self.assertIn("partner_tracking_api_code", providers.SECRET_CONFIG_FIELDS)


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
                        "carrier_id": "dhl_universal",
                        "carrier_name": "dhl_universal",
                        "credentials": {},
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
                    "username": "6e93d53968881714_updated",
                },
            }
        }
    }
}
