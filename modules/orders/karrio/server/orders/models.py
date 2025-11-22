import datetime
from functools import partial
from contextlib import contextmanager
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


class OrderKeyManager(models.Manager):
    """Manager for OrderKey with deduplication lock management."""

    @contextmanager
    def acquire_lock(
        self, scope: str, source: str, order_reference: str, test_mode: bool
    ):
        """Context manager for acquiring order deduplication lock.

        Provides automatic cleanup on failure and prevents duplicate orders
        at the database level using row-level locking.

        Args:
            scope: Organization or user scope identifier (format: 'org:{id}' or 'user:{id}')
            source: Order source (e.g., 'API', 'shopify', 'draft')
            order_reference: The order_id from the external system
            test_mode: Whether this is a test mode order

        Yields:
            OrderKey: The lock object that can be bound to an order

        Raises:
            APIException: If order with same identifier already exists (409 Conflict)

        Example:
            with OrderKey.objects.acquire_lock(scope, source, ref, test_mode) as lock:
                order = Order.objects.create(...)
                lock.bind_order(order)
        """
        from karrio.server.core.exceptions import APIException
        from rest_framework import status
        from django.db import IntegrityError

        lock = None
        lock_created = False

        try:
            # Try to create lock with row-level locking
            lock, lock_created = self.select_for_update().get_or_create(
                scope=scope,
                source=source,
                order_reference=order_reference,
                test_mode=test_mode,
                defaults={"order": None},
            )

            if not lock_created:
                raise APIException(
                    detail=f"An order with 'order_id' {order_reference} from {source} already exists.",
                    code="duplicate_order_id",
                    status_code=status.HTTP_409_CONFLICT,
                )

            yield lock

        except IntegrityError:
            raise APIException(
                detail=f"An order with 'order_id' {order_reference} from {source} already exists.",
                code="duplicate_order_id",
                status_code=status.HTTP_409_CONFLICT,
            )
        except Exception:
            # Rollback: delete lock if we created it
            if lock_created and lock:
                lock.delete()
            raise


@register_model
class OrderKey(models.Model):
    """Deduplication guard ensuring (scope, source, order_id, test_mode) uniqueness.

    This model prevents duplicate orders from being created through concurrent requests
    or repeated API calls by enforcing a unique constraint at the database level.

    The uniqueness is enforced on the combination of:
    - scope: Either organization ID or user ID
    - source: Where the order came from (API, Shopify, draft, etc.)
    - order_reference: The external order ID
    - test_mode: Whether this is a test or production order
    """

    objects = OrderKeyManager()

    class Meta:
        db_table = "order_key"
        unique_together = [("scope", "source", "order_reference", "test_mode")]
        indexes = [
            models.Index(
                fields=["scope", "source", "order_reference", "test_mode"],
                name="order_key_scope_idx",
            ),
        ]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="okey_"),
        editable=False,
    )
    scope = models.CharField(max_length=50, help_text="Organization or user scope id")
    source = models.CharField(max_length=50, default="API")
    order_reference = models.CharField(max_length=50)
    test_mode = models.BooleanField(default=False)
    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="dedup_key",
        null=True,
        blank=True,
        db_column="order_record_id",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        mode = "test" if self.test_mode else "prod"
        return f"OrderKey({self.scope}, {self.source}, {self.order_reference}, {mode})"

    def bind_order(self, order: "Order"):
        """Bind this deduplication key to an order.

        Args:
            order: The Order instance to bind to this key
        """
        self.order = order
        self.save(update_fields=["order", "updated_at"])


class OrderLineItemLink(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="line_item_links"
    )
    item = models.OneToOneField(
        LineItem, on_delete=models.CASCADE, related_name="order_link"
    )
