import json
import dataclasses
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase as BaseAPITestCase, APIClient

from karrio.server.user.models import Token
import karrio.server.providers.models as providers


@dataclasses.dataclass
class Result:
    data: dict = None
    status_code: str = None


class AdminGraphTestCase(BaseAPITestCase):
    """Base test case for admin GraphQL tests."""

    def setUp(self) -> None:
        self.maxDiff = None

        # Setup superuser for admin access
        self.user = get_user_model().objects.create_superuser(
            "admin@example.com", "test"
        )
        self.user.is_staff = True
        self.user.save()

        self.token = Token.objects.create(user=self.user, test_mode=False)

        # Create organization for multi-org support (if enabled)
        from django.conf import settings

        if settings.MULTI_ORGANIZATIONS:
            from karrio.server.orgs.models import Organization, TokenLink

            self.organization = Organization.objects.create(
                name="Test Organization", slug="test-org"
            )
            owner = self.organization.add_user(self.user, is_admin=True)
            self.organization.change_owner(owner)
            self.organization.save()

            TokenLink.objects.create(item=self.token, org=self.organization)

        # Setup API client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def query(
        self,
        query: str,
        operation_name: str = None,
        variables: dict = None,
    ) -> Result:
        url = reverse("karrio.server.admin:admin-graph")
        data = dict(
            query=query,
            variables=variables,
            operation_name=operation_name,
        )

        response = self.client.post(url, data)

        return Result(
            status_code=response.status_code,
            data=json.loads(response.content),
        )

    def assertResponseNoErrors(self, result: Result):
        if result.status_code != status.HTTP_200_OK:
            self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertIsNone(result.data.get("errors"))


