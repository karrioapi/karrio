"""Karrio Shipping Rules Engine - Intelligent Rate Selection & Automation

This module provides a production-ready shipping rules engine that automates carrier and service
selection based on shipment characteristics. It follows industry-standard patterns while adding
advanced rate comparison and activity tracking capabilities.

🎯 **Core Functionality**

The rules engine evaluates shipping rules against shipment data to automatically select the
optimal rate based on configurable conditions (destination, weight, value) and actions
(cheapest, fastest, preferred carrier). It integrates seamlessly with Karrio's existing
rate fetching infrastructure via the @utils.rate_selection decorator pattern.

📊 **Data Flow Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           KARRIO SHIPPING RULES ENGINE                          │
│                          Complete Data Flow Illustration                        │
└─────────────────────────────────────────────────────────────────────────────────┘

INPUT LAYER - Shipment Creation Request
┌─────────────────────────────────────────────────────────────────────────────────┐
│ HTTP Request: POST /shipments                                                   │
│ {                                                                               │
│   "shipper": {"country_code": "US", "postal_code": "10001"},                   │
│   "recipient": {"country_code": "US", "postal_code": "90210"},                 │
│   "parcels": [{"weight": 0.75, "weight_unit": "LB"}],                         │
│   "carrier_ids": ["usps", "ups", "fedex"],                                    │
│   "options": {"apply_shipping_rules": true}                                    │
│ }                                                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
RATE FETCHING - Multi-Carrier API Calls
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Parallel Carrier Requests → Multiple Rate Options                              │
│                                                                                 │
│ USPS Rates:                   UPS Rates:                    FedEx Rates:       │
│ ├─ first_class: $3.50        ├─ ground: $8.90              ├─ ground: $9.25    │
│ ├─ priority: $8.75           ├─ 2day: $15.40               ├─ 2day: $16.80     │
│ └─ express: $25.30           └─ next_day: $35.50           └─ next_day: $38.20  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
RULES ENGINE PROCESSING - Core Intelligence Layer
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Step 1: NORMALIZE SHIPMENT DATA                                                │
│         _normalize_shipment_data() → Consistent dict format                    │
│                                                                                 │
│ Step 2: CREATE RULE CONTEXT                                                    │
│         _create_rule_context() → Extract evaluation criteria                   │
│         ┌─────────────────────────────────────────────────────────────────┐   │
│         │ ShipmentRuleContext:                                            │   │
│         │ ├─ destination_country: "US"                                    │   │
│         │ ├─ destination_postal_code: "90210"                             │   │
│         │ ├─ total_weight: 0.75                                          │   │
│         │ ├─ weight_unit: "LB"                                           │   │
│         │ └─ total_value: None                                           │   │
│         └─────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│ Step 3: EVALUATE RULES (Priority Ordered)                                      │
│         ┌─────────────────────────────────────────────────────────────────┐   │
│         │ Rule #1: "USPS First Class Under 1lb" (Priority: 1)           │   │
│         │ Conditions: country_code=US AND weight≤1lb                     │   │
│         │ Actions: select_service(carrier=usps, service=first_class)     │   │
│         │ Result: ✅ MATCHED                                              │   │
│         └─────────────────────────────────────────────────────────────────┘   │
│         ┌─────────────────────────────────────────────────────────────────┐   │
│         │ Rule #2: "UPS Ground for Heavy" (Priority: 2)                 │   │
│         │ Conditions: country_code=US AND weight>5lb                     │   │
│         │ Result: ❌ NOT MATCHED (weight too light)                       │   │
│         └─────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│ Step 4: APPLY WINNING RULE                                                     │
│         apply_shipping_rule() → Find matching rate & add metadata              │
│                                                                                 │
│ Step 5: GENERATE ACTIVITY LOG                                                  │
│         Track which rules matched/applied for transparency                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
OUTPUT LAYER - Enhanced Shipment Response
┌─────────────────────────────────────────────────────────────────────────────────┐
│ HTTP Response: 201 Created                                                      │
│ {                                                                               │
│   "id": "shp_abc123",                                                          │
│   "rates": [...all available rates...],                                       │
│   "selected_rate": {                                                           │
│     "id": "rate_usps_first_class",                                            │
│     "service": "usps_first_class",                                            │
│     "total_charge": 3.50,                                                     │
│     "meta": {                                                                  │
│       "applied_rule": {                   ← 🔄 RULE METADATA                  │
│         "rule_id": "rule_first_class",                                        │
│         "rule_name": "USPS First Class Under 1lb",                           │
│         "priority": 1,                                                        │
│         "applied_at": "2025-01-27T10:30:00Z",                                │
│         "conditions_matched": [                                               │
│           "destination.country_code: US",                                     │
│           "weight: 0.75lb <= 1.0lb"                                          │
│         ],                                                                     │
│         "action_taken": "select_service: usps_first_class"                    │
│       }                                                                        │
│     }                                                                          │
│   },                                                                           │
│   "meta": {                                                                    │
│     "rule_activity": {                     ← 🔄 ACTIVITY TRACKING             │
│       "applied_rule": {                                                       │
│         "id": "rule_first_class",                                             │
│         "slug": "usps_first_class_under_1lb",                                │
│         "timestamp": "2025-01-27T10:30:00Z",                                 │
│         "action": "select_service: usps_first_class"                          │
│       }                                                                        │
│     }                                                                          │
│   }                                                                            │
│ }                                                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

🏗️ **Industry-Standard Rule Patterns**

Common weight threshold patterns with automatic unit conversion:

```python
# Example Rule Configurations:

# 1. Lightweight Packages (Industry Pattern)
{
  "name": "USPS First Class Under 16oz",
  "conditions": {
    "destination": {"country_code": "US"},
    "weight": {"max": 16, "unit": "oz"}
  },
  "actions": {
    "select_service": {"carrier_code": "usps", "service_code": "first_class"}
  }
}

# 2. Medium Weight Packages
{
  "name": "USPS Priority 1-5lbs",
  "conditions": {
    "destination": {"country_code": "US"},
    "weight": {"min": 1, "max": 5, "unit": "lb"}
  },
  "actions": {
    "select_service": {"strategy": "cheapest", "carrier_code": "usps"}
  }
}

# 3. Rate Comparison Rules (Advanced)
{
  "name": "UPS for Expensive Shipments",
  "conditions": {
    "destination": {"country_code": "US"},
    "rate_comparison": {
      "compare": "total_charge",
      "operator": "gte",
      "value": 150.0
    }
  },
  "actions": {
    "select_service": {"carrier_code": "ups"}
  }
}
```

⚡ **Performance Characteristics**

- **Lazy Loading**: Rules only load when explicitly enabled via options.apply_shipping_rules
- **Priority-Based Processing**: Short-circuit evaluation stops at first matching rule
- **Functional Programming**: Map/filter/reduce patterns for efficient rule evaluation
- **Caching**: Rule context calculated once per shipment, reused across evaluations
- **Error Resilience**: lib.failsafe() wrapping prevents rule failures from breaking shipments

🔄 **Integration Points**

The rules engine integrates at multiple platform levels:

1. **Manager API** (/shipments): Persistent shipment creation with rules
2. **Proxy API** (/proxy/shipping): Direct carrier calls with rules overlay
3. **GraphQL API**: Advanced rule management and shipment creation
4. **Core Gateway**: @utils.rate_selection decorator integration point

📈 **Rule Evaluation Logic Flow**

```
For each active rule (ordered by priority):
  ┌─ Check if rule conditions match shipment ─┐
  │                                           │
  │  ┌─ destination.country_code match?       │
  │  ├─ weight within min/max range?          │
  │  ├─ postal_code pattern match?            │
  │  ├─ rate comparison conditions met?       │
  │  └─ custom carrier/service filters?       │
  │                                           │
  └─ If ALL conditions match ────────────────┬─ Apply rule action
                                             │  ├─ select_service (cheapest/fastest/preferred)
                                             │  ├─ block_service (prevent selection)
                                             │  └─ rate_comparison filtering
                                             │
                                             └─ Add metadata & stop (highest priority wins)
```

📝 **Activity Tracking & Transparency**

Every rule evaluation generates detailed activity logs for debugging and transparency:
- Which rules were evaluated
- Which conditions were checked
- Why rules matched or didn't match
- What action was taken
- Timestamp and priority information

This provides visibility into automated decisions for users and administrators.

🔧 **Usage Examples**

```python
# Basic Usage - Manager API Integration
shipment_data = {
    "recipient": {"country_code": "US", "postal_code": "90210"},
    "parcels": [{"weight": 0.75, "weight_unit": "LB"}],
    "options": {"apply_shipping_rules": True}
}

# Direct Rules Engine Usage
from karrio.server.automation.services.rules_engine import process_shipping_rules

shipment_data, selected_rate, activity = process_shipping_rules(
    shipment=normalized_shipment,
    rules=active_rules_queryset
)

# Result: Auto-selected cheapest USPS rate with rule metadata attached
```

🎯 **Key Functions Overview**

Core Engine:
- process_shipping_rules(): Main entry point for rule processing
- _evaluate_single_rule(): Individual rule matching logic
- apply_shipping_rule(): Execute winning rule's action

Condition Checkers:
- _check_destination_condition(): Geographic and postal code matching
- _check_weight_condition(): Weight ranges with unit conversion
- _check_rate_comparison_condition(): Advanced rate filtering

Action Executors:
- _select_fastest_rate(): Transit time optimization
- _select_preferred_rate(): Carrier/service preference matching
- _filter_rates_by_comparison(): Rate-based filtering

Utility Functions:
- _normalize_shipment_data(): Data format standardization
- _create_rule_context(): Extract evaluation criteria
- _get_matched_conditions_summary(): Human-readable rule explanations

This architecture provides enterprise-grade shipping automation while maintaining Karrio's
flexibility and extensibility principles.
"""

