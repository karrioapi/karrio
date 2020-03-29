from django.db import models


class Carrier(models.Model):
    carrier_name = models.CharField(max_length=200, unique=True)
    test = models.BooleanField(default=True)


class CanadaPostSettings(Carrier):
    class Meta:
        db_table = "canada-post-settings"
        verbose_name = 'Canada Post Settings'
        verbose_name_plural = 'Canada Post Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    customer_number = models.CharField(max_length=200)
    contract_id = models.CharField(max_length=200, blank=True, default='')


CanadaPostSettings._meta.get_field('carrier_name').default = 'CanadaPost'


class DHLSettings(Carrier):
    class Meta:
        db_table = "dhl-settings"
        verbose_name = 'DHL Settings'
        verbose_name_plural = 'DHL Settings'

    site_id = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)


DHLSettings._meta.get_field('carrier_name').default = 'DHLExpress'


class PurolatorSettings(Carrier):
    class Meta:
        db_table = "purolator-settings"
        verbose_name = 'Purolator Settings'
        verbose_name_plural = 'Purolator Settings'

    user_token = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    language = models.CharField(max_length=200, default='en')


PurolatorSettings._meta.get_field('carrier_name').default = 'PurolatorCourrier'


class UPSSettings(Carrier):
    class Meta:
        db_table = "ups-settings"
        verbose_name = 'UPS Settings'
        verbose_name_plural = 'UPS Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    access_license_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)


UPSSettings._meta.get_field('carrier_name').default = 'UPS'


class FedexSettings(Carrier):
    class Meta:
        db_table = "fedex-settings"
        verbose_name = 'FedEx Settings'
        verbose_name_plural = 'FedEx Settings'

    user_key = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    meter_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)


FedexSettings._meta.get_field('carrier_name').default = 'FedEx'
