import typing
import strawberry
import karrio.server.automation.serializers as serializers


AuthTypeEnum: typing.Any = strawberry.enum(serializers.AutomationAuthType)  # type: ignore
WorkflowActionTypeEnum: typing.Any = strawberry.enum(serializers.AutomationActionType)  # type: ignore
HTTPMethodEnum: typing.Any = strawberry.enum(serializers.AutomationHTTPMethod)  # type: ignore
ParametersTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    serializers.AutomationParametersType
)
HTTPContentTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    serializers.AutomationHTTPContentType
)
WorkflowEventTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    serializers.AutomationEventType
)
WorkflowEventStatusEnum: typing.Any = strawberry.enum(  # type: ignore
    serializers.AutomationEventStatus
)
WorkflowTriggerTypeEnum: typing.Any = strawberry.enum(  # type: ignore
    serializers.AutomationTriggerType
)

# Shipping Rule related enums
RateComparisonFieldEnum: typing.Any = strawberry.enum(serializers.RateComparisonField)  # type: ignore
ComparisonOperatorEnum: typing.Any = strawberry.enum(serializers.ComparisonOperator)  # type: ignore
SelectServiceStrategyEnum: typing.Any = strawberry.enum(serializers.SelectServiceStrategy)  # type: ignore