from django.db import models
from karrio.server.providers.models.carrier import Carrier


class DicomSettings(Carrier):
    class Meta:
        db_table = "dicom-settings"
        verbose_name = 'Dicom Settings'
        verbose_name_plural = 'Dicom Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    billing_account = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return 'dicom'


SETTINGS = DicomSettings