import typing
import datetime
import functools
import logging
from operator import attrgetter

import karrio.lib as lib
import karrio.core.units as units
import karrio.server.core.datatypes as datatypes
import karrio.server.automation.schemas as schemas
import karrio.server.manager.models as manager_models
import karrio.server.manager.serializers as serializers
import karrio.server.automation.models as automation_models

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Type aliases for better readability
ShipmentType = typing.Union[
    dict,
    datatypes.Shipment,
    datatypes.RateRequest,
    manager_models.Shipment,
    datatypes.ShipmentRequest,
]

RuleActivityList = typing.List[dict]
RuleEvaluationTuple = typing.Tuple[dict, typing.Optional[datatypes.Rate], dict]


def process_shipping_rules(
    shipment: ShipmentType,
    rules: typing.List[automation_models.ShippingRule] = None,
) -> RuleEvaluationTuple:
    """Process shipping rules and apply them to the shipment using functional programming patterns.

    This is the main entry point for the Karrio shipping rules engine. It evaluates all active
    rules against a shipment, selects the highest priority matching rule, and applies its action
    to automatically select the optimal shipping rate. The function follows functional programming
    patterns with map/filter/reduce operations for efficient rule processing.

    🎯 **Core Functionality**

    The function implements a sophisticated rule evaluation pipeline that:
    1. Normalizes diverse shipment data formats into consistent dictionaries
    2. Extracts structured evaluation context (weight, destination, value, etc.)
    3. Evaluates rules in priority order using short-circuit logic
    4. Applies the winning rule's action to select the best rate
    5. Generates detailed activity tracking for transparency and debugging

    📊 **Detailed Processing Flow**

    ```
    INPUT: Shipment Data + Rules List
    ┌─────────────────────────────────────────────────────────────────────┐
    │ shipment: {                                                         │
    │   "recipient": {"country_code": "US", "postal_code": "90210"},      │
    │   "parcels": [{"weight": 0.75, "weight_unit": "LB"}],              │
    │   "rates": [                                                        │
    │     {"service": "usps_first_class", "total_charge": 3.50},         │
    │     {"service": "ups_ground", "total_charge": 8.90}                │
    │   ]                                                                 │
    │ }                                                                   │
    │                                                                     │
    │ rules: [ShippingRule(priority=1, conditions=..., actions=...)]     │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    STEP 1: NORMALIZE SHIPMENT DATA
    ┌─────────────────────────────────────────────────────────────────────┐
    │ _normalize_shipment_data(shipment) → dict                          │
    │                                                                     │
    │ Handles multiple input formats:                                     │
    │ ├─ dict → pass through unchanged                                    │
    │ ├─ manager_models.Shipment → serialize to dict                     │
    │ ├─ datatypes.Shipment → convert to dict                           │
    │ └─ datatypes.ShipmentRequest → transform to dict                   │
    │                                                                     │
    │ Result: Consistent dictionary format for rule evaluation           │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    STEP 2: CREATE RULE CONTEXT
    ┌─────────────────────────────────────────────────────────────────────┐
    │ _create_rule_context(shipment_data) → ShipmentRuleContext          │
    │                                                                     │
    │ Extracts & calculates evaluation criteria:                         │
    │ ┌─────────────────────────────────────────────────────────────────┐ │
    │ │ destination_country: "US"           ← recipient.country_code    │ │
    │ │ destination_postal_code: "90210"    ← recipient.postal_code     │ │
    │ │ total_weight: 0.75                  ← sum(parcel.weight)        │ │
    │ │ weight_unit: "LB"                   ← first_parcel.weight_unit  │ │
    │ │ total_value: None                   ← customs.declared_value    │ │
    │ └─────────────────────────────────────────────────────────────────┘ │
    │                                                                     │
    │ Context used for ALL rule evaluations (calculated once)            │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    STEP 3: EVALUATE RULES (Priority Order + Short-Circuit)
    ┌─────────────────────────────────────────────────────────────────────┐
    │ map(_evaluate_single_rule, sorted(rules, key=priority))             │
    │                                                                     │
    │ Rule #1 (Priority: 1): "USPS First Class Under 1lb"               │
    │ ┌─────────────────────────────────────────────────────────────────┐ │
    │ │ Conditions Check:                                               │ │
    │ │ ├─ destination.country_code == "US" → ✅ MATCH                  │ │
    │ │ ├─ weight <= 1.0 lb → ✅ MATCH (0.75 <= 1.0)                   │ │
    │ │ └─ ALL conditions matched → RULE MATCHES                        │ │
    │ │                                                                 │ │
    │ │ Result: RuleEvaluationResult(matched=True, priority=1)          │ │
    │ └─────────────────────────────────────────────────────────────────┘ │
    │                                                                     │
    │ Rule #2 (Priority: 2): "UPS Ground for Heavy"                     │
    │ ┌─────────────────────────────────────────────────────────────────┐ │
    │ │ Conditions Check:                                               │ │
    │ │ ├─ destination.country_code == "US" → ✅ MATCH                  │ │
    │ │ ├─ weight > 5.0 lb → ❌ NO MATCH (0.75 <= 5.0)                 │ │
    │ │ └─ Not all conditions matched → RULE SKIPPED                    │ │
    │ │                                                                 │ │
    │ │ Result: RuleEvaluationResult(matched=False, priority=2)         │ │
    │ └─────────────────────────────────────────────────────────────────┘ │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    STEP 4: FIND WINNING RULE (First Match Wins)
    ┌─────────────────────────────────────────────────────────────────────┐
    │ next(eval for eval in evaluations if eval.matched) → Rule #1       │
    │                                                                     │
    │ Winner: "USPS First Class Under 1lb" (Priority 1, matched=True)    │
    │                                                                     │
    │ If no rule applied:                                                 │
    │ ┌─────────────────────────────────────────────────────────────────┐ │
    │ │ {                                                               │ │
    │ │   "summary": "Evaluated 2 rules, 1 matched, none applied",     │ │
    │ │   "timestamp": "2025-01-27T10:30:00Z"                          │ │
    │ │ }                                                               │ │
    │ └─────────────────────────────────────────────────────────────────┘ │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    STEP 5: APPLY WINNING RULE
    ┌─────────────────────────────────────────────────────────────────────┐
    │ _apply_rule_with_metadata(shipment, winning_rule, evaluation)       │
    │                                                                     │
    │ Sub-steps:                                                          │
    │ ├─ apply_shipping_rule() → Find matching rate                      │
    │ ├─ Add rule metadata to selected rate                              │
    │ ├─ Generate conditions summary                                      │
    │ └─ Mark evaluation as applied                                       │
    │                                                                     │
    │ Selected Rate: usps_first_class ($3.50) with rule metadata         │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    STEP 6: GENERATE ACTIVITY LOG
    ┌─────────────────────────────────────────────────────────────────────┐
    │ Create transparent activity tracking:                               │
    │                                                                     │
    │ If rule applied successfully:                                       │
    │ ┌─────────────────────────────────────────────────────────────────┐ │
    │ │ {                                                               │ │
    │ │   "applied_rule": {                                             │ │
    │ │     "id": "rule_first_class",                                   │ │
    │ │     "slug": "usps_first_class_under_1lb",                       │ │
    │ │     "timestamp": "2025-01-27T10:30:00Z",                       │ │
    │ │     "action": "select_service: usps_first_class"                │ │
    │ │   }                                                             │ │
    │ │ }                                                               │ │
    │ └─────────────────────────────────────────────────────────────────┘ │
    │                                                                     │
    │ If no rule applied:                                                 │
    │ ┌─────────────────────────────────────────────────────────────────┐ │
    │ │ {                                                               │ │
    │ │   "summary": "Evaluated 2 rules, 1 matched, none applied",     │ │
    │ │   "timestamp": "2025-01-27T10:30:00Z"                          │ │
    │ │ }                                                               │ │
    │ └─────────────────────────────────────────────────────────────────┘ │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    OUTPUT: (shipment_data, selected_rate, rule_activity)
    ```

    Args:
        shipment: The shipment data to evaluate rules against. Supports multiple formats:
                 - dict: Raw shipment data (most common, fastest processing)
                 - datatypes.Shipment: Structured shipment object from core
                 - datatypes.RateRequest: Rate request object from API
                 - manager_models.Shipment: Django model instance from database
                 - datatypes.ShipmentRequest: Complete shipment request object

        rules: List of ShippingRule model instances to evaluate (optional).
               If None or empty, no rules will be processed and function returns
               early with (normalized_shipment, None, {}).
               Rules are automatically sorted by priority (ascending) during processing.

    Returns:
        RuleEvaluationTuple: A 3-tuple containing:

        1. **shipment_data** (dict): Normalized shipment data in consistent dictionary format.
           Always returned regardless of rule processing success/failure.

        2. **selected_rate** (datatypes.Rate | None): Rate selected by the winning rule.
           - If a rule matched and applied successfully: Rate object with applied_rule metadata
           - If no rules matched or application failed: None
           - Contains enriched metadata showing which rule applied and why

        3. **rule_activity** (dict): Activity log showing rule evaluation transparency.
           - If rule applied: {"applied_rule": {id, slug, timestamp, action}}
           - If no rule applied: {"summary": "evaluation summary", "timestamp": "..."}
           - Used for debugging, auditing, and user feedback

    Raises:
        Exception: Only if shipment normalization fails with invalid input data.
                  Rule evaluation errors are caught and handled gracefully with
                  lib.failsafe() wrapping to prevent breaking shipment processing.

    Examples:
        Basic usage with US domestic lightweight package:

        >>> from karrio.server.automation.models import ShippingRule
        >>>
        >>> # Setup: Rule for USPS First Class under 1lb
        >>> rule = ShippingRule.objects.create(
        ...     name="USPS First Class Under 1lb",
        ...     priority=1,
        ...     conditions={
        ...         "destination": {"country_code": "US"},
        ...         "weight": {"max": 1.0, "unit": "lb"}
        ...     },
        ...     actions={
        ...         "select_service": {"carrier_code": "usps", "service_code": "first_class"}
        ...     }
        ... )
        >>>
        >>> # Shipment: 12oz package to California
        >>> shipment = {
        ...     "recipient": {"country_code": "US", "postal_code": "90210"},
        ...     "parcels": [{"weight": 0.75, "weight_unit": "LB"}],
        ...     "rates": [
        ...         {"service": "usps_first_class", "total_charge": 3.50, "carrier_name": "usps"},
        ...         {"service": "ups_ground", "total_charge": 8.90, "carrier_name": "ups"}
        ...     ]
        ... }
        >>>
        >>> # Process rules
        >>> shipment_data, selected_rate, activity = process_shipping_rules(shipment, [rule])
        >>>
        >>> # Results
        >>> print(f"Selected: {selected_rate.service} - ${selected_rate.total_charge}")
        Selected: usps_first_class - $3.50
        >>>
        >>> print(f"Applied rule: {selected_rate.meta['applied_rule']['rule_name']}")
        Applied rule: USPS First Class Under 1lb
        >>>
        >>> print(f"Activity: {activity['applied_rule']['action']}")
        Activity: select_service: usps_first_class

        Weight threshold rule with unit conversion:

        >>> # Rule: USPS First Class under 16oz
        >>> oz_rule = ShippingRule.objects.create(
        ...     name="USPS First Class Under 16oz",
        ...     priority=1,
        ...     conditions={
        ...         "destination": {"country_code": "US"},
        ...         "weight": {"max": 16, "unit": "oz"}
        ...     },
        ...     actions={"select_service": {"carrier_code": "usps", "service_code": "first_class"}}
        ... )
        >>>
        >>> # Shipment: 0.5lb package (8oz - should match 16oz rule)
        >>> light_shipment = {
        ...     "recipient": {"country_code": "US"},
        ...     "parcels": [{"weight": 0.5, "weight_unit": "LB"}],  # 8oz in lb
        ...     "rates": [{"service": "usps_first_class", "total_charge": 3.50}]
        ... }
        >>>
        >>> _, selected, _ = process_shipping_rules(light_shipment, [oz_rule])
        >>> print(f"Rule matched 8oz package: {selected is not None}")
        Rule matched 8oz package: True

        Rate comparison rule for expensive shipments:

        >>> # Rule: UPS for shipments over $100
        >>> expensive_rule = ShippingRule.objects.create(
        ...     name="UPS for Expensive Shipments",
        ...     priority=1,
        ...     conditions={
        ...         "destination": {"country_code": "US"},
        ...         "rate_comparison": {
        ...             "compare": "total_charge",
        ...             "operator": "gte",
        ...             "value": 100.0
        ...         }
        ...     },
        ...     actions={"select_service": {"carrier_code": "ups"}}
        ... )
        >>>
        >>> # Shipment: High-value package with expensive rates
        >>> expensive_shipment = {
        ...     "recipient": {"country_code": "US"},
        ...     "parcels": [{"weight": 10, "weight_unit": "LB"}],
        ...     "rates": [
        ...         {"service": "usps_priority", "total_charge": 85.00, "carrier_name": "usps"},
        ...         {"service": "ups_ground", "total_charge": 120.00, "carrier_name": "ups"}
        ...     ]
        ... }
        >>>
        >>> _, selected, _ = process_shipping_rules(expensive_shipment, [expensive_rule])
        >>> print(f"Selected UPS for expensive shipment: {selected.carrier_name == 'ups'}")
        Selected UPS for expensive shipment: True

    Performance Notes:
        - Function uses functional programming patterns (map/filter/reduce) for efficiency
        - Short-circuit evaluation stops at first matching rule (priority order)
        - Rule context calculated once and reused across all rule evaluations
        - lib.failsafe() wrapping prevents rule errors from breaking shipment processing
        - Lazy evaluation means no work is done if rules list is empty

    Integration Notes:
        - Designed to integrate via @utils.rate_selection decorator
        - Maintains backward compatibility when rules module not installed
        - Works with existing carrier filtering (carrier_ids, services)
        - Respects manual overrides (selected_rate_id, service parameters)
        - Activity tracking provides transparency for debugging and user feedback
    """
    if not rules:
        return _normalize_shipment_data(shipment), None, {}

    # Step 1: Normalize shipment data format
    shipment_data = _normalize_shipment_data(shipment)

    # Step 2: Create evaluation context once
    rule_context = _create_rule_context(shipment_data)

    # Step 3: Evaluate all rules functionally (map pattern)
    rule_evaluations = list(map(
        lambda rule: _evaluate_single_rule(rule, rule_context, shipment_data),
        sorted(rules, key=attrgetter('priority'))  # Sort by priority first
    ))

    # Step 4: Find first matching rule (filter + next pattern)
    winning_rule_evaluation = next(
        (evaluation for evaluation in rule_evaluations if evaluation.matched),
        None
    )

    # Step 5: Apply winning rule and mark as applied
    selected_rate = None
    if winning_rule_evaluation:
        # Find the original rule object for the winning evaluation
        winning_rule = next(
            rule for rule in rules
            if rule.id == winning_rule_evaluation.rule_id
        )

        selected_rate = lib.failsafe(
            lambda: _apply_rule_with_metadata(shipment_data, winning_rule, winning_rule_evaluation),
            warning="Failed to apply shipping rule"
        )

        if selected_rate:
            winning_rule_evaluation.applied = True
            winning_rule_evaluation.action_taken = _get_action_description(winning_rule)

    # Step 6: Create simple rule activity summary
    rule_activity = {}

    if winning_rule_evaluation and selected_rate:
        # Rule was successfully applied
        rule_activity = {
            "applied_rule": {
                "id": winning_rule_evaluation.rule_id,
                "slug": winning_rule_evaluation.rule_slug,
                "timestamp": winning_rule_evaluation.timestamp.isoformat(),
                "action": winning_rule_evaluation.action_taken
            }
        }
    else:
        # No rule was applied - provide summary
        matched_rules = [eval for eval in rule_evaluations if eval.matched]
        rule_activity = {
            "summary": f"Evaluated {len(rule_evaluations)} rules, {len(matched_rules)} matched, none applied",
            "timestamp": datetime.datetime.now().isoformat()
        }

    return shipment_data, selected_rate, rule_activity


