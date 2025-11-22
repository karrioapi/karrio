import datetime
from functools import partial
from django.conf import settings
from django.db import models

from karrio.server.core.utils import identity
from karrio.server.core.models import OwnedEntity, uuid, register_model
from karrio.server.manager import models as manager
import karrio.server.providers.models as providers

from karrio.server.orders.serializers.base import ORDER_STATUS


class LineItem(manager.Commodity):
    class Meta:
        proxy = True

    @property
    def unfulfilled_quantity(self):
        quantity = self.quantity - sum(
            [
                child.quantity or 0
                for child in list(
                    self.children.exclude(
                        commodity_parcel__parcel_shipment__status__in=[
                            "cancelled",
                            "draft",
                        ]
                    ).filter(
                        commodity_parcel__isnull=False,
                        commodity_customs__isnull=True,
                    )
                )
            ],
            0,
        )
        return quantity if quantity > 0 else 0


class OrderManager(models.Manager):
    def get_queryset(self):
        from django.db.models import Prefetch

        # Get the current context if available to optimize shipment queries
        context = None
        try:
            from karrio.server.core.middleware import SessionContext
            context = SessionContext.get_current_request()
        except:
            pass

        queryset = (
            super()
            .get_queryset()
            .select_related(
                "created_by",
                "shipping_to",
                "shipping_from",
                "billing_address",
            )
            .prefetch_related(
                "line_items",
            )
        )

        # Only add optimized shipment prefetch if we have context
        # This prevents issues during deletion and other edge cases
        if context is not None:
            shipment_qs = manager.Shipment.access_by(context)
            queryset = queryset.prefetch_related(
                Prefetch("shipments", queryset=shipment_qs)
            )
        else:
            queryset = queryset.prefetch_related("shipments")

        return queryset


@register_model
class Order(OwnedEntity):
    HIDDEN_PROPS = (*(("org",) if settings.MULTI_ORGANIZATIONS else tuple()),)
    DIRECT_PROPS = [
        "order_id",
        "order_date",
        "source",
        "status",
        "options",
        "metadata",
        "test_mode",
        "created_by",
    ]
    objects = OrderManager()

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        indexes = [
            # Index for archiving queries based on creation date
            models.Index(fields=["created_at"], name="order_created_at_idx"),
        ]

    # CONTEXT_RELATIONS = ["shipments"]  # Temporarily disabled - causes issues during deletion

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="ord_"),
        editable=False,
    )
    order_id = models.CharField(max_length=50, db_index=True)
    order_date = models.DateField(default=datetime.date.today)
    source = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    status = models.CharField(
        max_length=25, choices=ORDER_STATUS, default=ORDER_STATUS[0][0], db_index=True
    )
    shipping_to = models.OneToOneField(
        "manager.Address", on_delete=models.CASCADE, related_name="recipient_order"
    )
    shipping_from = models.OneToOneField(
        "manager.Address",
        null=True,
        on_delete=models.CASCADE,
        related_name="shipper_order",
    )
    billing_address = models.OneToOneField(
        "manager.Address",
        null=True,
        on_delete=models.CASCADE,
        related_name="bill_to_order",
    )
    line_items = models.ManyToManyField(
        LineItem, related_name="commodity_order", through="OrderLineItemLink"
    )
    shipments = models.ManyToManyField(
        "manager.Shipment", related_name="shipment_order"
    )
    options = models.JSONField(
        blank=True, null=True, default=partial(identity, value={})
    )
    metadata = models.JSONField(
        blank=True, null=True, default=partial(identity, value={})
    )
    meta = models.JSONField(blank=True, null=True, default=partial(identity, value={}))
    test_mode = models.BooleanField()

    @property
    def object_type(self):
        return "order"


"""Models orders linking (for reverse OneToMany relations)"""


@register_model
class OrderCounter(models.Model):
    """Atomic counter for generating sequential order IDs per organization"""

    class Meta:
        db_table = "order_counter"
        unique_together = [("org_id", "test_mode")]
        indexes = [
            models.Index(fields=["org_id", "test_mode"], name="order_counter_org_idx"),
        ]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="octx_"),
        editable=False,
    )
    org_id = models.CharField(max_length=50, db_index=True)
    test_mode = models.BooleanField(default=False)
    counter = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        mode = "test" if self.test_mode else "prod"
        return f"OrderCounter({self.org_id}, {mode}, {self.counter})"


class OrderLineItemLink(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="line_item_links"
    )
    item = models.OneToOneField(
        LineItem, on_delete=models.CASCADE, related_name="order_link"
    )
