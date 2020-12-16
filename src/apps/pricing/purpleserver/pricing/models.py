import logging
from typing import cast
from functools import partial
from psycopg2.extras import NumericRange

from django.db import models
from django.contrib.postgres.fields import DecimalRangeField

from purplship.core.models import ChargeDetails
from purplship.core.utils import DP, NF
from purpleserver.core.fields import MultiChoiceField
from purpleserver.core.models import OwnedEntity, uuid
from purpleserver.core.views.references import REFERENCE_MODELS
from purpleserver.core.datatypes import RateResponse, Rate
from purpleserver.core.serializers import CARRIERS

logger = logging.getLogger(__name__)
SERVICES = [(code, code) for services in REFERENCE_MODELS["services"].values() for code in services]


class PricingCharge(OwnedEntity):
    class Meta:
        db_table = "pricing-charge"
        verbose_name = 'Pricing Charge'
        verbose_name_plural = 'Pricing Charges'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='chrg_'), editable=False)

    amount = models.FloatField()

    carriers = MultiChoiceField(models.CharField(max_length=50, choices=CARRIERS), null=True, blank=True)
    services = MultiChoiceField(models.CharField(max_length=75, choices=SERVICES), null=True, blank=True)
    discount_range = DecimalRangeField(blank=True, null=True)
    freight_range = DecimalRangeField(blank=True, null=True)

    def apply_charge(self, response: RateResponse) -> RateResponse:
        def apply(rate: Rate) -> Rate:
            applicable = []

            if any(self.carriers or []):
                applicable.append(rate.carrier_name in self.carriers)

            if any(self.services or []):
                applicable.append(rate.service in self.services)

            if self.discount_range is not None:
                applicable.append(rate.discount in cast(NumericRange, self.discount_range))

            if self.freight_range is not None:
                applicable.append(rate.total_charge in cast(NumericRange, self.freight_range))

            if any(applicable) and all(applicable):
                logger.debug('applying custom charge to returned rate')
                return Rate(**{
                    **DP.to_dict(rate),
                    'total_charge': NF.decimal(rate.total_charge + cast(float, self.amount)),
                    'extra_charges': (rate.extra_charges + [
                        ChargeDetails(name="Service charge", amount=cast(float, self.amount), currency=rate.currency)
                    ])
                })

            return rate

        return RateResponse(
            messages=response.messages,
            rates=sorted(
                [apply(rate) for rate in response.rates],
                key=lambda rate: rate.total_charge
            )
        )
