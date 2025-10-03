import typing
import strawberry
import karrio.server.graph.utils as utils
import karrio.server.automation.utils as automation
import karrio.server.graph.schemas.base.inputs as base


# -----------------------------------------------------------
# workflow related input definitions
# -----------------------------------------------------------
# region

@strawberry.input
class ActionNodeInput(utils.BaseInput):
    order: int
    slug: typing.Optional[str] = strawberry.UNSET
    index: typing.Optional[int] = strawberry.UNSET


@strawberry.input
class CreateWorkflowMutationInput(utils.BaseInput):
    name: str
    action_nodes: typing.List[ActionNodeInput]
    description: typing.Optional[str] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    template_slug: typing.Optional[str] = strawberry.UNSET
    trigger: typing.Optional["PartialWorkflowTriggerMutationInput"] = strawberry.UNSET
    actions: typing.Optional[
        typing.List["PartialWorkflowActionMutationInput"]
    ] = strawberry.UNSET


@strawberry.input
class UpdateWorkflowMutationInput(utils.BaseInput):
    id: str
    name: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    action_nodes: typing.Optional[typing.List[ActionNodeInput]] = strawberry.UNSET
    template_slug: typing.Optional[str] = strawberry.UNSET
    trigger: typing.Optional["PartialWorkflowTriggerMutationInput"] = strawberry.UNSET
    actions: typing.Optional[
        typing.List["PartialWorkflowActionMutationInput"]
    ] = strawberry.UNSET


@strawberry.input
class CreateWorkflowActionMutationInput(utils.BaseInput):
    name: str
    action_type: automation.WorkflowActionTypeEnum
    port: typing.Optional[int] = strawberry.UNSET
    host: typing.Optional[str] = strawberry.UNSET
    endpoint: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    method: typing.Optional[automation.HTTPMethodEnum] = strawberry.UNSET
    parameters_type: typing.Optional[automation.ParametersTypeEnum] = strawberry.UNSET
    parameters_template: typing.Optional[str] = strawberry.UNSET
    header_template: typing.Optional[str] = strawberry.UNSET
    content_type: typing.Optional[automation.HTTPContentTypeEnum] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    template_slug: typing.Optional[str] = strawberry.UNSET
    metafields: typing.Optional[
        typing.List[base.CreateMetafieldInput]
    ] = strawberry.UNSET
    connection: typing.Optional[
        "PartialWorkflowConnectionMutationInput"
    ] = strawberry.UNSET


@strawberry.input
class UpdateWorkflowActionMutationInput(CreateWorkflowActionMutationInput):
    id: str
    name: typing.Optional[str] = strawberry.UNSET
    action_type: typing.Optional[automation.WorkflowActionTypeEnum] = strawberry.UNSET
    metafields: typing.Optional[typing.List[base.MetafieldInput]] = strawberry.UNSET


@strawberry.input
class PartialWorkflowActionMutationInput(UpdateWorkflowActionMutationInput):
    id: typing.Optional[str] = strawberry.UNSET
    slug: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class CreateWorkflowConnectionMutationInput(utils.BaseInput):
    name: str
    auth_type: automation.AuthTypeEnum
    port: typing.Optional[int] = strawberry.UNSET
    host: typing.Optional[str] = strawberry.UNSET
    endpoint: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    credentials: typing.Optional[utils.JSON] = strawberry.UNSET
    auth_template: typing.Optional[str] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    parameters_template: typing.Optional[str] = strawberry.UNSET
    template_slug: typing.Optional[str] = strawberry.UNSET
    metafields: typing.Optional[
        typing.List[base.CreateMetafieldInput]
    ] = strawberry.UNSET


@strawberry.input
class UpdateWorkflowConnectionMutationInput(CreateWorkflowConnectionMutationInput):
    id: str
    name: typing.Optional[str] = strawberry.UNSET
    auth_type: typing.Optional[automation.AuthTypeEnum] = strawberry.UNSET
    metafields: typing.Optional[typing.List[base.MetafieldInput]] = strawberry.UNSET


@strawberry.input
class PartialWorkflowConnectionMutationInput(UpdateWorkflowConnectionMutationInput):
    id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class CreateWorkflowEventMutationInput(utils.BaseInput):
    workflow_id: str
    event_type: automation.WorkflowEventTypeEnum
    parameters: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class CancelWorkflowEventMutationInput(utils.BaseInput):
    id: str


@strawberry.input
class WorkflowFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    trigger_type: typing.Optional[automation.WorkflowTriggerTypeEnum] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class WorkflowActionFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    action_type: typing.Optional[automation.WorkflowActionTypeEnum] = strawberry.UNSET


