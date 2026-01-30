import typing
import functools
import django.conf as conf
import django.urls as urls
import django.db.models as models
import django.db.models.fields as fields
from django.contrib.contenttypes.fields import GenericRelation

import karrio.server.core.utils as utils
import karrio.server.core.models as core
import karrio.server.core.serializers as serializers


# -----------------------------------------------------------
# Model Managers
# -----------------------------------------------------------
# region


class AddressManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .defer("validation")
            .prefetch_related(
                *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
            )
        )


class ParcelManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "items",
                *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
            )
        )


class CommodityManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("parent")
            .prefetch_related(
                "children",
                *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
            )
        )


class PickupManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "shipments",
                *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
            )
        )


class ShipmentManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "created_by",
                "manifest",
                "shipment_tracker",
                "shipment_upload_record",
            )
            .prefetch_related(
                *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
            )
        )


class TrackingManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "created_by",
                "shipment",
            )
            .prefetch_related(
                *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
            )
        )


class DocumentUploadRecordManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
            )
        )


class ManifestManager(models.Manager):
    def get_queryset(self):
        # Load manifest details and associated carrier data efficiently
        return (
            super()
            .get_queryset()
            .defer("manifest")
            .prefetch_related(
                *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
            )
        )


# endregion

# -----------------------------------------------------------
# Shipping Management Models
# -----------------------------------------------------------
# region


@core.register_model
class Address(core.OwnedEntity):
    # Note: shipper_shipment, recipient_shipment, billing_address_shipment removed
    # as shipment addresses are now stored as JSON fields
    HIDDEN_PROPS = (
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
    objects = AddressManager()

    class Meta:
        db_table = "address"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="adr_"),
        editable=False,
    )

    postal_code = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    country_code = models.CharField(
        max_length=20, choices=serializers.COUNTRIES, db_index=True
    )
    email = models.EmailField(null=True, blank=True, db_index=True)
    city = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    federal_tax_id = models.CharField(max_length=100, null=True, blank=True)
    state_tax_id = models.CharField(max_length=100, null=True, blank=True)
    person_name = models.CharField(max_length=250, null=True, blank=True, db_index=True)
    company_name = models.CharField(
        max_length=250, null=True, blank=True, db_index=True
    )
    phone_number = models.CharField(max_length=250, null=True, blank=True)
    street_number = models.CharField(
        max_length=20, null=True, blank=True, db_index=True
    )
    address_line1 = models.CharField(
        max_length=100, null=True, blank=True, db_index=True
    )
    address_line2 = models.CharField(
        max_length=100, null=True, blank=True, db_index=True
    )
    state_code = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    suburb = models.CharField(max_length=100, null=True, blank=True)
    residential = models.BooleanField(null=True)

    validate_location = models.BooleanField(null=True)
    validation = models.JSONField(blank=True, null=True)

    # Template metadata: enables Address to serve as a reusable template
    # Structure: {"label": "Warehouse A", "is_default": true, "usage": ["sender", "return"]}
    meta = models.JSONField(
        blank=True,
        null=True,
        default=functools.partial(utils.identity, value={}),
        help_text="Template metadata: label, is_default, usage[]",
    )

    # Metafields via GenericRelation
    metafields = GenericRelation(
        "core.Metafield",
        related_query_name="address",
    )

    @property
    def is_template(self) -> bool:
        """Check if this address is a template (has meta with label)."""
        return bool(self.meta and self.meta.get("label"))

    @property
    def label(self) -> typing.Optional[str]:
        """Template label from meta field."""
        return (self.meta or {}).get("label")

    @property
    def is_default(self) -> bool:
        """Whether this is the default template."""
        return (self.meta or {}).get("is_default", False)

    @property
    def object_type(self):
        return "address"

    @property
    def shipment(self):
        if hasattr(self, "shipper_shipment"):
            return self.shipper_shipment
        if hasattr(self, "recipient_shipment"):
            return self.recipient_shipment
        if hasattr(self, "billing_address_shipment"):
            return self.billing_address_shipment

        return None

    @property
    def order(self):
        if hasattr(self, "shipper_order"):
            return self.shipper_order
        if hasattr(self, "recipient_order"):
            return self.recipient_order
        if hasattr(self, "bill_to_order"):
            return self.bill_to_order

        return None


