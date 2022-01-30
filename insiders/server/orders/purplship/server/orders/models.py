from functools import partial
from django.db import models

from purplship.server.core.utils import identity
from purplship.server.core.models import OwnedEntity, uuid
from purplship.server.manager import models as manager

from purplship.server.orders.serializers.base import (
    ORDER_STATUS,
)


class OrderManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "shipping_address",
                "line_items",
                "line_items__children__parcel__shipment",
            )
        )


class Order(OwnedEntity):
    DIRECT_PROPS = [
        "order_id",
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

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="ord_"),
        editable=False,
    )
    order_id = models.CharField(max_length=50)
    source = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(
        max_length=25, choices=ORDER_STATUS, default=ORDER_STATUS[0][0]
    )
    shipping_address = models.ForeignKey(
        "manager.Address", on_delete=models.CASCADE, related_name="order"
    )
    line_items = models.ManyToManyField(
        "manager.Commodity", related_name="order", through="OrderLineItemLink"
    )
    options = models.JSONField(
        blank=True, null=True, default=partial(identity, value={})
    )
    test_mode = models.BooleanField()
    metadata = models.JSONField(
        blank=True, null=True, default=partial(identity, value={})
    )

    @property
    def object_type(self):
        return "order"

    # computed fields

    @property
    def shipments(self):
        return manager.Shipment.objects.filter(
            parcels__items__parent_id__in=self.line_items.values_list("id", flat=True)
        ).distinct()


"""Models orders linking (for reverse OneToMany relations)"""


class OrderLineItemLink(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="line_item_links"
    )
    item = models.OneToOneField(
        "manager.Commodity", on_delete=models.CASCADE, related_name="order_link"
    )
