import typing
import functools
import django.conf as conf
import django.urls as urls
import django.db.models as models
import django.db.models.fields as fields

import karrio.server.core.utils as utils
import karrio.server.core.models as core
import karrio.server.providers.models as providers
import karrio.server.core.serializers as serializers


# -----------------------------------------------------------
# Model Managers
# -----------------------------------------------------------
# region


class AddressManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().defer("validation")


class ParcelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related("items")


class CommodityManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().select_related("parent").prefetch_related("children")
        )


class CustomsManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("duty_billing_address")
            .prefetch_related("commodities")
        )


class PickupManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("pickup_carrier")
            .prefetch_related("shipments")
        )


class ShipmentManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "created_by",
                "recipient",
                "shipper",
                "customs",
                "manifest",
                "return_address",
                "billing_address",
                "shipment_tracker",
                "selected_rate_carrier",
                "shipment_upload_record",
            )
            .prefetch_related(
                "parcels",
                "carriers",
            )
        )


class TrackingManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .defer("shipment")
            .prefetch_related(
                "tracking_carrier",
            )
            .select_related(
                "created_by",
            )
        )


class DocumentUploadRecordManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("upload_carrier")


class ManifestManager(models.Manager):
    def get_queryset(self):
        # Load manifest details and associated carrier data efficiently
        return (
            super().get_queryset().select_related("manifest_carrier").defer("manifest")
        )


# endregion

# -----------------------------------------------------------
# Shipping Management Models
# -----------------------------------------------------------
# region


@core.register_model
class Address(core.OwnedEntity):
    HIDDEN_PROPS = (
        "shipper_shipment",
        "recipient_shipment",
        "billing_address_shipment",
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
        *(
            ("shipper_order", "recipient_order")
            if conf.settings.ORDERS_MANAGEMENT
            else tuple()
        ),
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
    city = models.CharField(max_length=30, null=True, blank=True, db_index=True)
    federal_tax_id = models.CharField(max_length=20, null=True, blank=True)
    state_tax_id = models.CharField(max_length=20, null=True, blank=True)
    person_name = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    company_name = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    street_number = models.CharField(
        max_length=20, null=True, blank=True, db_index=True
    )
    address_line1 = models.CharField(
        max_length=100, null=True, blank=True, db_index=True
    )
    address_line2 = models.CharField(
        max_length=100, null=True, blank=True, db_index=True
    )
    state_code = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    suburb = models.CharField(max_length=20, null=True, blank=True)
    residential = models.BooleanField(null=True)

    validate_location = models.BooleanField(null=True)
    validation = models.JSONField(blank=True, null=True)

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
    def customs(self):
        if hasattr(self, "duty_billing_address_customs"):
            return self.duty_billing_address_customs

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
    HIDDEN_PROPS = (
        "parcel_shipment",
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
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
    packaging_type = models.CharField(max_length=50, null=True, blank=True)
    package_preset = models.CharField(max_length=50, null=True, blank=True)
    is_document = models.BooleanField(default=False, blank=True, null=True)
    description = models.CharField(max_length=35, null=True, blank=True)
    content = models.CharField(max_length=35, null=True, blank=True)
    reference_number = models.CharField(
        max_length=50, null=True, blank=True, db_index=True
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

    def delete(self, *args, **kwargs):
        self.items.all().delete()
        return super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "parcel"

    @property
    def shipment(self):
        return self.parcel_shipment.first()


@core.register_model
class Commodity(core.OwnedEntity):
    HIDDEN_PROPS = (
        "children",
        "commodity_parcel",
        "commodity_customs",
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
    title = models.CharField(max_length=35, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=35, null=True, blank=True, db_index=True)
    hs_code = models.CharField(max_length=35, null=True, blank=True, db_index=True)
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

    def delete(self, *args, **kwargs):
        self.children.all().delete()
        return super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "commodity"

    @property
    def parcel(self):
        return self.commodity_parcel.first()

    @property
    def customs(self):
        return self.commodity_customs.first()

    @property
    def shipment(self):
        related = self.customs or self.parcel

        return getattr(related, "shipment", None)

    @property
    def order(self):
        if hasattr(self, "order_link"):
            return self.order_link.order
        if self.parent is not None:
            return self.parent.order

        return None


@core.register_model
class Customs(core.OwnedEntity):
    DIRECT_PROPS = [
        "content_description",
        "content_type",
        "incoterm",
        "commercial_invoice",
        "certify",
        "duty",
        "created_by",
        "signer",
        "invoice",
        "invoice_date",
        "options",
    ]
    RELATIONAL_PROPS = ["commodities", "duty_billing_address"]
    HIDDEN_PROPS = (
        "customs_shipment",
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
    objects = CustomsManager()

    class Meta:
        db_table = "customs"
        verbose_name = "Customs Info"
        verbose_name_plural = "Customs Info"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="cst_"),
        editable=False,
    )

    certify = models.BooleanField(null=True)
    commercial_invoice = models.BooleanField(null=True)
    content_type = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    content_description = models.CharField(max_length=250, null=True, blank=True)
    incoterm = models.CharField(
        max_length=20, choices=serializers.INCOTERMS, db_index=True
    )
    invoice = models.CharField(max_length=50, null=True, blank=True)
    invoice_date = models.CharField(max_length=50, null=True, blank=True)
    signer = models.CharField(max_length=50, null=True, blank=True)

    duty = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=None)
    )
    options = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )

    # System Reference fields

    commodities = models.ManyToManyField(
        "Commodity", blank=True, related_name="commodity_customs"
    )
    duty_billing_address = models.OneToOneField(
        "Address",
        null=True,
        on_delete=models.SET_NULL,
        related_name="duty_billing_address_customs",
    )

    def delete(self, *args, **kwargs):
        self.commodities.all().delete()
        return super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "customs_info"

    @property
    def shipment(self):
        if hasattr(self, "customs_shipment"):
            return self.customs_shipment

        return None