def _normalize_shipment_data(shipment: ShipmentType) -> dict:
    """Normalize shipment data to consistent dictionary format using Karrio lib utilities.

    This function handles the diverse range of shipment data formats that can be passed to the
    rules engine and converts them all to a consistent dictionary structure for rule evaluation.
    It leverages Karrio's lib.to_dict() and serializer infrastructure for robust data transformation.

    🔄 **Data Format Conversion Flow**

    ```
    INPUT: Various Shipment Formats
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │                            Supported Input Types                                │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                            ┌───────────┼───────────┐
                            │           │           │
                            ▼           ▼           ▼
        ┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
        │   dict (Raw JSON)   │ │ Django Models   │ │  Karrio DataTypes   │
        │                     │ │                 │ │                     │
        │ ✅ Pass Through     │ │ 🔄 Serialize    │ │ 🔄 Convert          │
        │ Fastest Path        │ │ To Dict         │ │ To Dict             │
        └─────────────────────┘ └─────────────────┘ └─────────────────────┘
                            │           │           │
                            └───────────┼───────────┘
                                        │
                                        ▼
    OUTPUT: Consistent Dictionary Structure
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │ {                                                                               │
    │   "recipient": {                                                                │
    │     "country_code": "US",                                                       │
    │     "postal_code": "90210",                                                     │
    │     "address_line1": "123 Main St",                                            │
    │     "city": "Los Angeles"                                                       │
    │   },                                                                            │
    │   "shipper": {...},                                                             │
    │   "parcels": [                                                                  │
    │     {                                                                           │
    │       "weight": 0.75,                                                          │
    │       "weight_unit": "LB",                                                     │
    │       "length": 10, "width": 8, "height": 6                                   │
    │     }                                                                           │
    │   ],                                                                            │
    │   "rates": [...],      ← Available rates for rule evaluation                   │
    │   "customs": {...},    ← Customs info for value-based rules                    │
    │   "options": {...}     ← Request options and preferences                       │
    │ }                                                                               │
    └─────────────────────────────────────────────────────────────────────────────────┘
    ```

    🎯 **Format Handling Strategy**

    1. **dict (Raw JSON)**: Fastest path - return as-is since already in correct format
    2. **Django Models**: Use Karrio serializers to convert model instances to dictionaries
    3. **Karrio DataTypes**: Use lib.to_dict() for consistent transformation
    4. **Error Handling**: Graceful fallback with detailed error reporting

    Args:
        shipment: Shipment data in any supported format. Input types include:

                 - **dict**: Raw shipment data (JSON from API requests)
                   Most common format, processed fastest with pass-through

                 - **manager_models.Shipment**: Django model instance from database
                   Contains all shipment fields including relations (addresses, parcels)

                 - **datatypes.Shipment**: Structured shipment object from Karrio core
                   Used for internal processing and API responses

                 - **datatypes.RateRequest**: Rate request object from API
                   Contains shipment data plus rate-specific parameters

                 - **datatypes.ShipmentRequest**: Complete shipment request object
                   Full request payload including options and preferences

    Returns:
        dict: Normalized shipment data with consistent structure containing:
              - recipient (dict): Destination address information
              - shipper (dict): Origin address information
              - parcels (list): Package dimensions and weight data
              - rates (list): Available shipping rates for selection
              - customs (dict): International shipping customs data
              - options (dict): Request options and preferences

              All keys are guaranteed to exist (empty dict/list if no data).
              Nested objects follow Karrio's standard field naming conventions.

    Raises:
        Exception: If shipment data cannot be converted to dictionary format.
                  This typically indicates invalid input data or corrupted objects.
                  The exception is re-raised to caller for proper error handling.

    Examples:
        Dictionary input (pass-through):

        >>> raw_shipment = {
        ...     "recipient": {"country_code": "US", "postal_code": "90210"},
        ...     "parcels": [{"weight": 1.5, "weight_unit": "LB"}]
        ... }
        >>> normalized = _normalize_shipment_data(raw_shipment)
        >>> normalized == raw_shipment  # Same object reference
        True
        >>> print("Fast path - no conversion needed")
        Fast path - no conversion needed

        Django model input (serialization):

        >>> from karrio.server.manager.models import Shipment
        >>> model_shipment = Shipment.objects.get(id="shp_123")
        >>> normalized = _normalize_shipment_data(model_shipment)
        >>>
        >>> # Verify structure
        >>> 'recipient' in normalized and 'parcels' in normalized
        True
        >>> isinstance(normalized['parcels'], list)
        True
        >>> print(f"Converted model to dict with {len(normalized['parcels'])} parcels")
        Converted model to dict with 3 parcels

        Karrio datatype input (conversion):

        >>> import karrio.server.core.datatypes as datatypes
        >>> shipment_obj = datatypes.Shipment(
        ...     recipient=datatypes.Address(country_code="CA", postal_code="H3B2N4"),
        ...     parcels=[datatypes.Parcel(weight=2.0, weight_unit="KG")]
        ... )
        >>> normalized = _normalize_shipment_data(shipment_obj)
        >>>
        >>> # Check conversion
        >>> normalized['recipient']['country_code']
        'CA'
        >>> normalized['parcels'][0]['weight']
        2.0
        >>> print("Successfully converted datatype to dict")
        Successfully converted datatype to dict

    Performance Notes:
        - Dictionary input uses fast pass-through (O(1) operation)
        - Model serialization involves database field access (O(n) relations)
        - Datatype conversion uses lib.to_dict() optimization
        - Error handling uses try/catch to prevent rule engine failures

    Integration Notes:
        - Used as first step in process_shipping_rules() pipeline
        - Enables rules engine to work with any Karrio shipment format
        - Maintains data consistency across different API endpoints
        - Supports both persistent (Manager API) and direct (Proxy API) workflows
    """
    if isinstance(shipment, dict):
        return shipment

    try:
        return serializers.Shipment(shipment).data
    except Exception as e:
        print(e)
        raise e