class TestAdminRateSheets(AdminGraphTestCase):
    """Tests for Admin Rate Sheet CRUD operations."""

    def setUp(self):
        super().setUp()

        # Create a test rate sheet with shared zones and surcharges
        # Using dhl_parcel_de which supports ratesheets (not carriers with live rates like ups/fedex)
        self.rate_sheet = providers.RateSheet.objects.create(
            name="Admin Test Rate Sheet",
            carrier_name="dhl_parcel_de",
            slug="admin_test_rate_sheet",
            is_system=True,
            zones=[
                {
                    "id": "zone_1",
                    "label": "Zone 1",
                    "cities": ["Berlin", "Munich"],
                    "country_codes": ["DE"],
                }
            ],
            surcharges=[
                {
                    "id": "surch_fuel",
                    "name": "Fuel Surcharge",
                    "amount": 10.0,
                    "surcharge_type": "percentage",
                    "active": True,
                }
            ],
            created_by=self.user,
        )

        # Create a test service
        self.service = providers.ServiceLevel.objects.create(
            service_name="DHL Parcel DE Paket",
            service_code="dhl_parcel_de_paket",
            carrier_service_code="V01PAK",
            currency="EUR",
            active=True,
            zone_ids=["zone_1"],
            surcharge_ids=["surch_fuel"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

        # Update service_rates with actual service ID
        self.rate_sheet.service_rates = [
            {
                "service_id": self.service.id,
                "zone_id": "zone_1",
                "rate": 10.00,
                "cost": 8.00,
            }
        ]
        self.rate_sheet.save()

    def test_query_rate_sheets(self):
        """Test querying all rate sheets through admin API."""
        response = self.query(
            """
            query get_rate_sheets {
              rate_sheets {
                edges {
                  node {
                    id
                    name
                    carrier_name
                    slug
                    zones {
                      id
                      label
                    }
                    surcharges {
                      id
                      name
                    }
                    services {
                      id
                      service_name
                    }
                  }
                }
              }
            }
            """,
            operation_name="get_rate_sheets",
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["rate_sheets"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "Admin Test Rate Sheet")

    def test_create_rate_sheet(self):
        """Test creating a new rate sheet through admin API."""
        response = self.query(
            """
            mutation create_rate_sheet($data: CreateRateSheetMutationInput!) {
              create_rate_sheet(input: $data) {
                rate_sheet {
                  id
                  name
                  carrier_name
                  zones {
                    id
                    label
                  }
                  services {
                    id
                    service_name
                  }
                }
              }
            }
            """,
            operation_name="create_rate_sheet",
            variables={
                "data": {
                    "name": "New Admin Rate Sheet",
                    "carrier_name": "dhl_parcel_de",
                    "zones": [
                        {
                            "label": "New Zone",
                            "country_codes": ["DE", "AT"],
                        }
                    ],
                    "services": [
                        {
                            "service_name": "DHL Europaket",
                            "service_code": "dhl_parcel_de_europaket",
                            "carrier_service_code": "V54EPAK",
                            "currency": "EUR",
                        }
                    ],
                }
            },
        )

        self.assertResponseNoErrors(response)
        rate_sheet = response.data["data"]["create_rate_sheet"]["rate_sheet"]
        self.assertEqual(rate_sheet["name"], "New Admin Rate Sheet")
        self.assertEqual(rate_sheet["carrier_name"], "dhl_parcel_de")
        self.assertEqual(len(rate_sheet["zones"]), 1)
        self.assertEqual(len(rate_sheet["services"]), 1)

    def test_update_rate_sheet(self):
        """Test updating a rate sheet through admin API."""
        response = self.query(
            """
            mutation update_rate_sheet($data: UpdateRateSheetMutationInput!) {
              update_rate_sheet(input: $data) {
                rate_sheet {
                  id
                  name
                }
              }
            }
            """,
            operation_name="update_rate_sheet",
            variables={
                "data": {
                    "id": self.rate_sheet.id,
                    "name": "Updated Admin Rate Sheet",
                }
            },
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data["data"]["update_rate_sheet"]["rate_sheet"]["name"],
            "Updated Admin Rate Sheet",
        )

    def test_delete_rate_sheet(self):
        """Test deleting a rate sheet through admin API."""
        # Create a rate sheet to delete
        new_sheet = providers.RateSheet.objects.create(
            name="To Be Deleted",
            carrier_name="ups",
            slug="to_be_deleted",
            is_system=True,
            created_by=self.user,
        )

        response = self.query(
            """
            mutation delete_rate_sheet($data: DeleteMutationInput!) {
              delete_rate_sheet(input: $data) {
                id
              }
            }
            """,
            operation_name="delete_rate_sheet",
            variables={"data": {"id": new_sheet.id}},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["data"]["delete_rate_sheet"]["id"], new_sheet.id)
        self.assertFalse(providers.RateSheet.objects.filter(id=new_sheet.id).exists())


class TestAdminRateSheetZones(AdminGraphTestCase):
    """Tests for admin shared zone CRUD operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Zone Test Sheet",
            carrier_name="ups",
            slug="zone_test_sheet",
            is_system=True,
            zones=[
                {
                    "id": "zone_1",
                    "label": "Zone 1",
                    "cities": ["New York", "Los Angeles"],
                    "country_codes": ["US"],
                }
            ],
            created_by=self.user,
        )

    def test_add_shared_zone(self):
        """Test adding a new shared zone through admin API."""
        response = self.query(
            """
            mutation add_zone($data: AddSharedZoneMutationInput!) {
              add_shared_zone(input: $data) {
                rate_sheet {
                  id
                  zones {
                    id
                    label
                    country_codes
                  }
                }
              }
            }
            """,
            operation_name="add_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone": {
                        "label": "Zone 2",
                        "country_codes": ["CA", "MX"],
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        zones = response.data["data"]["add_shared_zone"]["rate_sheet"]["zones"]
        self.assertEqual(len(zones), 2)
        self.assertEqual(zones[1]["label"], "Zone 2")
        self.assertEqual(zones[1]["country_codes"], ["CA", "MX"])

    def test_update_shared_zone(self):
        """Test updating an existing shared zone through admin API."""
        response = self.query(
            """
            mutation update_zone($data: UpdateSharedZoneMutationInput!) {
              update_shared_zone(input: $data) {
                rate_sheet {
                  zones {
                    id
                    label
                    country_codes
                  }
                }
              }
            }
            """,
            operation_name="update_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone_id": "zone_1",
                    "zone": {
                        "label": "Updated Zone 1",
                        "country_codes": ["US", "CA"],
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        zones = response.data["data"]["update_shared_zone"]["rate_sheet"]["zones"]
        self.assertEqual(zones[0]["label"], "Updated Zone 1")
        self.assertEqual(zones[0]["country_codes"], ["US", "CA"])

    def test_delete_shared_zone(self):
        """Test deleting a shared zone through admin API."""
        # Add a second zone first
        self.rate_sheet.zones.append(
            {
                "id": "zone_2",
                "label": "Zone 2",
                "country_codes": ["CA"],
            }
        )
        self.rate_sheet.save()

        response = self.query(
            """
            mutation delete_zone($data: DeleteSharedZoneMutationInput!) {
              delete_shared_zone(input: $data) {
                rate_sheet {
                  zones {
                    id
                    label
                  }
                }
              }
            }
            """,
            operation_name="delete_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone_id": "zone_2",
                },
            },
        )

        self.assertResponseNoErrors(response)
        zones = response.data["data"]["delete_shared_zone"]["rate_sheet"]["zones"]
        self.assertEqual(len(zones), 1)
        self.assertEqual(zones[0]["id"], "zone_1")


class TestAdminRateSheetSurcharges(AdminGraphTestCase):
    """Tests for admin shared surcharge CRUD operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Surcharge Test Sheet",
            carrier_name="ups",
            slug="surcharge_test_sheet",
            is_system=True,
            surcharges=[
                {
                    "id": "surch_1",
                    "name": "Fuel Surcharge",
                    "amount": 10.0,
                    "surcharge_type": "percentage",
                    "active": True,
                }
            ],
            created_by=self.user,
        )

    def test_add_shared_surcharge(self):
        """Test adding a new shared surcharge through admin API."""
        response = self.query(
            """
            mutation add_surcharge($data: AddSharedSurchargeMutationInput!) {
              add_shared_surcharge(input: $data) {
                rate_sheet {
                  id
                  surcharges {
                    id
                    name
                    amount
                    surcharge_type
                  }
                }
              }
            }
            """,
            operation_name="add_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge": {
                        "name": "Handling Fee",
                        "amount": 5.0,
                        "surcharge_type": "amount",
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["add_shared_surcharge"]["rate_sheet"][
            "surcharges"
        ]
        self.assertEqual(len(surcharges), 2)
        self.assertEqual(surcharges[1]["name"], "Handling Fee")
        self.assertEqual(surcharges[1]["amount"], 5.0)

    def test_update_shared_surcharge(self):
        """Test updating an existing shared surcharge through admin API."""
        response = self.query(
            """
            mutation update_surcharge($data: UpdateSharedSurchargeMutationInput!) {
              update_shared_surcharge(input: $data) {
                rate_sheet {
                  surcharges {
                    id
                    name
                    amount
                  }
                }
              }
            }
            """,
            operation_name="update_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge_id": "surch_1",
                    "surcharge": {
                        "name": "Updated Fuel Surcharge",
                        "amount": 15.0,
                    },
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["update_shared_surcharge"]["rate_sheet"][
            "surcharges"
        ]
        self.assertEqual(surcharges[0]["name"], "Updated Fuel Surcharge")
        self.assertEqual(surcharges[0]["amount"], 15.0)

    def test_delete_shared_surcharge(self):
        """Test deleting a shared surcharge through admin API."""
        # Add a second surcharge first
        self.rate_sheet.surcharges.append(
            {
                "id": "surch_2",
                "name": "Handling Fee",
                "amount": 5.0,
                "surcharge_type": "amount",
            }
        )
        self.rate_sheet.save()

        response = self.query(
            """
            mutation delete_surcharge($data: DeleteSharedSurchargeMutationInput!) {
              delete_shared_surcharge(input: $data) {
                rate_sheet {
                  surcharges {
                    id
                    name
                  }
                }
              }
            }
            """,
            operation_name="delete_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge_id": "surch_2",
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["delete_shared_surcharge"]["rate_sheet"][
            "surcharges"
        ]
        self.assertEqual(len(surcharges), 1)
        self.assertEqual(surcharges[0]["id"], "surch_1")

    def test_batch_update_surcharges(self):
        """Test batch updating surcharges through admin API."""
        response = self.query(
            """
            mutation batch_surcharges($data: BatchUpdateSurchargesMutationInput!) {
              batch_update_surcharges(input: $data) {
                rate_sheet {
                  surcharges {
                    id
                    name
                    amount
                  }
                }
              }
            }
            """,
            operation_name="batch_surcharges",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharges": [
                        {
                            "id": "surch_1",
                            "name": "Updated Fuel",
                            "amount": 12.0,
                            "surcharge_type": "percentage",
                        },
                        {
                            "id": "surch_new",
                            "name": "New Surcharge",
                            "amount": 3.0,
                            "surcharge_type": "amount",
                        },
                    ],
                },
            },
        )

        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["batch_update_surcharges"]["rate_sheet"][
            "surcharges"
        ]
        self.assertEqual(len(surcharges), 2)


class TestAdminServiceRates(AdminGraphTestCase):
    """Tests for admin service rate operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Service Rate Test Sheet",
            carrier_name="ups",
            slug="service_rate_test_sheet",
            is_system=True,
            zones=[
                {"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]},
                {"id": "zone_2", "label": "Zone 2", "country_codes": ["CA"]},
            ],
            service_rates=[],
            created_by=self.user,
        )

        self.service = providers.ServiceLevel.objects.create(
            service_name="UPS Standard",
            service_code="ups_standard",
            carrier_service_code="11",
            currency="USD",
            zone_ids=["zone_1", "zone_2"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

    def test_update_service_rate(self):
        """Test updating a service rate through admin API."""
        response = self.query(
            """
            mutation update_rate($data: UpdateServiceRateMutationInput!) {
              update_service_rate(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    rate
                    cost
                  }
                }
              }
            }
            """,
            operation_name="update_rate",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_id": "zone_1",
                    "rate": 15.99,
                    "cost": 12.00,
                },
            },
        )

        self.assertResponseNoErrors(response)
        rates = response.data["data"]["update_service_rate"]["rate_sheet"][
            "service_rates"
        ]
        self.assertEqual(len(rates), 1)
        self.assertEqual(rates[0]["rate"], 15.99)
        self.assertEqual(rates[0]["cost"], 12.00)

    def test_batch_update_service_rates(self):
        """Test batch updating service rates through admin API."""
        response = self.query(
            """
            mutation batch_rates($data: BatchUpdateServiceRatesMutationInput!) {
              batch_update_service_rates(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    rate
                    cost
                  }
                }
              }
            }
            """,
            operation_name="batch_rates",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "rates": [
                        {
                            "service_id": self.service.id,
                            "zone_id": "zone_1",
                            "rate": 10.99,
                            "cost": 8.00,
                        },
                        {
                            "service_id": self.service.id,
                            "zone_id": "zone_2",
                            "rate": 15.99,
                            "cost": 12.00,
                        },
                    ],
                },
            },
        )

        self.assertResponseNoErrors(response)
        rates = response.data["data"]["batch_update_service_rates"]["rate_sheet"][
            "service_rates"
        ]
        self.assertEqual(len(rates), 2)


class TestAdminServiceAssignments(AdminGraphTestCase):
    """Tests for admin service zone/surcharge assignment operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Assignment Test Sheet",
            carrier_name="ups",
            slug="assignment_test_sheet",
            is_system=True,
            zones=[
                {"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]},
                {"id": "zone_2", "label": "Zone 2", "country_codes": ["CA"]},
            ],
            surcharges=[
                {
                    "id": "surch_1",
                    "name": "Fuel",
                    "amount": 10.0,
                    "surcharge_type": "percentage",
                },
                {
                    "id": "surch_2",
                    "name": "Handling",
                    "amount": 5.0,
                    "surcharge_type": "amount",
                },
            ],
            created_by=self.user,
        )

        self.service = providers.ServiceLevel.objects.create(
            service_name="UPS Standard",
            service_code="ups_standard",
            carrier_service_code="11",
            currency="USD",
            zone_ids=["zone_1"],
            surcharge_ids=["surch_1"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

    def test_update_service_zone_ids(self):
        """Test updating service zone assignments through admin API."""
        response = self.query(
            """
            mutation update_zones($data: UpdateServiceZoneIdsMutationInput!) {
              update_service_zone_ids(input: $data) {
                rate_sheet {
                  services {
                    id
                    zone_ids
                  }
                }
              }
            }
            """,
            operation_name="update_zones",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_ids": ["zone_1", "zone_2"],
                },
            },
        )

        self.assertResponseNoErrors(response)
        services = response.data["data"]["update_service_zone_ids"]["rate_sheet"][
            "services"
        ]
        self.assertEqual(services[0]["zone_ids"], ["zone_1", "zone_2"])

    def test_update_service_surcharge_ids(self):
        """Test updating service surcharge assignments through admin API."""
        response = self.query(
            """
            mutation update_surcharges($data: UpdateServiceSurchargeIdsMutationInput!) {
              update_service_surcharge_ids(input: $data) {
                rate_sheet {
                  services {
                    id
                    surcharge_ids
                  }
                }
              }
            }
            """,
            operation_name="update_surcharges",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "surcharge_ids": ["surch_1", "surch_2"],
                },
            },
        )

        self.assertResponseNoErrors(response)
        services = response.data["data"]["update_service_surcharge_ids"]["rate_sheet"][
            "services"
        ]
        self.assertEqual(services[0]["surcharge_ids"], ["surch_1", "surch_2"])