@core.register_model
class Pickup(core.OwnedEntity):
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
    ]
    objects = PickupManager()

    class Meta:
        db_table = "pickup"
        verbose_name = "Pickup"
        verbose_name_plural = "Pickups"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="pck_"),
        editable=False,
    )
    confirmation_number = models.CharField(max_length=50, blank=False, db_index=True)
    test_mode = models.BooleanField(null=False)
    pickup_date = models.DateField(blank=False)
    ready_time = models.CharField(max_length=5, blank=False)
    closing_time = models.CharField(max_length=5, blank=False)
    instruction = models.CharField(max_length=200, null=True, blank=True)
    package_location = models.CharField(max_length=200, null=True, blank=True)

    options = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    pickup_charge = models.JSONField(blank=True, null=True)
    address = models.ForeignKey(
        "Address",
        on_delete=models.CASCADE,
        related_name="address_pickup",
        blank=True,
        null=True,
    )
    metadata = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    meta = models.JSONField(
        blank=True, default=functools.partial(utils.identity, value={})
    )

    # System Reference fields

    pickup_carrier = models.ForeignKey(providers.Carrier, on_delete=models.CASCADE)
    shipments = models.ManyToManyField("Shipment", related_name="shipment_pickup")

    def delete(self, *args, **kwargs):
        handle = self.address or super()
        return handle.delete(*args, **kwargs)

    @property
    def object_type(self):
        return "pickup"

    # Computed properties

    @property
    def carrier_id(self) -> str:
        return typing.cast(providers.Carrier, self.pickup_carrier).carrier_id

    @property
    def carrier_name(self) -> str:
        return typing.cast(providers.Carrier, self.pickup_carrier).data.carrier_name

    @property
    def parcels(self) -> typing.List[Parcel]:
        return sum(
            [list(shipment.parcels.all()) for shipment in self.shipments.all()], []
        )

    @property
    def tracking_numbers(self) -> typing.List[str]:
        return [shipment.tracking_number for shipment in self.shipments.all()]


