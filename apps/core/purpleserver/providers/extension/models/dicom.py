from django.db import models
from purpleserver.providers.models.carrier import Carrier


class DicomSettings(Carrier):
    CARRIER_NAME = 'dicom'

    class Meta:
        db_table = "dicom-settings"
        verbose_name = 'Dicom Settings'
        verbose_name_plural = 'Dicom Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    billing_account = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


SETTINGS = DicomSettings
