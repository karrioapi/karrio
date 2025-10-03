import typing
import datetime
import strawberry

import karrio.lib as lib
import karrio.server.core.models as core
import karrio.server.graph.utils as utils
import karrio.server.tracing.models as tracing
import karrio.server.graph.schemas.base as base
import karrio.server.automation.models as models
import karrio.server.automation.filters as filters
import karrio.server.automation.utils as automation
import karrio.server.automation.schemas as schemas
import karrio.server.graph.schemas.automation.inputs as inputs

# -----------------------------------------------------------
# workflow related types
# -----------------------------------------------------------
# region

@strawberry.type
class WorkflowTriggerTemplateType:
    object_type: str
    slug: str
    trigger_type: automation.WorkflowTriggerTypeEnum
    schedule: typing.Optional[str] = None
    template_slug: typing.Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime


@strawberry.type
class WorkflowTriggerType(WorkflowTriggerTemplateType):
    id: str
    secret: typing.Optional[str] = None
    secret_key: typing.Optional[str] = None
    next_run_at: typing.Optional[datetime.datetime] = None
    last_run_at: typing.Optional[datetime.datetime] = None

    @strawberry.field
    def is_due(self: models.WorkflowTrigger) -> bool:
        """Check if the scheduled workflow trigger is due for execution"""
        return self.is_due

    @strawberry.field
    def next_run_description(self: models.WorkflowTrigger) -> typing.Optional[str]:
        """Human-readable description of when the workflow will run next"""
        if self.trigger_type == automation.WorkflowTriggerTypeEnum.scheduled and self.schedule:
            try:
                from karrio.server.automation.cron_utils import get_cron_description
                return get_cron_description(self.schedule)
            except:
                return None
        return None


@strawberry.type
class WorkflowActionNodeType:
    order: int
    slug: str

    @staticmethod
    def parse(data: dict):
        return WorkflowActionNodeType(
            **{
                k: v
                for k, v in data.items()
                if k in WorkflowActionNodeType.__annotations__
            }
        )


