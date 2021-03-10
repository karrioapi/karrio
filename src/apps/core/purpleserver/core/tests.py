from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase as BaseAPITestCase, APIClient
from rest_framework.authtoken.models import Token
from purpleserver.providers.extension.models.canadapost import CanadaPostSettings
from purpleserver.providers.extension.models.ups_package import UPSPackageSettings
from purpleserver.providers.extension.models.fedex_express import FedexExpressSettings
from purpleserver.providers.extension.models.dhl_universal import DHLUniversalSettings


class APITestCase(BaseAPITestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        self.user = get_user_model().objects.create_superuser('admin@example.com', 'test')
        self.token = Token.objects.create(user=self.user)
        self.carrier = CanadaPostSettings.objects.create(
            carrier_id='canadapost',
            test=True,
            username='6e93d53968881714',
            customer_number='2004381',
            contract_id='42708517',
            password='0bfa9fcb9853d1f51ee57a',
            user=self.user)
        self.ups_carrier = UPSPackageSettings.objects.create(
            carrier_id='ups_package',
            test=True,
            username='test',
            account_number='000000',
            access_license_number='000000',
            password='test',
            user=self.user)
        self.fedex_carrier = FedexExpressSettings.objects.create(
            carrier_id='fedex_express',
            test=True,
            user_key="test",
            password="password",
            meter_number="000000",
            account_number="000000")
        self.dhl_carrier = DHLUniversalSettings.objects.create(
            carrier_id='dhl_universal',
            test=True,
            consumer_key="test",
            consumer_secret="password")
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