@core.register_model
class Tracking(core.OwnedEntity):
    DIRECT_PROPS = [
        "metadata",
        "info",
    ]
    HIDDEN_PROPS = (
        "tracking_carrier",
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
    objects = TrackingManager()

    class Meta:
        db_table = "tracking-status"
        verbose_name = "Tracking Status"
        verbose_name_plural = "Tracking Statuses"
        ordering = ["-created_at"]

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
    tracking_number = models.CharField(max_length=50, db_index=True)
    account_number = models.CharField(max_length=35, null=True, blank=True)
    reference = models.CharField(max_length=35, null=True, blank=True)
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

    # System Reference fields

    tracking_carrier = models.ForeignKey(providers.Carrier, on_delete=models.CASCADE)
    shipment = models.OneToOneField(
        "Shipment", on_delete=models.CASCADE, related_name="shipment_tracker", null=True
    )

    @property
    def object_type(self):
        return "tracker"

    # Computed properties

    @property
    def carrier_id(self) -> str:
        return typing.cast(providers.Carrier, self.tracking_carrier).carrier_id

    @property
    def carrier_name(self) -> str:
        return typing.cast(providers.Carrier, self.tracking_carrier).data.carrier_name

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
    DIRECT_PROPS = [
        "options",
        "services",
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
    ]
    RELATIONAL_PROPS = [
        "shipper",
        "recipient",
        "parcels",
        "customs",
        "selected_rate",
        "return_address",
        "billing_address",
    ]
    HIDDEN_PROPS = (
        "carriers",
        "label",
        "invoice",
        "shipment_pickup",
        "shipment_tracker",
        "selected_rate_carrier",
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
    objects = ShipmentManager()

    class Meta:
        db_table = "shipment"
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields.json.KeyTextTransform("service", "selected_rate"),
                condition=models.Q(meta__object_id__isnull=False),
                name="shipment_service_idx",
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

    recipient = models.OneToOneField(
        "Address", on_delete=models.CASCADE, related_name="recipient_shipment"
    )
    shipper = models.OneToOneField(
        "Address", on_delete=models.CASCADE, related_name="shipper_shipment"
    )
    return_address = models.OneToOneField(
        "Address",
        null=True,
        on_delete=models.SET_NULL,
        related_name="return_address_shipment",
    )
    billing_address = models.OneToOneField(
        "Address",
        null=True,
        on_delete=models.SET_NULL,
        related_name="billing_address_shipment",
    )
    label_type = models.CharField(max_length=25, null=True, blank=True)
    tracking_number = models.CharField(
        max_length=50, null=True, blank=True, db_index=True
    )
    shipment_identifier = models.CharField(max_length=50, null=True, blank=True)
    tracking_url = models.TextField(max_length=None, null=True, blank=True)
    test_mode = models.BooleanField(null=False)
    customs = models.OneToOneField(
        "Customs",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="customs_shipment",
    )

    label = models.TextField(max_length=None, null=True, blank=True)
    invoice = models.TextField(max_length=None, null=True, blank=True)
    reference = models.CharField(max_length=35, null=True, blank=True)
    selected_rate = models.JSONField(blank=True, null=True)
    payment = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=None)
    )
    options = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value={})
    )
    services = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
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

    # System Reference fields

    rates = models.JSONField(
        blank=True, null=True, default=functools.partial(utils.identity, value=[])
    )
    parcels = models.ManyToManyField("Parcel", related_name="parcel_shipment")
    carriers = models.ManyToManyField(
        providers.Carrier, blank=True, related_name="related_shipments"
    )
    selected_rate_carrier = models.ForeignKey(
        providers.Carrier,
        on_delete=models.CASCADE,
        related_name="carrier_shipments",
        blank=True,
        null=True,
    )
    manifest = models.ForeignKey(
        "Manifest",
        on_delete=models.SET_NULL,
        related_name="shipments",
        blank=True,
        null=True,
    )

    def delete(self, *args, **kwargs):
        self.parcels.all().delete()
        self.customs and self.customs.delete()
        return super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "shipment"

    # Computed properties

    @property
    def carrier_id(self) -> str:
        return typing.cast(providers.Carrier, self.selected_rate_carrier).carrier_id

    @property
    def carrier_name(self) -> str:
        return typing.cast(providers.Carrier, self.selected_rate_carrier).carrier_name

    @property
    def tracker_id(self) -> typing.Optional[str]:
        return getattr(self.tracker, "id", None)

    @property
    def carrier_ids(self) -> typing.List[str]:
        return [carrier.carrier_id for carrier in self.carriers.all()]

    @property
    def selected_rate_id(self) -> str:
        return (
            typing.cast(dict, self.selected_rate).get("id")
            if self.selected_rate is not None
            else None
        )

    @property
    def service(self) -> str:
        return (
            typing.cast(dict, self.selected_rate).get("service")
            if self.selected_rate is not None
            else None
        )

    @property
    def tracker(self):
        if hasattr(self, "shipment_tracker"):
            return self.shipment_tracker

        return None

    @property
    def label_url(self) -> str:
        if self.label is None:
            return None

        return urls.reverse(
            "karrio.server.manager:shipment-docs",
            kwargs=dict(
                pk=self.pk, doc="label", format=(self.label_type or "PDF").lower()
            ),
        )

    @property
    def invoice_url(self) -> str:
        if self.invoice is None:
            return None

        return urls.reverse(
            "karrio.server.manager:shipment-docs",
            kwargs=dict(pk=self.pk, doc="invoice", format="pdf"),
        )