@strawberry.type
class WorkflowTemplateType:
    object_type: str
    slug: str
    name: str
    description: typing.Optional[str] = None
    trigger: typing.Optional[WorkflowTriggerTemplateType] = None
    template_slug: typing.Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @strawberry.field
    def action_nodes(self: models.Workflow) -> typing.List[WorkflowActionNodeType]:
        return [
            WorkflowActionNodeType.parse(_)
            for _ in self.action_nodes
            if isinstance(_, dict)
        ]

    @strawberry.field
    def actions(self: models.Workflow) -> typing.List["WorkflowActionTemplateType"]:
        return self.actions

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.WorkflowFilter] = strawberry.UNSET,
    ) -> utils.Connection["WorkflowTemplateType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.WorkflowFilter()
        queryset = filters.WorkflowFilter(
            _filter.to_dict(), models.Workflow.objects.filter(is_public=True)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class WorkflowType(WorkflowTemplateType):
    id: str
    trigger: typing.Optional[WorkflowTriggerType] = None

    @strawberry.field
    def metadata(self: models.Workflow) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.metadata)
        except:
            return self.metadata

    @strawberry.field
    def actions(self: models.Workflow) -> typing.List["WorkflowActionType"]:
        return self.actions

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["WorkflowType"]:
        return models.Workflow.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.WorkflowFilter] = strawberry.UNSET,
    ) -> utils.Connection["WorkflowType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.WorkflowFilter()
        queryset = filters.WorkflowFilter(
            _filter.to_dict(), models.Workflow.access_by(info.context.request)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())

    @staticmethod
    @utils.authentication_required
    def resolve_scheduled_workflows(
        info,
        filter: typing.Optional[inputs.WorkflowFilter] = strawberry.UNSET,
    ) -> utils.Connection["WorkflowType"]:
        """Resolve active scheduled workflows specifically"""
        _filter = filter if not utils.is_unset(filter) else inputs.WorkflowFilter()

        # Override filter to only include scheduled workflows
        filter_dict = _filter.to_dict()
        filter_dict.update({
            'trigger_type': automation.WorkflowTriggerTypeEnum.scheduled,
            'is_active': True
        })

        queryset = filters.WorkflowFilter(
            filter_dict, models.Workflow.access_by(info.context.request)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class WorkflowConnectionTemplateType:
    object_type: str
    name: str
    slug: str
    auth_type: automation.AuthTypeEnum
    port: typing.Optional[int] = None
    host: typing.Optional[str] = None
    endpoint: typing.Optional[str] = None
    description: typing.Optional[str] = None
    parameters_template: typing.Optional[str] = None
    auth_template: typing.Optional[str] = None
    template_slug: typing.Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @strawberry.field
    def metafields(self: core.Metafield) -> typing.List[base.types.MetafieldType]:
        return self.metafields.all()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.WorkflowConnectionFilter] = strawberry.UNSET,
    ) -> utils.Connection["WorkflowConnectionTemplateType"]:
        _filter = (
            filter if not utils.is_unset(filter) else inputs.WorkflowConnectionFilter()
        )
        queryset = filters.WorkflowConnectionFilter(
            _filter.to_dict(), models.WorkflowConnection.objects.filter(is_public=True)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class WorkflowConnectionType(WorkflowConnectionTemplateType):
    id: str

    @strawberry.field
    def credentials(self: models.WorkflowConnection) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.credentials)
        except:
            return self.credentials

    @strawberry.field
    def metadata(self: models.WorkflowConnection) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.metadata)
        except:
            return self.metadata

    @strawberry.field
    def credentials_from_metafields(self: models.WorkflowConnection) -> typing.Optional[utils.JSON]:
        """Get credentials from metafields, replacing the credentials JSONField"""
        return self.credentials_from_metafields

    @strawberry.field
    def required_credentials(self: models.WorkflowConnection) -> typing.List[str]:
        """Get list of required credential metafields that need to be filled"""
        return self.required_credentials

    @strawberry.field
    def is_credentials_complete(self: models.WorkflowConnection) -> bool:
        """Check if all required credential metafields are provided"""
        return self.is_credentials_complete

    @strawberry.field
    def credential_validation(self: models.WorkflowConnection) -> utils.JSON:
        """Validate that all required credentials are provided"""
        return self.validate_credentials()

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["WorkflowConnectionType"]:
        return (
            models.WorkflowConnection.access_by(info.context.request)
            .filter(id=id)
            .first()
        )

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.WorkflowConnectionFilter] = strawberry.UNSET,
    ) -> utils.Connection["WorkflowConnectionType"]:
        _filter = (
            filter if not utils.is_unset(filter) else inputs.WorkflowConnectionFilter()
        )
        queryset = filters.WorkflowConnectionFilter(
            _filter.to_dict(), models.WorkflowConnection.access_by(info.context.request)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class WorkflowActionTemplateType:
    object_type: str
    slug: str
    name: str
    action_type: automation.WorkflowActionTypeEnum
    description: typing.Optional[str] = None
    port: typing.Optional[int] = None
    host: typing.Optional[str] = None
    endpoint: typing.Optional[str] = None
    method: typing.Optional[automation.HTTPMethodEnum] = None
    parameters_type: typing.Optional[automation.ParametersTypeEnum] = None
    parameters_template: typing.Optional[str] = None
    header_template: typing.Optional[str] = None
    content_type: typing.Optional[automation.HTTPContentTypeEnum] = None
    connection: typing.Optional[WorkflowConnectionTemplateType] = None
    template_slug: typing.Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @strawberry.field
    def metafields(self: core.Metafield) -> typing.List[base.types.MetafieldType]:
        return self.metafields.all()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.WorkflowActionFilter] = strawberry.UNSET,
    ) -> utils.Connection["WorkflowActionType"]:
        _filter = (
            filter if not utils.is_unset(filter) else inputs.WorkflowActionFilter()
        )
        queryset = filters.WorkflowActionFilter(
            _filter.to_dict(), models.WorkflowAction.objects.filter(is_public=True)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class WorkflowActionType(WorkflowActionTemplateType):
    id: str
    connection: typing.Optional[WorkflowConnectionType] = None

    @strawberry.field
    def metadata(self: models.WorkflowAction) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.metadata)
        except:
            return self.metadata

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["WorkflowActionType"]:
        return (
            models.WorkflowAction.access_by(info.context.request).filter(id=id).first()
        )

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.WorkflowActionFilter] = strawberry.UNSET,
    ) -> utils.Connection["WorkflowActionType"]:
        _filter = (
            filter if not utils.is_unset(filter) else inputs.WorkflowActionFilter()
        )
        queryset = filters.WorkflowActionFilter(
            _filter.to_dict(), models.WorkflowAction.access_by(info.context.request)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


@strawberry.type
class WorkflowEventType:
    object_type: str
    id: str
    test_mode: bool
    status: automation.WorkflowEventStatusEnum
    event_type: automation.WorkflowEventTypeEnum
    workflow: WorkflowType
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @strawberry.field
    def parameters(self: models.WorkflowEvent) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.parameters)
        except:
            return self.parameters

    @strawberry.field
    def records(
        self: models.WorkflowConnection,
    ) -> typing.List[base.types.TracingRecordType]:
        return tracing.TracingRecord.objects.filter(meta__workflow_event_id=self.id)

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["WorkflowEventType"]:
        return (
            models.WorkflowEvent.access_by(info.context.request).filter(id=id).first()
        )

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.WorkflowEventFilter] = strawberry.UNSET,
    ) -> utils.Connection["WorkflowEventType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.WorkflowEventFilter()
        queryset = filters.WorkflowEventFilter(
            _filter.to_dict(), models.WorkflowEvent.access_by(info.context.request)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())

@strawberry.type
class SchedulerStatusType:
    """Status information about the scheduled workflow system"""
    registered_triggers_count: int
    active_scheduled_workflows_count: int
    registered_trigger_ids: typing.List[str]

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["manage_workflows"])
    def resolve(info) -> "SchedulerStatusType":
        """Get the current status of the workflow scheduler"""
        from karrio.server.automation.services.scheduler import ScheduledWorkflowRegistry

        # Get registered triggers from the registry
        registered_triggers = ScheduledWorkflowRegistry.get_registered_triggers()

        # Count active scheduled workflows in database
        active_scheduled_count = models.Workflow.access_by(info.context.request).filter(
            is_active=True,
            trigger__trigger_type=automation.WorkflowTriggerTypeEnum.scheduled
        ).count()

        return SchedulerStatusType(
            registered_triggers_count=len(registered_triggers),
            active_scheduled_workflows_count=active_scheduled_count,
            registered_trigger_ids=registered_triggers
        )

