import json

import karrio.server.providers.models as providers
from django.contrib.auth import get_user_model
from django.urls import reverse
from karrio.server.admin.tests.base import AdminGraphTestCase, Result
from karrio.server.user.models import Token
from rest_framework.test import APIClient


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

    def test_update_rate_sheet_accepts_all_service_level_feature_flags(self):
        """Regression: the admin Service Editor dialog sends a 14-flag
        features object (tracked, b2c, b2b, signature, insurance, express,
        dangerous_goods, saturday_delivery, sunday_delivery, multicollo,
        neighbor_delivery, labelless, notification, address_validation).
        ServiceLevelFeaturesInput must accept all three of
        labelless / notification / address_validation — otherwise any save
        from the admin UI fails with
        "Field 'labelless' is not defined by type 'ServiceLevelFeaturesInput'"."""
        response = self.query(
            """
            mutation update_rate_sheet($data: UpdateRateSheetMutationInput!) {
              update_rate_sheet(input: $data) {
                errors { field messages }
                rate_sheet {
                  id
                  services {
                    id
                    features {
                      tracked
                      labelless
                      notification
                      address_validation
                    }
                  }
                }
              }
            }
            """,
            operation_name="update_rate_sheet",
            variables={
                "data": {
                    "id": self.rate_sheet.id,
                    "services": [
                        {
                            "service_name": "DHL Paket",
                            "service_code": "dhl_parcel_de_paket",
                            "carrier_service_code": "V01PAK",
                            "currency": "EUR",
                            "features": {
                                "tracked": True,
                                "b2c": True,
                                "b2b": True,
                                "signature": False,
                                "insurance": False,
                                "express": False,
                                "dangerous_goods": False,
                                "saturday_delivery": False,
                                "sunday_delivery": False,
                                "multicollo": False,
                                "neighbor_delivery": False,
                                "labelless": True,
                                "notification": True,
                                "address_validation": False,
                                "first_mile": "pickup_dropoff",
                                "last_mile": "home_delivery",
                                "form_factor": "parcel",
                                "shipment_type": "outbound",
                            },
                        }
                    ],
                }
            },
        )

        self.assertResponseNoErrors(response)
        result = response.data["data"]["update_rate_sheet"]
        self.assertIsNone(result.get("errors"))
        service = next(s for s in result["rate_sheet"]["services"] if s["features"] is not None)
        self.assertTrue(service["features"]["labelless"])
        self.assertTrue(service["features"]["notification"])
        self.assertFalse(service["features"]["address_validation"])

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
        self.admin2 = get_user_model().objects.create_superuser("admin2@example.com", "test2")
        self.admin2.is_staff = True
        self.admin2.save()
        self.token2 = Token.objects.create(user=self.admin2, test_mode=False)

        from django.conf import settings

        if settings.MULTI_ORGANIZATIONS:
            from karrio.server.orgs.models import Organization, TokenLink

            self.org2 = Organization.objects.create(name="Second Organization", slug="second-org")
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
        surcharges = response.data["data"]["add_shared_surcharge"]["rate_sheet"]["surcharges"]
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
        surcharges = response.data["data"]["update_shared_surcharge"]["rate_sheet"]["surcharges"]
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
        surcharges = response.data["data"]["delete_shared_surcharge"]["rate_sheet"]["surcharges"]
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
        surcharges = response.data["data"]["batch_update_surcharges"]["rate_sheet"]["surcharges"]
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
        rates = response.data["data"]["update_service_rate"]["rate_sheet"]["service_rates"]
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
        rates = response.data["data"]["batch_update_service_rates"]["rate_sheet"]["service_rates"]
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
        services = response.data["data"]["update_service_zone_ids"]["rate_sheet"]["services"]
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
        services = response.data["data"]["update_service_surcharge_ids"]["rate_sheet"]["services"]
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
        services = response.data["data"]["delete_rate_sheet_service"]["rate_sheet"]["services"]
        self.assertEqual(len(services), 0)
        self.assertFalse(providers.ServiceLevel.objects.filter(id=self.service.id).exists())


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
            {
                "service_id": self.service.id,
                "zone_id": "zone_1",
                "rate": 20.00,
                "cost": 16.00,
                "min_weight": 0.0,
                "max_weight": 5.0,
            },
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
            r for r in rates if r["zone_id"] == "zone_1" and r.get("min_weight") == 0 and r.get("max_weight") == 5
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


