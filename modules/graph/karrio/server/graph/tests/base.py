import json
import dataclasses
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase as BaseAPITestCase, APIClient

from karrio.server.core.logging import logger
from karrio.server.user.models import Token
import karrio.server.providers.models as providers


@dataclasses.dataclass
class Result:
    data: dict = None
    status_code: str = None


class GraphTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        # Loguru is already configured globally in settings

        # Setup user and API Token.
        self.user = get_user_model().objects.create_superuser(
            "admin@example.com", "test"
        )

        self.token = Token.objects.create(user=self.user, test_mode=False)

        # Create organization for multi-org support (if enabled)
        from django.conf import settings
        if settings.MULTI_ORGANIZATIONS:
            from karrio.server.orgs.models import Organization, TokenLink
            self.organization = Organization.objects.create(
                name="Test Organization",
                slug="test-org"
            )
            # Add user as owner (triggers permission sync via signals)
            owner = self.organization.add_user(self.user, is_admin=True)
            self.organization.change_owner(owner)
            self.organization.save()

            # Link token to organization
            TokenLink.objects.create(
                item=self.token,
                org=self.organization
            )

        # Setup API client.
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Setup test carrier connections.
        self.carrier = providers.CarrierConnection.objects.create(
            carrier_code="canadapost",
            carrier_id="canadapost",
            test_mode=False,
            created_by=self.user,
            credentials=dict(
                username="6e93d53968881714",
                customer_number="2004381",
                contract_id="42708517",
                password="0bfa9fcb9853d1f51ee57a",
            ),
            capabilities=["pickup", "rating", "tracking", "shipping"],
        )
        self.ups_carrier = providers.CarrierConnection.objects.create(
            carrier_code="ups",
            carrier_id="ups_package",
            test_mode=False,
            created_by=self.user,
            credentials=dict(
                client_id="test",
                client_secret="test",
                account_number="000000",
            ),
            capabilities=["pickup", "rating", "tracking", "shipping"],
        )
        self.fedex_carrier = providers.CarrierConnection.objects.create(
            carrier_code="fedex",
            carrier_id="fedex_express",
            test_mode=False,
            created_by=self.user,
            credentials=dict(
                api_key="test",
                secret_key="password",
                account_number="000000",
                track_api_key="test",
                track_secret_key="password",
            ),
            capabilities=["pickup", "rating", "tracking", "shipping"],
        )
        self.dhl_carrier = providers.CarrierConnection.objects.create(
            carrier_code="dhl_universal",
            carrier_id="dhl_universal",
            test_mode=False,
            created_by=self.user,
            credentials=dict(
                consumer_key="test",
                consumer_secret="password",
            ),
            capabilities=["tracking"],
        )

        # Setup system connections for system_connections queries
        self.dhl_system_connection = providers.SystemConnection.objects.create(
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
        self.fedex_system_connection = providers.SystemConnection.objects.create(
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

        response = self.client.post(
            url, data, **({"x-org-id": org_id} if org_id else {})
        )

        return Result(
            status_code=response.status_code,
            data=json.loads(response.content),
        )

    def getJWTToken(self, email: str, password: str) -> str:
        url = reverse("jwt-obtain-pair")
        data = dict(
            email=email,
            password=password,
        )
        response = self.client.post(url, data)

        return response.data.get("access")

    def assertResponseNoErrors(self, result: Result):
        if (
            result.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED]
            or result.data.get("errors") is not None
        ):
            logger.error("GraphQL response has errors",
                        status_code=result.status_code,
                        response_data=result.data)

        if result.status_code != status.HTTP_201_CREATED:
            self.assertEqual(result.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        assert result.data.get("errors") is None
