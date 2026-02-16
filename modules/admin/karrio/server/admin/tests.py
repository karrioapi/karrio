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


class TestAdminMarkups(AdminGraphTestCase):
    """Tests for Admin Markup CRUD operations including meta field."""

    def setUp(self):
        super().setUp()
        import karrio.server.pricing.models as pricing

        self.pricing = pricing

        # Create a test markup with meta field
        self.markup = pricing.Markup.objects.create(
            name="Brokerage Fee - Scale",
            amount=0.85,
            markup_type="PERCENTAGE",
            active=True,
            is_visible=True,
            meta={
                "type": "brokerage-fee",
                "plan": "scale",
                "show_in_preview": True,
            },
            metadata={"notes": "Default brokerage fee"},
        )

    def test_query_markups(self):
        """Test querying all markups through admin API."""
        response = self.query(
            """
            query get_markups {
              markups {
                edges {
                  node {
                    id
                    name
                    active
                    amount
                    markup_type
                    is_visible
                    meta
                    metadata
                    carrier_codes
                    service_codes
                    connection_ids
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)

        node = edges[0]["node"]
        self.assertEqual(node["name"], "Brokerage Fee - Scale")
        self.assertEqual(node["amount"], 0.85)
        self.assertEqual(node["markup_type"], "PERCENTAGE")
        self.assertTrue(node["active"])
        self.assertTrue(node["is_visible"])
        self.assertEqual(node["meta"]["type"], "brokerage-fee")
        self.assertEqual(node["meta"]["plan"], "scale")
        self.assertTrue(node["meta"]["show_in_preview"])
        self.assertEqual(node["metadata"]["notes"], "Default brokerage fee")

    def test_query_single_markup(self):
        """Test querying a single markup by ID."""
        response = self.query(
            """
            query get_markup($id: String!) {
              markup(id: $id) {
                id
                name
                amount
                markup_type
                meta
                metadata
              }
            }
            """,
            operation_name="get_markup",
            variables={"id": self.markup.id},
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["markup"]
        self.assertEqual(markup["name"], "Brokerage Fee - Scale")
        self.assertEqual(markup["meta"]["type"], "brokerage-fee")
        self.assertEqual(markup["meta"]["plan"], "scale")

    def test_create_markup_with_meta(self):
        """Test creating a markup with meta field (category, plan, show_in_preview)."""
        response = self.query(
            """
            mutation create_markup($input: CreateMarkupMutationInput!) {
              create_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  active
                  amount
                  markup_type
                  is_visible
                  meta
                  metadata
                  carrier_codes
                  service_codes
                  connection_ids
                }
              }
            }
            """,
            operation_name="create_markup",
            variables={
                "input": {
                    "name": "Insurance - Basic",
                    "amount": 50.00,
                    "markup_type": "AMOUNT",
                    "active": True,
                    "is_visible": True,
                    "meta": {
                        "type": "insurance",
                        "plan": "basic",
                        "show_in_preview": True,
                    },
                    "metadata": {"coverage": "up to $500"},
                }
            },
        )

        self.assertResponseNoErrors(response)
        result = response.data["data"]["create_markup"]
        self.assertIsNone(result["errors"])

        markup = result["markup"]
        self.assertEqual(markup["name"], "Insurance - Basic")
        self.assertEqual(markup["amount"], 50.00)
        self.assertEqual(markup["markup_type"], "AMOUNT")
        self.assertTrue(markup["active"])
        self.assertTrue(markup["is_visible"])
        self.assertEqual(markup["meta"]["type"], "insurance")
        self.assertEqual(markup["meta"]["plan"], "basic")
        self.assertTrue(markup["meta"]["show_in_preview"])
        self.assertEqual(markup["metadata"]["coverage"], "up to $500")

    def test_create_markup_percentage_type(self):
        """Test creating a percentage-based markup."""
        response = self.query(
            """
            mutation create_markup($input: CreateMarkupMutationInput!) {
              create_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  amount
                  markup_type
                  meta
                }
              }
            }
            """,
            operation_name="create_markup",
            variables={
                "input": {
                    "name": "Brokerage Fee - Launch",
                    "amount": 1.5,
                    "markup_type": "PERCENTAGE",
                    "meta": {
                        "type": "brokerage-fee",
                        "plan": "launch",
                        "show_in_preview": True,
                    },
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["create_markup"]["markup"]
        self.assertEqual(markup["amount"], 1.5)
        self.assertEqual(markup["markup_type"], "PERCENTAGE")
        self.assertEqual(markup["meta"]["type"], "brokerage-fee")
        self.assertEqual(markup["meta"]["plan"], "launch")

    def test_create_markup_without_meta(self):
        """Test creating a markup without meta field (defaults to empty dict)."""
        response = self.query(
            """
            mutation create_markup($input: CreateMarkupMutationInput!) {
              create_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  amount
                  markup_type
                  meta
                }
              }
            }
            """,
            operation_name="create_markup",
            variables={
                "input": {
                    "name": "Simple Surcharge",
                    "amount": 5.0,
                    "markup_type": "AMOUNT",
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["create_markup"]["markup"]
        self.assertEqual(markup["name"], "Simple Surcharge")
        # meta should default to empty dict
        self.assertEqual(markup["meta"], {})

    def test_create_markup_with_filters(self):
        """Test creating a markup with carrier/service/connection filters."""
        response = self.query(
            """
            mutation create_markup($input: CreateMarkupMutationInput!) {
              create_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  amount
                  markup_type
                  carrier_codes
                  service_codes
                  connection_ids
                  meta
                }
              }
            }
            """,
            operation_name="create_markup",
            variables={
                "input": {
                    "name": "DHL Only Surcharge",
                    "amount": 2.0,
                    "markup_type": "AMOUNT",
                    "carrier_codes": ["dhl_express", "dhl_parcel_de"],
                    "service_codes": ["dhl_express_worldwide"],
                    "meta": {
                        "type": "surcharge",
                        "show_in_preview": False,
                    },
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["create_markup"]["markup"]
        self.assertEqual(markup["carrier_codes"], ["dhl_express", "dhl_parcel_de"])
        self.assertEqual(markup["service_codes"], ["dhl_express_worldwide"])
        self.assertEqual(markup["meta"]["type"], "surcharge")
        self.assertFalse(markup["meta"]["show_in_preview"])

    def test_update_markup_meta(self):
        """Test updating a markup's meta field."""
        response = self.query(
            """
            mutation update_markup($input: UpdateMarkupMutationInput!) {
              update_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  amount
                  markup_type
                  meta
                  metadata
                }
              }
            }
            """,
            operation_name="update_markup",
            variables={
                "input": {
                    "id": self.markup.id,
                    "meta": {
                        "type": "brokerage-fee",
                        "plan": "enterprise",
                        "show_in_preview": False,
                    },
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["update_markup"]["markup"]
        self.assertEqual(markup["meta"]["plan"], "enterprise")
        self.assertFalse(markup["meta"]["show_in_preview"])
        # Original fields should be preserved
        self.assertEqual(markup["name"], "Brokerage Fee - Scale")
        self.assertEqual(markup["amount"], 0.85)

    def test_update_markup_amount_and_type(self):
        """Test updating markup amount and type."""
        response = self.query(
            """
            mutation update_markup($input: UpdateMarkupMutationInput!) {
              update_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  name
                  amount
                  markup_type
                  active
                  is_visible
                }
              }
            }
            """,
            operation_name="update_markup",
            variables={
                "input": {
                    "id": self.markup.id,
                    "amount": 25.0,
                    "markup_type": "AMOUNT",
                    "active": False,
                    "is_visible": False,
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["update_markup"]["markup"]
        self.assertEqual(markup["amount"], 25.0)
        self.assertEqual(markup["markup_type"], "AMOUNT")
        self.assertFalse(markup["active"])
        self.assertFalse(markup["is_visible"])

    def test_update_markup_filters(self):
        """Test updating markup carrier/service filters."""
        response = self.query(
            """
            mutation update_markup($input: UpdateMarkupMutationInput!) {
              update_markup(input: $input) {
                errors {
                  field
                  messages
                }
                markup {
                  id
                  carrier_codes
                  service_codes
                  connection_ids
                }
              }
            }
            """,
            operation_name="update_markup",
            variables={
                "input": {
                    "id": self.markup.id,
                    "carrier_codes": ["ups", "fedex"],
                    "service_codes": ["ups_ground"],
                }
            },
        )

        self.assertResponseNoErrors(response)
        markup = response.data["data"]["update_markup"]["markup"]
        self.assertEqual(markup["carrier_codes"], ["ups", "fedex"])
        self.assertEqual(markup["service_codes"], ["ups_ground"])

    def test_delete_markup(self):
        """Test deleting a markup through admin API."""
        # Create a markup to delete
        to_delete = self.pricing.Markup.objects.create(
            name="To Be Deleted",
            amount=1.0,
            markup_type="AMOUNT",
            meta={"type": "surcharge"},
        )

        response = self.query(
            """
            mutation delete_markup($input: DeleteMutationInput!) {
              delete_markup(input: $input) {
                errors {
                  field
                  messages
                }
                id
              }
            }
            """,
            operation_name="delete_markup",
            variables={"input": {"id": to_delete.id}},
        )

        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data["data"]["delete_markup"]["id"], to_delete.id
        )
        self.assertFalse(
            self.pricing.Markup.objects.filter(id=to_delete.id).exists()
        )

    def test_query_markups_returns_all(self):
        """Test querying markups returns all markups."""
        # Create a second markup
        self.pricing.Markup.objects.create(
            name="Inactive Fee",
            amount=3.0,
            markup_type="AMOUNT",
            active=False,
            meta={"type": "notification"},
        )

        response = self.query(
            """
            query get_markups {
              markups {
                edges {
                  node {
                    id
                    name
                    active
                    markup_type
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 2)
        names = {e["node"]["name"] for e in edges}
        self.assertIn("Brokerage Fee - Scale", names)
        self.assertIn("Inactive Fee", names)

    def test_filter_markups_by_meta_key_value(self):
        """Test filtering markups by generic meta key/value."""
        self.pricing.Markup.objects.create(
            name="Insurance Fee",
            amount=5.0,
            markup_type="AMOUNT",
            active=True,
            meta={"type": "insurance", "plan": "pro"},
        )
        self.pricing.Markup.objects.create(
            name="Notification Fee",
            amount=0.5,
            markup_type="AMOUNT",
            active=True,
            meta={"type": "notification"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"meta_key": "type", "meta_value": "insurance"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "Insurance Fee")
        self.assertEqual(edges[0]["node"]["meta"]["type"], "insurance")

    def test_filter_markups_by_meta_plan(self):
        """Test filtering markups by meta plan using generic key/value."""
        self.pricing.Markup.objects.create(
            name="Pro Brokerage",
            amount=2.0,
            markup_type="PERCENTAGE",
            active=True,
            meta={"type": "brokerage-fee", "plan": "pro"},
        )
        self.pricing.Markup.objects.create(
            name="Enterprise Brokerage",
            amount=1.5,
            markup_type="PERCENTAGE",
            active=True,
            meta={"type": "brokerage-fee", "plan": "enterprise"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"meta_key": "plan", "meta_value": "enterprise"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "Enterprise Brokerage")
        self.assertEqual(edges[0]["node"]["meta"]["plan"], "enterprise")

    def test_filter_markups_by_meta_key_only(self):
        """Test filtering markups by meta key existence (no value)."""
        self.pricing.Markup.objects.create(
            name="Has Plan",
            amount=2.0,
            markup_type="PERCENTAGE",
            active=True,
            meta={"type": "brokerage-fee", "plan": "pro"},
        )
        self.pricing.Markup.objects.create(
            name="No Plan",
            amount=0.5,
            markup_type="AMOUNT",
            active=True,
            meta={"type": "notification"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"meta_key": "plan"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        # setUp markup has plan="scale", plus "Has Plan" with plan="pro"
        names = {e["node"]["name"] for e in edges}
        self.assertIn("Has Plan", names)
        self.assertIn("Brokerage Fee - Scale", names)
        self.assertNotIn("No Plan", names)

    def test_filter_markups_by_metadata_key_value(self):
        """Test filtering markups by generic metadata key/value."""
        self.pricing.Markup.objects.create(
            name="With Coverage",
            amount=50.0,
            markup_type="AMOUNT",
            active=True,
            metadata={"coverage": "up to $500"},
        )
        self.pricing.Markup.objects.create(
            name="With Region",
            amount=3.0,
            markup_type="AMOUNT",
            active=True,
            metadata={"region": "north-america"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    metadata
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"metadata_key": "coverage", "metadata_value": "up to $500"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "With Coverage")

    def test_filter_markups_by_meta_value_icontains(self):
        """Test that meta_value uses case-insensitive partial matching."""
        self.pricing.Markup.objects.create(
            name="Brokerage Pro",
            amount=2.0,
            markup_type="PERCENTAGE",
            active=True,
            meta={"type": "brokerage-fee", "plan": "Pro-Enterprise"},
        )

        # Search with partial lowercase value
        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"meta_key": "plan", "meta_value": "enterprise"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        names = {e["node"]["name"] for e in edges}
        self.assertIn("Brokerage Pro", names)

    def test_filter_markups_by_metadata_value_icontains(self):
        """Test that metadata_value uses case-insensitive partial matching."""
        self.pricing.Markup.objects.create(
            name="Regional Fee",
            amount=3.0,
            markup_type="AMOUNT",
            active=True,
            metadata={"region": "North-America"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    metadata
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"metadata_key": "region", "metadata_value": "north"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "Regional Fee")

    def test_filter_markups_by_active(self):
        """Test filtering markups by active status."""
        self.pricing.Markup.objects.create(
            name="Inactive Surcharge",
            amount=3.0,
            markup_type="AMOUNT",
            active=False,
            meta={"type": "surcharge"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    active
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"active": True}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        for edge in edges:
            self.assertTrue(edge["node"]["active"])

    def test_filter_markups_by_markup_type(self):
        """Test filtering markups by markup_type."""
        self.pricing.Markup.objects.create(
            name="Flat Fee",
            amount=10.0,
            markup_type="AMOUNT",
            active=True,
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    markup_type
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"markup_type": "PERCENTAGE"}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        for edge in edges:
            self.assertEqual(edge["node"]["markup_type"], "PERCENTAGE")

    def test_filter_markups_combined(self):
        """Test combining meta key/value and active filters."""
        self.pricing.Markup.objects.create(
            name="Active Insurance",
            amount=5.0,
            markup_type="AMOUNT",
            active=True,
            meta={"type": "insurance"},
        )
        self.pricing.Markup.objects.create(
            name="Inactive Insurance",
            amount=3.0,
            markup_type="AMOUNT",
            active=False,
            meta={"type": "insurance"},
        )

        response = self.query(
            """
            query get_markups($filter: MarkupFilter) {
              markups(filter: $filter) {
                edges {
                  node {
                    id
                    name
                    active
                    meta
                  }
                }
              }
            }
            """,
            operation_name="get_markups",
            variables={"filter": {"meta_key": "type", "meta_value": "insurance", "active": True}},
        )

        self.assertResponseNoErrors(response)
        edges = response.data["data"]["markups"]["edges"]
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0]["node"]["name"], "Active Insurance")
        self.assertTrue(edges[0]["node"]["active"])
        self.assertEqual(edges[0]["node"]["meta"]["type"], "insurance")

    def test_create_markup_all_meta_categories(self):
        """Test creating markups for each meta category type."""
        categories = [
            ("brokerage-fee", "Brokerage Fee - Pro", "PERCENTAGE", 1.2),
            ("insurance", "Coverage - Premium", "AMOUNT", 100.0),
            ("surcharge", "Handling Surcharge", "AMOUNT", 3.50),
            ("notification", "SMS Notification", "AMOUNT", 0.50),
            ("address-validation", "Address Validation", "AMOUNT", 1.00),
        ]

        for meta_type, name, markup_type, amount in categories:
            response = self.query(
                """
                mutation create_markup($input: CreateMarkupMutationInput!) {
                  create_markup(input: $input) {
                    errors {
                      field
                      messages
                    }
                    markup {
                      id
                      name
                      meta
                    }
                  }
                }
                """,
                operation_name="create_markup",
                variables={
                    "input": {
                        "name": name,
                        "amount": amount,
                        "markup_type": markup_type,
                        "meta": {
                            "type": meta_type,
                            "show_in_preview": True,
                        },
                    }
                },
            )

            self.assertResponseNoErrors(response)
            markup = response.data["data"]["create_markup"]["markup"]
            self.assertEqual(markup["name"], name)
            self.assertEqual(markup["meta"]["type"], meta_type)


class TestMarkupFeatureGating(BaseAPITestCase):
    """Tests for feature-gated markup applicability logic."""

    def setUp(self):
        super().setUp()
        import karrio.server.pricing.models as pricing
        import karrio.server.core.datatypes as datatypes
        import karrio.core.models as karrio_models

        self.pricing = pricing
        self.datatypes = datatypes
        self.karrio_models = karrio_models

        # Create feature-gated markups (using meta.feature_gate)
        self.insurance_markup = pricing.Markup.objects.create(
            name="Insurance Fee",
            amount=50.0,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "insurance", "feature_gate": "insurance", "show_in_preview": True},
        )
        self.notification_markup = pricing.Markup.objects.create(
            name="Notification Fee",
            amount=2.0,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "notification", "feature_gate": "notification", "show_in_preview": True},
        )
        self.address_validation_markup = pricing.Markup.objects.create(
            name="Address Validation Fee",
            amount=1.5,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "address-validation", "feature_gate": "address_validation", "show_in_preview": True},
        )

        # Create feature-gated surcharge (conditional at runtime, unconditional in CSV preview)
        self.surcharge_markup = pricing.Markup.objects.create(
            name="Fuel Surcharge",
            amount=3.0,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "surcharge", "feature_gate": "fuel_surcharge"},
        )

        # Create unconditional markups (no feature_gate)
        self.brokerage_markup = pricing.Markup.objects.create(
            name="Brokerage Fee",
            amount=0.85,
            markup_type="PERCENTAGE",
            active=True,
            is_visible=True,
            meta={"type": "brokerage-fee", "show_in_preview": True},
        )

        # Helper: build a rate with given meta
        def make_rate(service_features=None, **kwargs):
            meta = {"service_features": service_features or []}
            meta.update(kwargs.get("extra_meta", {}))
            return self.datatypes.Rate(
                carrier_name="generic",
                carrier_id="car_test",
                currency="USD",
                total_charge=100.0,
                service="test_service",
                extra_charges=[],
                meta=meta,
            )

        self.make_rate = make_rate

        # Helper: build a rate response
        def make_response(rates):
            return self.datatypes.RateResponse(
                messages=[],
                rates=rates,
            )

        self.make_response = make_response

    def test_insurance_markup_skips_when_service_lacks_feature(self):
        """Insurance markup should NOT apply when service doesn't have insurance feature."""
        rate = self.make_rate(service_features=["tracked", "express"])
        result = self.insurance_markup._is_applicable(rate, options={"insurance": True})

        self.assertFalse(result)

    def test_insurance_markup_skips_when_option_not_requested(self):
        """Insurance markup should NOT apply when option not in request."""
        rate = self.make_rate(service_features=["insurance", "tracked"])
        result = self.insurance_markup._is_applicable(rate, options={})

        self.assertFalse(result)

    def test_insurance_markup_applies_when_feature_and_option_present(self):
        """Insurance markup should apply when service has feature AND option is requested."""
        rate = self.make_rate(service_features=["insurance", "tracked"])
        result = self.insurance_markup._is_applicable(rate, options={"insurance": True})

        self.assertTrue(result)

    def test_notification_markup_feature_gate(self):
        """Notification markup requires 'notification' feature and option."""
        rate_with = self.make_rate(service_features=["notification"])
        rate_without = self.make_rate(service_features=["tracked"])

        self.assertTrue(self.notification_markup._is_applicable(rate_with, options={"notification": True}))
        self.assertFalse(self.notification_markup._is_applicable(rate_with, options={}))
        self.assertFalse(self.notification_markup._is_applicable(rate_without, options={"notification": True}))

    def test_address_validation_markup_feature_gate(self):
        """Address validation markup requires 'address_validation' feature and option."""
        rate_with = self.make_rate(service_features=["address_validation"])
        rate_without = self.make_rate(service_features=["tracked"])

        result_applies = self.address_validation_markup._is_applicable(
            rate_with, options={"address_validation": True}
        )
        result_no_feature = self.address_validation_markup._is_applicable(
            rate_without, options={"address_validation": True}
        )

        self.assertTrue(result_applies)
        self.assertFalse(result_no_feature)

    def test_brokerage_markup_always_applies(self):
        """Brokerage-fee markup should always apply regardless of features/options."""
        rate = self.make_rate(service_features=[])
        result = self.brokerage_markup._is_applicable(rate, options={})

        self.assertTrue(result)

    def test_surcharge_with_feature_gate_is_conditional(self):
        """Surcharge with meta.feature_gate is conditional during live rates."""
        rate_with = self.make_rate(service_features=["fuel_surcharge"])
        rate_without = self.make_rate(service_features=["tracked"])

        result_applies = self.surcharge_markup._is_applicable(
            rate_with, options={"fuel_surcharge": True}
        )
        result_no_feature = self.surcharge_markup._is_applicable(
            rate_without, options={"fuel_surcharge": True}
        )
        result_no_option = self.surcharge_markup._is_applicable(
            rate_with, options={}
        )

        self.assertTrue(result_applies)
        self.assertFalse(result_no_feature)
        self.assertFalse(result_no_option)

    def test_surcharge_without_feature_gate_always_applies(self):
        """Surcharge without meta.feature_gate should always apply."""
        unconditional_surcharge = self.pricing.Markup.objects.create(
            name="Unconditional Surcharge",
            amount=2.0,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "surcharge"},
        )
        rate = self.make_rate(service_features=[])
        result = unconditional_surcharge._is_applicable(rate, options={})

        self.assertTrue(result)

    def test_apply_charge_passes_options(self):
        """apply_charge should pass options to _is_applicable for feature-gating."""
        rate = self.make_rate(service_features=["insurance"])
        response = self.make_response([rate])

        # Without insurance option: markup should not be applied
        result_without = self.insurance_markup.apply_charge(response, options={})
        self.assertEqual(result_without.rates[0].total_charge, 100.0)

        # With insurance option: markup should be applied
        result_with = self.insurance_markup.apply_charge(response, options={"insurance": True})
        self.assertEqual(result_with.rates[0].total_charge, 150.0)

    def test_brokerage_apply_charge_ignores_options(self):
        """Brokerage markup should apply regardless of options."""
        rate = self.make_rate(service_features=[])
        response = self.make_response([rate])

        result = self.brokerage_markup.apply_charge(response, options={})
        # 100.0 * 0.85% = 0.85, total = 100.85
        self.assertEqual(result.rates[0].total_charge, 100.85)

    def test_markup_without_feature_gate_always_applies(self):
        """A markup with no meta.feature_gate should always apply (unconditional)."""
        no_gate_markup = self.pricing.Markup.objects.create(
            name="Generic Markup",
            amount=5.0,
            markup_type="AMOUNT",
            active=True,
            is_visible=True,
            meta={"type": "insurance"},  # has type but no feature_gate
        )
        rate = self.make_rate(service_features=[])
        result = no_gate_markup._is_applicable(rate, options={})

        self.assertTrue(result)