@strawberry.input
class WorkflowConnectionFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    auth_type: typing.Optional[automation.AuthTypeEnum] = strawberry.UNSET


@strawberry.input
class WorkflowEventFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    parameters_key: typing.Optional[typing.List[str]] = strawberry.UNSET
    status: typing.Optional[automation.WorkflowEventStatusEnum] = strawberry.UNSET
    event_type: typing.Optional[automation.WorkflowEventTypeEnum] = strawberry.UNSET


@strawberry.input
class CreateWorkflowTriggerMutationInput(utils.BaseInput):
    workflow_id: str
    trigger_type: automation.WorkflowTriggerTypeEnum
    schedule: typing.Optional[str] = strawberry.UNSET
    secret: typing.Optional[str] = strawberry.UNSET
    secret_key: typing.Optional[str] = strawberry.UNSET
    template_slug: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class UpdateWorkflowTriggerMutationInput(utils.BaseInput):
    id: str
    trigger_type: typing.Optional[automation.WorkflowTriggerTypeEnum] = strawberry.UNSET
    schedule: typing.Optional[str] = strawberry.UNSET
    secret: typing.Optional[str] = strawberry.UNSET
    secret_key: typing.Optional[str] = strawberry.UNSET
    template_slug: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class PartialWorkflowTriggerMutationInput(UpdateWorkflowTriggerMutationInput):
    id: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class ValidateCronExpressionInput(utils.BaseInput):
    expression: str

# endregion

# -----------------------------------------------------------
# shipping rule related input definitions
# -----------------------------------------------------------
# region


@strawberry.input
class DestinationConditionInput:
    country_code: typing.Optional[str] = strawberry.UNSET
    postal_code: typing.Optional[typing.List[str]] = strawberry.UNSET


@strawberry.input
class WeightConditionInput:
    min: typing.Optional[float] = strawberry.UNSET
    max: typing.Optional[float] = strawberry.UNSET
    unit: typing.Optional[str] = strawberry.UNSET


@strawberry.input
class RateComparisonConditionInput:
    """Rate comparison criteria input

    Fields:
        compare: Rate field to compare (total_charge, transit_days, etc.)
        operator: Comparison operator (eq, gt, gte, lt, lte)
        value: Value to compare against
    """

    compare: automation.RateComparisonFieldEnum
    operator: automation.ComparisonOperatorEnum
    value: float


@strawberry.input
class AddressTypeConditionInput:
    type: str  # residential, commercial


@strawberry.input
class ShippingRuleConditionsInput:
    destination: typing.Optional[DestinationConditionInput] = strawberry.UNSET
    carrier_id: typing.Optional[str] = strawberry.UNSET
    service: typing.Optional[str] = strawberry.UNSET
    weight: typing.Optional[WeightConditionInput] = strawberry.UNSET
    rate_comparison: typing.Optional[RateComparisonConditionInput] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    address_type: typing.Optional[AddressTypeConditionInput] = strawberry.UNSET
    value: typing.Optional[float] = strawberry.UNSET


@strawberry.input
class SelectServiceActionInput:
    carrier_code: typing.Optional[str] = strawberry.UNSET
    carrier_id: typing.Optional[str] = strawberry.UNSET
    service_code: typing.Optional[str] = strawberry.UNSET
    strategy: typing.Optional[automation.SelectServiceStrategyEnum] = strawberry.UNSET


@strawberry.input
class ShippingRuleActionsInput:
    select_service: typing.Optional[SelectServiceActionInput] = strawberry.UNSET
    block_service: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class CreateShippingRuleMutationInput(utils.BaseInput):
    name: str
    description: typing.Optional[str] = strawberry.UNSET
    priority: typing.Optional[int] = strawberry.UNSET
    conditions: typing.Optional[ShippingRuleConditionsInput] = strawberry.UNSET
    actions: typing.Optional[ShippingRuleActionsInput] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class UpdateShippingRuleMutationInput(utils.BaseInput):
    id: str
    name: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    priority: typing.Optional[int] = strawberry.UNSET
    conditions: typing.Optional[ShippingRuleConditionsInput] = strawberry.UNSET
    actions: typing.Optional[ShippingRuleActionsInput] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET


@strawberry.input
class ShippingRuleFilter(utils.Paginated):
    keyword: typing.Optional[str] = strawberry.UNSET
    is_active: typing.Optional[bool] = strawberry.UNSET
    priority: typing.Optional[int] = strawberry.UNSET

# endregion