@core.register_model
class Parcel(core.OwnedEntity):
    """Standalone parcel model - used for parcel templates only.

    Parcels attached to shipments are stored as JSON in Shipment.parcels field.
    """

    HIDDEN_PROPS = (*(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),)
    objects = ParcelManager()

    class Meta:
        db_table = "parcel"
        verbose_name = "Parcel"
        verbose_name_plural = "Parcels"
        ordering = ["created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="pcl_"),
        editable=False,
    )

    weight = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    packaging_type = models.CharField(max_length=100, null=True, blank=True)
    package_preset = models.CharField(max_length=100, null=True, blank=True)
    is_document = models.BooleanField(default=False, blank=True, null=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    content = models.CharField(max_length=250, null=True, blank=True)
    reference_number = models.CharField(
        max_length=100, null=True, blank=True, db_index=True
    )
    weight_unit = models.CharField(
        max_length=2, choices=serializers.WEIGHT_UNIT, null=True, blank=True
    )
    dimension_unit = models.CharField(
        max_length=2, choices=serializers.DIMENSION_UNIT, null=True, blank=True
    )
    items = models.ManyToManyField(
        "Commodity", blank=True, related_name="commodity_parcel"
    )
    freight_class = models.CharField(max_length=10, null=True, blank=True)
    options = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )

    # Template metadata: enables Parcel to serve as a reusable template
    # Structure: {"label": "Standard Box", "is_default": true}
    meta = models.JSONField(
        blank=True,
        null=True,
        default=functools.partial(utils.identity, value={}),
        help_text="Template metadata: label, is_default",
    )

    # Metafields via GenericRelation
    metafields = GenericRelation(
        "core.Metafield",
        related_query_name="parcel",
    )

    def delete(self, *args, **kwargs):
        self.items.all().delete()
        return super().delete(*args, **kwargs)

    @property
    def is_template(self) -> bool:
        """Check if this parcel is a template (has meta with label)."""
        return bool(self.meta and self.meta.get("label"))

    @property
    def label(self) -> typing.Optional[str]:
        """Template label from meta field."""
        return (self.meta or {}).get("label")

    @property
    def is_default(self) -> bool:
        """Whether this is the default template."""
        return (self.meta or {}).get("is_default", False)

    @property
    def object_type(self):
        return "parcel"

    @property
    def shipment(self):
        # Standalone parcels (templates) don't have a shipment relationship
        # Parcels attached to shipments are stored as JSON in Shipment.parcels
        return None