class TestAdminRateSheetCSVImport(AdminGraphTestCase):
    """Integration tests for CSV import via the admin import endpoint.

    Verifies:
    - Dry run returns correct diff against an existing rate sheet
    - Confirm import updates rates in the targeted rate sheet
    - rate_sheet_id parameter targets the correct sheet (not CSV-derived slug)
    """

    CSV_HEADER = (
        "carrier_name,service_code,carrier_service_code,service_name,"
        "shipment_type,origin_country,zone_label,country_codes,"
        "min_weight,max_weight,weight_unit,max_length,max_width,max_height,"
        "dimension_unit,currency,base_rate,cost,transit_days,transit_time"
    )

    def setUp(self):
        super().setUp()

        # Create a rate sheet with a custom slug (different from carrier_name)
        self.rate_sheet = providers.SystemRateSheet.objects.create(
            name="JTL Test Import Sheet",
            carrier_name="dhl_parcel_de",
            slug="jtl_test_import_sheet",
            zones=[
                {"id": "zone_de", "label": "DE", "country_codes": ["DE"]},
            ],
            service_rates=[],
            created_by=self.user,
        )

        # Create a service and attach to rate sheet
        self.service = providers.ServiceLevel.objects.create(
            service_name="DHL Paket",
            service_code="dhl_parcel_de_paket",
            carrier_service_code="V01PAK",
            currency="EUR",
            active=True,
            zone_ids=["zone_de"],
            surcharge_ids=[],
            created_by=self.user,
        )
        self.rate_sheet.services.add(self.service)

        # Set initial rates
        self.rate_sheet.service_rates = [
            {
                "service_id": self.service.id,
                "zone_id": "zone_de",
                "rate": 7.50,
                "cost": 4.80,
                "min_weight": 0,
                "max_weight": 2.001,
            },
            {
                "service_id": self.service.id,
                "zone_id": "zone_de",
                "rate": 10.30,
                "cost": 8.00,
                "min_weight": 5.001,
                "max_weight": 10.001,
            },
        ]
        self.rate_sheet.save()

        self.import_url = reverse("karrio.server.admin:admin-data-import")

    def _make_csv(self, rows):
        """Build a CSV bytes object from a list of row strings."""
        import io

        lines = [self.CSV_HEADER] + rows
        return io.BytesIO("\n".join(lines).encode("utf-8"))

    def test_dry_run_shows_correct_diff_for_existing_rates(self):
        """Dry run with rate_sheet_id should show existing rates as updated, not added."""
        csv_file = self._make_csv(
            [
                "dhl_parcel_de,dhl_parcel_de_paket,V01PAK,DHL Paket,"
                "outbound,DE,DE,DE,"
                "0,2.001,KG,60,30,15,CM,EUR,99.99,5.0,2,",
            ]
        )
        csv_file.name = "test-update.csv"

        response = self.client.post(
            self.import_url,
            {
                "resource_type": "rate_sheet",
                "dry_run": "true",
                "data_file": csv_file,
                "rate_sheet_id": self.rate_sheet.id,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)

        self.assertTrue(data["dry_run"])
        self.assertIn("diff", data)

        summary = data["diff"]["summary"]
        # The existing rate (7.50 → 99.99) should show as updated, not added
        self.assertGreater(
            summary["updated"],
            0,
            "Should detect existing rate as 'updated' when rate_sheet_id is provided",
        )

        # Verify the diff row has old and new rates
        updated_rows = [r for r in data["diff"]["rows"] if r["change"] == "updated"]
        self.assertTrue(len(updated_rows) > 0)
        first_updated = updated_rows[0]
        self.assertEqual(first_updated["new_rate"], 99.99)
        self.assertEqual(first_updated["old_rate"], 7.50)

    def test_confirm_import_updates_rates_in_target_sheet(self):
        """Confirm import should update the targeted rate sheet's rates."""
        # Verify initial rate
        self.rate_sheet.refresh_from_db()
        initial_rate = next(r for r in self.rate_sheet.service_rates if r["min_weight"] == 0)
        self.assertEqual(initial_rate["rate"], 7.50)

        csv_file = self._make_csv(
            [
                "dhl_parcel_de,dhl_parcel_de_paket,V01PAK,DHL Paket,"
                "outbound,DE,DE,DE,"
                "0,2.001,KG,60,30,15,CM,EUR,25.99,5.0,2,",
                "dhl_parcel_de,dhl_parcel_de_paket,V01PAK,DHL Paket,"
                "outbound,DE,DE,DE,"
                "5.001,10.001,KG,120,60,60,CM,EUR,35.50,12.0,2,",
            ]
        )
        csv_file.name = "test-confirm.csv"

        response = self.client.post(
            self.import_url,
            {
                "resource_type": "rate_sheet",
                "data_file": csv_file,
                "rate_sheet_id": self.rate_sheet.id,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertFalse(data.get("dry_run", False))

        # Reload the rate sheet and verify rates were updated
        self.rate_sheet.refresh_from_db()
        rates_by_weight = {r["min_weight"]: r["rate"] for r in self.rate_sheet.service_rates}
        self.assertEqual(rates_by_weight[0], 25.99, "0-2kg rate should be updated to 25.99")
        self.assertEqual(rates_by_weight[5.001], 35.50, "5-10kg rate should be updated to 35.50")

    def test_import_targets_correct_sheet_not_slug_match(self):
        """When rate_sheet_id is set, import should update that sheet even if
        another sheet exists with a slug matching the CSV carrier_name."""
        # Create a second sheet with slug=dhl_parcel_de (matches CSV carrier_name)
        other_sheet = providers.SystemRateSheet.objects.create(
            name="Other DHL Sheet",
            carrier_name="dhl_parcel_de",
            slug="dhl_parcel_de",
            zones=[{"id": "zone_other", "label": "Other"}],
            service_rates=[],
            created_by=self.user,
        )

        csv_file = self._make_csv(
            [
                "dhl_parcel_de,dhl_parcel_de_paket,V01PAK,DHL Paket,"
                "outbound,DE,DE,DE,"
                "0,2.001,KG,60,30,15,CM,EUR,88.88,5.0,2,",
            ]
        )
        csv_file.name = "test-targeting.csv"

        response = self.client.post(
            self.import_url,
            {
                "resource_type": "rate_sheet",
                "data_file": csv_file,
                "rate_sheet_id": self.rate_sheet.id,  # target the JTL sheet, not the slug-matched one
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)

        # The JTL sheet should be updated, not the other one
        self.rate_sheet.refresh_from_db()
        other_sheet.refresh_from_db()

        target_rates = {r["min_weight"]: r["rate"] for r in self.rate_sheet.service_rates}
        self.assertEqual(
            target_rates.get(0),
            88.88,
            "Target sheet (JTL) should have the imported rate",
        )

        # The other sheet should be unchanged (no service_rates added)
        self.assertEqual(
            len(other_sheet.service_rates or []),
            0,
            "Other sheet (slug=dhl_parcel_de) should NOT be modified",
        )


class TestAdminRateSheetPlanRateImport(AdminGraphTestCase):
    """Integration tests for per-plan rate and surcharge import.

    Uses realistic CSV fixtures from DHL-DE, DPD-DE, and Landmark Global
    with plan_rate_*, plan_cost_*, and surcharge columns.
    """

    CSV_HEADER = (
        "carrier_name,service_code,carrier_service_code,service_name,"
        "shipment_type,origin_country,zone_label,country_codes,"
        "min_weight,max_weight,weight_unit,max_length,max_width,max_height,"
        "dimension_unit,currency,base_rate,cost,transit_days,transit_time,"
        "plan_rate_start,plan_cost_start,plan_rate_advanced,plan_cost_advanced,"
        "plan_rate_pro,plan_cost_pro,plan_rate_enterprise,plan_cost_enterprise,"
        "tracked,b2c,b2b,first_mile,last_mile,form_factor,signature,age_check,"
        "saturday,neighbor_delivery,insurance,"
        "fuel_surcharge,seasonal_surcharge,customs_surcharge,"
        "energy_surcharge,road_toll,security_surcharge,notes\n"
    )

    # DHL Parcel DE — 3 rows with surcharges (energy_surcharge, road_toll)
    DHL_CSV = (
        CSV_HEADER + "dhl_parcel_de,dhl_parcel_de_kleinpaket,V62KP,DHL KleinPaket,"
        "outbound,DE,DE,,"
        "0.01,1.001,KG,35,25,8,CM,EUR,3.39,3.432375,,best_effort,"
        "4.08,4.08,3.98,3.98,3.9,3.9,3.82,3.82,"
        "True,True,True,dropoff,home_delivery,mailbox,False,,"
        "True,True,20,"
        ",0,0,0.042375,,,DHL Kleinpaket 0-1kg\n"
        "dhl_parcel_de,dhl_parcel_de_paket,V01PAK,DHL Paket,"
        "outbound,DE,DE,,"
        "0.01,2.001,KG,60,30,15,CM,EUR,6,6.19,,best_effort,"
        "6.81,6.81,6.64,6.64,6.5,6.5,6.37,6.37,"
        "True,True,True,pickup_dropoff,home_delivery,parcel,False,,"
        "True,True,500,"
        ",0,0,,0.19,,DHL Paket 0-2kg\n"
        "dhl_parcel_de,dhl_parcel_de_paket,V01PAK,DHL Paket,"
        "outbound,DE,DE,,"
        "5.001,10.001,KG,120,60,60,CM,EUR,10.3,10.49,,best_effort,"
        "11.59,11.59,11.31,11.31,11.07,11.07,10.84,10.84,"
        "True,True,True,pickup_dropoff,home_delivery,parcel,False,,"
        "True,True,500,"
        ",0,0,,0.19,,DHL Paket 5-10kg\n"
    )

    # DPD (dpd_meta) — 2 rows, different plan rate margins
    DPD_CSV = (
        CSV_HEADER + "dpd_meta,dpd_parcel_letter,PL,DPD ParcelLetter,"
        "outbound,DE,DE,DE,"
        "0.01,1.001,KG,35,25,3,CM,EUR,1.62,1.62,,best_effort,"
        "2.51,2.51,2.43,2.43,2.37,2.37,2.31,2.31,"
        "True,True,True,dropoff,home_delivery,mailbox,False,,"
        "False,False,0,"
        ",,,,,,DPD ParcelLetter 0-1kg\n"
        "dpd_meta,dpd_classic,CL,DPD Classic,"
        "outbound,DE,DE,DE,"
        "0.01,31.501,KG,175,100,120,CM,EUR,5.29,5.29,,best_effort,"
        "6.49,6.49,6.3,6.3,6.14,6.14,5.98,5.98,"
        "True,True,True,pickup_dropoff,home_delivery,parcel,False,,"
        "False,True,500,"
        ",,,,,,DPD Classic 0-31.5kg\n"
    )

    # Landmark Global — 2 rows, international zones with country_codes
    LANDMARK_CSV = (
        CSV_HEADER + "landmark,landmark_eu_di_home_dpd_at,,Landmark Global EU DI HOME - DPD AT,"
        "outbound,DE,Austria,AT,"
        "0.01,2.001,KG,120,60,60,CM,EUR,4.03,4.03,,best_effort,"
        "4.92,4.92,4.77,4.77,4.65,4.65,4.52,4.52,"
        "True,True,True,pickup_dropoff,home_delivery,parcel,False,,"
        "False,False,0,"
        ",,,,,,Landmark AT 0-2kg\n"
        "landmark,landmark_eu_di_home_dpd_at,,Landmark Global EU DI HOME - DPD AT,"
        "outbound,DE,Austria,AT,"
        "2.001,5.001,KG,120,60,60,CM,EUR,5.18,5.18,,best_effort,"
        "6.38,6.38,6.19,6.19,6.03,6.03,5.87,5.87,"
        "True,True,True,pickup_dropoff,home_delivery,parcel,False,,"
        "False,False,0,"
        ",,,,,,Landmark AT 2-5kg\n"
    )

    def setUp(self):
        super().setUp()
        self.import_url = reverse("karrio.server.admin:admin-data-import")

    def _make_csv_file(self, content, name="test.csv"):
        import io

        f = io.BytesIO(content.encode("utf-8"))
        f.name = name
        return f

    def _import_csv(self, content, name="test.csv", **extra):
        csv_file = self._make_csv_file(content, name)
        payload = {"resource_type": "rate_sheet", "data_file": csv_file, **extra}
        response = self.client.post(self.import_url, payload, format="multipart")
        self.assertEqual(response.status_code, 200, response.json())
        return response.json()

    # ── DHL Parcel DE tests ──────────────────────────────────────────────────

    def test_dhl_import_stores_plan_rates(self):
        """DHL CSV import persists plan_rate_*/plan_cost_* on service_rates."""
        data = self._import_csv(self.DHL_CSV, "DHL-DE.csv")
        print(data)

        from karrio.server.providers.models import SystemRateSheet

        sheet = SystemRateSheet.objects.get(id=data["rate_sheet_id"])

        # Verify kleinpaket plan rates
        kr = next(r for r in sheet.service_rates if r["min_weight"] == 0.01 and r["max_weight"] == 1.001)
        self.assertEqual(kr["rate"], 3.39)
        self.assertEqual(kr["plan_rate_start"], 4.08)
        self.assertEqual(kr["plan_cost_start"], 4.08)
        self.assertEqual(kr["plan_rate_advanced"], 3.98)
        self.assertEqual(kr["plan_rate_pro"], 3.9)
        self.assertEqual(kr["plan_rate_enterprise"], 3.82)

        # Verify paket 5-10kg plan rates
        pr = next(r for r in sheet.service_rates if r["min_weight"] == 5.001)
        self.assertEqual(pr["rate"], 10.3)
        self.assertEqual(pr["plan_rate_start"], 11.59)
        self.assertEqual(pr["plan_rate_enterprise"], 10.84)

        sheet.delete()

    def test_dhl_import_creates_surcharges(self):
        """DHL CSV creates energy_surcharge and road_toll, linked to services."""
        data = self._import_csv(self.DHL_CSV, "DHL-DE.csv")
        print(data)

        from karrio.server.providers.models import SystemRateSheet

        sheet = SystemRateSheet.objects.get(id=data["rate_sheet_id"])

        surcharge_ids = {s["id"] for s in sheet.surcharges}
        self.assertIn("energy_surcharge", surcharge_ids)
        self.assertIn("road_toll", surcharge_ids)

        services = {s.service_code: s for s in sheet.services.all()}
        self.assertIn("road_toll", services["dhl_parcel_de_paket"].surcharge_ids)
        self.assertIn("energy_surcharge", services["dhl_parcel_de_kleinpaket"].surcharge_ids)

        sheet.delete()

    def test_dhl_plan_rate_change_detected_in_diff(self):
        """Changing only plan_rate_start (base_rate unchanged) shows as 'updated'."""
        data = self._import_csv(self.DHL_CSV, "DHL-DE.csv")
        sheet_id = data["rate_sheet_id"]

        modified = self.DHL_CSV.replace(
            "4.08,4.08,3.98,3.98,3.9,3.9,3.82,3.82", "99.99,4.08,3.98,3.98,3.9,3.9,3.82,3.82", 1
        )
        diff_data = self._import_csv(modified, "DHL-DE-mod.csv", dry_run="true", rate_sheet_id=sheet_id)
        print(diff_data)

        self.assertTrue(diff_data["dry_run"])
        updated = [r for r in diff_data["diff"]["rows"] if r["change"] == "updated"]
        self.assertEqual(len(updated), 1, "Only kleinpaket row should be updated")
        self.assertEqual(updated[0]["plan_rate_start"], 99.99)
        self.assertEqual(updated[0]["old_rate"], 3.39)  # base_rate unchanged

        from karrio.server.providers.models import SystemRateSheet

        SystemRateSheet.objects.filter(id=sheet_id).delete()

    # ── DPD (dpd_meta) tests ─────────────────────────────────────────────────

    def test_dpd_import_stores_plan_rates(self):
        """DPD CSV import stores correct plan rates for ParcelLetter and Classic."""
        data = self._import_csv(self.DPD_CSV, "DPD-DE.csv")
        print(data)

        from karrio.server.providers.models import SystemRateSheet

        sheet = SystemRateSheet.objects.get(id=data["rate_sheet_id"])

        self.assertEqual(sheet.carrier_name, "dpd_meta")
        self.assertEqual(len(sheet.service_rates), 2)

        # ParcelLetter: base=1.62, start=2.51, enterprise=2.31
        pl = next(r for r in sheet.service_rates if r["rate"] == 1.62)
        self.assertEqual(pl["plan_rate_start"], 2.51)
        self.assertEqual(pl["plan_rate_enterprise"], 2.31)

        # Classic: base=5.29, start=6.49, enterprise=5.98
        cl = next(r for r in sheet.service_rates if r["rate"] == 5.29)
        self.assertEqual(cl["plan_rate_start"], 6.49)
        self.assertEqual(cl["plan_rate_enterprise"], 5.98)

        # Verify services created
        service_codes = {s.service_code for s in sheet.services.all()}
        self.assertEqual(service_codes, {"dpd_parcel_letter", "dpd_classic"})

        sheet.delete()

    def test_dpd_reimport_shows_unchanged(self):
        """Importing the same DPD CSV twice shows all rows as unchanged."""
        data = self._import_csv(self.DPD_CSV, "DPD-DE.csv")
        sheet_id = data["rate_sheet_id"]

        diff_data = self._import_csv(self.DPD_CSV, "DPD-DE.csv", dry_run="true", rate_sheet_id=sheet_id)
        print(diff_data)

        self.assertEqual(diff_data["diff"]["summary"]["unchanged"], 2)
        self.assertEqual(diff_data["diff"]["summary"]["added"], 0)
        self.assertEqual(diff_data["diff"]["summary"]["updated"], 0)

        from karrio.server.providers.models import SystemRateSheet

        SystemRateSheet.objects.filter(id=sheet_id).delete()

    # ── Landmark Global tests ────────────────────────────────────────────────

    def test_landmark_import_with_international_zones(self):
        """Landmark CSV creates zones with country_codes and correct plan rates."""
        data = self._import_csv(self.LANDMARK_CSV, "Landmark.csv")
        print(data)

        from karrio.server.providers.models import SystemRateSheet

        sheet = SystemRateSheet.objects.get(id=data["rate_sheet_id"])

        self.assertEqual(sheet.carrier_name, "landmark")
        self.assertEqual(len(sheet.service_rates), 2)

        # Verify zone has country_codes
        austria_zone = next((z for z in sheet.zones if z["label"] == "Austria"), None)
        self.assertIsNotNone(austria_zone)
        self.assertIn("AT", austria_zone["country_codes"])

        # Verify plan rates on 0-2kg
        r1 = next(r for r in sheet.service_rates if r["min_weight"] == 0.01)
        self.assertEqual(r1["rate"], 4.03)
        self.assertEqual(r1["plan_rate_start"], 4.92)
        self.assertEqual(r1["plan_rate_enterprise"], 4.52)

        # Verify plan rates on 2-5kg
        r2 = next(r for r in sheet.service_rates if r["min_weight"] == 2.001)
        self.assertEqual(r2["rate"], 5.18)
        self.assertEqual(r2["plan_rate_start"], 6.38)
        self.assertEqual(r2["plan_rate_enterprise"], 5.87)

        sheet.delete()

    def test_landmark_plan_rate_update_detected(self):
        """Landmark: changing enterprise plan rate is detected in diff."""
        data = self._import_csv(self.LANDMARK_CSV, "Landmark.csv")
        sheet_id = data["rate_sheet_id"]

        # Change enterprise rate for 0-2kg: 4.52 -> 10.00
        modified = self.LANDMARK_CSV.replace(
            "4.92,4.92,4.77,4.77,4.65,4.65,4.52,4.52", "4.92,4.92,4.77,4.77,4.65,4.65,10.00,10.00"
        )
        diff_data = self._import_csv(modified, "Landmark-mod.csv", dry_run="true", rate_sheet_id=sheet_id)
        print(diff_data)

        updated = [r for r in diff_data["diff"]["rows"] if r["change"] == "updated"]
        self.assertEqual(len(updated), 1)
        self.assertEqual(updated[0]["plan_rate_enterprise"], 10.00)
        self.assertEqual(updated[0]["old_rate"], 4.03)  # base unchanged

        from karrio.server.providers.models import SystemRateSheet

        SystemRateSheet.objects.filter(id=sheet_id).delete()

    # ── Cross-carrier roundtrip test ─────────────────────────────────────────

    def test_full_roundtrip_all_carriers(self):
        """Import DHL, DPD, and Landmark — verify all preserve plan rates."""
        from karrio.server.providers.models import SystemRateSheet

        sheets = []
        for csv, name, carrier, expected_rates in [
            (self.DHL_CSV, "DHL-DE.csv", "dhl_parcel_de", 3),
            (self.DPD_CSV, "DPD-DE.csv", "dpd_meta", 2),
            (self.LANDMARK_CSV, "Landmark.csv", "landmark", 2),
        ]:
            data = self._import_csv(csv, name)
            sheet = SystemRateSheet.objects.get(id=data["rate_sheet_id"])
            sheets.append(sheet)

            self.assertEqual(sheet.carrier_name, carrier)
            self.assertEqual(len(sheet.service_rates), expected_rates)

            # Every rate should have plan fields
            for sr in sheet.service_rates:
                self.assertIn("plan_rate_start", sr, f"{carrier}: missing plan_rate_start")
                self.assertIn("plan_rate_enterprise", sr, f"{carrier}: missing plan_rate_enterprise")
                self.assertIsNotNone(sr["plan_rate_start"], f"{carrier}: plan_rate_start is None")
                self.assertGreater(sr["plan_rate_start"], 0, f"{carrier}: plan_rate_start should be > 0")

            # Every service should have features populated from CSV
            for svc in sheet.services.all():
                features = svc.features or {}
                self.assertIn(
                    "shipment_type",
                    features,
                    f"{carrier}/{svc.service_code}: missing features.shipment_type",
                )
                self.assertIn(
                    features["shipment_type"],
                    ("outbound", "returns", "both"),
                    f"{carrier}/{svc.service_code}: invalid shipment_type={features['shipment_type']}",
                )

        for sheet in sheets:
            sheet.delete()
