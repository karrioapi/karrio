import dataclasses
import json

import karrio.server.providers.models as providers
from django.contrib.auth import get_user_model
from django.urls import reverse
from karrio.server.core.logging import logger
from karrio.server.user.models import Token
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase as BaseAPITestCase


@dataclasses.dataclass
class Result:
    data: dict = None
    status_code: str = None


class GraphTestCase(BaseAPITestCase):
    """
    Base test case for GraphQL tests with class-level fixtures.

    Shared DB objects are created once per test class via setUpTestData,
    wrapped in a savepoint. Each test method rolls back its own changes
    but the class-level data is re-used, avoiding redundant bcrypt and
    carrier insertions on every method.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        # Setup user and API Token (once per class).
        cls.user = get_user_model().objects.create_superuser("admin@example.com", "test")
        cls.token = Token.objects.create(user=cls.user, test_mode=False)

        # Create organization for multi-org support (if enabled).
        from django.conf import settings

        if settings.MULTI_ORGANIZATIONS:
            from karrio.server.orgs.models import Organization, TokenLink

            cls.organization = Organization.objects.create(
                name="Test Organization",
                slug="test-org",
                metadata={"tenantId": "test-tenant-id"},
            )
            owner = cls.organization.add_user(cls.user, is_admin=True)
            cls.organization.change_owner(owner)
            cls.organization.save()
            TokenLink.objects.create(item=cls.token, org=cls.organization)

        # Setup test carrier connections (shared across all test methods).
        cls.carrier = providers.CarrierConnection.objects.create(
            carrier_code="canadapost",
            carrier_id="canadapost",
            test_mode=False,
            created_by=cls.user,
            credentials=dict(
                username="6e93d53968881714",
                customer_number="2004381",
                contract_id="42708517",
                password="0bfa9fcb9853d1f51ee57a",
            ),
            capabilities=["pickup", "rating", "tracking", "shipping"],
        )
        cls.ups_carrier = providers.CarrierConnection.objects.create(
            carrier_code="ups",
            carrier_id="ups_package",
            test_mode=False,
            created_by=cls.user,
            credentials=dict(
                client_id="test",
                client_secret="test",
                account_number="000000",
            ),
            capabilities=["pickup", "rating", "tracking", "shipping"],
        )
        cls.fedex_carrier = providers.CarrierConnection.objects.create(
            carrier_code="fedex",
            carrier_id="fedex_express",
            test_mode=False,
            created_by=cls.user,
            credentials=dict(
                api_key="test",
                secret_key="password",
                account_number="000000",
                track_api_key="test",
                track_secret_key="password",
            ),
            capabilities=["pickup", "rating", "tracking", "shipping"],
        )
        cls.dhl_carrier = providers.CarrierConnection.objects.create(
            carrier_code="dhl_universal",
            carrier_id="dhl_universal",
            test_mode=False,
            created_by=cls.user,
            credentials=dict(
                consumer_key="test",
                consumer_secret="password",
            ),
            capabilities=["tracking"],
        )

        # Setup system connections for system_connections queries.
        cls.dhl_system_connection = providers.SystemConnection.objects.create(
            carrier_code="dhl_universal",
            carrier_id="dhl_universal",
            test_mode=False,
            active=True,
            credentials=dict(
                consumer_key="system_test",
                consumer_secret="system_password",
            ),
            capabilities=["tracking"],
        )
        cls.fedex_system_connection = providers.SystemConnection.objects.create(
            carrier_code="fedex",
            carrier_id="fedex_express",
            test_mode=False,
            active=True,
            credentials=dict(
                api_key="system_test",
                secret_key="system_password",
                account_number="000000",
                track_api_key="system_test",
                track_secret_key="system_password",
            ),
            capabilities=["pickup", "rating", "tracking", "shipping"],
        )

    def setUp(self) -> None:
        self.maxDiff = None
        # Re-create client per test so credential changes don't bleed between methods.
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def query(
        self,
        query: str,
        operation_name: str = None,
        variables: dict = None,
        org_id: str = None,
    ) -> Result:
        url = reverse("karrio.server.graph:graphql")
        data = dict(
            query=query,
            variables=variables,
            operation_name=operation_name,
        )

        response = self.client.post(url, data, **({"x-org-id": org_id} if org_id else {}))

        return Result(
            status_code=response.status_code,
            data=json.loads(response.content),
        )

    def getJWTToken(self, email: str, password: str) -> str:
        url = reverse("jwt-obtain-pair")
        data = dict(email=email, password=password)
        response = self.client.post(url, data)
        return response.data.get("access")

    def assertResponseNoErrors(self, result: Result):
        if (
            result.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED]
            or result.data.get("errors") is not None
        ):
            logger.error(
                "GraphQL response has errors",
                status_code=result.status_code,
                response_data=result.data,
            )

        if result.status_code != status.HTTP_201_CREATED:
            self.assertEqual(result.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        assert result.data.get("errors") is None