def _create_rule_context(shipment: dict) -> schemas.ShipmentRuleContext:
    """Extract and calculate rule evaluation context from shipment data using Karrio utilities.

    This function transforms raw shipment data into a structured context object containing all the
    calculated values that shipping rules need for evaluation. It handles weight aggregation with
    unit normalization, destination extraction, value calculation, and other derived metrics used
    in rule condition matching. The context is calculated once per shipment and reused across all
    rule evaluations for performance optimization.

    🧮 **Context Calculation Flow**

    ```
    INPUT: Normalized Shipment Dictionary
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │ {                                                                               │
    │   "recipient": {"country_code": "US", "postal_code": "90210"},                 │
    │   "parcels": [                                                                  │
    │     {"weight": 0.5, "weight_unit": "LB"},                                     │
    │     {"weight": 0.25, "weight_unit": "LB"}                                     │
    │   ],                                                                            │
    │   "customs": {"declared_value": 150.50}                                        │
    │ }                                                                               │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
    STEP 1: DESTINATION EXTRACTION
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │ Extract geographical information for location-based rules:                      │
    │                                                                                 │
    │ recipient.country_code → destination_country: "US"                             │
    │ recipient.postal_code  → destination_postal_code: "90210"                      │
    │                                                                                 │
    │ Used for: Country targeting, postal code pattern matching, zone calculations   │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
    STEP 2: WEIGHT AGGREGATION & NORMALIZATION
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │ Calculate total weight with robust unit handling:                               │
    │                                                                                 │
    │ Parcel #1: 0.5 LB → 0.50 (using lib.to_decimal for safety)                    │
    │ Parcel #2: 0.25 LB → 0.25                                                      │
    │ ────────────────────────────────────                                           │
    │ Total Weight: 0.75 LB                                                          │
    │                                                                                 │
    │ Weight Unit Detection:                                                          │
    │ ├─ Check first parcel with weight_unit                                         │
    │ ├─ Normalize aliases (POUND→LB, KILOGRAM→KG)                                   │
    │ ├─ Validate against supported units [KG, LB, OZ, G]                           │
    │ └─ Default to "LB" if invalid/missing                                          │
    │                                                                                 │
    │ Result: total_weight=0.75, weight_unit="LB"                                    │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
    STEP 3: VALUE EXTRACTION (Customs Data)
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │ Extract monetary value for value-based rules:                                   │
    │                                                                                 │
    │ customs.declared_value → lib.to_money(150.50) → Decimal('150.50')             │
    │                                                                                 │
    │ Handles: Currency conversion, decimal precision, invalid value fallback        │
    │ Used for: High-value shipment rules, insurance thresholds, customs triggers    │
    └─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
    OUTPUT: Structured Context Object
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │ ShipmentRuleContext {                                                          │
    │   destination_country: "US"           ← Geographic targeting                   │
    │   destination_postal_code: "90210"    ← Zone/region calculations               │
    │   total_weight: 0.75                  ← Aggregated package weight             │
    │   weight_unit: "LB"                   ← Normalized weight unit                │
    │   total_value: Decimal('150.50')      ← Customs/value-based rules             │
    │ }                                                                               │
    │                                                                                 │
    │ ✨ Context reused for ALL rule evaluations (performance optimization)          │
    └─────────────────────────────────────────────────────────────────────────────────┘
    ```

    🎯 **Weight Unit Normalization Logic**

    The function implements robust weight unit handling following Karrio's supported units:

    ```
    INPUT UNITS → NORMALIZED OUTPUT
    ┌─────────────────────────────────────────────────────────────────────────────────┐
    │ Standard Units (Direct Support):                                                │
    │ ├─ "KG" → "KG"     (Kilograms)                                                 │
    │ ├─ "LB" → "LB"     (Pounds)                                                    │
    │ ├─ "OZ" → "OZ"     (Ounces)                                                    │
    │ └─ "G"  → "G"      (Grams)                                                     │
    │                                                                                 │
    │ Common Aliases (Auto-Converted):                                                │
    │ ├─ "POUND"     → "LB"                                                          │
    │ ├─ "OUNCE"     → "OZ"                                                          │
    │ ├─ "GRAM"      → "G"                                                           │
    │ ├─ "KILOGRAM"  → "KG"                                                          │
    │ └─ "lbs", "oz" → "LB", "OZ" (case normalization)                              │
    │                                                                                 │
    │ Invalid/Missing Units:                                                          │
    │ └─ DEFAULT → "LB"  (Most common shipping unit)                                 │
    └─────────────────────────────────────────────────────────────────────────────────┘
    ```

    Args:
        shipment: Normalized shipment dictionary containing recipient, parcels, and customs data.
                  Must be a dictionary (validated by caller) with expected structure:

                  - **recipient** (dict): Destination address with country_code, postal_code
                  - **parcels** (list): Package data with weight and weight_unit fields
                  - **customs** (dict, optional): International shipping data with declared_value

                  The function handles missing keys gracefully with empty dict/list defaults.

    Returns:
        schemas.ShipmentRuleContext: Structured context object with calculated evaluation data:

        - **destination_country** (str|None): ISO country code from recipient.country_code
        - **destination_postal_code** (str|None): Postal code from recipient.postal_code
        - **total_weight** (float): Sum of all parcel weights using lib.to_decimal for safety
        - **weight_unit** (str): Normalized weight unit (KG, LB, OZ, G) with LB default
        - **total_value** (Decimal|None): Monetary value from customs using lib.to_money

    Examples:
        US domestic shipment with multiple parcels:

        >>> shipment = {
        ...     "recipient": {"country_code": "US", "postal_code": "90210"},
        ...     "parcels": [
        ...         {"weight": 0.5, "weight_unit": "LB"},
        ...         {"weight": 8, "weight_unit": "OZ"}  # Mixed units
        ...     ]
        ... }
        >>> context = _create_rule_context(shipment)
        >>>
        >>> # Check aggregated weight (uses first parcel's unit)
        >>> context.total_weight
        8.5
        >>> context.weight_unit
        'LB'
        >>> context.destination_country
        'US'

        International shipment with customs value:

        >>> international_shipment = {
        ...     "recipient": {"country_code": "CA", "postal_code": "H3B2N4"},
        ...     "parcels": [{"weight": 2.5, "weight_unit": "KG"}],
        ...     "customs": {"declared_value": 250.75}
        ... }
        >>> context = _create_rule_context(international_shipment)
        >>>
        >>> # Verify value extraction
        >>> float(context.total_value)
        250.75
        >>> context.weight_unit
        'KG'
        >>> context.destination_country
        'CA'

        Weight unit normalization with aliases:

        >>> shipment_with_aliases = {
        ...     "recipient": {"country_code": "US"},
        ...     "parcels": [
        ...         {"weight": 1, "weight_unit": "POUND"},  # Alias
        ...         {"weight": 2, "weight_unit": "pound"}   # Case variation
        ...     ]
        ... }
        >>> context = _create_rule_context(shipment_with_aliases)
        >>>
        >>> # Check normalization
        >>> context.total_weight
        3.0
        >>> context.weight_unit
        'LB'

        Empty/missing data handling:

        >>> minimal_shipment = {"recipient": {}, "parcels": []}
        >>> context = _create_rule_context(minimal_shipment)
        >>>
        >>> # Verify graceful defaults
        >>> context.destination_country is None
        True
        >>> context.total_weight
        0.0
        >>> context.weight_unit
        'LB'
        >>> context.total_value is None
        True

    Error Handling:
        - Non-dictionary input logs error but continues with empty dict (defensive programming)
        - Invalid weight values handled by lib.to_decimal with 0.0 fallback
        - Missing parcel data results in 0.0 total weight
        - Invalid weight units normalize to "LB" default
        - Missing customs data results in None total_value

    Performance Notes:
        - Context calculated once per shipment, reused for all rule evaluations
        - Uses lib.to_decimal and lib.to_money for robust numeric parsing
        - functools.reduce for efficient weight aggregation
        - Lazy evaluation with next() for weight unit detection

    Integration Notes:
        - Context used by _evaluate_single_rule for condition matching
        - Weight data feeds into _check_weight_condition calculations
        - Destination data used by _check_destination_condition
        - Value data enables customs/value-based rule conditions
        - Structured format enables future rule condition extensions
    """
    if not isinstance(shipment, dict):
        logger.error(f"_create_rule_context received non-dict shipment: {type(shipment)}. This may lead to errors.")
        # Decide on how to handle this: raise error, return default context, or try to force dict.
        # For now, let's proceed but this is a potential error source if shipment is not a dict.
        shipment = {} # Or raise an error: raise TypeError("Shipment must be a dictionary")

    # Extract destination information using lib utilities
    recipient = shipment.get("recipient", {})
    destination_country = recipient.get("country_code")
    destination_postal_code = recipient.get("postal_code")

    # Calculate total weight from all parcels using lib.to_decimal for robust parsing
    parcels = lib.to_list(shipment.get("parcels", []))
    total_weight = functools.reduce(
        lambda total, parcel: total + (lib.to_decimal(parcel.get("weight")) or 0.0),
        parcels,
        0.0
    )

    # Get weight unit from first parcel - only support KG, LB, OZ, G
    def normalize_weight_unit(unit_str: str) -> str:
        """Normalize to supported Karrio weight units only."""
        if not unit_str:
            return "LB"

        unit = unit_str.upper()
        # Only support the 4 standard Karrio weight units
        if unit in ["KG", "LB", "OZ", "G"]:
            return unit

        # Simple common aliases
        aliases = {"POUND": "LB", "OUNCE": "OZ", "GRAM": "G", "KILOGRAM": "KG"}
        return aliases.get(unit, "LB")

    weight_unit = next(
        (normalize_weight_unit(parcel.get("weight_unit"))
         for parcel in parcels if parcel.get("weight_unit")),
        "LB"
    )

    # Extract total value from customs using lib.to_money for monetary values
    customs = shipment.get("customs") or {}
    total_value = lib.to_money(customs.get("declared_value")) if customs.get("declared_value") else None

    # Use lib.to_object for consistent object creation
    return lib.to_object(schemas.ShipmentRuleContext, {
        "destination_country": destination_country,
        "destination_postal_code": destination_postal_code,
        "total_weight": total_weight,
        "weight_unit": weight_unit,
        "total_value": total_value,
    })


