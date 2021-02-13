from django.db import models
from purpleserver.providers.models.carrier import Carrier


class UPSPackageSettings(Carrier):
    CARRIER_NAME = 'ups_package'

    class Meta:
        db_table = "ups_package-settings"
        verbose_name = 'UPS Package Settings'
        verbose_name_plural = 'UPS Package Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    access_license_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = UPSPackageSettings
