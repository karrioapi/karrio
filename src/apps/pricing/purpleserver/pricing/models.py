import logging
from typing import cast
from functools import partial
from psycopg2.extras import NumericRange

from django.db import models
from django.contrib.postgres.fields import DecimalRangeField

from purplship.core.models import ChargeDetails
from purplship.core.utils import DP, NF
from purpleserver.core.fields import MultiChoiceField
from purpleserver.core.models import Entity, uuid
from purpleserver.core.views.references import REFERENCE_MODELS
from purpleserver.core.datatypes import RateResponse, Rate
from purpleserver.core.serializers import CARRIERS

logger = logging.getLogger(__name__)
SERVICES = [(code, code) for services in REFERENCE_MODELS["services"].values() for code in services]


class Surcharge(Entity):
    class Meta:
        db_table = "surcharge"
        verbose_name = 'Broker Surcharge'
        verbose_name_plural = 'Broker Surcharges'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='chrg_'), editable=False)

    name = models.CharField(max_length=100, unique=True,
                            help_text="The surcharge name (label) that will appear in the rate (quote)")

    amount = models.FloatField(help_text="The surcharge amount to add to the quote")

    carriers = MultiChoiceField(
        models.CharField(max_length=50, choices=CARRIERS), null=True, blank=True,  help_text="""
        The list of carriers you want to apply the surcharge to.
        
        Note that by default, the surcharge is applied to all carriers
        """
    )
    services = MultiChoiceField(
        models.CharField(max_length=100, choices=SERVICES), null=True, blank=True, help_text="""
        The list of services you want to apply the surcharge to.
        Note that by default, the surcharge is applied to all services
        """
    )
    discount_range = DecimalRangeField(
        blank=True, null=True, help_text="""
        Add the surcharge, if the rate discount is within this discount rate range. 
        
        By default, the surcharge is applied to all quotes no matter the discount amount.
        """
    )
    freight_range = DecimalRangeField(
        blank=True, null=True, help_text="""
        Add the surcharge, if the rate charge is within this freight (quote) price range. 
        
        By default, the surcharge is applied to all quotes no matter the amount.
        """
    )

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
                logger.debug('applying broker surcharge to rates')
                return Rate(**{
                    **DP.to_dict(rate),
                    'total_charge': NF.decimal(rate.total_charge + cast(float, self.amount)),
                    'extra_charges': (rate.extra_charges + [
                        ChargeDetails(
                            name=cast(str, self.name),
                            amount=cast(float, self.amount),
                            currency=rate.currency
                        )
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