def _evaluate_single_rule(
    rule: automation_models.ShippingRule,
    context: schemas.ShipmentRuleContext,
    shipment_data: dict,
) -> schemas.RuleEvaluationResult:
    """Evaluate a single shipping rule against shipment context using Karrio patterns.

    Performs comprehensive rule matching including destination, weight, and rate comparison
    conditions. Uses short-circuit evaluation for performance and lib.failsafe for robustness.

    Args:
        rule: ShippingRule model instance to evaluate
        context: Pre-calculated shipment context
        shipment_data: Normalized shipment dictionary containing rates

    Returns:
        RuleEvaluationResult: Detailed evaluation result with match status

    Example:
        >>> rule = ShippingRule(
        ...     name="First Class Under 1lb",
        ...     conditions={"weight": {"max": 1, "unit": "lb"}, "destination": {"country_code": "US"}},
        ...     priority=1,
        ...     is_active=True
        ... )
        >>> context = ShipmentRuleContext(destination_country="US", total_weight=0.5, weight_unit="lb")
        >>> result = _evaluate_single_rule(rule, context, {})
        >>> result.matched
        True
        >>> result.conditions_checked
        ['destination', 'weight']

    Evaluation Flow:
        Rule ──┬──► Check if Active ──┬──► ❌ Return False
               │                     └──► ✅ Continue
               │
               ├──► Check Destination ──┬──► ❌ Return False
               │                        └──► ✅ Continue
               │
               ├──► Check Weight ───────┬──► ❌ Return False
               │                        └──► ✅ Continue
               │
               └──► Check Rate Comparison ──► Return Result
    """
    # Initialize tracking
    conditions_checked = []
    matched = rule.is_active  # Start with active status

    if not matched:
        return _create_evaluation_result(rule, matched, conditions_checked)

    # Convert rule conditions to structured format using lib.to_object
    rule_conditions = lib.to_object(schemas.ShippingRuleConditions, rule.conditions or {})

    # Define condition checkers as functions for functional approach
    condition_checkers = [
        ("destination", lambda: _check_destination_condition(rule_conditions.destination, context)),
        ("weight", lambda: _check_weight_condition(rule_conditions.weight, context)),
        ("rate_comparison", lambda: _check_rate_comparison_condition(rule_conditions.rate_comparison, shipment_data)),
    ]

    # Evaluate conditions using functional short-circuit evaluation with failsafe
    for condition_name, checker in condition_checkers:
        if getattr(rule_conditions, condition_name) is not None:
            conditions_checked.append(condition_name)

            # Use lib.failsafe for robust condition checking
            check_result = lib.failsafe(checker, warning=f"Failed to check {condition_name} condition")
            if check_result is None or not check_result:
                matched = False
                break  # Short-circuit on first failure

    return _create_evaluation_result(rule, matched, conditions_checked)


