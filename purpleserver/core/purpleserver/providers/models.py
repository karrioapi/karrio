import pkgutil
import logging
from functools import partial
from typing import Any, Dict

from django.db import models
from django.forms.models import model_to_dict

from purplship.package import gateway
from purpleserver.core.models import Entity, uuid
from purpleserver.core.datatypes import CarrierSettings
import purpleserver.providers.extension.models as extensions

logger = logging.getLogger(__name__)


class Carrier(Entity):
    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='car_'), editable=False)
    carrier_id = models.CharField(
        max_length=200, unique=True,
        help_text="eg. canadapost, dhl_express, fedex, purolator_courrier, ups..."
    )
    test = models.BooleanField(default=True)

    def __str__(self):
        return self.carrier_id

    def _linked_settings(self):
        for field in [f for f in self._meta.get_fields() if isinstance(f, models.OneToOneRel)]:
            try:
                return getattr(self, field.get_accessor_name())
            except:
                pass
        return None

    @property
    def data(self) -> CarrierSettings:
        settings = self._linked_settings()
        return CarrierSettings.create({
            'id': settings.pk,
            'carrier_name': settings.CARRIER_NAME,
            **model_to_dict(settings)
        })


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
    if name in gateway.providers:
        try:
            extension = __import__(f"{extensions.__name__}.{name}", fromlist=[name])
            MODELS.update({name: extension.settings()})
        except Exception as e:
            logger.warning(f'Failed to register extension "{name}" Model')
            logger.exception(e)
