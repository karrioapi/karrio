import json
import logging
import dataclasses
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase as BaseAPITestCase, APIClient

from karrio.server.providers.models import MODELS
from karrio.server.user.models import Token

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Result:
    data: dict = None
    status_code: str = None


class GraphTestCase(BaseAPITestCase):
    def setUp(self) -> None:
        self.maxDiff = None

        # Setup user and API Token.
        self.user = get_user_model().objects.create_superuser(
            "admin@example.com", "test"
        )
        self.token = Token.objects.create(user=self.user, test_mode=False)

        # Setup API client.
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Setup test carrier connections.
        self.carrier = MODELS["canadapost"].objects.create(
            carrier_id="canadapost",
            test_mode=False,
            username="6e93d53968881714",
            customer_number="2004381",
            contract_id="42708517",
            password="0bfa9fcb9853d1f51ee57a",
            created_by=self.user,
        )
        self.ups_carrier = MODELS["ups"].objects.create(
            carrier_id="ups_package",
            test_mode=False,
            username="test",
            account_number="000000",
            access_license_number="000000",
            password="test",
            created_by=self.user,
        )
        self.fedex_carrier = MODELS["fedex"].objects.create(
            carrier_id="fedex_express",
            test_mode=False,
            user_key="test",
            password="password",
            meter_number="000000",
            account_number="000000",
        )
        self.dhl_carrier = MODELS["dhl_universal"].objects.create(
            carrier_id="dhl_universal",
            test_mode=False,
            consumer_key="test",
            consumer_secret="password",
        )

    def query(
        self, query: str, operation_name: str = None, variables: dict = None
    ) -> Result:
        url = reverse("karrio.server.graph:graphql")
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
        if (
            result.status_code != status.HTTP_200_OK
            or result.data.get("errors") is not None
        ):
            print(result.data)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        assert result.data.get("errors") is None
