import dataclasses
import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from karrio.server.user.models import Token
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase as BaseAPITestCase


@dataclasses.dataclass
class Result:
    data: dict = None
    status_code: str = None


class AdminGraphTestCase(BaseAPITestCase):
    """
    Base test case for admin GraphQL tests.

    Uses setUpTestData so the superuser, token, and org are created once per
    class (not once per test method), cutting setUp cost significantly.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_superuser("admin@example.com", "test")
        cls.user.is_staff = True
        cls.user.save()

        cls.token = Token.objects.create(user=cls.user, test_mode=False)

        from django.conf import settings

        if settings.MULTI_ORGANIZATIONS:
            from karrio.server.orgs.models import Organization, TokenLink

            cls.organization = Organization.objects.create(name="Test Organization", slug="test-org")
            owner = cls.organization.add_user(cls.user, is_admin=True)
            cls.organization.change_owner(owner)
            cls.organization.save()
            TokenLink.objects.create(item=cls.token, org=cls.organization)

    def setUp(self) -> None:
        self.maxDiff = None
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def query(
        self,
        query: str,
        operation_name: str = None,
        variables: dict = None,
    ) -> Result:
        url = reverse("karrio.server.admin:admin-graph")
        data = dict(query=query, variables=variables, operation_name=operation_name)
        response = self.client.post(url, data)
        return Result(status_code=response.status_code, data=json.loads(response.content))

    def assertResponseNoErrors(self, result: Result):
        if result.status_code != status.HTTP_200_OK:
            self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertIsNone(result.data.get("errors"))