@core.register_model
class DocumentUploadRecord(core.OwnedEntity):
    HIDDEN_PROPS = (
        "upload_carrier",
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

    # System Reference fields

    upload_carrier = models.ForeignKey(providers.Carrier, on_delete=models.CASCADE)
    shipment = models.OneToOneField(
        "Shipment",
        on_delete=models.CASCADE,
        related_name="shipment_upload_record",
    )

    # Computed properties

    @property
    def carrier_id(self) -> str:
        return typing.cast(providers.Carrier, self.upload_carrier).carrier_id

    @property
    def carrier_name(self) -> str:
        return typing.cast(providers.Carrier, self.upload_carrier).data.carrier_name


@core.register_model
class Manifest(core.OwnedEntity):
    DIRECT_PROPS = [
        "meta",
        "options",
        "metadata",
        "messages",
        "created_by",
        "reference",
    ]
    RELATIONAL_PROPS = [
        "address",
    ]
    HIDDEN_PROPS = (
        "manifest_carrier",
        *(("org",) if conf.settings.MULTI_ORGANIZATIONS else tuple()),
    )
    objects = ManifestManager()

    class Meta:
        db_table = "manifest"
        verbose_name = "Manifest"
        verbose_name_plural = "Manifests"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="manf_"),
        editable=False,
    )
    address = models.OneToOneField(
        "Address", on_delete=models.CASCADE, related_name="manifest"
    )
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
    reference = models.CharField(max_length=100, null=True, blank=True)
    manifest = models.TextField(max_length=None, null=True, blank=True)
    test_mode = models.BooleanField(null=False)

    # System Reference fields

    manifest_carrier = models.ForeignKey(providers.Carrier, on_delete=models.CASCADE)

    # Computed properties

    @property
    def object_type(self):
        return "manifest"

    @property
    def carrier_id(self) -> str:
        return self.manifest_carrier.carrier_id

    @property
    def carrier_name(self) -> str:
        return self.manifest_carrier.data.carrier_name

    @property
    def manifest_url(self) -> str:
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
