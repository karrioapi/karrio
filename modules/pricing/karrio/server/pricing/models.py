import typing
import logging
import functools
import django.db.models as models
import django.core.validators as validators

import karrio.lib as lib
import karrio.core.models as karrio
import karrio.server.core.models as core
import karrio.server.core.fields as fields
import karrio.server.core.datatypes as datatypes
import karrio.server.providers.models as providers
import karrio.server.pricing.serializers as serializers

logger = logging.getLogger(__name__)


@core.register_model
class Surcharge(core.Entity):
    class Meta:
        db_table = "surcharge"
        verbose_name = "Markup"
        verbose_name_plural = "Markups"

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="chrg_"),
        editable=False,
    )
    active = models.BooleanField(default=True)

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The surcharge name (label) that will appear in the rate (quote)",
    )
    amount = models.FloatField(
        validators=[validators.MinValueValidator(0.1)],
        default=0.0,
        help_text="""
        The surcharge amount or percentage to add to the quote
        """,
    )
    surcharge_type = models.CharField(
        max_length=25,
        choices=serializers.SURCHAGE_TYPE,
        default=serializers.SURCHAGE_TYPE[0][0],
        help_text="""
        Determine whether the surcharge is in percentage or net amount
        <br/><br/>
        For <strong>AMOUNT</strong>: rate ($22) and amount (1) will result in a new total_charge of ($23)
        <br/>
        For <strong>PERCENTAGE</strong>: rate ($22) and amount (5) will result in a new total_charge of ($23.10)
        """,
    )
    carriers = fields.MultiChoiceField(
        choices=serializers.CARRIERS,
        null=True,
        blank=True,
        help_text="""
        The list of carriers you want to apply the surcharge to.
        <br/>
        Note that by default, the surcharge is applied to all carriers
        """,
    )
    carrier_accounts = models.ManyToManyField(
        providers.Carrier,
        blank=True,
        help_text="""
        The list of carrier accounts you want to apply the surcharge to.
        <br/>
        Note that by default, the surcharge is applied to all carrier accounts
        """,
    )
    services = fields.MultiChoiceField(
        choices=serializers.SERVICES,
        null=True,
        blank=True,
        help_text="""
        The list of services you want to apply the surcharge to.
        <br/>
        Note that by default, the surcharge is applied to all services
        """,
    )

    @property
    def object_type(self):
        return "surcharge"

    def __str__(self):
        type_ = "$" if self.surcharge_type == "AMOUNT" else "%"
        return f"{self.id} ({self.amount} {type_})"

    def apply_charge(self, response: datatypes.RateResponse) -> datatypes.RateResponse:
        def apply(rate: datatypes.Rate) -> datatypes.Rate:
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

                amount = lib.to_decimal(
                    self.amount
                    if self.surcharge_type == "AMOUNT"
                    else (rate.total_charge * (typing.cast(float, self.amount) / 100))
                )
                total_charge = lib.to_decimal(rate.total_charge + amount)
                extra_charges = rate.extra_charges + [
                    karrio.ChargeDetails(
                        name=typing.cast(str, self.name),
                        amount=amount,
                        currency=rate.currency,
                    )
                ]

                return datatypes.Rate(
                    **{
                        **lib.to_dict(rate),
                        "total_charge": total_charge,
                        "extra_charges": extra_charges,
                    }
                )

            return rate

        return datatypes.RateResponse(
            messages=response.messages,
            rates=sorted(
                [apply(rate) for rate in response.rates],
                key=lambda rate: rate.total_charge,
            ),
        )
