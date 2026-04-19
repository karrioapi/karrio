import karrio.server.providers.models as providers
from django.contrib.auth import get_user_model
from karrio.server.admin.tests.base import AdminGraphTestCase


class TestAdminCarrierConnections(AdminGraphTestCase):
    """Tests for Admin Carrier Connection queries and mutations.

    These tests ensure that the admin GraphQL schema correctly queries
    CarrierConnection and SystemConnection models after the architecture
    refactoring that removed the `user_carriers` and `system_carriers` managers.
    """

    def setUp(self):
        super().setUp()

        # Create a user-owned carrier connection (CarrierConnection)
        self.user_connection = providers.CarrierConnection.objects.create(
            carrier_code="fedex",
            carrier_id="fedex_user_account",
            credentials={"api_key": "test_key", "password": "test_pass"},
            test_mode=False,
            active=True,
            created_by=self.user,
        )

        # Create a system connection (SystemConnection) with a realistic
        # admin-set config so we can assert the config resolver exposes it
        # on the admin graph (it's stripped on the tenant graph).
        self.system_connection = providers.SystemConnection.objects.create(
            carrier_code="ups",
            carrier_id="ups_system_account",
            credentials={"api_key": "system_key"},
            test_mode=False,
            active=True,
            config={
                "label_type": "PDF",
                "default_billing_number": "11111111110000",
                "service_billing_numbers": [
                    {"id": "sbn_a", "service": "dhl_parcel_de_paket", "billing_number": "22222222220101"},
                ],
            },
        )

    def test_query_system_carrier_connections(self):
        """Test querying system carrier connections through admin API."""
        response = self.query(
            """
            query get_system_carrier_connections {
              system_carrier_connections {
                edges {
                  node {
                    id
                    carrier_id
                    carrier_name
                    test_mode
                  }
                }
              }
            }
            """,
            operation_name="get_system_carrier_connections",
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["system_carrier_connections"]["edges"]
        self.assertGreaterEqual(len(edges), 1)
        connection_ids = [e["node"]["carrier_id"] for e in edges]
        self.assertIn("ups_system_account", connection_ids)

    def test_query_single_system_connection(self):
        """Test querying a specific system connection by ID."""
        response = self.query(
            """
            query get_system_carrier_connection($id: String!) {
              system_carrier_connection(id: $id) {
                id
                carrier_id
                carrier_name
              }
            }
            """,
            operation_name="get_system_carrier_connection",
            variables={"id": self.system_connection.id},
        )

        self.assertResponseNoErrors(response)
        connection = response.data["data"]["system_carrier_connection"]
        self.assertEqual(connection["carrier_id"], "ups_system_account")
        self.assertEqual(connection["carrier_name"], "ups")

    def test_admin_graph_returns_system_connection_config(self):
        """Admin graph must expose the raw SystemConnection config so staff can
        manage billing numbers. (The tenant graph strips it — see base types.)"""
        response = self.query(
            """
            query q($id: String!) {
              system_carrier_connection(id: $id) { config credentials }
            }
            """,
            operation_name="q",
            variables={"id": self.system_connection.id},
        )
        self.assertResponseNoErrors(response)
        conn = response.data["data"]["system_carrier_connection"]
        self.assertIsNotNone(conn["config"])
        self.assertEqual(conn["config"]["default_billing_number"], "11111111110000")
        self.assertEqual(
            conn["config"]["service_billing_numbers"][0]["billing_number"],
            "22222222220101",
        )

    def test_create_system_carrier_connection(self):
        """Test creating a system carrier connection through admin API."""
        response = self.query(
            """
            mutation create_system_connection($data: CreateConnectionMutationInput!) {
              create_system_carrier_connection(input: $data) {
                connection {
                  id
                  carrier_id
                  carrier_name
                  active
                }
              }
            }
            """,
            operation_name="create_system_connection",
            variables={
                "data": {
                    "carrier_name": "usps",
                    "carrier_id": "usps_system_account",
                    "credentials": {
                        "client_id": "test_client_id",
                        "client_secret": "test_client_secret",
                    },
                    "active": True,
                }
            },
        )

        self.assertResponseNoErrors(response)
        connection = response.data["data"]["create_system_carrier_connection"]["connection"]
        self.assertEqual(connection["carrier_id"], "usps_system_account")
        self.assertEqual(connection["carrier_name"], "usps")
        self.assertTrue(connection["active"])

    def test_update_system_carrier_connection(self):
        """Test updating a system carrier connection through admin API."""
        response = self.query(
            """
            mutation update_system_connection($data: UpdateConnectionMutationInput!) {
              update_system_carrier_connection(input: $data) {
                connection {
                  id
                  carrier_id
                }
              }
            }
            """,
            operation_name="update_system_connection",
            variables={
                "data": {
                    "id": self.system_connection.id,
                    "carrier_id": "ups_system_updated",
                }
            },
        )

        self.assertResponseNoErrors(response)
        connection = response.data["data"]["update_system_carrier_connection"]["connection"]
        self.assertEqual(connection["carrier_id"], "ups_system_updated")

    def test_delete_system_connection(self):
        """Test deleting a system connection through admin API."""
        # Create a connection to delete
        to_delete = providers.SystemConnection.objects.create(
            carrier_code="purolator",
            carrier_id="purolator_to_delete",
            credentials={"api_key": "delete_key"},
            test_mode=False,
            active=True,
        )

        response = self.query(
            """
            mutation delete_connection($data: DeleteConnectionMutationInput!) {
              delete_system_carrier_connection(input: $data) {
                id
              }
            }
            """,
            operation_name="delete_connection",
            variables={"data": {"id": to_delete.id}},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data["data"]["delete_system_carrier_connection"]["id"],
            to_delete.id,
        )
        self.assertFalse(providers.SystemConnection.objects.filter(id=to_delete.id).exists())


class TestAdminBrokeredConnections(AdminGraphTestCase):
    """Tests for BrokeredConnection edge cases.

    BrokeredConnections are user-specific references to SystemConnections,
    allowing users to access system-level carrier accounts with optional
    configuration overrides.
    """

    def setUp(self):
        super().setUp()

        # Create a system connection
        self.system_connection = providers.SystemConnection.objects.create(
            carrier_code="fedex",
            carrier_id="fedex_system",
            credentials={"api_key": "system_key", "account_number": "123456789"},
            test_mode=False,
            active=True,
        )

    def test_create_brokered_connection(self):
        """Test creating a brokered connection linking user to system connection."""
        brokered = providers.BrokeredConnection.objects.create(
            system_connection=self.system_connection,
            config_overrides={"account_number": "999999999"},
            is_enabled=True,
            created_by=self.user,
        )

        # Verify the brokered connection links correctly
        self.assertEqual(brokered.system_connection, self.system_connection)
        self.assertEqual(brokered.config_overrides.get("account_number"), "999999999")
        # Brokered connection inherits carrier_code from system connection
        self.assertEqual(brokered.carrier_code, "fedex")

    def test_brokered_connection_inherits_credentials(self):
        """Test that brokered connections inherit credentials from system connection."""
        brokered = providers.BrokeredConnection.objects.create(
            system_connection=self.system_connection,
            is_enabled=True,
            created_by=self.user,
        )

        # The brokered connection should inherit system credentials
        self.assertEqual(brokered.system_connection.credentials.get("api_key"), "system_key")

    def test_brokered_connection_with_config_overrides(self):
        """Test brokered connection config overrides merge with system config."""
        brokered = providers.BrokeredConnection.objects.create(
            system_connection=self.system_connection,
            config_overrides={
                "account_number": "override_account",
                "meter_number": "override_meter",
            },
            is_enabled=True,
            created_by=self.user,
        )

        self.assertEqual(brokered.config_overrides.get("account_number"), "override_account")
        self.assertEqual(brokered.config_overrides.get("meter_number"), "override_meter")

    def test_brokered_connection_deletion_preserves_system(self):
        """Test that deleting brokered connection does not delete system connection."""
        brokered = providers.BrokeredConnection.objects.create(
            system_connection=self.system_connection,
            is_enabled=True,
            created_by=self.user,
        )
        brokered_id = brokered.id
        system_id = self.system_connection.id

        brokered.delete()

        # Brokered connection should be deleted
        self.assertFalse(providers.BrokeredConnection.objects.filter(id=brokered_id).exists())
        # System connection should still exist
        self.assertTrue(providers.SystemConnection.objects.filter(id=system_id).exists())

    def test_system_connection_deletion_cascades_to_brokered(self):
        """Test that deleting system connection cascades to brokered connections."""
        brokered = providers.BrokeredConnection.objects.create(
            system_connection=self.system_connection,
            is_enabled=True,
            created_by=self.user,
        )
        brokered_id = brokered.id

        self.system_connection.delete()

        # Brokered connection should also be deleted (cascade)
        self.assertFalse(providers.BrokeredConnection.objects.filter(id=brokered_id).exists())

    def test_multiple_users_can_have_brokered_connections_to_same_system(self):
        """Test that multiple users can create brokered connections to same system."""
        # Create another user
        other_user = get_user_model().objects.create_user(email="other@example.com", password="test")

        # Both users create brokered connections to same system
        brokered1 = providers.BrokeredConnection.objects.create(
            system_connection=self.system_connection,
            config_overrides={"account_number": "user1_account"},
            is_enabled=True,
            created_by=self.user,
        )
        brokered2 = providers.BrokeredConnection.objects.create(
            system_connection=self.system_connection,
            config_overrides={"account_number": "user2_account"},
            is_enabled=True,
            created_by=other_user,
        )

        # Both should exist with different overrides
        self.assertNotEqual(brokered1.id, brokered2.id)
        self.assertEqual(brokered1.config_overrides.get("account_number"), "user1_account")
        self.assertEqual(brokered2.config_overrides.get("account_number"), "user2_account")

    def test_brokered_connection_inherits_test_mode(self):
        """Test that brokered connection inherits test_mode from system connection."""
        # System connection is in test_mode=False (set in setUp)
        self.assertFalse(self.system_connection.test_mode)

        # Brokered connection inherits test_mode from system
        brokered = providers.BrokeredConnection.objects.create(
            system_connection=self.system_connection,
            is_enabled=True,
            created_by=self.user,
        )

        # test_mode is inherited from system connection
        self.assertEqual(brokered.test_mode, self.system_connection.test_mode)
        self.assertFalse(brokered.test_mode)
