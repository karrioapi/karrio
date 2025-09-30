import uuid
import typing
import datetime
import strawberry
from strawberry.types import Info
from rest_framework import exceptions
import logging

import karrio.lib as lib
import karrio.server.graph.utils as utils
import karrio.server.serializers as serializers
import karrio.server.automation.models as models
import karrio.server.graph.serializers as graph_serializers
import karrio.server.graph.schemas.automation.types as types
import karrio.server.graph.schemas.automation.inputs as inputs
import karrio.server.graph.schemas.base.inputs as base_inputs
import karrio.server.automation.serializers.models as model_serializers


@strawberry.type
class CreateWorkflowMutation(utils.BaseMutation):
    workflow: typing.Optional[types.WorkflowType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        template_slug: typing.Optional[str] = None,
        trigger: typing.Optional[inputs.PartialWorkflowTriggerMutationInput] = None,
        actions: typing.Optional[
            typing.List[inputs.PartialWorkflowActionMutationInput]
        ] = None,
        **input: inputs.CreateWorkflowMutationInput,
    ) -> "CreateWorkflowMutation":
        data = input.copy()
        data.update(slug=f"$.{uuid.uuid4().hex}.workflow")

        if any(template_slug or ""):
            data.update(
                template=models.Workflow.filter(is_public=True).get(
                    slug=template_slug,
                )
            )

        if any(actions or []):
            _action_nodes = data["action_nodes"]
            for index, action in enumerate(actions):
                _metafields = action.pop("metafields", [])
                _queryset = models.WorkflowAction.access_by(
                    info.context.request
                ).filter(id=action.get("id"))

                if "connection" in action and action["connection"] is not None:
                    _connection = (
                        _queryset.first().connection if _queryset.exists() else None
                    )
                    action.update(
                        connection=model_serializers.WorkflowConnectionModelSerializer.map(
                            data={
                                "slug": getattr(
                                    _connection,
                                    "slug",
                                    f"$.{uuid.uuid4().hex}.workflow.connection",
                                ),
                                **action.pop("connection"),
                            },
                            partial=_connection is not None,
                            instance=_connection,
                            context=info.context.request,
                        )
                        .save()
                        .instance
                    )

                _action = (
                    model_serializers.WorkflowActionModelSerializer.map(
                        data={
                            "slug": getattr(
                                _queryset.first(),
                                "slug",
                                f"$.{uuid.uuid4().hex}.workflow.action",
                            ),
                            **action,
                        },
                        partial=_queryset.exists(),
                        instance=_queryset.first(),
                        context=info.context.request,
                    )
                    .save()
                    .instance
                )
                data.update(
                    action_nodes=[
                        (
                            dict(slug=_action.slug, order=_.get("order"))
                            if _.get("slug") == _action.slug or _.get("index") == index
                            else _
                        )
                        for _ in _action_nodes
                    ]
                )

                if any(_metafields):
                    serializers.save_many_to_many_data(
                        "metafields",
                        graph_serializers.MetafieldModelSerializer,
                        _action,
                        data=dict(metafields=_metafields),
                        context=info.context.request,
                    )

        workflow = (
            model_serializers.WorkflowModelSerializer.map(
                data=data,
                context=info.context.request,
            )
            .save()
            .instance
        )

        if trigger is not None:
            model_serializers.WorkflowTriggerModelSerializer.map(
                data={
                    "workflow": workflow,
                    "slug": getattr(
                        workflow.trigger,
                        "slug",
                        f"$.{uuid.uuid4().hex}.workflow.trigger",
                    ),
                    **trigger,
                },
                partial=workflow.trigger is not None,
                instance=workflow.trigger,
                context=info.context.request,
            ).save()

        return CreateWorkflowMutation(
            workflow=models.Workflow.objects.get(id=workflow.id)
        )  # type:ignore


