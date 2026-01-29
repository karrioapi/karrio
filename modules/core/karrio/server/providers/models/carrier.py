"""
Carrier Model - User/Organization-owned carrier connections.

This model represents carrier connections owned by users or organizations.
System-wide connections are handled by SystemConnection model.
Users can enable system connections via BrokeredConnection.
"""
import typing
import functools
import django.conf as conf
import django.forms as forms
import django.db.models as models
import django.core.cache as caching
from django.contrib.contenttypes.fields import GenericRelation

import karrio.lib as lib
import karrio.sdk as karrio
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


class CarrierConnectionQuerySet(models.QuerySet):
    """QuerySet for CarrierConnection with common filters."""

    def active(self):
        return self.filter(active=True)

    def for_carrier(self, carrier_code: str):
        return self.filter(carrier_code=carrier_code)


class CarrierConnectionManager(models.Manager):
    """Manager for user/org-owned carrier connections."""

    def get_queryset(self):
        return (
            CarrierConnectionQuerySet(self.model, using=self._db)
            .select_related(
                "created_by",
                "rate_sheet",
                *(("link",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
            )
        )

    def active(self):
        return self.get_queryset().active()

    def for_carrier(self, carrier_code: str):
        return self.get_queryset().for_carrier(carrier_code)


@core.register_model
class CarrierConnection(core.OwnedEntity):
    """
    User/Organization-owned carrier connections.

    Key characteristics:
    - Created and managed by users/orgs
    - Full access to credentials and config
    - Visibility:
      - OSS: Accessible to ALL users (system-wide shared)
      - Insiders: Scoped to organization members via CarrierLink
    """

    class Meta:
        db_table = "CarrierConnection"
        verbose_name = "Carrier Connection"
        verbose_name_plural = "Carrier Connections"
        ordering = ["test_mode", "-created_at"]
        indexes = [
            models.Index(fields=["carrier_code", "active"]),
        ]

    CONTEXT_RELATIONS = ["rate_sheet"]

    objects = CarrierConnectionManager()

    # ─────────────────────────────────────────────────────────────────
    # IDENTITY
    # ─────────────────────────────────────────────────────────────────
    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="car_"),
        editable=False,
    )
    carrier_code = models.CharField(
        max_length=100,
        db_index=True,
        default="generic",
        help_text="Carrier identifier (e.g., 'dhl_express', 'fedex')",
    )
    carrier_id = models.CharField(
        max_length=150,
        db_index=True,
        help_text="User-defined connection identifier",
    )

    # ─────────────────────────────────────────────────────────────────
    # CREDENTIALS (User-managed)
    # ─────────────────────────────────────────────────────────────────
    credentials = models.JSONField(
        default=core.field_default({}),
        help_text="Carrier API credentials",
    )

    # ─────────────────────────────────────────────────────────────────
    # CONFIGURATION (Full control)
    # ─────────────────────────────────────────────────────────────────
    config = models.JSONField(
        default=core.field_default({}),
        blank=True,
        help_text="Operational configuration",
    )

    # ─────────────────────────────────────────────────────────────────
    # CAPABILITIES & STATUS
    # ─────────────────────────────────────────────────────────────────
    capabilities = fields.MultiChoiceField(
        choices=datatypes.CAPABILITIES_CHOICES,
        default=core.field_default([]),
        help_text="Enabled carrier capabilities",
    )
    active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Enable/disable carrier connection",
    )
    test_mode = models.BooleanField(
        default=True,
        db_column="test_mode",
        help_text="Toggle carrier connection mode",
    )

    # ─────────────────────────────────────────────────────────────────
    # OWNERSHIP
    # ─────────────────────────────────────────────────────────────────
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )

    # NOTE: Organization linking is handled via CarrierLink in orgs package (Insiders only)

    # ─────────────────────────────────────────────────────────────────
    # RATE SHEET
    # ─────────────────────────────────────────────────────────────────
    rate_sheet = models.ForeignKey(
        "RateSheet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="carrier_connections",
    )

    # ─────────────────────────────────────────────────────────────────
    # METADATA
    # ─────────────────────────────────────────────────────────────────
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=core.field_default({}),
        help_text="User defined metadata",
    )

    # Metafields via GenericRelation
    metafields = GenericRelation(
        "core.Metafield",
        related_query_name="carrier_connection",
    )

    def __str__(self):
        return self.carrier_id

    # ─────────────────────────────────────────────────────────────────
    # COMPUTED PROPERTIES
    # ─────────────────────────────────────────────────────────────────

    @property
    def object_type(self):
        return "carrier-connection"

    @property
    def ext(self) -> str:
        """Get carrier extension name for SDK lookup."""
        return (
            "generic"
            if "custom_carrier_name" in self.credentials
            else lib.failsafe(lambda: self.carrier_code) or "generic"
        )

    @property
    def carrier_name(self) -> str:
        """Alias for ext - the carrier type name."""
        return self.ext

    @property
    def display_name(self) -> str:
        """Get human-readable display name."""
        import karrio.references as references

        return (
            self.credentials.get("display_name")
            or references.REFERENCES.get("carriers", {}).get(self.ext)
            or self.carrier_id
        )

    @property
    def services(self) -> typing.Optional[typing.List]:
        """Get services from linked rate sheet."""
        if self.rate_sheet is None:
            return None
        return self.rate_sheet.services.all()

    # ─────────────────────────────────────────────────────────────────
    # SDK INTEGRATION
    # ─────────────────────────────────────────────────────────────────

    @property
    def data(self) -> datatypes.CarrierSettings:
        """Build CarrierSettings for SDK gateway creation."""
        _computed_data: typing.Dict = dict(
            id=self.id,
            config=self.config or {},
            test_mode=self.test_mode,
            metadata=self.metadata or {},
            carrier_id=self.carrier_id,
            carrier_name=self.ext,
            display_name=self.display_name,
        )

        # Include services from rate sheet
        if any(self.services or []):
            _computed_data.update(
                services=[
                    {
                        **forms.model_to_dict(s),
                        "zones": s.zones,
                        "surcharges": s.surcharges,
                    }
                    for s in self.services
                ]
            )

        return datatypes.CarrierSettings.create({**self.credentials, **_computed_data})

    @property
    def gateway(self) -> gateway.Gateway:
        """Create SDK gateway instance for this connection."""
        import karrio.server.core.middleware as middleware
        import karrio.server.core.config as system_config

        _context = middleware.SessionContext.get_current_request()
        _tracer = getattr(_context, "tracer", lib.Tracer())
        _cache = lib.Cache(caching.cache)
        _config = lib.SystemConfig(system_config.config)

        return karrio.gateway[self.ext].create(
            self.data.to_dict(),
            _tracer,
            _cache,
            _config,
        )


def create_carrier_proxy(carrier_name: str, display_name: str):
    """Create a proxy model for a specific carrier type."""

    class _CarrierConnectionManager(CarrierConnectionManager):
        def get_queryset(self):
            return super().get_queryset().filter(carrier_code=carrier_name)

    return type(
        f"{carrier_name}Connection",
        (CarrierConnection,),
        {
            "Meta": type(
                "Meta",
                (),
                {
                    "proxy": True,
                    "__module__": __name__,
                    "verbose_name": f"{display_name} Connection",
                    "verbose_name_plural": f"{display_name} Connections",
                },
            ),
            "__module__": __name__,
            "objects": _CarrierConnectionManager(),
        },
    )
