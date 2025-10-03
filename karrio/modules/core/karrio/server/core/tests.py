import logging
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase as BaseAPITestCase, APIClient

from karrio.server.user.models import Token
import karrio.server.iam.permissions as iam
import karrio.server.providers.models as providers

logger = logging.getLogger(__name__)
iam.setup_groups()


class APITestCase(BaseAPITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        logging.basicConfig(level=logging.DEBUG)

        # Setup user and API Token.
        self.user = get_user_model().objects.create_superuser(
            "admin@example.com", "test"
        )
        self.token = Token.objects.create(user=self.user, test_mode=True)

        # Setup API client.
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Setup test carrier connections.
        self.carrier = providers.Carrier.objects.create(
            carrier_code="canadapost",
            carrier_id="canadapost",
            test_mode=True,
            active=True,
            created_by=self.user,
            credentials=dict(
                username="6e93d53968881714",
                customer_number="2004381",
                contract_id="42708517",
                password="0bfa9fcb9853d1f51ee57a",
            ),
        )
        self.ups_carrier = providers.Carrier.objects.create(
            carrier_code="ups",
            carrier_id="ups_package",
            test_mode=True,
            active=True,
            created_by=self.user,
            credentials=dict(
                client_id="test",
                client_secret="test",
                account_number="000000",
            ),
        )
        self.fedex_carrier = providers.Carrier.objects.create(
            carrier_code="fedex",
            carrier_id="fedex_express",
            test_mode=True,
            active=True,
            created_by=self.user,
            credentials=dict(
                api_key="test",
                secret_key="password",
                account_number="000000",
                track_api_key="test",
                track_secret_key="password",
            ),
        )
        self.dhl_carrier = providers.Carrier.objects.create(
            carrier_code="dhl_express",
            carrier_id="dhl_express",
            test_mode=True,
            active=True,
            created_by=self.user,
            credentials=dict(
                site_id="test",
                password="password",
                account_number="000000",
            )
        )

    def getJWTToken(self, email: str, password: str) -> str:
        url = reverse("jwt-obtain-pair")
        data = dict(
            email=email,
            password=password,
        )
        response = self.client.post(url, data)

        return response.data.get("access")

    def assertResponseNoErrors(self, response):
        is_ok = f"{response.status_code}".startswith("2")

        if is_ok is False or response.data.get("errors") is not None:
            print(response.data)

        self.assertTrue(is_ok)
        assert response.data.get("errors") is None