@strawberry.type
class UpdateWorkflowMutation(utils.BaseMutation):
    workflow: typing.Optional[types.WorkflowType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        metadata: typing.Optional[utils.JSON] = None,
        template_slug: typing.Optional[str] = strawberry.UNSET,
        trigger: typing.Optional[inputs.PartialWorkflowTriggerMutationInput] = None,
        actions: typing.Optional[
            typing.List[inputs.PartialWorkflowActionMutationInput]
        ] = None,
        **input: inputs.UpdateWorkflowMutationInput,
    ) -> "UpdateWorkflowMutation":
        data = input.copy()
        instance = models.Workflow.access_by(info.context.request).get(
            id=data.get("id"),
        )

        if template_slug is None:
            data.update({"template": None})

        if metadata is not None:
            data.update(
                serializers.process_dictionaries_mutations(["metadata"], data, instance)
            )

        if any(actions or []):
            _action_nodes = data.get("action_nodes") or instance.action_nodes
            for index, action in enumerate(actions):
                _metafields = action.pop("metafields", [])
                _queryset = models.WorkflowAction.access_by(
                    info.context.request
                ).filter(id=action.get("id"))

                if "connection" in action and action["connection"] is not None:
                    _connection = (
                        _queryset.first().connection if _queryset.exists() else None
                    )
                    action.update(
                        connection=model_serializers.WorkflowConnectionModelSerializer.map(
                            data={
                                "slug": getattr(
                                    _connection,
                                    "slug",
                                    f"$.{uuid.uuid4().hex}.workflow.connection",
                                ),
                                **action.pop("connection"),
                            },
                            partial=_connection is not None,
                            instance=_connection,
                            context=info.context.request,
                        )
                        .save()
                        .instance
                    )

                _action = (
                    model_serializers.WorkflowActionModelSerializer.map(
                        data={
                            "slug": getattr(
                                _queryset.first(),
                                "slug",
                                f"$.{uuid.uuid4().hex}.workflow.action",
                            ),
                            **action,
                        },
                        partial=_queryset.exists(),
                        instance=_queryset.first(),
                        context=info.context.request,
                    )
                    .save()
                    .instance
                )
                data.update(
                    action_nodes=[
                        (
                            dict(slug=_action.slug, order=_.get("order"))
                            if _.get("slug") == _action.slug or _.get("index") == index
                            else _
                        )
                        for _ in _action_nodes
                    ]
                )

                if any(_metafields):
                    serializers.save_many_to_many_data(
                        "metafields",
                        graph_serializers.MetafieldModelSerializer,
                        _action,
                        data=dict(metafields=_metafields),
                        context=info.context.request,
                    )

        workflow = (
            model_serializers.WorkflowModelSerializer.map(
                data=data,
                partial=True,
                instance=instance,
                context=info.context.request,
            )
            .save()
            .instance
        )

        if trigger is not None:
            model_serializers.WorkflowTriggerModelSerializer.map(
                data={
                    "workflow": workflow,
                    "slug": getattr(
                        workflow.trigger,
                        "slug",
                        f"$.{uuid.uuid4().hex}.workflow.trigger",
                    ),
                    **trigger,
                },
                partial=workflow.trigger is not None,
                instance=workflow.trigger,
                context=info.context.request,
            ).save()

        return UpdateWorkflowMutation(
            workflow=models.Workflow.objects.get(id=workflow.id)
        )  # type:ignore


