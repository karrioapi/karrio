import json
from unittest.mock import ANY
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from karrio.server.admin.tests.base import AdminGraphTestCase, Result
from karrio.server.user.models import Token
import karrio.server.providers.models as providers

class TestAdminRateSheets(AdminGraphTestCase):
    """Tests for Admin Rate Sheet CRUD operations."""

    def setUp(self):
        super().setUp()

        # Create a test rate sheet with shared zones and surcharges
        # Using dhl_parcel_de which supports ratesheets (not carriers with live rates like ups/fedex)
        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Admin Test Rate Sheet",
            carrier_name="dhl_parcel_de",
            slug="admin_test_rate_sheet",

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
        new_sheet = providers.SystemRateSheet.objects.create(
            name="To Be Deleted",
            carrier_name="ups",
            slug="to_be_deleted",

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
        self.assertFalse(providers.SystemRateSheet.objects.filter(id=new_sheet.id).exists())


class TestAdminRateSheetCrossAdminAccess(AdminGraphTestCase):
    """Tests that any staff admin can read/update system ratesheets,
    regardless of which admin created them and regardless of org membership."""

    def setUp(self):
        super().setUp()  # Creates self.user (admin1) + self.organization

        # Create a second independent admin with their own org
        self.admin2 = get_user_model().objects.create_superuser(
            "admin2@example.com", "test2"
        )
        self.admin2.is_staff = True
        self.admin2.save()
        self.token2 = Token.objects.create(user=self.admin2, test_mode=False)

        from django.conf import settings
        if settings.MULTI_ORGANIZATIONS:
            from karrio.server.orgs.models import Organization, TokenLink
            self.org2 = Organization.objects.create(
                name="Second Organization", slug="second-org"
            )
            owner2 = self.org2.add_user(self.admin2, is_admin=True)
            self.org2.change_owner(owner2)
            self.org2.save()
            TokenLink.objects.create(item=self.token2, org=self.org2)

        # Rate sheet created by admin1
        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Cross Admin Rate Sheet",
            carrier_name="dhl_parcel_de",
            slug="cross_admin_rate_sheet",

            created_by=self.user,
        )

    def query_as_admin2(self, query, operation_name=None, variables=None):
        """Execute a GraphQL query authenticated as admin2."""
        from rest_framework.test import APIClient
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + self.token2.key)
        url = reverse("karrio.server.admin:admin-graph")
        data = dict(query=query, variables=variables, operation_name=operation_name)
        response = client.post(url, data)
        return Result(status_code=response.status_code, data=json.loads(response.content))

    def test_admin2_can_query_system_ratesheet_created_by_admin1(self):
        """System ratesheets are global — any staff admin can read them."""
        response = self.query_as_admin2(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
                id
                name
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": self.rate_sheet.id},
        )
        self.assertResponseNoErrors(response)
        data = response.data["data"]["rate_sheet"]
        self.assertIsNotNone(data)
        self.assertEqual(data["id"], self.rate_sheet.id)

    def test_admin2_can_update_system_ratesheet_created_by_admin1(self):
        """System ratesheets are global — any staff admin can update them."""
        response = self.query_as_admin2(
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
            variables={"data": {"id": self.rate_sheet.id, "name": "Updated By Admin2"}},
        )
        self.assertResponseNoErrors(response)
        result = response.data["data"]["update_rate_sheet"]["rate_sheet"]
        self.assertEqual(result["name"], "Updated By Admin2")
        # Confirm persisted in DB
        self.rate_sheet.refresh_from_db()
        self.assertEqual(self.rate_sheet.name, "Updated By Admin2")

    def test_system_ratesheet_has_no_org_link_after_create(self):
        """System ratesheets must not be linked to any org, regardless of who created them."""
        from django.conf import settings
        if not settings.MULTI_ORGANIZATIONS:
            self.skipTest("MULTI_ORGANIZATIONS is disabled")

        # Create via mutation as admin1
        response = self.query(
            """
            mutation create_rate_sheet($data: CreateRateSheetMutationInput!) {
              create_rate_sheet(input: $data) {
                rate_sheet {
                  id
                  name
                }
              }
            }
            """,
            operation_name="create_rate_sheet",
            variables={"data": {"name": "No Org Sheet", "carrier_name": "dhl_parcel_de"}},
        )
        self.assertResponseNoErrors(response)
        sheet_id = response.data["data"]["create_rate_sheet"]["rate_sheet"]["id"]
        sheet = providers.SystemRateSheet.objects.get(id=sheet_id)

        # Must have no org link
        if hasattr(sheet, "org"):
            self.assertFalse(
                sheet.org.exists(),
                "System ratesheet must not be linked to any org",
            )

        # Admin2 (different org) must still be able to read it
        r2 = self.query_as_admin2(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) { id name }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": sheet_id},
        )
        self.assertResponseNoErrors(r2)
        self.assertIsNotNone(r2.data["data"]["rate_sheet"])


