import pkgutil
import logging
import purpleserver.core.extension.models as extensions
from typing import Any, Dict
from django.db import models
from purpleserver.core.models.carrier import Carrier

logger = logging.getLogger(__name__)


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
    account_number = models.CharField(max_length=200, blank=True, default='')


DHLSettings._meta.get_field('carrier_name').default = 'DHLExpress'


class PurolatorSettings(Carrier):
    class Meta:
        db_table = "purolator-settings"
        verbose_name = 'Purolator Settings'
        verbose_name_plural = 'Purolator Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    user_token = models.CharField(max_length=200, blank=True, default='')


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


MODELS: Dict[str, Any] = {
    'canadapost': CanadaPostSettings,
    'dhl': DHLSettings,
    'fedex': FedexSettings,
    'purolator': PurolatorSettings,
    'ups': UPSSettings,
}


# Register purplship-server models extensions

for _, name, _ in pkgutil.iter_modules(extensions.__path__):
    try:
        extension = __import__(f"{extensions.__name__}.{name}", fromlist=[name])
        MODELS.update({name: extension.settings()})
    except Exception as e:
        logger.warning(f'Failed to register extension "{name}" Model')
        logger.exception(e)
