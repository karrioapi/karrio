import karrio.server.providers.models as providers
from django.contrib.auth import get_user_model
from django.urls import reverse
from karrio.server.core.logging import logger
from karrio.server.user.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase as BaseAPITestCase


class APITestCase(BaseAPITestCase):
    """
    Base test case with class-level fixtures via setUpTestData.

    Shared DB objects (user, carriers, token) are created once per test class
    inside a transaction savepoint — each test method rolls back its own
    changes but the class-level data is preserved. This avoids re-running
    bcrypt and multiple DB inserts for every individual test method.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        # Setup user and API Token (runs once per test class).
        cls.user = get_user_model().objects.create_superuser("admin@example.com", "test")
        cls.token = Token.objects.create(user=cls.user, test_mode=True)

        # Setup test carrier connections (shared across all test methods).
        cls.carrier = providers.CarrierConnection.objects.create(
            carrier_code="canadapost",
            carrier_id="canadapost",
            test_mode=True,
            active=True,
            created_by=cls.user,
            credentials=dict(
                username="6e93d53968881714",
                customer_number="2004381",
                contract_id="42708517",
                password="0bfa9fcb9853d1f51ee57a",
            ),
        )
        cls.ups_carrier = providers.CarrierConnection.objects.create(
            carrier_code="ups",
            carrier_id="ups_package",
            test_mode=True,
            active=True,
            created_by=cls.user,
            credentials=dict(
                client_id="test",
                client_secret="test",
                account_number="000000",
            ),
        )
        cls.fedex_carrier = providers.CarrierConnection.objects.create(
            carrier_code="fedex",
            carrier_id="fedex_express",
            test_mode=True,
            active=True,
            created_by=cls.user,
            credentials=dict(
                api_key="test",
                secret_key="password",
                account_number="000000",
                track_api_key="test",
                track_secret_key="password",
            ),
        )
        cls.dhl_carrier = providers.CarrierConnection.objects.create(
            carrier_code="dhl_express",
            carrier_id="dhl_express",
            test_mode=True,
            active=True,
            created_by=cls.user,
            credentials=dict(
                site_id="test",
                password="password",
                account_number="000000",
            ),
        )

    def setUp(self) -> None:
        self.maxDiff = None
        # Re-create client each test so credential changes in one test don't bleed.
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

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
            logger.error("Response has errors", status_code=response.status_code, response_data=response.data)

        self.assertTrue(is_ok)
        assert response.data.get("errors") is None