class TestAdminRateSheetZones(AdminGraphTestCase):
    """Tests for admin shared zone CRUD operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Zone Test Sheet",
            carrier_name="ups",
            slug="zone_test_sheet",

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

        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Surcharge Test Sheet",
            carrier_name="ups",
            slug="surcharge_test_sheet",

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

        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Service Rate Test Sheet",
            carrier_name="ups",
            slug="service_rate_test_sheet",

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

        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Assignment Test Sheet",
            carrier_name="ups",
            slug="assignment_test_sheet",

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

        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Service Test Sheet",
            carrier_name="ups",
            slug="service_test_sheet",

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


class TestAdminDeleteServiceRate(AdminGraphTestCase):
    """Tests for admin delete_service_rate mutation."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Delete Rate Test Sheet",
            carrier_name="ups",
            slug="delete_rate_test_sheet",

            zones=[
                {"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]},
                {"id": "zone_2", "label": "Zone 2", "country_codes": ["CA"]},
            ],
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

        self.rate_sheet.service_rates = [
            {"service_id": self.service.id, "zone_id": "zone_1", "rate": 10.00, "cost": 8.00},
            {"service_id": self.service.id, "zone_id": "zone_2", "rate": 15.00, "cost": 12.00},
            {"service_id": self.service.id, "zone_id": "zone_1", "rate": 20.00, "cost": 16.00, "min_weight": 0.0, "max_weight": 5.0},
        ]
        self.rate_sheet.save()

    def test_delete_service_rate(self):
        """Test deleting a service rate without weight range through admin API."""
        response = self.query(
            """
            mutation delete_rate($data: DeleteServiceRateMutationInput!) {
              delete_service_rate(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    rate
                  }
                }
              }
            }
            """,
            operation_name="delete_rate",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_id": "zone_2",
                },
            },
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        rates = response.data["data"]["delete_service_rate"]["rate_sheet"]["service_rates"]
        zone_2_rates = [r for r in rates if r["zone_id"] == "zone_2"]
        self.assertEqual(len(zone_2_rates), 0)

    def test_delete_service_rate_with_weight_range(self):
        """Test deleting a service rate by weight range through admin API."""
        response = self.query(
            """
            mutation delete_rate($data: DeleteServiceRateMutationInput!) {
              delete_service_rate(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    rate
                    min_weight
                    max_weight
                  }
                }
              }
            }
            """,
            operation_name="delete_rate",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_id": "zone_1",
                    "min_weight": 0,
                    "max_weight": 5,
                },
            },
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        rates = response.data["data"]["delete_service_rate"]["rate_sheet"]["service_rates"]
        zone_1_weighted = [
            r for r in rates
            if r["zone_id"] == "zone_1" and r.get("min_weight") == 0 and r.get("max_weight") == 5
        ]
        self.assertEqual(len(zone_1_weighted), 0)
        # The base zone_1 rate without weight should remain
        zone_1_base = [r for r in rates if r["zone_id"] == "zone_1"]
        self.assertGreaterEqual(len(zone_1_base), 1)

    def test_delete_service_rate_then_query(self):
        """Test querying rate sheet after deleting a service rate verifies persistence."""
        self.query(
            """
            mutation delete_rate($data: DeleteServiceRateMutationInput!) {
              delete_service_rate(input: $data) {
                rate_sheet { id }
              }
            }
            """,
            operation_name="delete_rate",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_id": "zone_2",
                },
            },
        )

        response = self.query(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
                service_rates {
                  zone_id
                  rate
                }
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": self.rate_sheet.id},
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        rates = response.data["data"]["rate_sheet"]["service_rates"]
        zone_ids = [r["zone_id"] for r in rates]
        # zone_2 base rate should be gone
        zone_2_count = sum(1 for z in zone_ids if z == "zone_2")
        self.assertEqual(zone_2_count, 0)


class TestAdminWeightRanges(AdminGraphTestCase):
    """Tests for admin weight range mutations (add_weight_range, remove_weight_range)."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Weight Range Test Sheet",
            carrier_name="ups",
            slug="weight_range_test_sheet",

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

    def test_add_weight_range(self):
        """Test adding a weight range through admin API creates entries for all combos."""
        response = self.query(
            """
            mutation add_wr($data: AddWeightRangeMutationInput!) {
              add_weight_range(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    rate
                    min_weight
                    max_weight
                  }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="add_wr",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "min_weight": 0,
                    "max_weight": 5,
                },
            },
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        rates = response.data["data"]["add_weight_range"]["rate_sheet"]["service_rates"]
        # 1 service x 2 zones = 2 entries
        self.assertEqual(len(rates), 2)
        for rate in rates:
            self.assertEqual(rate["min_weight"], 0)
            self.assertEqual(rate["max_weight"], 5)
            self.assertEqual(rate["rate"], 0)

    def test_add_multiple_weight_ranges(self):
        """Test adding multiple weight ranges sequentially through admin API."""
        for min_w, max_w in [(0, 5), (5, 10), (10, 20)]:
            response = self.query(
                """
                mutation add_wr($data: AddWeightRangeMutationInput!) {
                  add_weight_range(input: $data) {
                    rate_sheet {
                      service_rates {
                        min_weight
                        max_weight
                      }
                    }
                  }
                }
                """,
                operation_name="add_wr",
                variables={
                    "data": {
                        "rate_sheet_id": self.rate_sheet.id,
                        "min_weight": min_w,
                        "max_weight": max_w,
                    },
                },
            )
            print(response.data)
            self.assertResponseNoErrors(response)

        # 3 ranges x 2 zones x 1 service = 6
        self.rate_sheet.refresh_from_db()
        self.assertEqual(len(self.rate_sheet.service_rates), 6)

    def test_remove_weight_range(self):
        """Test removing a weight range through admin API removes from all services."""
        # Seed two weight ranges
        self.rate_sheet.add_weight_range(min_weight=0, max_weight=5)
        self.rate_sheet.add_weight_range(min_weight=5, max_weight=10)
        self.rate_sheet.refresh_from_db()

        response = self.query(
            """
            mutation remove_wr($data: RemoveWeightRangeMutationInput!) {
              remove_weight_range(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    min_weight
                    max_weight
                  }
                }
              }
            }
            """,
            operation_name="remove_wr",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "min_weight": 0,
                    "max_weight": 5,
                },
            },
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        rates = response.data["data"]["remove_weight_range"]["rate_sheet"]["service_rates"]
        # Only the 5-10 range should remain (2 entries for 1 service x 2 zones)
        self.assertEqual(len(rates), 2)
        for rate in rates:
            self.assertEqual(rate["min_weight"], 5)
            self.assertEqual(rate["max_weight"], 10)

    def test_add_weight_range_then_query(self):
        """Test that querying after adding a weight range shows the new entries."""
        self.query(
            """
            mutation add_wr($data: AddWeightRangeMutationInput!) {
              add_weight_range(input: $data) {
                rate_sheet { id }
              }
            }
            """,
            operation_name="add_wr",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "min_weight": 0,
                    "max_weight": 10,
                },
            },
        )

        response = self.query(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
                service_rates {
                  service_id
                  zone_id
                  rate
                  min_weight
                  max_weight
                }
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": self.rate_sheet.id},
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        rates = response.data["data"]["rate_sheet"]["service_rates"]
        self.assertEqual(len(rates), 2)

    def test_add_weight_range_with_multiple_services(self):
        """Test weight range addition creates entries for all services."""
        # Add a second service
        service2 = providers.ServiceLevel.objects.create(
            service_name="UPS Express",
            service_code="ups_express",
            carrier_service_code="01",
            currency="USD",
            zone_ids=["zone_1"],
            created_by=self.user,
        )
        self.rate_sheet.services.add(service2)

        response = self.query(
            """
            mutation add_wr($data: AddWeightRangeMutationInput!) {
              add_weight_range(input: $data) {
                rate_sheet {
                  service_rates {
                    service_id
                    zone_id
                    min_weight
                    max_weight
                  }
                }
              }
            }
            """,
            operation_name="add_wr",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "min_weight": 0,
                    "max_weight": 5,
                },
            },
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        rates = response.data["data"]["add_weight_range"]["rate_sheet"]["service_rates"]
        # service1 x 2 zones + service2 x 1 zone = 3
        self.assertEqual(len(rates), 3)


