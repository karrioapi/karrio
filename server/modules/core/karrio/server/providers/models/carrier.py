import typing
import functools
import django.conf as conf
import django.forms as forms
import django.db.models as models
import django.core.validators as validators

import karrio
import karrio.lib as lib
import karrio.core.utils as utils
import karrio.core.units as units
import karrio.api.gateway as gateway
import karrio.server.core.models as core
import karrio.server.core.fields as fields
import karrio.server.core.datatypes as datatypes


COUNTRIES = [(c.name, c.name) for c in units.Country]
CURRENCIES = [(c.name, c.name) for c in units.Currency]
WEIGHT_UNITS = [(c.name, c.name) for c in units.WeightUnit]
DIMENSION_UNITS = [(c.name, c.name) for c in units.DimensionUnit]
CAPABILITIES_CHOICES = [(c, c) for c in units.CarrierCapabilities.get_capabilities()]


class Manager(models.Manager):
    def get_queryset(self):
        from karrio.server.providers.models import MODELS

        return (
            super()
            .get_queryset()
            .prefetch_related(
                "configs",
                *[Model.__name__.lower() for Model in MODELS.values()],
            )
        )

        return queryset.filter(is_system=False)


class CarrierManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_system=False)


class SystemCarrierManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_system=True)


class Carrier(core.OwnedEntity):
    class Meta:
        ordering = ["test_mode", "-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="car_"),
        editable=False,
    )
    carrier_id = models.CharField(
        max_length=200,
        db_index=True,
        help_text="eg. canadapost, dhl_express, fedex, purolator_courrier, ups...",
    )
    test_mode = models.BooleanField(
        default=True,
        db_column="test_mode",
        help_text="Toggle carrier connection mode",
    )
    active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Disable/Hide carrier from clients",
    )
    is_system = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Determine that the carrier connection is available system wide.",
    )
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )
    active_users = models.ManyToManyField(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        related_name="active_users",
    )
    capabilities = fields.MultiChoiceField(
        choices=datatypes.CAPABILITIES_CHOICES,
        default=core.field_default([]),
        help_text="Select the capabilities of the carrier that you want to enable",
    )
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default({}),
        help_text="User defined metadata",
    )

    objects = Manager()
    user_carriers = CarrierManager()
    system_carriers = SystemCarrierManager()

    def __str__(self):
        return self.carrier_id

    @property
    def object_type(self):
        return "carrier"

    @property
    def carrier_name(self):
        return getattr(self.settings, "carrier_name", None)

    @property
    def settings(self):
        _, settings = self.__class__.resolve_settings(self)
        return settings

    @property
    def ext(self) -> str:
        return (
            "generic"
            if hasattr(self.settings, "custom_carrier_name")
            else getattr(self.settings, "carrier_name", None)
        )

    @property
    def gateway(self) -> gateway.Gateway:
        from karrio.server.core import middleware

        _context = middleware.SessionContext.get_current_request()
        _tracer = getattr(_context, "tracer", utils.Tracer())
        _carrier_name = self.ext

        return karrio.gateway[_carrier_name].create({**self.data.to_dict()}, _tracer)

    @property
    def data(self) -> datatypes.CarrierSettings:
        _computed_data: typing.Dict = dict(
            id=self.settings.id,
            carrier_name=self.settings.carrier_name,
            display_name=self.settings.carrier_display_name,
            config=self.config,
        )

        if hasattr(self.settings, "services"):
            _computed_data.update(
                services=[forms.model_to_dict(s) for s in self.settings.services.all()]
            )

        if hasattr(self.settings, "cache"):
            _computed_data.update(cache=self.settings.cache)

        if self.is_system and self.config is None:
            _computed_data.update(
                config=self.__class__.resolve_config(self, is_system_config=True)
            )

        return datatypes.CarrierSettings.create(
            {
                **forms.model_to_dict(self.settings),
                **_computed_data,
            }
        )

    @staticmethod
    def resolve_settings(carrier):
        from karrio.server.providers.models import MODELS

        return next(
            (
                (name, getattr(carrier, model.__name__.lower()))
                for name, model in MODELS.items()
                if hasattr(carrier, model.__name__.lower())
            ),
            (None, None),
        )

    @property
    def carrier_display_name(self):
        if hasattr(self.settings, "display_name"):
            return self.settings.display_name

        import karrio.references as references

        return references.collect_references()["carriers"].get(
            self.settings.carrier_name
        )

    @property
    def config(self):
        carrier = self.__class__.resolve_config(self)

        return getattr(carrier, "config", None)

    @staticmethod
    def resolve_config(
        carrier, is_user_config: bool = False, is_system_config: bool = False
    ):
        """Resolve the config for a carrier.
        Here are the rules:
        - If the carrier is a system carrier, return the first config with no org
        - If the carrier is an org carrier, return the first config from the org
        - If the carrier is a user carrier, return the first config from the user
        """
        from karrio.server.providers.models.config import CarrierConfig
        from karrio.server import serializers
        import karrio.server.core.middleware as middleware

        if carrier.id is None:
            return None

        _ctx = serializers.get_object_context(carrier)
        ctx = (
            _ctx
            if (_ctx.user or _ctx.org)
            else lib.failsafe(lambda: middleware.SessionContext.get_current_request())
        )
        has_ctx_user = ctx and (ctx.user or ctx.org)

        queryset = (
            CarrierConfig.objects.filter(carrier=carrier)
            if carrier.is_system
            else CarrierConfig.access_by(ctx).filter(carrier=carrier)
        )

        if carrier.is_system:
            _config = queryset.filter(
                created_by__is_staff=True,
                **({"org": None} if hasattr(carrier, "org") else {}),
            ).first()

            if has_ctx_user:
                return queryset.filter(
                    **(
                        {"org": (None if is_system_config else ctx.org)}
                        if hasattr(carrier, "org")
                        else {"created_by": ctx.user}
                    )
                ).first() or (None if is_user_config else _config)

            return _config

        return queryset.first()