# endregion

# -----------------------------------------------------------
# shipping rule related types
# -----------------------------------------------------------
# region


@strawberry.type
class DestinationConditionType:
    country_code: typing.Optional[str] = None
    postal_code: typing.Optional[typing.List[str]] = None


@strawberry.type
class WeightConditionType:
    min: typing.Optional[float] = None
    max: typing.Optional[float] = None
    unit: typing.Optional[str] = None


@strawberry.type
class RateComparisonConditionType:
    compare: automation.RateComparisonFieldEnum
    operator: automation.ComparisonOperatorEnum
    value: float


@strawberry.type
class AddressTypeConditionType:
    type: str  # residential, commercial


@strawberry.type
class ShippingRuleConditionsType:
    destination: typing.Optional[DestinationConditionType] = None
    carrier_id: typing.Optional[str] = None
    service: typing.Optional[str] = None
    weight: typing.Optional[WeightConditionType] = None
    rate_comparison: typing.Optional[RateComparisonConditionType] = None
    metadata: typing.Optional[utils.JSON] = None
    address_type: typing.Optional[AddressTypeConditionType] = None
    value: typing.Optional[float] = None


@strawberry.type
class SelectServiceActionType:
    carrier_code: typing.Optional[str] = None
    carrier_id: typing.Optional[str] = None
    service_code: typing.Optional[str] = None
    strategy: automation.SelectServiceStrategyEnum = automation.SelectServiceStrategyEnum.preferred


@strawberry.type
class ShippingRuleActionsType:
    """Shipping rule actions schema

    Examples:
        {
            "select_service": {
                "strategy": "cheapest",
                "carrier_code": "fedex",
                "carrier_id": "fedex_us_west",
                "service_code": "fedex_ground"
            },
            "block_service": true,
        }
    """

    select_service: typing.Optional[SelectServiceActionType] = None
    block_service: typing.Optional[bool] = False


@strawberry.type
class ShippingRuleType:
    object_type: str
    id: str
    name: str
    slug: str
    priority: int
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: typing.Optional[str] = None

    @strawberry.field
    def conditions(
        self: models.ShippingRule,
    ) -> typing.Optional[ShippingRuleConditionsType]:
        try:
            return lib.to_object(
                schemas.ShippingRuleConditions, lib.to_dict(self.conditions)
            )
        except:
            return None

    @strawberry.field
    def actions(self: models.ShippingRule) -> typing.Optional[ShippingRuleActionsType]:
        try:
            return lib.to_object(schemas.ShippingRuleActions, lib.to_dict(self.actions))
        except:
            return None

    @strawberry.field
    def metadata(self: models.ShippingRule) -> typing.Optional[utils.JSON]:
        try:
            return lib.to_dict(self.metadata)
        except:
            return self.metadata

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["ShippingRuleType"]:
        return models.ShippingRule.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.ShippingRuleFilter] = strawberry.UNSET,
    ) -> utils.Connection["ShippingRuleType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.ShippingRuleFilter()
        queryset = filters.ShippingRuleFilter(
            _filter.to_dict(), models.ShippingRule.access_by(info.context.request)
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())


# endregion