class TestAdminRateSheetQueryVerification(AdminGraphTestCase):
    """Tests that verify query results after mutation operations."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Query Verify Test Sheet",
            carrier_name="ups",
            slug="query_verify_test_sheet",

            zones=[
                {"id": "zone_1", "label": "Zone 1", "country_codes": ["US"]},
            ],
            surcharges=[
                {"id": "surch_1", "name": "Fuel", "amount": 10.0, "surcharge_type": "percentage", "active": True},
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

    def test_query_single_rate_sheet(self):
        """Test querying a single rate sheet by ID through admin API."""
        response = self.query(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
                id
                name
                carrier_name
                zones {
                  id
                  label
                  country_codes
                }
                surcharges {
                  id
                  name
                  amount
                }
                services {
                  id
                  service_name
                  zone_ids
                  surcharge_ids
                }
                service_rates {
                  service_id
                  zone_id
                  rate
                }
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": self.rate_sheet.id},
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        rs = response.data["data"]["rate_sheet"]
        self.assertEqual(rs["name"], "Query Verify Test Sheet")
        self.assertEqual(rs["carrier_name"], "ups")
        self.assertEqual(len(rs["zones"]), 1)
        self.assertEqual(len(rs["surcharges"]), 1)
        self.assertEqual(len(rs["services"]), 1)

    def test_create_then_query_rate_sheet(self):
        """Test creating a rate sheet then querying it to verify state."""
        create_response = self.query(
            """
            mutation create_rate_sheet($data: CreateRateSheetMutationInput!) {
              create_rate_sheet(input: $data) {
                rate_sheet {
                  id
                  name
                }
              }
            }
            """,
            operation_name="create_rate_sheet",
            variables={
                "data": {
                    "name": "Created For Query Test",
                    "carrier_name": "fedex",
                    "zones": [{"label": "Zone A", "country_codes": ["US"]}],
                    "services": [
                        {
                            "service_name": "FedEx Ground",
                            "service_code": "fedex_ground",
                            "carrier_service_code": "FEDEX_GROUND",
                            "currency": "USD",
                        }
                    ],
                }
            },
        )

        print(create_response.data)
        self.assertResponseNoErrors(create_response)
        created_id = create_response.data["data"]["create_rate_sheet"]["rate_sheet"]["id"]

        # Now query it
        query_response = self.query(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
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
                  service_code
                }
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": created_id},
        )

        print(query_response.data)
        self.assertResponseNoErrors(query_response)
        rs = query_response.data["data"]["rate_sheet"]
        self.assertEqual(rs["name"], "Created For Query Test")
        self.assertEqual(rs["carrier_name"], "fedex")
        self.assertEqual(len(rs["zones"]), 1)
        self.assertEqual(rs["zones"][0]["label"], "Zone A")
        self.assertEqual(len(rs["services"]), 1)
        self.assertEqual(rs["services"][0]["service_name"], "FedEx Ground")

    def test_update_then_query_rate_sheet(self):
        """Test updating a rate sheet then querying to verify state."""
        self.query(
            """
            mutation update_rate_sheet($data: UpdateRateSheetMutationInput!) {
              update_rate_sheet(input: $data) {
                rate_sheet { id }
              }
            }
            """,
            operation_name="update_rate_sheet",
            variables={
                "data": {
                    "id": self.rate_sheet.id,
                    "name": "Updated Name For Query",
                }
            },
        )

        response = self.query(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
                name
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": self.rate_sheet.id},
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        self.assertEqual(response.data["data"]["rate_sheet"]["name"], "Updated Name For Query")

    def test_add_zone_then_query(self):
        """Test adding a zone then querying to verify state."""
        self.query(
            """
            mutation add_zone($data: AddSharedZoneMutationInput!) {
              add_shared_zone(input: $data) {
                rate_sheet { id }
              }
            }
            """,
            operation_name="add_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone": {"label": "Zone 2", "country_codes": ["CA"]},
                },
            },
        )

        response = self.query(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
                zones {
                  id
                  label
                  country_codes
                }
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": self.rate_sheet.id},
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        zones = response.data["data"]["rate_sheet"]["zones"]
        self.assertEqual(len(zones), 2)
        labels = [z["label"] for z in zones]
        self.assertIn("Zone 2", labels)

    def test_add_surcharge_then_query(self):
        """Test adding a surcharge then querying to verify state."""
        self.query(
            """
            mutation add_surcharge($data: AddSharedSurchargeMutationInput!) {
              add_shared_surcharge(input: $data) {
                rate_sheet { id }
              }
            }
            """,
            operation_name="add_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge": {"name": "Handling Fee", "amount": 5.0, "surcharge_type": "fixed"},
                },
            },
        )

        response = self.query(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
                surcharges {
                  id
                  name
                  amount
                }
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": self.rate_sheet.id},
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["rate_sheet"]["surcharges"]
        self.assertEqual(len(surcharges), 2)
        names = [s["name"] for s in surcharges]
        self.assertIn("Handling Fee", names)

    def test_update_service_rate_then_query(self):
        """Test updating a service rate then querying to verify state."""
        self.query(
            """
            mutation update_rate($data: UpdateServiceRateMutationInput!) {
              update_service_rate(input: $data) {
                rate_sheet { id }
              }
            }
            """,
            operation_name="update_rate",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "service_id": self.service.id,
                    "zone_id": "zone_1",
                    "rate": 25.99,
                    "cost": 20.00,
                },
            },
        )

        response = self.query(
            """
            query get_rate_sheet($id: String!) {
              rate_sheet(id: $id) {
                service_rates {
                  service_id
                  zone_id
                  rate
                  cost
                }
              }
            }
            """,
            operation_name="get_rate_sheet",
            variables={"id": self.rate_sheet.id},
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        rates = response.data["data"]["rate_sheet"]["service_rates"]
        self.assertEqual(len(rates), 1)
        self.assertEqual(rates[0]["rate"], 25.99)
        self.assertEqual(rates[0]["cost"], 20.00)


class TestAdminRateSheetEdgeCases(AdminGraphTestCase):
    """Tests for admin rate sheet edge cases and error handling."""

    def setUp(self):
        super().setUp()

        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="Edge Case Sheet",
            carrier_name="ups",
            slug="edge_case_sheet",

            zones=[],
            surcharges=[],
            service_rates=[],
            created_by=self.user,
        )

    def test_operations_on_empty_rate_sheet(self):
        """Test that zone/surcharge operations work on an empty rate sheet."""
        response = self.query(
            """
            mutation add_zone($data: AddSharedZoneMutationInput!) {
              add_shared_zone(input: $data) {
                rate_sheet {
                  zones {
                    id
                    label
                  }
                }
              }
            }
            """,
            operation_name="add_zone",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "zone": {"label": "First Zone", "country_codes": ["US"]},
                },
            },
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        zones = response.data["data"]["add_shared_zone"]["rate_sheet"]["zones"]
        self.assertEqual(len(zones), 1)

    def test_create_rate_sheet_minimal(self):
        """Test creating a rate sheet with only required fields through admin API."""
        response = self.query(
            """
            mutation create_rate_sheet($data: CreateRateSheetMutationInput!) {
              create_rate_sheet(input: $data) {
                rate_sheet {
                  id
                  name
                  carrier_name
                  zones { id }
                  surcharges { id }
                  services { id }
                }
                errors {
                  field
                  messages
                }
              }
            }
            """,
            operation_name="create_rate_sheet",
            variables={
                "data": {
                    "name": "Minimal Admin Sheet",
                    "carrier_name": "generic",
                }
            },
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        rs = response.data["data"]["create_rate_sheet"]["rate_sheet"]
        self.assertEqual(rs["name"], "Minimal Admin Sheet")
        self.assertEqual(rs["zones"], [])
        self.assertEqual(rs["surcharges"], [])
        self.assertEqual(rs["services"], [])

    def test_delete_rate_sheet_cascades_services(self):
        """Test that deleting a rate sheet also deletes its associated services."""
        sheet = providers.SystemRateSheet.objects.create(
            name="Cascade Test Sheet",
            carrier_name="ups",
            slug="cascade_test_sheet",

            created_by=self.user,
        )
        service = providers.ServiceLevel.objects.create(
            service_name="Cascade Service",
            service_code="cascade_svc",
            carrier_service_code="CS",
            currency="USD",
            created_by=self.user,
        )
        sheet.services.add(service)
        service_id = service.id

        response = self.query(
            """
            mutation delete_rate_sheet($data: DeleteMutationInput!) {
              delete_rate_sheet(input: $data) {
                id
              }
            }
            """,
            operation_name="delete_rate_sheet",
            variables={"data": {"id": sheet.id}},
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        self.assertFalse(providers.SystemRateSheet.objects.filter(id=sheet.id).exists())
        self.assertFalse(providers.ServiceLevel.objects.filter(id=service_id).exists())

    def test_surcharge_with_zero_amount(self):
        """Test adding a surcharge with zero amount through admin API."""
        response = self.query(
            """
            mutation add_surcharge($data: AddSharedSurchargeMutationInput!) {
              add_shared_surcharge(input: $data) {
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
            operation_name="add_surcharge",
            variables={
                "data": {
                    "rate_sheet_id": self.rate_sheet.id,
                    "surcharge": {"name": "Zero Surcharge", "amount": 0.0},
                },
            },
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        surcharges = response.data["data"]["add_shared_surcharge"]["rate_sheet"]["surcharges"]
        self.assertEqual(surcharges[0]["amount"], 0.0)

    def test_zone_with_empty_arrays(self):
        """Test zone with empty country_codes, cities, postal_codes through admin API."""
        response = self.query(
            """
            mutation add_zone($data: AddSharedZoneMutationInput!) {
              add_shared_zone(input: $data) {
                rate_sheet {
                  zones {
                    id
                    label
                    country_codes
                    cities
                    postal_codes
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
                        "label": "Empty Zone",
                        "country_codes": [],
                        "cities": [],
                        "postal_codes": [],
                    },
                },
            },
        )

        print(response.data)
        self.assertResponseNoErrors(response)
        zone = response.data["data"]["add_shared_zone"]["rate_sheet"]["zones"][0]
        self.assertEqual(zone["country_codes"], [])
        self.assertEqual(zone["cities"], [])
        self.assertEqual(zone["postal_codes"], [])