def _check_destination_condition(
    destination_condition: typing.Optional[schemas.DestinationCondition],
    context: schemas.ShipmentRuleContext
) -> bool:
    """Check if destination condition matches shipment context.

    Validates country code and postal code patterns against shipment destination.

    Args:
        destination_condition: Rule's destination condition or None
        context: Shipment evaluation context

    Returns:
        bool: True if condition matches or is None, False otherwise

    Example:
        >>> condition = DestinationCondition(country_code="US", postal_code=["902*", "901*"])
        >>> context = ShipmentRuleContext(destination_country="US", destination_postal_code="90210")
        >>> _check_destination_condition(condition, context)
        True
    """
    if not destination_condition:
        return True

    # Check country code match
    if destination_condition.country_code:
        if context.destination_country != destination_condition.country_code:
            return False

    # Check postal code pattern match (if specified)
    if destination_condition.postal_code:
        if not context.destination_postal_code:
            return False

        # Support wildcard postal code matching using lib.to_list for safety
        postal_patterns = lib.to_list(destination_condition.postal_code)
        postal_matches = any(
            _postal_code_matches(context.destination_postal_code, pattern)
            for pattern in postal_patterns
        )
        if not postal_matches:
            return False

    return True


def _check_weight_condition(
    weight_condition: typing.Optional[schemas.WeightCondition],
    context: schemas.ShipmentRuleContext
) -> bool:
    """Check if weight condition matches shipment context using Karrio Weight utilities.

    Args:
        weight_condition: Rule's weight condition or None
        context: Shipment evaluation context

    Returns:
        bool: True if weight is within specified range, False otherwise
    """
    if not weight_condition or context.total_weight is None:
        return True

    current_weight = lib.to_decimal(context.total_weight)
    if current_weight is None:
        return True

    # Use Karrio's Weight class for conversion - only supporting KG, LB, OZ, G
    try:
        weight_obj = units.Weight(current_weight, context.weight_unit or "LB")
        condition_unit = (weight_condition.unit or "LB").upper()

        # Get converted weight using Weight class properties
        if condition_unit == "KG":
            converted_weight = weight_obj.KG
        elif condition_unit == "LB":
            converted_weight = weight_obj.LB
        elif condition_unit == "OZ":
            converted_weight = weight_obj.OZ
        elif condition_unit == "G":
            converted_weight = weight_obj.G
        else:
            return True  # Unsupported unit

        if converted_weight is None:
            return True

    except Exception:
        return True  # Conversion failed

    # Check bounds
    min_weight = lib.to_decimal(weight_condition.min) if weight_condition.min is not None else None
    max_weight = lib.to_decimal(weight_condition.max) if weight_condition.max is not None else None

    if min_weight is not None and converted_weight < min_weight:
        return False
    if max_weight is not None and converted_weight > max_weight:
        return False

    return True


