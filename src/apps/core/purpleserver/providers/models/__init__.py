import pkgutil
import logging
from typing import Any, Dict

from django.db import models

from purplship import gateway
from purpleserver.providers.models.carrier import Carrier
import purpleserver.providers.extension.models as extensions

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

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


class DHLSettings(Carrier):
    CARRIER_NAME = 'dhl_express'

    class Meta:
        db_table = "dhl_express-settings"
        verbose_name = 'DHL Express Settings'
        verbose_name_plural = 'DHL Express Settings'

    site_id = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200, blank=True, default='')

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


class FedexSettings(Carrier):
    CARRIER_NAME = 'fedex_express'

    class Meta:
        db_table = "fedex_express-settings"
        verbose_name = 'FedEx Express Settings'
        verbose_name_plural = 'FedEx Express Settings'

    user_key = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    meter_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


class PurolatorSettings(Carrier):
    CARRIER_NAME = 'purolator_courier'

    class Meta:
        db_table = "purolator_courier-settings"
        verbose_name = 'Purolator Courier Settings'
        verbose_name_plural = 'Purolator Courier Settings'

    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    user_token = models.CharField(max_length=200, blank=True, default='')

    @property
    def carrier_name(self) -> str:
        return self.CARRIER_NAME


class UPSSettings(Carrier):
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
    if name in gateway.providers:
        try:
            extension = __import__(f"{extensions.__name__}.{name}", fromlist=[name])
            MODELS.update({name: extension.settings()})
        except Exception as e:
            logger.warning(f'Failed to register extension "{name}" Model')
            logger.exception(e)