@core.register_model
class Commodity(core.OwnedEntity):
    HIDDEN_PROPS = (
        "children",
        "commodity_parcel",
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
    objects = CommodityManager()

    class Meta:
        db_table = "commodity"
        verbose_name = "Commodity"
        verbose_name_plural = "Commodities"
        ordering = ["created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="cdt_"),
        editable=False,
    )

    weight = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    sku = models.CharField(max_length=250, null=True, blank=True, db_index=True)
    hs_code = models.CharField(max_length=250, null=True, blank=True, db_index=True)
    product_url = models.CharField(max_length=250, null=True, blank=True)
    image_url = models.CharField(max_length=250, null=True, blank=True)
    product_id = models.CharField(max_length=250, null=True, blank=True)
    variant_id = models.CharField(max_length=250, null=True, blank=True)
    value_amount = models.FloatField(blank=True, null=True)
    weight_unit = models.CharField(
        max_length=2, choices=serializers.WEIGHT_UNIT, null=True, blank=True
    )
    value_currency = models.CharField(
        max_length=3, choices=serializers.CURRENCIES, null=True, blank=True
    )
    origin_country = models.CharField(
        max_length=3,
        choices=serializers.COUNTRIES,
        null=True,
        blank=True,
        db_index=True,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    metadata = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )

    # Template metadata: enables Commodity to serve as a reusable template (product)
    # Structure: {"label": "Widget Pro", "is_default": false}
    meta = models.JSONField(
        blank=True,
        null=True,
        default=functools.partial(utils.identity, value={}),
        help_text="Template metadata: label, is_default",
    )

    def delete(self, *args, **kwargs):
        self.children.all().delete()
        return super().delete(*args, **kwargs)

    @property
    def is_template(self) -> bool:
        """Check if this commodity is a template/product (has meta with label)."""
        return bool(self.meta and self.meta.get("label"))

    @property
    def label(self) -> typing.Optional[str]:
        """Template label from meta field."""
        return (self.meta or {}).get("label")

    @property
    def is_default(self) -> bool:
        """Whether this is the default template."""
        return (self.meta or {}).get("is_default", False)

    @property
    def object_type(self):
        return "commodity"

    @property
    def parcel(self):
        return self.commodity_parcel.first()

    @property
    def shipment(self):
        return getattr(self.parcel, "shipment", None)

    @property
    def order(self):
        if hasattr(self, "order_link"):
            return self.order_link.order
        if self.parent is not None:
            return self.parent.order

        return None


class Product(Commodity):
    """Product is a proxy model for Commodity, used for template/product API endpoints.

    This provides a cleaner "Product" naming for the template API while using
    the same underlying Commodity table.
    """

    class Meta:
        proxy = True
        verbose_name = "Product"
        verbose_name_plural = "Products"

    @property
    def object_type(self):
        return "product"


@core.register_model
class Pickup(core.OwnedEntity):
    """Pickup model with embedded JSON address and carrier snapshot."""

    DIRECT_PROPS = [
        "confirmation_number",
        "pickup_date",
        "instruction",
        "package_location",
        "ready_time",
        "closing_time",
        "test_mode",
        "pickup_charge",
        "created_by",
        "metadata",
        "meta",
        "address",  # Embedded JSON field
        "carrier",  # Carrier snapshot
    ]
    objects = PickupManager()

    class Meta:
        db_table = "pickups"
        verbose_name = "Pickup"
        verbose_name_plural = "Pickups"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="pck_"),
        editable=False,
    )
    confirmation_number = models.CharField(max_length=100, blank=False, db_index=True)
    test_mode = models.BooleanField(null=False)
    pickup_date = models.DateField(blank=False)
    ready_time = models.CharField(max_length=5, blank=False)
    closing_time = models.CharField(max_length=5, blank=False)
    instruction = models.CharField(max_length=250, null=True, blank=True)
    package_location = models.CharField(max_length=250, null=True, blank=True)

    # ─────────────────────────────────────────────────────────────────
    # EMBEDDED JSON FIELDS
    # ─────────────────────────────────────────────────────────────────
    address = models.JSONField(
        blank=True,
        null=True,
        help_text="Pickup address (embedded JSON)",
    )

    # Carrier snapshot - replaces pickup_carrier FK
    # Structure: {connection_id, connection_type, carrier_code, carrier_id, carrier_name, test_mode}
    carrier = models.JSONField(
        blank=True,
        null=True,
        help_text="Carrier snapshot at time of pickup creation",
    )

    # ─────────────────────────────────────────────────────────────────
    # OPERATIONAL JSON FIELDS
    # ─────────────────────────────────────────────────────────────────
    options = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    pickup_charge = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    meta = models.JSONField(
        blank=True, default=functools.partial(utils.identity, value={})
    )

    # ─────────────────────────────────────────────────────────────────
    # SHIPMENT RELATION (kept - operational necessity)
    # ─────────────────────────────────────────────────────────────────
    shipments = models.ManyToManyField("Shipment", related_name="shipment_pickup")

    # Metafields via GenericRelation
    metafields = GenericRelation(
        "core.Metafield",
        related_query_name="pickup",
    )

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "pickup"

    # Computed properties from carrier snapshot

    @property
    def carrier_id(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_id")

    @property
    def carrier_name(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_name")

    @property
    def carrier_code(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_code")

    @property
    def parcels(self) -> typing.List[dict]:
        """Get all parcels from related shipments as JSON data."""
        if self.pk is None:
            return []
        return sum(
            [shipment.parcels or [] for shipment in self.shipments.all()], []
        )

    @property
    def tracking_numbers(self) -> typing.List[str]:
        if self.pk is None:
            return []
        return [shipment.tracking_number for shipment in self.shipments.all()]

    @property
    def pickup_type(self) -> typing.Optional[str]:
        """Get pickup type from meta field (one_time, daily, recurring)."""
        if self.meta is None:
            return "one_time"
        return self.meta.get("pickup_type", "one_time")

    @property
    def recurrence(self) -> typing.Optional[dict]:
        """Get recurrence config from meta field."""
        if self.meta is None:
            return None
        return self.meta.get("recurrence")


@core.register_model
class Tracking(core.OwnedEntity):
    """Tracking model with embedded carrier snapshot."""

    DIRECT_PROPS = [
        "metadata",
        "info",
        "carrier",  # Carrier snapshot
    ]
    HIDDEN_PROPS = (
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
    objects = TrackingManager()

    class Meta:
        db_table = "tracking-status"
        verbose_name = "Tracking Status"
        verbose_name_plural = "Tracking Statuses"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"], name="tracking_created_at_idx"),
            # JSONField indexes for carrier snapshot queries
            models.Index(
                fields.json.KeyTextTransform("carrier_code", "carrier"),
                condition=models.Q(carrier__isnull=False),
                name="tracking_carrier_code_idx",
            ),
            models.Index(
                fields.json.KeyTextTransform("connection_id", "carrier"),
                condition=models.Q(carrier__isnull=False),
                name="tracking_connection_id_idx",
            ),
        ]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="trk_"),
        editable=False,
    )

    status = models.CharField(
        max_length=25,
        choices=serializers.TRACKER_STATUS,
        default=serializers.TRACKER_STATUS[0][0],
        db_index=True,
    )
    tracking_number = models.CharField(max_length=100, db_index=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    info = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    events = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
    )
    delivered = models.BooleanField(blank=True, null=True, default=False)
    estimated_delivery = models.DateField(null=True, blank=True)
    test_mode = models.BooleanField(null=False)
    messages = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
    )
    options = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    meta = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    metadata = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )

    delivery_image = models.TextField(max_length=None, null=True, blank=True)
    signature_image = models.TextField(max_length=None, null=True, blank=True)

    # ─────────────────────────────────────────────────────────────────
    # CARRIER SNAPSHOT (replaces tracking_carrier FK)
    # ─────────────────────────────────────────────────────────────────
    # Structure: {connection_id, connection_type, carrier_code, carrier_id, carrier_name, test_mode}
    carrier = models.JSONField(
        blank=True,
        null=True,
        help_text="Carrier snapshot at time of tracker creation",
    )

    # ─────────────────────────────────────────────────────────────────
    # SHIPMENT RELATION (kept - operational necessity)
    # ─────────────────────────────────────────────────────────────────
    shipment = models.OneToOneField(
        "Shipment", on_delete=models.CASCADE, related_name="shipment_tracker", null=True
    )

    # Metafields via GenericRelation
    metafields = GenericRelation(
        "core.Metafield",
        related_query_name="tracking",
    )

    @property
    def object_type(self):
        return "tracker"

    # Computed properties from carrier snapshot

    @property
    def carrier_id(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_id")

    @property
    def carrier_name(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_name")

    @property
    def carrier_code(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_code")

    @property
    def pending(self) -> bool:
        return len(self.events) == 0 or (
            len(self.events) == 1 and self.events[0].get("code") == "CREATED"
        )

    @property
    def delivery_image_url(self) -> str:
        if self.delivery_image is None:
            return None

        return urls.reverse(
            "karrio.server.manager:tracker-docs",
            kwargs=dict(pk=self.pk, doc="delivery_image"),
        )

    @property
    def signature_image_url(self) -> str:
        if self.signature_image is None:
            return None

        return urls.reverse(
            "karrio.server.manager:tracker-docs",
            kwargs=dict(pk=self.pk, doc="signature_image"),
        )


@core.register_model
class Shipment(core.OwnedEntity):
    """Shipment model with embedded JSON data for addresses, parcels, customs, and carrier."""

    DIRECT_PROPS = [
        "options",
        "services",
        "carrier_ids",
        "status",
        "meta",
        "label_type",
        "tracking_number",
        "tracking_url",
        "shipment_identifier",
        "test_mode",
        "messages",
        "rates",
        "payment",
        "metadata",
        "created_by",
        "reference",
        "applied_fees",  # Accounting: addons + surcharge COGS values
        # Embedded JSON fields
        "shipper",
        "recipient",
        "parcels",
        "customs",
        "return_address",
        "billing_address",
        "selected_rate",
        "carrier",  # Carrier snapshot
    ]
    HIDDEN_PROPS = (
        "label",
        "invoice",
        "shipment_pickup",
        "shipment_tracker",
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
    objects = ShipmentManager()

    class Meta:
        db_table = "shipments"
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields.json.KeyTextTransform("service", "selected_rate"),
                condition=models.Q(meta__object_id__isnull=False),
                name="shipment_service_idx",
            ),
            models.Index(fields=["created_at"], name="shipment_created_at_idx"),
            # JSONField index for carrier snapshot queries
            models.Index(
                fields.json.KeyTextTransform("carrier_code", "carrier"),
                condition=models.Q(carrier__isnull=False),
                name="shipment_carrier_code_idx",
            ),
        ]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="shp_"),
        editable=False,
    )
    status = models.CharField(
        max_length=50,
        choices=serializers.SHIPMENT_STATUS,
        default=serializers.SHIPMENT_STATUS[0][0],
        db_index=True,
    )
    label_type = models.CharField(max_length=25, null=True, blank=True)
    tracking_number = models.CharField(
        max_length=100, null=True, blank=True, db_index=True
    )
    shipment_identifier = models.CharField(max_length=100, null=True, blank=True)
    tracking_url = models.TextField(max_length=None, null=True, blank=True)
    test_mode = models.BooleanField(null=False)
    reference = models.CharField(max_length=100, null=True, blank=True)

    # Document storage
    label = models.TextField(max_length=None, null=True, blank=True)
    invoice = models.TextField(max_length=None, null=True, blank=True)

    # ─────────────────────────────────────────────────────────────────
    # EMBEDDED JSON FIELDS
    # ─────────────────────────────────────────────────────────────────
    shipper = models.JSONField(
        blank=True,
        null=True,
        help_text="Shipper address (embedded JSON)",
    )
    recipient = models.JSONField(
        blank=True,
        null=True,
        help_text="Recipient address (embedded JSON)",
    )
    return_address = models.JSONField(
        blank=True,
        null=True,
        help_text="Return address (embedded JSON)",
    )
    billing_address = models.JSONField(
        blank=True,
        null=True,
        help_text="Billing address (embedded JSON)",
    )
    parcels = models.JSONField(
        blank=True,
        null=True,
        default=functools.partial(utils.identity, value=[]),
        help_text="Parcels array with nested items (embedded JSON)",
    )
    customs = models.JSONField(
        blank=True,
        null=True,
        help_text="Customs information (embedded JSON)",
    )

    # ─────────────────────────────────────────────────────────────────
    # OPERATIONAL JSON FIELDS
    # ─────────────────────────────────────────────────────────────────
    # selected_rate contains rate details:
    # {id, carrier_id, carrier_name, service, currency, total_charge, test_mode, meta: {...}}
    selected_rate = models.JSONField(blank=True, null=True)
    rates = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
    )
    payment = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=None)
    )
    options = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    services = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
    )
    carrier_ids = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[]),
        help_text="List of carrier IDs to filter rate requests",
    )
    messages = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
    )
    meta = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    metadata = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    extra_documents = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
    )
    applied_fees = models.JSONField(
        blank=True,
        null=True,
        default=functools.partial(utils.identity, value=[]),
        help_text="Applied fees for accounting: addons + surcharge COGS values",
    )

    # ─────────────────────────────────────────────────────────────────
    # CARRIER SNAPSHOT (consistent with Tracking, Pickup, Manifest, DocumentUploadRecord)
    # ─────────────────────────────────────────────────────────────────
    # Structure: {connection_id, connection_type, carrier_code, carrier_id, carrier_name, test_mode}
    carrier = models.JSONField(
        blank=True,
        null=True,
        help_text="Carrier snapshot at time of label purchase",
    )

    # ─────────────────────────────────────────────────────────────────
    # MANIFEST RELATION (kept - operational necessity)
    # ─────────────────────────────────────────────────────────────────
    manifest = models.ForeignKey(
        "Manifest",
        on_delete=models.SET_NULL,
        related_name="shipments",
        blank=True,
        null=True,
    )

    # Metafields via GenericRelation
    metafields = GenericRelation(
        "core.Metafield",
        related_query_name="shipment",
    )

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "shipment"

    # Computed properties from carrier snapshot

    @property
    def carrier_id(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_id")

    @property
    def carrier_name(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_name")

    @property
    def carrier_code(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_code")

    @property
    def tracker_id(self) -> typing.Optional[str]:
        return getattr(self.tracker, "id", None)

    @property
    def selected_rate_id(self) -> typing.Optional[str]:
        if self.selected_rate is None:
            return None
        return self.selected_rate.get("id")

    @property
    def service(self) -> typing.Optional[str]:
        if self.selected_rate is None:
            return None
        return self.selected_rate.get("service")

    @property
    def tracker(self):
        if hasattr(self, "shipment_tracker"):
            return self.shipment_tracker
        return None

    @property
    def label_url(self) -> typing.Optional[str]:
        if self.label is None:
            return None

        return urls.reverse(
            "karrio.server.manager:shipment-docs",
            kwargs=dict(
                pk=self.pk, doc="label", format=(self.label_type or "PDF").lower()
            ),
        )

    @property
    def invoice_url(self) -> typing.Optional[str]:
        if self.invoice is None:
            return None

        return urls.reverse(
            "karrio.server.manager:shipment-docs",
            kwargs=dict(pk=self.pk, doc="invoice", format="pdf"),
        )

    @property
    def documents(self) -> typing.Dict[str, str]:
        return dict(
            label=self.label,
            invoice=self.invoice,
        )

@core.register_model
class DocumentUploadRecord(core.OwnedEntity):
    """Document upload record with embedded carrier snapshot."""

    DIRECT_PROPS = [
        "documents",
        "messages",
        "meta",
        "options",
        "reference",
        "carrier",  # Carrier snapshot
    ]
    HIDDEN_PROPS = (
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
    objects = DocumentUploadRecordManager()

    class Meta:
        db_table = "document-upload-record"
        verbose_name = "Document Upload Record"
        verbose_name_plural = "Document Upload Records"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="uprec_"),
        editable=False,
    )
    documents = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
    )
    messages = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
    )
    meta = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    options = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    reference = models.CharField(max_length=100, null=True, blank=True)

    # ─────────────────────────────────────────────────────────────────
    # CARRIER SNAPSHOT (replaces upload_carrier FK)
    # ─────────────────────────────────────────────────────────────────
    # Structure: {connection_id, connection_type, carrier_code, carrier_id, carrier_name, test_mode}
    carrier = models.JSONField(
        blank=True,
        null=True,
        help_text="Carrier snapshot at time of document upload",
    )

    # ─────────────────────────────────────────────────────────────────
    # SHIPMENT RELATION (kept - operational necessity)
    # ─────────────────────────────────────────────────────────────────
    shipment = models.OneToOneField(
        "Shipment",
        on_delete=models.CASCADE,
        related_name="shipment_upload_record",
    )

    # Computed properties from carrier snapshot

    @property
    def carrier_id(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_id")

    @property
    def carrier_name(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_name")

    @property
    def carrier_code(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_code")


@core.register_model
class Manifest(core.OwnedEntity):
    """Manifest model with embedded JSON address and carrier snapshot."""

    DIRECT_PROPS = [
        "meta",
        "options",
        "metadata",
        "messages",
        "created_by",
        "reference",
        "address",  # Embedded JSON field
        "carrier",  # Carrier snapshot
    ]
    HIDDEN_PROPS = (
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
    objects = ManifestManager()

    class Meta:
        db_table = "manifests"
        verbose_name = "Manifest"
        verbose_name_plural = "Manifests"
        ordering = ["-created_at"]
        indexes = [
            # JSONField index for carrier snapshot queries
            models.Index(
                fields.json.KeyTextTransform("carrier_code", "carrier"),
                condition=models.Q(carrier__isnull=False),
                name="manifest_carrier_code_idx",
            ),
        ]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="manf_"),
        editable=False,
    )
    reference = models.CharField(max_length=100, null=True, blank=True)
    manifest = models.TextField(max_length=None, null=True, blank=True)
    test_mode = models.BooleanField(null=False)

    # ─────────────────────────────────────────────────────────────────
    # EMBEDDED JSON FIELDS
    # ─────────────────────────────────────────────────────────────────
    address = models.JSONField(
        blank=True,
        null=True,
        help_text="Manifest address (embedded JSON)",
    )

    # Carrier snapshot - replaces manifest_carrier FK
    # Structure: {connection_id, connection_type, carrier_code, carrier_id, carrier_name, test_mode}
    carrier = models.JSONField(
        blank=True,
        null=True,
        help_text="Carrier snapshot at time of manifest creation",
    )

    # ─────────────────────────────────────────────────────────────────
    # OPERATIONAL JSON FIELDS
    # ─────────────────────────────────────────────────────────────────
    metadata = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    meta = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    options = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    messages = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
    )

    # Computed properties from carrier snapshot

    @property
    def object_type(self):
        return "manifest"

    @property
    def carrier_id(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_id")

    @property
    def carrier_name(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_name")

    @property
    def carrier_code(self) -> typing.Optional[str]:
        if self.carrier is None:
            return None
        return self.carrier.get("carrier_code")

    @property
    def manifest_url(self) -> typing.Optional[str]:
        if self.manifest is None:
            return None

        return urls.reverse(
            "karrio.server.manager:manifest-docs",
            kwargs=dict(pk=self.pk, doc="manifest", format="pdf"),
        )

    @property
    def shipment_identifiers(self) -> typing.List[str]:
        return [shipment.shipment_identifier for shipment in self.shipments.all()]


# endregion