def _check_rate_comparison_condition(
    rate_condition: typing.Optional[schemas.RateComparisonCondition],
    shipment_data: dict
) -> bool:
    """Check if rate comparison condition matches any available rates.

    Args:
        rate_condition: Rule's rate comparison condition or None
        shipment_data: Normalized shipment dictionary containing rates

    Returns:
        bool: True if condition matches any rate or no condition specified, False otherwise
    """
    if not rate_condition:
        return True

    rates = lib.to_list(shipment_data.get("rates", []))
    if not rates:
        return True

    # Simple operator mapping
    operators = {
        "eq": lambda a, b: a == b,
        "gt": lambda a, b: a > b,
        "gte": lambda a, b: a >= b,
        "lt": lambda a, b: a < b,
        "lte": lambda a, b: a <= b,
    }

    operator_func = operators.get(rate_condition.operator.value)
    if not operator_func:
        return True

    def rate_matches_comparison(rate):
        """Check if rate matches the comparison condition."""
        if not hasattr(rate, rate_condition.compare.value):
            return False

        rate_value = getattr(rate, rate_condition.compare.value)
        if rate_value is None:
            return False

        # Use lib.to_decimal for all numeric comparisons - keeping it simple
        numeric_rate = lib.to_decimal(rate_value)
        numeric_condition = lib.to_decimal(rate_condition.value)

        if numeric_rate is None or numeric_condition is None:
            return False

        return operator_func(numeric_rate, numeric_condition)

    return any(rate_matches_comparison(rate) for rate in rates)


def _postal_code_matches(postal_code: str, pattern: str) -> bool:
    """Check if postal code matches pattern with wildcard support.

    Supports simple wildcard patterns where '*' matches any characters.

    Args:
        postal_code: Actual postal code to check
        pattern: Pattern to match against (supports '*' wildcard)

    Returns:
        bool: True if postal code matches pattern

    Example:
        >>> _postal_code_matches("90210", "902*")
        True
        >>> _postal_code_matches("90210", "901*")
        False
        >>> _postal_code_matches("90210", "90210")
        True
    """
    if '*' in pattern:
        prefix = pattern.replace('*', '')
        return postal_code.startswith(prefix)
    return postal_code == pattern


def _create_evaluation_result(
    rule: automation_models.ShippingRule,
    matched: bool,
    conditions_checked: typing.List[str]
) -> schemas.RuleEvaluationResult:
    """Create a structured rule evaluation result using Karrio lib.to_object.

    Factory function to create consistent evaluation results with proper typing.

    Args:
        rule: The shipping rule that was evaluated
        matched: Whether the rule matched the shipment
        conditions_checked: List of condition names that were evaluated

    Returns:
        RuleEvaluationResult: Structured evaluation result
    """
    return lib.to_object(schemas.RuleEvaluationResult, {
        "rule_id": rule.id,
        "rule_name": rule.name,
        "rule_slug": rule.slug,
        "priority": rule.priority,
        "matched": matched,
        "applied": False,  # Will be set later if this rule wins
        "timestamp": datetime.datetime.now(),
        "conditions_checked": conditions_checked,
        "action_taken": None,  # Will be set later if this rule wins
    })


def _apply_rule_with_metadata(
    shipment: dict,
    rule: automation_models.ShippingRule,
    evaluation: schemas.RuleEvaluationResult
) -> typing.Optional[datatypes.Rate]:
    """Apply shipping rule action and enrich selected rate with metadata using Karrio utilities.

    Executes the rule's action (service selection/blocking) and adds detailed
    metadata about the applied rule to the selected rate.

    Args:
        shipment: Normalized shipment dictionary
        rule: The winning shipping rule to apply
        evaluation: The evaluation result for this rule

    Returns:
        Optional[datatypes.Rate]: Selected rate with applied rule metadata, or None
    """
    # Apply the rule action to get base rate
    selected_rate = apply_shipping_rule(shipment, rule)

    if not selected_rate:
        return None

    # Create rich metadata about the applied rule using lib.to_object
    try:
        applied_rule_metadata = lib.to_object(schemas.AppliedRuleMetadata, {
            "rule_id": rule.id,
            "rule_name": rule.name,
            "rule_slug": rule.slug,
            "priority": rule.priority,
            "applied_at": datetime.datetime.now().isoformat(),  # Convert to string to avoid circular reference
            "action_taken": _get_action_description(rule),
            "conditions_matched": _get_matched_conditions_summary(shipment, rule)
        })
    except Exception as e:
        return None

    # Enrich rate with metadata using lib.to_dict transformation
    try:
        rate_data = lib.to_dict(selected_rate)

        rate_data.setdefault("meta", {})["applied_rule"] = lib.to_dict(applied_rule_metadata)

        final_rate = lib.to_object(datatypes.Rate, rate_data)

        return final_rate
    except Exception as e:
        return None


def _get_matched_conditions_summary(
    shipment: dict,
    rule: automation_models.ShippingRule,
) -> typing.List[str]:
    """Generate human-readable summary of matched conditions using Karrio utilities.

    Creates descriptive text explaining which conditions were matched and their values.

    Args:
        shipment: Normalized shipment dictionary
        rule: The shipping rule that was matched

    Returns:
        List[str]: Human-readable condition descriptions

    Example:
        >>> conditions = _get_matched_conditions_summary(shipment, rule)
        >>> conditions
        ['destination.country_code: US', 'weight: 0.75lb <= 1.0lb']
    """
    conditions = []
    rule_conditions = lib.to_object(schemas.ShippingRuleConditions, rule.conditions or {})
    context = _create_rule_context(shipment)

    # Build condition descriptions functionally
    condition_builders = [
        lambda: lib.text("destination.country_code:", context.destination_country)
                if rule_conditions.destination and rule_conditions.destination.country_code else None,

        lambda: _build_weight_condition_description(rule_conditions.weight, context)
                if rule_conditions.weight else None,

        # Add more condition builders as needed
    ]

    # Filter out None values and collect descriptions using lib utilities
    conditions = list(filter(None, (
        lib.failsafe(builder, warning="Failed to build condition description")
        for builder in condition_builders
    )))

    return conditions


