import pkgutil
import logging
import purpleserver.core.extension.models as extensions
from typing import Any, Dict
from django.db import models
from purpleserver.core.models.carrier import Carrier
from purplship.package import gateway

logger = logging.getLogger(__name__)


class CanadaPostSettings(Carrier):
    CARRIER_NAME = 'canadapost'

    class Meta:
        db_table = "canada-post-settings"
        verbose_name = 'Canada Post Settings'
        verbose_name_plural = 'Canada Post Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    customer_number = models.CharField(max_length=200)
    contract_id = models.CharField(max_length=200, blank=True, default='')


class DHLSettings(Carrier):
    CARRIER_NAME = 'dhl'

    class Meta:
        db_table = "dhl-settings"
        verbose_name = 'DHL Settings'
        verbose_name_plural = 'DHL Settings'

    site_id = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200, blank=True, default='')


class FedexSettings(Carrier):
    CARRIER_NAME = 'fedex'

    class Meta:
        db_table = "fedex-settings"
        verbose_name = 'FedEx Settings'
        verbose_name_plural = 'FedEx Settings'

    user_key = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    meter_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)


class PurolatorSettings(Carrier):
    CARRIER_NAME = 'purolator'

    class Meta:
        db_table = "purolator-settings"
        verbose_name = 'Purolator Settings'
        verbose_name_plural = 'Purolator Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    user_token = models.CharField(max_length=200, blank=True, default='')


class UPSSettings(Carrier):
    CARRIER_NAME = 'ups'

    class Meta:
        db_table = "ups-settings"
        verbose_name = 'UPS Settings'
        verbose_name_plural = 'UPS Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    access_license_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)


# Register purplship settings defined above
MODELS: Dict[str, Any] = {
    setting.CARRIER_NAME: setting for setting in [
        CanadaPostSettings,
        DHLSettings,
        FedexSettings,
        PurolatorSettings,
        UPSSettings
    ]
    if setting.CARRIER_NAME in gateway.providers
}


# Register purplship-server models extensions
for _, name, _ in pkgutil.iter_modules(extensions.__path__):
    try:
        extension = __import__(f"{extensions.__name__}.{name}", fromlist=[name])
        MODELS.update({name: extension.settings()})
    except Exception as e:
        logger.warning(f'Failed to register extension "{name}" Model')
        logger.exception(e)
