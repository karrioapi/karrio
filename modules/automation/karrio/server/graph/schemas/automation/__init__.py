import typing
import strawberry
from strawberry.types import Info

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.automation.models as models
import karrio.server.graph.schemas.automation.mutations as mutations
import karrio.server.graph.schemas.automation.inputs as inputs
import karrio.server.graph.schemas.automation.types as types

extra_types: list = []


@strawberry.type
class Query:
    workflow: typing.Optional[types.WorkflowType] = strawberry.field(
        resolver=types.WorkflowType.resolve
    )
    workflows: utils.Connection[types.WorkflowType] = strawberry.field(
        resolver=types.WorkflowType.resolve_list
    )

        # Convenient query for scheduled workflows specifically
    scheduled_workflows: utils.Connection[types.WorkflowType] = strawberry.field(
        resolver=types.WorkflowType.resolve_scheduled_workflows
    )

    workflow_action: typing.Optional[types.WorkflowActionType] = strawberry.field(
        resolver=types.WorkflowActionType.resolve
    )
    workflow_actions: utils.Connection[types.WorkflowActionType] = strawberry.field(
        resolver=types.WorkflowActionType.resolve_list
    )
    workflow_connection: typing.Optional[
        types.WorkflowConnectionType
    ] = strawberry.field(resolver=types.WorkflowConnectionType.resolve)
    workflow_connections: utils.Connection[
        types.WorkflowConnectionType
    ] = strawberry.field(resolver=types.WorkflowConnectionType.resolve_list)

    workflow_event: typing.Optional[types.WorkflowEventType] = strawberry.field(
        resolver=types.WorkflowEventType.resolve
    )
    workflow_events: utils.Connection[types.WorkflowEventType] = strawberry.field(
        resolver=types.WorkflowEventType.resolve_list
    )

    workflow_templates: utils.Connection[types.WorkflowTemplateType] = strawberry.field(
        resolver=types.WorkflowTemplateType.resolve_list
    )
    workflow_action_templates: utils.Connection[
        types.WorkflowActionTemplateType
    ] = strawberry.field(resolver=types.WorkflowActionTemplateType.resolve_list)
    workflow_connection_templates: utils.Connection[
        types.WorkflowConnectionTemplateType
    ] = strawberry.field(resolver=types.WorkflowConnectionTemplateType.resolve_list)

    shipping_rule: typing.Optional[types.ShippingRuleType] = strawberry.field(
        resolver=types.ShippingRuleType.resolve
    )
    shipping_rules: utils.Connection[types.ShippingRuleType] = strawberry.field(
        resolver=types.ShippingRuleType.resolve_list
    )

    scheduler_status: types.SchedulerStatusType = strawberry.field(
        resolver=types.SchedulerStatusType.resolve
    )

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_workflow(
        self, info: Info, input: inputs.CreateWorkflowMutationInput
    ) -> mutations.CreateWorkflowMutation:
        return mutations.CreateWorkflowMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_workflow(
        self, info: Info, input: inputs.UpdateWorkflowMutationInput
    ) -> mutations.UpdateWorkflowMutation:
        return mutations.UpdateWorkflowMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_workflow(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> base.mutations.DeleteMutation:
        return base.mutations.DeleteMutation.mutate(
            info, model=models.Workflow, **input.to_dict()
        )

    @strawberry.mutation
    def create_workflow_action(
        self, info: Info, input: inputs.CreateWorkflowActionMutationInput
    ) -> mutations.CreateWorkflowActionMutation:
        return mutations.CreateWorkflowActionMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_workflow_action(
        self, info: Info, input: inputs.UpdateWorkflowActionMutationInput
    ) -> mutations.UpdateWorkflowActionMutation:
        return mutations.UpdateWorkflowActionMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_workflow_action(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> base.mutations.DeleteMutation:
        return base.mutations.DeleteMutation.mutate(
            info, model=models.WorkflowAction, **input.to_dict()
        )

    @strawberry.mutation
    def create_workflow_connection(
        self, info: Info, input: inputs.CreateWorkflowConnectionMutationInput
    ) -> mutations.CreateWorkflowConnectionMutation:
        return mutations.CreateWorkflowConnectionMutation.mutate(
            info, **input.to_dict()
        )

    @strawberry.mutation
    def update_workflow_connection(
        self, info: Info, input: inputs.UpdateWorkflowConnectionMutationInput
    ) -> mutations.UpdateWorkflowConnectionMutation:
        return mutations.UpdateWorkflowConnectionMutation.mutate(
            info, **input.to_dict()
        )

    @strawberry.mutation
    def delete_workflow_connection(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> base.mutations.DeleteMutation:
        return base.mutations.DeleteMutation.mutate(
            info, model=models.WorkflowConnection, **input.to_dict()
        )

    @strawberry.mutation
    def create_workflow_event(
        self, info: Info, input: inputs.CreateWorkflowEventMutationInput
    ) -> mutations.CreateWorkflowEventMutation:
        return mutations.CreateWorkflowEventMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def cancel_workflow_event(
        self, info: Info, input: inputs.CancelWorkflowEventMutationInput
    ) -> mutations.CancelWorkflowEventMutation:
        return mutations.CancelWorkflowEventMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def create_workflow_trigger(
        self, info: Info, input: inputs.CreateWorkflowTriggerMutationInput
    ) -> mutations.CreateWorkflowTriggerMutation:
        return mutations.CreateWorkflowTriggerMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_workflow_trigger(
        self, info: Info, input: inputs.UpdateWorkflowTriggerMutationInput
    ) -> mutations.UpdateWorkflowTriggerMutation:
        return mutations.UpdateWorkflowTriggerMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_workflow_trigger(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> base.mutations.DeleteMutation:
        return base.mutations.DeleteMutation.mutate(
            info, model=models.WorkflowTrigger, **input.to_dict()
        )

    @strawberry.mutation
    def trigger_scheduled_workflow(
        self, info: Info, trigger_id: str
    ) -> mutations.TriggerScheduledWorkflowMutation:
        """Manually trigger a scheduled workflow for testing purposes"""
        return mutations.TriggerScheduledWorkflowMutation.mutate(
            info, trigger_id=trigger_id
        )

    @strawberry.mutation
    def validate_cron_expression(
        self, info: Info, input: inputs.ValidateCronExpressionInput
    ) -> mutations.ValidateCronExpressionMutation:
        """Validate a cron expression and get helpful information"""
        return mutations.ValidateCronExpressionMutation.mutate(
            info, **input.to_dict()
        )

    @strawberry.mutation
    def create_shipping_rule(
        self, info: Info, input: inputs.CreateShippingRuleMutationInput
    ) -> mutations.CreateShippingRuleMutation:
        return mutations.CreateShippingRuleMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def update_shipping_rule(
        self, info: Info, input: inputs.UpdateShippingRuleMutationInput
    ) -> mutations.UpdateShippingRuleMutation:
        return mutations.UpdateShippingRuleMutation.mutate(info, **input.to_dict())

    @strawberry.mutation
    def delete_shipping_rule(
        self, info: Info, input: base.inputs.DeleteMutationInput
    ) -> mutations.DeleteShippingRuleMutation:
        return mutations.DeleteShippingRuleMutation.mutate(info, **input.to_dict())
