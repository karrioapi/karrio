import logging
from typing import cast
from functools import partial

from django.db import models
from django.core.validators import MinValueValidator

from karrio.core.models import ChargeDetails
from karrio.core.utils import DP, NF
from karrio.server.core.fields import MultiChoiceField
from karrio.server.core.models import Entity, uuid, register_model
from karrio.server.core.dataunits import REFERENCE_MODELS
from karrio.server.core.datatypes import RateResponse, Rate
from karrio.server.core.serializers import CARRIERS
from karrio.server.providers.models import Carrier

logger = logging.getLogger(__name__)
CARRIER_SERVICES = [
    REFERENCE_MODELS["services"][name]
    for name in sorted(REFERENCE_MODELS["services"].keys())
]
SERVICES = [(code, code) for services in CARRIER_SERVICES for code in services]
SURCHAGE_TYPE = (
    ("AMOUNT", "$"),
    ("PERCENTAGE", "%"),
)


@register_model
class Surcharge(Entity):
    class Meta:
        db_table = "surcharge"
        verbose_name = "Markup"
        verbose_name_plural = "Markups"

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="chrg_"),
        editable=False,
    )
    active = models.BooleanField(default=True)

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The surcharge name (label) that will appear in the rate (quote)",
    )
    amount = models.FloatField(
        validators=[MinValueValidator(0.1)],
        default=0.0,
        help_text="""
        The surcharge amount or percentage to add to the quote
        """,
    )
    surcharge_type = models.CharField(
        max_length=25,
        choices=SURCHAGE_TYPE,
        default=SURCHAGE_TYPE[0][0],
        help_text="""
        Determine whether the surcharge is in percentage or net amount
        <br/><br/>
        For <strong>AMOUNT</strong>: rate ($22) and amount (1) will result in a new total_charge of ($23)
        <br/>
        For <strong>PERCENTAGE</strong>: rate ($22) and amount (5) will result in a new total_charge of ($23.10)
        """,
    )
    carriers = MultiChoiceField(
        choices=CARRIERS,
        null=True,
        blank=True,
        help_text="""
        The list of carriers you want to apply the surcharge to.
        <br/>
        Note that by default, the surcharge is applied to all carriers
        """,
    )
    carrier_accounts = models.ManyToManyField(
        Carrier,
        blank=True,
        help_text="""
        The list of carrier accounts you want to apply the surcharge to.
        <br/>
        Note that by default, the surcharge is applied to all carrier accounts
        """,
    )
    services = MultiChoiceField(
        choices=SERVICES,
        null=True,
        blank=True,
        help_text="""
        The list of services you want to apply the surcharge to.
        <br/>
        Note that by default, the surcharge is applied to all services
        """,
    )

    def __str__(self):
        type_ = "$" if self.surcharge_type == "AMOUNT" else "%"
        return f"{self.id} ({self.amount} {type_})"

    def apply_charge(self, response: RateResponse) -> RateResponse:
        def apply(rate: Rate) -> Rate:
            applicable = []
            carrier_ids = [c.carrier_id for c in self.carrier_accounts.all()]
            charges = getattr(rate, "extra_charges", None) or []

            if any(self.carriers or []):
                applicable.append(rate.carrier_name in self.carriers)

            if any(carrier_ids):
                applicable.append(rate.carrier_id in carrier_ids)

            if any(self.services or []):
                applicable.append(rate.service in self.services)

            if any(applicable) and all(applicable):
                logger.debug("applying broker surcharge to rate")

                amount = NF.decimal(
                    self.amount
                    if self.surcharge_type == "AMOUNT"
                    else (rate.total_charge * (cast(float, self.amount) / 100))
                )
                total_charge = NF.decimal(rate.total_charge + amount)
                extra_charges = rate.extra_charges + [
                    ChargeDetails(
                        name=cast(str, self.name), amount=amount, currency=rate.currency
                    )
                ]

                return Rate(
                    **{
                        **DP.to_dict(rate),
                        "total_charge": total_charge,
                        "extra_charges": extra_charges,
                    }
                )

            return rate

        return RateResponse(
            messages=response.messages,
            rates=sorted(
                [apply(rate) for rate in response.rates],
                key=lambda rate: rate.total_charge,
            ),
        )