@strawberry.type
class CreateWorkflowActionMutation(utils.BaseMutation):
    workflow_action: typing.Optional[types.WorkflowActionType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        metafields: typing.Optional[
            typing.List[inputs.base.CreateMetafieldInput]
        ] = None,
        **input: inputs.CreateWorkflowActionMutationInput,
    ) -> "CreateWorkflowActionMutation":
        data = input.copy()
        data.update(slug=f"$.{uuid.uuid4().hex}.workflow.action")

        if "connection" in data and data["connection"] is not None:
            _connection = models.WorkflowConnection.access_by(
                info.context.request
            ).filter(id=data["connection"].get("connection_id"))
            data.update(
                connection=model_serializers.WorkflowConnectionModelSerializer.map(
                    data={
                        "slug": getattr(
                            _connection.first(),
                            "slug",
                            f"$.{uuid.uuid4().hex}.workflow.connection",
                        ),
                        **data.pop("connection"),
                    },
                    partial=_connection.exists(),
                    instance=_connection.first(),
                    context=info.context.request,
                )
                .save()
                .instance
            )

        serializer = model_serializers.WorkflowActionModelSerializer(
            data=data,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        action = serializer.save()

        if any(metafields or []):
            serializers.save_many_to_many_data(
                "metafields",
                graph_serializers.MetafieldModelSerializer,
                action,
                data=dict(metafields=metafields),
                context=info.context.request,
            )

        return CreateWorkflowActionMutation(
            workflow_action=models.WorkflowAction.objects.get(id=action.id)
        )  # type:ignore


@strawberry.type
class UpdateWorkflowActionMutation(utils.BaseMutation):
    workflow_action: typing.Optional[types.WorkflowActionType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        metafields: typing.Optional[typing.List[inputs.base.MetafieldInput]] = None,
        **input: inputs.UpdateWorkflowActionMutationInput,
    ) -> "UpdateWorkflowActionMutation":
        data = input.copy()
        instance = models.WorkflowAction.access_by(info.context.request).get(
            id=data.get("id"),
        )

        if "connection" in data and data["connection"] is not None:
            _connection = models.WorkflowConnection.access_by(
                info.context.request
            ).filter(id=data["connection"].get("connection_id"))
            data.update(
                connection=model_serializers.WorkflowConnectionModelSerializer.map(
                    data={
                        "slug": getattr(
                            _connection.first(),
                            "slug",
                            f"$.{uuid.uuid4().hex}.workflow.connection",
                        ),
                        **data.pop("connection"),
                    },
                    partial=_connection.exists(),
                    instance=_connection.first(),
                    context=info.context.request,
                )
                .save()
                .instance
            )

        if "template_slug" in data and data["template_slug"] is None:
            data.update({"template": None})

        serializer = model_serializers.WorkflowActionModelSerializer(
            instance,
            data=data,
            partial=True,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if any(metafields or []):
            serializers.save_many_to_many_data(
                "metafields",
                graph_serializers.MetafieldModelSerializer,
                instance,
                data=dict(metafields=metafields),
                context=info.context.request,
            )

        return UpdateWorkflowActionMutation(
            workflow_action=models.WorkflowAction.objects.get(id=instance.id)
        )  # type:ignore


@strawberry.type
class CreateWorkflowConnectionMutation(utils.BaseMutation):
    workflow_connection: typing.Optional[types.WorkflowConnectionType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        metafields: typing.Optional[
            typing.List[inputs.base.CreateMetafieldInput]
        ] = None,
        **input: inputs.CreateWorkflowConnectionMutationInput,
    ) -> "CreateWorkflowConnectionMutation":
        data = input.copy()
        data.update(slug=f"$.{uuid.uuid4().hex}.workflow.connection")

        if "template_slug" in input:
            data.update(
                template=models.WorkflowConnection.filter(is_public=True).get(
                    slug=input.pop("template_slug"),
                )
            )

        serializer = model_serializers.WorkflowConnectionModelSerializer(
            data=data,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if any(metafields or []):
            serializers.save_many_to_many_data(
                "metafields",
                graph_serializers.MetafieldModelSerializer,
                instance,
                data=dict(metafields=metafields),
                context=info.context.request,
            )

        return CreateWorkflowConnectionMutation(
            workflow_connection=models.WorkflowConnection.objects.get(id=instance.id)
        )


@strawberry.type
class UpdateWorkflowConnectionMutation(utils.BaseMutation):
    workflow_connection: typing.Optional[types.WorkflowConnectionType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        metafields: typing.Optional[typing.List[inputs.base.MetafieldInput]] = None,
        **input: inputs.UpdateWorkflowConnectionMutationInput,
    ) -> "UpdateWorkflowConnectionMutation":
        data = input.copy()
        instance = models.WorkflowConnection.access_by(info.context.request).get(
            id=input.get("id"),
        )

        if "template_slug" in data and data["template_slug"] is None:
            data.update({"template": None})

        serializer = model_serializers.WorkflowConnectionModelSerializer(
            instance,
            data=data,
            partial=True,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if any(metafields or []):
            serializers.save_many_to_many_data(
                "metafields",
                graph_serializers.MetafieldModelSerializer,
                instance,
                data=dict(metafields=metafields),
                context=info.context.request,
            )

        return UpdateWorkflowConnectionMutation(
            workflow_connection=models.WorkflowConnection.objects.get(id=instance.id)
        )


@strawberry.type
class CreateWorkflowEventMutation(utils.BaseMutation):
    workflow_event: typing.Optional[types.WorkflowEventType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info, **input: inputs.CreateWorkflowEventMutationInput
    ) -> "CreateWorkflowEventMutation":
        test_mode = getattr(info.context.request, "test_mode", False)
        workflow = models.Workflow.access_by(info.context.request).get(
            id=input.get("workflow_id"),
        )
        serializer = model_serializers.WorkflowEventModelSerializer(
            data={**input, "workflow": workflow, "test_mode": test_mode},
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return CreateWorkflowEventMutation(workflow_event=serializer.save())


@strawberry.type
class CancelWorkflowEventMutation(utils.BaseMutation):
    workflow_event: typing.Optional[types.WorkflowEventType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info, **input: inputs.CancelWorkflowEventMutationInput
    ) -> "CancelWorkflowEventMutation":
        instance = models.WorkflowEvent.access_by(info.context.request).get(
            id=input.get("id"),
        )

        if instance.status in ["cancelled", "success", "failed"]:
            raise exceptions.ValidationError(
                {"id": f"Workflow event has already reached status: {instance.status}"}
            )

        instance.status = "cancelled"
        instance.save()

        return CancelWorkflowEventMutation(workflow_event=instance)


@strawberry.type
class CreateWorkflowTriggerMutation(utils.BaseMutation):
    workflow_trigger: typing.Optional[types.WorkflowTriggerType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        **input: inputs.CreateWorkflowTriggerMutationInput,
    ) -> "CreateWorkflowTriggerMutation":
        data = input.copy()
        data.update(slug=f"$.{uuid.uuid4().hex}.workflow.trigger")
        data.update(
            workflow=models.Workflow.access_by(info.context.request).get(
                id=input.get("workflow_id"),
            )
        )

        if "template_slug" in input:
            data.update(
                template=models.WorkflowTrigger.filter(is_public=True).get(
                    slug=input.pop("template_slug"),
                )
            )

        serializer = model_serializers.WorkflowTriggerModelSerializer(
            data=data,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return CreateWorkflowTriggerMutation(workflow_trigger=serializer.save())


@strawberry.type
class UpdateWorkflowTriggerMutation(utils.BaseMutation):
    workflow_trigger: typing.Optional[types.WorkflowTriggerType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        **input: inputs.UpdateWorkflowTriggerMutationInput,
    ) -> "UpdateWorkflowTriggerMutation":
        data = input.copy()
        instance = models.WorkflowTrigger.access_by(info.context.request).get(
            id=input.get("id"),
        )

        if "template_slug" in data and data["template_slug"] is None:
            data.update({"template": None})

        serializer = model_serializers.WorkflowTriggerModelSerializer(
            instance,
            data=data,
            partial=True,
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return UpdateWorkflowTriggerMutation(workflow_trigger=serializer.save())


@strawberry.type
class TriggerScheduledWorkflowMutation(utils.BaseMutation):
    workflow_event: typing.Optional[types.WorkflowEventType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        trigger_id: str,
    ) -> "TriggerScheduledWorkflowMutation":
        """Manually trigger a scheduled workflow for testing purposes"""
        # Get the trigger and verify it's scheduled
        trigger = models.WorkflowTrigger.access_by(info.context.request).get(
            id=trigger_id
        )

        if trigger.trigger_type != "scheduled":
            raise exceptions.ValidationError(
                {"trigger_id": "Trigger must be of type 'scheduled'"}
            )

        if not trigger.workflow.is_active:
            raise exceptions.ValidationError(
                {"trigger_id": "Workflow must be active"}
            )

        # Create a manual scheduled workflow event
        test_mode = getattr(info.context.request, "test_mode", False)
        serializer = model_serializers.WorkflowEventModelSerializer(
            data={
                "workflow": trigger.workflow,
                "event_type": "scheduled",
                "test_mode": test_mode,
                "parameters": {
                    "trigger_id": trigger_id,
                    "manually_triggered": True,
                    "triggered_at": lib.now().isoformat(),
                }
            },
            context=info.context.request,
        )
        serializer.is_valid(raise_exception=True)

        return TriggerScheduledWorkflowMutation(workflow_event=serializer.save())


@strawberry.type
class ValidateCronExpressionMutation(utils.BaseMutation):
    is_valid: bool = False
    description: typing.Optional[str] = None
    next_run_times: typing.Optional[typing.List[datetime.datetime]] = None
    error_message: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        **input: inputs.ValidateCronExpressionInput,
    ) -> "ValidateCronExpressionMutation":
        """Validate a cron expression and return helpful information"""
        from karrio.server.automation.cron_utils import (
            validate_cron_expression,
            get_cron_description,
            calculate_next_run_time
        )
        from django.utils import timezone

        expression = input.get("expression")

        try:
            # Validate the expression
            validate_cron_expression(expression)

            # Get human-readable description
            description = get_cron_description(expression)

            # Calculate next few run times
            base_time = timezone.now()
            next_runs = []
            current_time = base_time

            for _ in range(5):  # Show next 5 execution times
                next_time = calculate_next_run_time(expression, current_time)
                next_runs.append(next_time)
                current_time = next_time

            return ValidateCronExpressionMutation(
                is_valid=True,
                description=description,
                next_run_times=next_runs
            )

        except Exception as e:
            return ValidateCronExpressionMutation(
                is_valid=False,
                error_message=str(e)
            )


@strawberry.type
class CreateShippingRuleMutation(utils.BaseMutation):
    shipping_rule: typing.Optional[types.ShippingRuleType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        **input: inputs.CreateShippingRuleMutationInput,
    ) -> "CreateShippingRuleMutation":
        import uuid

        data = input.copy()
        data.update(slug=f"$.{uuid.uuid4().hex}.shipping_rule")

        # Use lib.failsafe for robust serializer operations
        def create_shipping_rule():
            return (
                model_serializers.ShippingRuleModelSerializer.map(
                    data=data,
                    context=info.context.request,
                )
                .save()
                .instance
            )

        shipping_rule = lib.failsafe(
            create_shipping_rule,
            warning="Failed to create shipping rule with serializer"
        )

        if shipping_rule is None:
            raise exceptions.ValidationError(
                {"non_field_errors": ["Failed to create shipping rule"]}
            )

        # Use lib.failsafe for database retrieval
        final_rule = lib.failsafe(
            lambda: models.ShippingRule.objects.get(id=shipping_rule.id),
            warning="Failed to retrieve created shipping rule"
        )

        if final_rule is None:
            raise exceptions.ValidationError(
                {"non_field_errors": ["Shipping rule created but could not be retrieved"]}
            )

        return CreateShippingRuleMutation(shipping_rule=final_rule)


@strawberry.type
class UpdateShippingRuleMutation(utils.BaseMutation):
    shipping_rule: typing.Optional[types.ShippingRuleType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        **input: inputs.UpdateShippingRuleMutationInput,
    ) -> "UpdateShippingRuleMutation":
        data = input.copy()
        instance = models.ShippingRule.access_by(info.context.request).get(
            id=data.get("id"),
        )

        # Handle JSON field updates
        for field in ["conditions", "actions", "metadata"]:
            if field in data and data[field] is not None:
                data.update(
                    serializers.process_dictionaries_mutations([field], data, instance)
                )

        shipping_rule = (
            model_serializers.ShippingRuleModelSerializer.map(
                data=data,
                instance=instance,
                partial=True,
                context=info.context.request,
            )
            .save()
            .instance
        )

        return UpdateShippingRuleMutation(
            shipping_rule=models.ShippingRule.objects.get(id=shipping_rule.id)
        )


@strawberry.type
class DeleteShippingRuleMutation(utils.BaseMutation):
    id: str = strawberry.UNSET

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def mutate(
        info: Info,
        **input: base_inputs.DeleteMutationInput,
    ) -> "DeleteShippingRuleMutation":
        id = input.get("id")
        instance = models.ShippingRule.access_by(info.context.request).get(id=id)
        instance.delete()
        return DeleteShippingRuleMutation(id=id)