class TestAdminRateSheetService(AdminGraphTestCase):
    """Tests for admin rate sheet service operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.RateSheet.objects.create(
            name="Service Test Sheet",
            carrier_name="ups",
            slug="service_test_sheet",
            is_system=True,
            created_by=self.user,
        )

        self.service = providers.ServiceLevel.objects.create(
            service_name="UPS Standard",
            service_code="ups_standard",
            carrier_service_code="11",
            currency="USD",
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

    def test_delete_rate_sheet_service(self):
        """Test deleting a service from a rate sheet through admin API."""
        response = self.query(
            """
            mutation delete_service($data: DeleteRateSheetServiceMutationInput!) {
              delete_rate_sheet_service(input: $data) {
                rate_sheet {
                  services {
                    id
                  }
                }
              }
            }
            """,
            operation_name="delete_service",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                },
            },
        )

        self.assertResponseNoErrors(response)
        services = response.data["data"]["delete_rate_sheet_service"]["rate_sheet"][
            "services"
        ]
        self.assertEqual(len(services), 0)
        self.assertFalse(
            providers.ServiceLevel.objects.filter(id=self.service.id).exists()
        )


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

        # Create a system connection (SystemConnection)
        self.system_connection = providers.SystemConnection.objects.create(
            carrier_code="ups",
            carrier_id="ups_system_account",
            credentials={"api_key": "system_key"},
            test_mode=False,
            active=True,
        )

    def test_query_account_carrier_connections(self):
        """Test querying user/account carrier connections through admin API."""
        response = self.query(
            """
            query get_carrier_connections {
              carrier_connections {
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
            operation_name="get_carrier_connections",
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["carrier_connections"]["edges"]
        # Should return user-owned connections
        self.assertGreaterEqual(len(edges), 1)
        connection_ids = [e["node"]["carrier_id"] for e in edges]
        self.assertIn("fedex_user_account", connection_ids)

    def test_query_single_account_connection(self):
        """Test querying a specific account connection by ID."""
        response = self.query(
            """
            query get_carrier_connection($id: String!) {
              carrier_connection(id: $id) {
                id
                carrier_id
                carrier_name
              }
            }
            """,
            operation_name="get_carrier_connection",
            variables={"id": self.user_connection.id},
        )

        self.assertResponseNoErrors(response)
        connection = response.data["data"]["carrier_connection"]
        self.assertEqual(connection["carrier_id"], "fedex_user_account")
        self.assertEqual(connection["carrier_name"], "fedex")

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
        connection = response.data["data"]["create_system_carrier_connection"][
            "connection"
        ]
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
        connection = response.data["data"]["update_system_carrier_connection"][
            "connection"
        ]
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
        self.assertFalse(
            providers.SystemConnection.objects.filter(id=to_delete.id).exists()
        )

    def test_system_connection_not_in_account_connections(self):
        """Ensure system connections are not returned in account connections query."""
        response = self.query(
            """
            query get_carrier_connections {
              carrier_connections {
                edges {
                  node {
                    id
                    carrier_id
                  }
                }
              }
            }
            """,
            operation_name="get_carrier_connections",
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["carrier_connections"]["edges"]
        connection_ids = [e["node"]["carrier_id"] for e in edges]
        # System connection should NOT appear in carrier connections (user/org owned)
        self.assertNotIn("ups_system_account", connection_ids)


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
        self.assertEqual(
            brokered.system_connection.credentials.get("api_key"), "system_key"
        )

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

        self.assertEqual(
            brokered.config_overrides.get("account_number"), "override_account"
        )
        self.assertEqual(
            brokered.config_overrides.get("meter_number"), "override_meter"
        )

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
        self.assertFalse(
            providers.BrokeredConnection.objects.filter(id=brokered_id).exists()
        )
        # System connection should still exist
        self.assertTrue(
            providers.SystemConnection.objects.filter(id=system_id).exists()
        )

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
        self.assertFalse(
            providers.BrokeredConnection.objects.filter(id=brokered_id).exists()
        )

    def test_multiple_users_can_have_brokered_connections_to_same_system(self):
        """Test that multiple users can create brokered connections to same system."""
        # Create another user
        other_user = get_user_model().objects.create_user(
            email="other@example.com", password="test"
        )

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
        self.assertEqual(
            brokered1.config_overrides.get("account_number"), "user1_account"
        )
        self.assertEqual(
            brokered2.config_overrides.get("account_number"), "user2_account"
        )

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
