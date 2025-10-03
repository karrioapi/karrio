import typing
import datetime
import attr
import jstruct
from karrio.server.automation.serializers import (
    RateComparisonField,
    ComparisonOperator,
    SelectServiceStrategy,
)


@attr.s(auto_attribs=True)
class DestinationCondition:
    """Destination condition schema for shipping rules."""
    country_code: typing.Optional[str] = None
    postal_code: typing.Optional[typing.List[str]] = jstruct.JList[str]


@attr.s(auto_attribs=True)
class WeightCondition:
    """Weight condition schema for shipping rules."""
    min: typing.Optional[float] = None
    max: typing.Optional[float] = None
    unit: typing.Optional[str] = "lb"


@attr.s(auto_attribs=True)
class RateComparisonCondition:
    """Rate comparison condition schema for shipping rules."""
    compare: RateComparisonField
    operator: ComparisonOperator
    value: float


@attr.s(auto_attribs=True)
class AddressTypeCondition:
    """Address type condition schema for shipping rules."""
    type: str  # residential, commercial


@attr.s(auto_attribs=True)
class ShippingRuleConditions:
    """Complete conditions schema for shipping rules."""
    carrier_id: typing.Optional[str] = None
    service: typing.Optional[str] = None
    value: typing.Optional[float] = None
    destination: typing.Optional[DestinationCondition] = jstruct.JStruct[DestinationCondition]
    weight: typing.Optional[WeightCondition] = jstruct.JStruct[WeightCondition]
    rate_comparison: typing.Optional[RateComparisonCondition] = jstruct.JStruct[RateComparisonCondition]
    address_type: typing.Optional[AddressTypeCondition] = jstruct.JStruct[AddressTypeCondition]
    metadata: typing.Optional[typing.Dict[str, typing.Any]] = {}


@attr.s(auto_attribs=True)
class SelectServiceAction:
    """Select service action schema for shipping rules."""
    carrier_code: typing.Optional[str] = None
    carrier_id: typing.Optional[str] = None
    service_code: typing.Optional[str] = None
    strategy: SelectServiceStrategy = SelectServiceStrategy.preferred


@attr.s(auto_attribs=True)
class ShippingRuleActions:
    """Complete actions schema for shipping rules."""
    select_service: typing.Optional[SelectServiceAction] = jstruct.JStruct[SelectServiceAction]
    block_service: typing.Optional[bool] = False


@attr.s(auto_attribs=True)
class ShippingRuleSchema:
    """Complete shipping rule schema for internal use."""
    id: typing.Optional[str] = None
    name: str = None
    slug: typing.Optional[str] = None
    description: typing.Optional[str] = None
    priority: int = 1
    is_active: bool = True
    conditions: typing.Optional[ShippingRuleConditions] = jstruct.JStruct[ShippingRuleConditions]
    actions: typing.Optional[ShippingRuleActions] = jstruct.JStruct[ShippingRuleActions]
    metadata: typing.Optional[typing.Dict[str, typing.Any]] = {}
    created_at: typing.Optional[datetime.datetime] = None
    updated_at: typing.Optional[datetime.datetime] = None


@attr.s(auto_attribs=True)
class RuleEvaluationResult:
    """Result of rule evaluation for activity tracking."""
    rule_id: str
    rule_name: str
    rule_slug: str
    priority: int
    matched: bool
    applied: bool
    timestamp: datetime.datetime
    conditions_checked: typing.List[str] = jstruct.JList[str]
    action_taken: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class AppliedRuleMetadata:
    """Metadata about applied rule for rate response."""
    rule_id: str
    rule_name: str
    rule_slug: str
    priority: int
    applied_at: datetime.datetime
    action_taken: str
    conditions_matched: typing.List[str] = jstruct.JList[str]


@attr.s(auto_attribs=True)
class ShipmentRuleContext:
    """Context for rule evaluation including shipment data."""
    destination_country: typing.Optional[str] = None
    destination_postal_code: typing.Optional[str] = None
    total_weight: typing.Optional[float] = None
    weight_unit: typing.Optional[str] = None
    total_value: typing.Optional[float] = None
    address_type: typing.Optional[str] = None
    carrier_preferences: typing.Optional[typing.List[str]] = jstruct.JList[str]
    service_preferences: typing.Optional[typing.List[str]] = jstruct.JList[str]