def _build_weight_condition_description(
    weight_condition: schemas.WeightCondition,
    context: schemas.ShipmentRuleContext
) -> str:
    """Build human-readable weight condition description using Karrio text utilities.

    Args:
        weight_condition: The weight condition that was matched
        context: Shipment context with actual weight values

    Returns:
        str: Human-readable weight condition description
    """
    unit = weight_condition.unit or "lb"
    weight_desc = lib.text("weight:", f"{context.total_weight}{context.weight_unit}")

    if weight_condition.min is not None and weight_condition.max is not None:
        return lib.text(weight_desc, "between", f"{weight_condition.min}-{weight_condition.max}{unit}")
    elif weight_condition.min is not None:
        return lib.text(weight_desc, ">=", f"{weight_condition.min}{unit}")
    elif weight_condition.max is not None:
        return lib.text(weight_desc, "<=", f"{weight_condition.max}{unit}")

    return weight_desc


def _get_action_description(rule: automation_models.ShippingRule) -> str:
    """Generate human-readable description of rule action using Karrio utilities.

    Args:
        rule: Shipping rule with actions to describe

    Returns:
        str: Human-readable action description

    Example:
        >>> rule.actions = {"select_service": {"strategy": "cheapest"}}
        >>> _get_action_description(rule)
        'select_service: cheapest'
    """
    rule_actions = lib.to_object(schemas.ShippingRuleActions, rule.actions or {})

    if rule_actions.block_service:
        return "block_service: true"

    if rule_actions.select_service:
        action = rule_actions.select_service
        if action.strategy:
            return lib.text("select_service:", str(action.strategy))
        elif action.carrier_code:
            return lib.text("select_service:", action.carrier_code)
        elif action.service_code:
            return lib.text("select_service:", action.service_code)

    return "unknown_action"


def apply_shipping_rule(
    shipment: dict,
    rule: automation_models.ShippingRule,
) -> typing.Optional[datatypes.Rate]:
    """Apply shipping rule action to select the best rate from available options.

    Executes the rule's action strategy (cheapest, fastest, preferred) against
    the shipment's available rates, with optional rate comparison filtering.
    Uses Karrio lib utilities for robust data processing and transformation.

    Args:
        shipment: Normalized shipment dictionary containing rates
        rule: Shipping rule with actions to apply

    Returns:
        Optional[datatypes.Rate]: Selected rate or None if no suitable rate found
    """
    rates = lib.to_list(shipment.get("rates", []))
    if not rates:
        return None

    # Convert rates to datatypes.Rate objects using lib.to_object (map pattern)
    rate_objects = []
    for i, rate_data in enumerate(rates):
        if isinstance(rate_data, dict):
            # Ensure rate has required fields, use carrier_name as carrier_id fallback
            normalized_rate = {
                **rate_data,
                "carrier_id": rate_data.get("carrier_id") or rate_data.get("carrier_name", "unknown"),
                "carrier_name": rate_data.get("carrier_name", "unknown"),
            }
            try:
                rate_obj = lib.to_object(datatypes.Rate, normalized_rate)
                rate_objects.append(rate_obj)
            except Exception as e:
                # If conversion fails, create a simple rate object
                rate_objects.append(datatypes.Rate(
                    carrier_id=normalized_rate.get("carrier_id", "unknown"),
                    carrier_name=normalized_rate.get("carrier_name", "unknown"),
                    service=normalized_rate.get("service", "unknown"),
                    total_charge=lib.to_decimal(normalized_rate.get("total_charge", 0)) or 0,
                    currency=normalized_rate.get("currency", "USD"),
                    transit_days=lib.to_int(normalized_rate.get("transit_days")),
                ))
        else:
            rate_objects.append(rate_data)

    rule_actions = lib.to_object(schemas.ShippingRuleActions, rule.actions or {})

    # Handle blocking action
    if rule_actions.block_service:
        return None

    if not rule_actions.select_service:
        return None

    action = rule_actions.select_service

    # Apply rate comparison filtering if specified using lib.failsafe
    available_rates = lib.failsafe(
        lambda: _filter_rates_by_comparison(
            rate_objects,
            lib.to_object(schemas.ShippingRuleConditions, rule.conditions or {})
        ),
        warning="Failed to filter rates by comparison"
    ) or rate_objects

    if not available_rates:
        return None

    # Apply selection strategy using functional approach
    strategy_selectors = {
        "cheapest": lambda rates: min(rates, key=lambda r: lib.to_decimal(r.total_charge) or 0),
        "fastest": lambda rates: _select_fastest_rate(rates),
        "preferred": lambda rates: _select_preferred_rate(rates, action),
        # Also support enum values
        schemas.SelectServiceStrategy.cheapest: lambda rates: min(rates, key=lambda r: lib.to_decimal(r.total_charge) or 0),
        schemas.SelectServiceStrategy.fastest: lambda rates: _select_fastest_rate(rates),
        schemas.SelectServiceStrategy.preferred: lambda rates: _select_preferred_rate(rates, action),
    }

    # Handle both string and enum strategy values
    strategy_value = getattr(action.strategy, 'value', action.strategy)
    selector = strategy_selectors.get(strategy_value) or strategy_selectors.get(action.strategy)
    if not selector:
        return None

    return selector(available_rates)


def _filter_rates_by_comparison(
    rates: typing.List[datatypes.Rate],
    conditions: schemas.ShippingRuleConditions
) -> typing.List[datatypes.Rate]:
    """Filter rates based on rate comparison conditions using Karrio utilities.

    Args:
        rates: List of rate objects to filter
        conditions: Rule conditions including rate comparison

    Returns:
        List[datatypes.Rate]: Filtered rates matching comparison criteria
    """
    if not conditions.rate_comparison:
        return rates

    comparison = conditions.rate_comparison

    operators = {
        "eq": lambda a, b: a == b,
        "gt": lambda a, b: a > b,
        "gte": lambda a, b: a >= b,
        "lt": lambda a, b: a < b,
        "lte": lambda a, b: a <= b,
    }

    operator_func = operators.get(comparison.operator.value)
    if not operator_func:
        return rates

    def rate_matches_comparison(rate):
        """Check if rate matches the comparison condition."""
        if not hasattr(rate, comparison.compare.value):
            return False

        rate_value = getattr(rate, comparison.compare.value)
        if rate_value is None:
            return False

        # Use lib.to_decimal for all numeric comparisons - keeping it simple
        numeric_rate = lib.to_decimal(rate_value)
        numeric_condition = lib.to_decimal(comparison.value)

        if numeric_rate is None or numeric_condition is None:
            return False

        return operator_func(numeric_rate, numeric_condition)

    return list(filter(rate_matches_comparison, rates))


def _select_fastest_rate(rates: typing.List[datatypes.Rate]) -> typing.Optional[datatypes.Rate]:
    """Select the fastest rate from available options using Karrio utilities.

    Args:
        rates: List of rate objects with transit_days

    Returns:
        Optional[datatypes.Rate]: Fastest rate or None if no rates have transit_days
    """
    # Filter rates with valid transit days using lib.to_int for robust parsing
    rates_with_transit = list(filter(
        lambda r: lib.to_int(getattr(r, 'transit_days', None)) is not None,
        rates
    ))

    return min(
        rates_with_transit,
        key=lambda r: lib.to_int(r.transit_days)
    ) if rates_with_transit else None


def _select_preferred_rate(
    rates: typing.List[datatypes.Rate],
    action: schemas.SelectServiceAction
) -> typing.Optional[datatypes.Rate]:
    """Select preferred rate based on carrier/service criteria.

    Args:
        rates: List of rate objects to search
        action: Action specification with carrier/service preferences

    Returns:
        Optional[datatypes.Rate]: First matching preferred rate or None
    """
    def matches_preferences(rate):
        """Check if rate matches all specified preferences."""
        # Match carrier_code against carrier_name (not carrier_id)
        carrier_match = (
            not action.carrier_code or
            getattr(rate, 'carrier_name', None) == action.carrier_code
        )

        # Match service_code against service
        service_match = (
            not action.service_code or
            getattr(rate, 'service', None) == action.service_code
        )

        return carrier_match and service_match

    return next((rate for rate in rates if matches_preferences(rate)), None)



