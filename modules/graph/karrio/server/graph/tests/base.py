import json
import logging
import dataclasses
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase as BaseAPITestCase, APIClient

from karrio.server.user.models import Token
import karrio.server.providers.models as providers

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Result:
    data: dict = None
    status_code: str = None


class GraphTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        logging.basicConfig(level=logging.DEBUG)
        # Setup user and API Token.
        self.user = get_user_model().objects.create_superuser(
            "admin@example.com", "test"
        )
        self.token = Token.objects.create(user=self.user, test_mode=False)

        # Setup API client.
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Setup test carrier connections.
        self.carrier = providers.Carrier.objects.create(
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
        self.ups_carrier = providers.Carrier.objects.create(
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
        self.fedex_carrier = providers.Carrier.objects.create(
            carrier_code="fedex",
            carrier_id="fedex_express",
            test_mode=False,
            credentials=dict(
                api_key="test",
                secret_key="password",
                account_number="000000",
                track_api_key="test",
                track_secret_key="password",
            ),
            capabilities=["pickup", "rating", "tracking", "shipping"],
            is_system=True,
        )
        self.dhl_carrier = providers.Carrier.objects.create(
            carrier_code="dhl_universal",
            carrier_id="dhl_universal",
            test_mode=False,
            is_system=True,
            credentials=dict(
                consumer_key="test",
                consumer_secret="password",
            ),
            capabilities=["tracking"],
        )

    def query(
        self, query: str, operation_name: str = None, variables: dict = None, org_id: str = None
    ) -> Result:
        url = reverse("karrio.server.graph:graphql")
        data = dict(
            query=query,
            variables=variables,
            operation_name=operation_name,
        )

        response = self.client.post(url, data, **(
            { "x-org-id": org_id } if org_id else {}
        ))

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
            result.status_code != status.HTTP_200_OK
            or result.data.get("errors") is not None
        ):
            print(result.data)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        assert result.data.get("errors") is None
