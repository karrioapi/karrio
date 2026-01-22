import typing
import strawberry
from strawberry.types import Info
import django.utils.timezone as timezone
import django.db.transaction as transaction
from django.db.models import F

import karrio.lib as lib
import karrio.server.graph.utils as utils
import karrio.server.orders.models as models
import karrio.server.serializers as serializers
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.orders.types as types
import karrio.server.graph.schemas.orders.inputs as inputs
import karrio.server.orders.serializers.order as model_serializers


@strawberry.type
class CreateOrderMutation(utils.BaseMutation):
    order: typing.Optional[types.OrderType] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.CreateOrderMutationInput
    ) -> "CreateOrderMutation":
        test_mode = info.context.request.test_mode

        # Generate order_id using atomic counter per scope (organization or user)
        scope_id = model_serializers.ScopeResolver.from_context(info.context.request)

        with transaction.atomic():
            # Get or create counter with immediate lock to prevent any race condition
            counter_obj, _ = models.OrderCounter.objects.select_for_update().get_or_create(
                org_id=scope_id, test_mode=test_mode, defaults={"counter": 0}
            )

            # Increment counter atomically at database level using F() expression
            models.OrderCounter.objects.filter(id=counter_obj.id).update(
                counter=F("counter") + 1, updated_at=timezone.now()
            )

            # Refresh to get the updated counter value
            counter_obj.refresh_from_db()
            counter_value = counter_obj.counter

            # Generate sequential order_id
            order_id = f"order_{counter_value:09d}"

        serializer = model_serializers.OrderSerializer(
            context=info.context.request,
            data={
                "order_id": order_id,
                "source": "draft",
                "test_mode": test_mode,
                "order_date": lib.fdate(timezone.now()),
                **lib.to_dict(input),
            },
        )
        serializer.is_valid(raise_exception=True)

        return CreateOrderMutation(order=serializer.save())  # type:ignore


@strawberry.type
class UpdateOrderMutation(utils.BaseMutation):
    order: typing.Optional[types.OrderType] = None

    @staticmethod
    @transaction.atomic
    @utils.authentication_required
    def mutate(
        info: Info,
        line_items: typing.Optional[
            typing.List[base.inputs.UpdateCommodityInput]
        ] = None,
        **input: inputs.UpdateOrderMutationInput,
    ) -> "UpdateOrderMutation":
        data = lib.to_dict(input)

        # Include line_items in data if provided (JSON field mutation)
        if any(line_items or ""):
            data["line_items"] = [lib.to_dict(item) for item in line_items]

        order = models.Order.access_by(info.context.request).get(
            id=input.get("id"),
            source="draft",
        )
        model_serializers.can_mutate_order(order, update=True, payload=data)

        serializer = model_serializers.OrderSerializer(
            order,
            context=info.context.request,
            data=data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # refetch the order to get the updated state with signals processed
        update = models.Order.access_by(info.context.request).get(id=input.get("id"))

        return UpdateOrderMutation(errors=None, order=update)  # type:ignore


@strawberry.type
class DeleteOrderMutation(utils.BaseMutation):
    id: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    def mutate(
        info: Info, **input: inputs.DeleteOrderMutationInput
    ) -> "DeleteOrderMutation":
        id = input["id"]
        order = models.Order.access_by(info.context.request).get(id=id, source="draft")
        model_serializers.can_mutate_order(order, delete=True)

        order.delete()

        return DeleteOrderMutation(id=id)
