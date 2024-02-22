import logging
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase as BaseAPITestCase, APIClient

from karrio.server.providers.models import MODELS
from karrio.server.user.models import Token

logger = logging.getLogger(__name__)


class APITestCase(BaseAPITestCase):
    def setUp(self) -> None:
        self.maxDiff = None

        # Setup user and API Token.
        self.user = get_user_model().objects.create_superuser(
            "admin@example.com", "test"
        )
        self.token = Token.objects.create(user=self.user, test_mode=True)

        # Setup API client.
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Setup test carrier connections.
        self.carrier = MODELS["canadapost"].objects.create(
            carrier_id="canadapost",
            test_mode=True,
            username="6e93d53968881714",
            customer_number="2004381",
            contract_id="42708517",
            password="0bfa9fcb9853d1f51ee57a",
            created_by=self.user,
        )
        self.ups_carrier = MODELS["ups"].objects.create(
            carrier_id="ups_package",
            test_mode=True,
            client_id="test",
            client_secret="test",
            account_number="000000",
            created_by=self.user,
        )
        self.fedex_carrier = MODELS["fedex_ws"].objects.create(
            carrier_id="fedex_express",
            test_mode=True,
            user_key="test",
            password="password",
            meter_number="000000",
            account_number="000000",
        )
        self.dhl_carrier = MODELS["dhl_universal"].objects.create(
            carrier_id="dhl_universal",
            test_mode=True,
            consumer_key="test",
            consumer_secret="password",
        )

    def assertResponseNoErrors(self, response):
        is_ok = f"{response.status_code}".startswith("2")

        if is_ok is False or response.data.get("errors") is not None:
            print(response.data)

        self.assertTrue(is_ok)
        assert response.data.get("errors") is None
