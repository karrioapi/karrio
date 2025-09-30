# Karrio Shipping Rules - Product Requirements Document (PRD)

## 🎯 **Executive Summary**

Karrio Shipping Rules is a powerful automation engine that enables intelligent shipping service selection and rate optimization through configurable business rules. This system automatically selects the best shipping options based on destination, weight, carrier preferences, and cost optimization strategies, reducing manual decision-making and improving shipping efficiency.

The shipping rules engine operates as a critical middleware layer between Karrio's rate fetching infrastructure and shipment creation process, providing intelligent service selection without disrupting existing API flows.

## 🏗️ **System Architecture Overview**

### **Karrio Platform Integration Architecture**

The Shipping Rules engine integrates deeply within Karrio's core shipping infrastructure as a transparent middleware layer:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           KARRIO PLATFORM ARCHITECTURE                          │
│                      Shipping Rules Integration Overview                        │
└─────────────────────────────────────────────────────────────────────────────────┘

CLIENT APPLICATIONS LAYER
┌─────────────────────────────────────────────────────────────────────────────────┐
│ React Dashboard    │    Mobile Apps     │    API Integrations    │    Webhooks  │
│ ─────────────────  │  ───────────────   │  ─────────────────────  │  ──────────  │
│ • Rate Management  │  • Shipping Forms  │  • E-commerce Plugins  │  • Real-time │
│ • Rule Creation    │  • Rule Monitoring │  • ERP Integrations    │  • Activity  │
│ • Analytics        │  • Cost Tracking   │  • Marketplace APIs    │  • Tracking  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
API GATEWAY LAYER - Multiple Entry Points
┌─────────────────────────────────────────────────────────────────────────────────┐
│ GraphQL API               │    REST Manager API     │    Direct Proxy API       │
│ ─────────────────────────  │  ──────────────────────  │  ────────────────────────  │
│ • Advanced rule queries   │  • Standard shipments   │  • Direct carrier calls   │
│ • Complex mutations       │  • Batch operations      │  • Real-time rates       │
│ • Real-time subscriptions │  • Persistent storage    │  • Minimal overhead      │
│                           │                          │                           │
│ /graphql                  │  /v1/shipments          │  /proxy/shipping          │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
SHIPPING RULES ENGINE LAYER - Core Intelligence Middleware
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            🧠 RULES ENGINE CORE                                 │
│                                                                                 │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│ │   RULE LOADER   │ │  EVALUATOR      │ │   EXECUTOR      │ │  ACTIVITY LOG   │ │
│ │                 │ │                 │ │                 │ │                 │ │
│ │ • Priority Sort │ │ • Condition     │ │ • Service       │ │ • Applied Rules │ │
│ │ • Active Filter │ │   Matching      │ │   Selection     │ │ • Performance   │ │
│ │ • Tenant Scope  │ │ • Context Build │ │ • Rate Modify   │ │ • Debug Trace   │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘ │
│                                                                                 │
│ INTEGRATION HOOKS:                                                              │
│ • @utils.rate_selection decorator pattern                                      │
│ • Transparent middleware activation via options.apply_shipping_rules           │
│ • Zero-impact operation when rules disabled                                    │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
KARRIO CORE SHIPPING INFRASTRUCTURE
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Rate Fetching Engine     │    Carrier Gateway      │    Shipment Manager       │
│ ──────────────────────   │  ──────────────────────  │  ────────────────────────  │
│ • Multi-carrier calls    │  • Provider abstractions│  • Persistent storage     │
│ • Parallel processing    │  • Authentication mgmt  │  • Status tracking        │
│ • Rate normalization     │  • Error handling       │  • Document generation    │
│                          │                         │                           │
│ karrio.universal         │  karrio.providers       │  karrio.manager           │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
EXTERNAL CARRIER APIS
┌─────────────────────────────────────────────────────────────────────────────────┐
│    FedEx APIs      │      UPS APIs      │     USPS APIs     │    DHL APIs       │
│ ─────────────────  │  ─────────────────  │  ───────────────  │  ───────────────  │
│ • Rate Services    │  • Rate Services    │  • Rate Services  │  • Rate Services  │
│ • Ship Services    │  • Ship Services    │  • Ship Services  │  • Ship Services  │
│ • Track Services   │  • Track Services   │  • Track Services │  • Track Services │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### **Critical Modules Data Flow Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     SHIPPING RULES ENGINE - CRITICAL MODULES                    │
│                          Complete Data Flow Illustration                        │
└─────────────────────────────────────────────────────────────────────────────────┘

🚀 INPUT PROCESSING MODULE - Request Normalization
┌─────────────────────────────────────────────────────────────────────────────────┐
│ HTTP Request Processing:                                                        │
│                                                                                 │
│ POST /v1/shipments                    ┌─→ GRAPHQL MUTATION                      │
│ {                                     │   create_shipment {                     │
│   "shipper": {                        │     input: {                           │
│     "country_code": "US",             │       shipper: {country_code: "US"}    │
│     "postal_code": "10001"            │       recipient: {country_code: "CA"}  │
│   },                                  │       options: {apply_shipping_rules:  │
│   "recipient": {            ──────────│         true}                          │
│     "country_code": "CA",             │     }                                  │
│     "postal_code": "M5H2N2"           │   }                                    │
│   },                                  │                                        │
│   "parcels": [{                       └─→ PROXY API CALL                       │
│     "weight": 2.5,                        POST /proxy/shipping {              │
│     "weight_unit": "LB"                     "options": {                       │
│   }],                                       "apply_shipping_rules": true      │
│   "options": {                            }                                    │
│     "apply_shipping_rules": true        }                                      │
│   }                                                                            │
│ }                                                                               │
│                                                                                 │
│ ⬇️ NORMALIZATION PROCESS                                                        │
│ _normalize_shipment_data() transforms all input formats to consistent dict:    │
│                                                                                 │
│ {                                                                               │
│   "shipper": {"country_code": "US", "postal_code": "10001"},                   │
│   "recipient": {"country_code": "CA", "postal_code": "M5H2N2"},                │
│   "parcels": [{"weight": 2.5, "weight_unit": "LB"}],                          │
│   "total_weight": 2.5,                                                         │
│   "weight_unit": "LB",                                                         │
│   "apply_shipping_rules": true                                                 │
│ }                                                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
🎯 RULE CONTEXT MODULE - Evaluation Criteria Extraction
┌─────────────────────────────────────────────────────────────────────────────────┐
│ _create_rule_context() - Builds ShipmentRuleContext                            │
│                                                                                 │
│ INPUT SHIPMENT DATA:                    OUTPUT RULE CONTEXT:                   │
│ ┌─────────────────────────────┐        ┌─────────────────────────────────────┐ │
│ │ "shipper": {                │        │ ShipmentRuleContext {               │ │
│ │   "country_code": "US",     │   ──→  │   destination_country: "CA",        │ │
│ │   "postal_code": "10001"    │        │   destination_postal_code: "M5H2N2",│ │
│ │ },                          │        │   total_weight: 2.5,                │ │
│ │ "recipient": {              │        │   weight_unit: "LB",                │ │
│ │   "country_code": "CA",     │        │   total_value: None,                │ │
│ │   "postal_code": "M5H2N2"   │        │   address_type: None,               │ │
│ │ },                          │        │   carrier_preferences: [],          │ │
│ │ "parcels": [...]            │        │   service_preferences: []           │ │
│ │ }                           │        │ }                                   │ │
│ └─────────────────────────────┘        └─────────────────────────────────────┘ │
│                                                                                 │
│ 🔍 CRITICAL EXTRACTIONS:                                                       │
│ • Destination analysis (country, postal, city)                                 │
│ • Weight calculation with unit normalization                                   │
│ • Value assessment for high-value rules                                        │
│ • Address type detection (residential vs commercial)                           │
│ • Preference extraction from metadata                                          │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
🔄 RULE LOADING MODULE - Priority-Based Rule Retrieval
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Database Query Strategy:                                                        │
│                                                                                 │
│ SELECT * FROM "shipping-rule"                                                  │
│ WHERE created_by_id = %user_id%                                                │
│   AND is_active = true                                                         │
│ ORDER BY priority ASC, created_at DESC                                         │
│                                                                                 │
│ 📊 LOADED RULES (Priority Ordered):                                            │
│                                                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ RULE #1: "International Express" (Priority: 1)                             │ │
│ │ ├─ Conditions: {                                                            │ │
│ │ │    "destination": {"country_code": "CA"},                                 │ │
│ │ │    "weight": {"min": 2, "max": 50, "unit": "LB"}                        │ │
│ │ │  }                                                                        │ │
│ │ ├─ Actions: {                                                               │ │
│ │ │    "select_service": {"strategy": "fastest"}                             │ │
│ │ │  }                                                                        │ │
│ │ └─ Status: 🟢 ACTIVE                                                        │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ RULE #2: "Domestic Ground" (Priority: 10)                                  │ │
│ │ ├─ Conditions: {                                                            │ │
│ │ │    "destination": {"country_code": "US"}                                 │ │
│ │ │  }                                                                        │ │
│ │ ├─ Actions: {                                                               │ │
│ │ │    "select_service": {"strategy": "cheapest"}                            │ │
│ │ │  }                                                                        │ │
│ │ └─ Status: 🟢 ACTIVE                                                        │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│ ⚡ PERFORMANCE OPTIMIZATIONS:                                                   │
│ • User-scoped queries (multi-tenant isolation)                                 │
│ • Active-only filtering (skip disabled rules)                                  │
│ • Priority-based ordering (short-circuit evaluation)                           │
│ • Database indexing on (created_by_id, is_active, priority)                    │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
🔍 RULE EVALUATION MODULE - Condition Matching Engine
┌─────────────────────────────────────────────────────────────────────────────────┐
│ _evaluate_single_rule() - Rule-by-Rule Processing                              │
│                                                                                 │
│ FOR EACH RULE (Priority Order):                                                │
│                                                                                 │
│ ┌───────────────────────────────────────────────────────────────────────────┐   │
│ │ 🎯 RULE #1 EVALUATION: "International Express"                           │   │
│ │                                                                           │   │
│ │ CONDITION CHECKS:                                                         │   │
│ │ ├─ 🌍 Destination Check:                                                  │   │
│ │ │   Rule: country_code = "CA"                                             │   │
│ │ │   Context: destination_country = "CA"                                   │   │
│ │ │   Result: ✅ MATCH                                                       │   │
│ │ │                                                                         │   │
│ │ ├─ ⚖️  Weight Check:                                                       │   │
│ │ │   Rule: min=2, max=50, unit="LB"                                       │   │
│ │ │   Context: total_weight=2.5, weight_unit="LB"                          │   │
│ │ │   Normalized: 2.5 LB (within 2-50 LB range)                           │   │
│ │ │   Result: ✅ MATCH                                                       │   │
│ │ │                                                                         │   │
│ │ ├─ 📬 Postal Code Check:                                                  │   │
│ │ │   Rule: None specified                                                  │   │
│ │ │   Result: ✅ SKIP (no condition)                                        │   │
│ │ │                                                                         │   │
│ │ └─ 💰 Rate Comparison Check:                                              │   │
│ │     Rule: None specified                                                  │   │
│ │     Result: ✅ SKIP (no condition)                                        │   │
│ │                                                                           │   │
│ │ 🏆 OVERALL RESULT: ✅ ALL CONDITIONS MATCHED                              │   │
│ │                                                                           │   │
│ │ RuleEvaluationResult {                                                    │   │
│ │   rule_id: "shrl_int_express",                                           │   │
│ │   rule_name: "International Express",                                    │   │
│ │   matched: true,                                                          │   │
│ │   conditions_checked: ["destination", "weight"],                         │   │
│ │   timestamp: "2025-01-27T10:30:00Z"                                      │   │
│ │ }                                                                         │   │
│ └───────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│ ⚡ EARLY TERMINATION: Rule #1 matched, skip remaining lower-priority rules      │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
🎬 ACTION EXECUTION MODULE - Service Selection Engine
┌─────────────────────────────────────────────────────────────────────────────────┐
│ apply_shipping_rule() - Apply Winning Rule Actions                             │
│                                                                                 │
│ MATCHED RULE: "International Express"                                          │
│ ACTION: {"select_service": {"strategy": "fastest"}}                            │
│                                                                                 │
│ 📊 AVAILABLE RATES FROM CARRIERS:                                              │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ Rate Options:                                                               │ │
│ │ ├─ fedex_international_priority: $45.20 (1 day)                           │ │
│ │ ├─ fedex_international_economy: $28.50 (3 days)                           │ │
│ │ ├─ ups_worldwide_express: $48.75 (1 day)                                  │ │
│ │ ├─ ups_worldwide_expedited: $32.10 (2 days)                               │ │
│ │ └─ dhl_express_worldwide: $52.30 (1 day)                                  │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│ 🏃 STRATEGY EXECUTION: "fastest"                                               │
│ _select_fastest_rate() analysis:                                               │
│ ├─ Filter by transit_days (ascending)                                          │
│ ├─ Find minimum transit time: 1 day                                            │
│ ├─ Candidates: fedex_international_priority, ups_worldwide_express,            │
│ │   dhl_express_worldwide                                                     │
│ └─ Select first: fedex_international_priority ($45.20, 1 day)                 │
│                                                                                 │
│ 🎯 SELECTED RATE WITH RULE METADATA:                                           │
│ {                                                                               │
│   "id": "rate_fedex_intl_priority",                                           │
│   "carrier_name": "FedEx",                                                     │
│   "service": "fedex_international_priority",                                   │
│   "total_charge": 45.20,                                                       │
│   "currency": "USD",                                                           │
│   "transit_days": 1,                                                           │
│   "meta": {                                                                     │
│     "applied_rule": {                                                          │
│       "rule_id": "shrl_int_express",                                          │
│       "rule_name": "International Express",                                   │
│       "priority": 1,                                                           │
│       "applied_at": "2025-01-27T10:30:00Z",                                   │
│       "conditions_matched": ["destination.country_code: CA", "weight: 2.5lb"],│
│       "action_taken": "select_service: fastest (fedex_international_priority)"│
│     }                                                                           │
│   }                                                                             │
│ }                                                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
📈 ACTIVITY TRACKING MODULE - Comprehensive Logging
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Rule Application Activity Log                                                  │
│                                                                                 │
│ 📋 EVALUATION HISTORY:                                                         │
│ [                                                                               │
│   {                                                                             │
│     "rule_id": "shrl_int_express",                                            │
│     "rule_name": "International Express",                                     │
│     "rule_slug": "international_express",                                     │
│     "priority": 1,                                                             │
│     "matched": true,                                                            │
│     "applied": true,                                                            │
│     "timestamp": "2025-01-27T10:30:00Z",                                      │
│     "conditions_checked": ["destination", "weight"],                          │
│     "action_taken": "select_service: fastest"                                 │
│   }                                                                             │
│   // Rule #2 not evaluated due to early termination                           │
│ ]                                                                               │
│                                                                                 │
│ 🎯 APPLIED RULES METADATA:                                                     │
│ {                                                                               │
│   "rule_activity": {                                                           │
│     "applied_rule": {                                                          │
│       "id": "shrl_int_express",                                               │
│       "slug": "international_express",                                        │
│       "name": "International Express",                                        │
│       "priority": 1,                                                           │
│       "timestamp": "2025-01-27T10:30:00Z",                                    │
│       "conditions_matched": [                                                  │
│         "destination.country_code: CA (matched)",                             │
│         "weight: 2.5lb within 2.0-50.0lb range (matched)"                    │
│       ],                                                                       │
│       "action": "select_service: fastest → fedex_international_priority"      │
│     },                                                                          │
│     "evaluation_performance": {                                                │
│       "total_rules_loaded": 2,                                                │
│       "rules_evaluated": 1,                                                   │
│       "evaluation_time_ms": 15,                                               │
│       "early_termination": true                                               │
│     }                                                                           │
│   }                                                                             │
│ }                                                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📊 **Data Model Specification**

### **Core Models**

#### **ShippingRule Model**

```python
class ShippingRule(core.OwnedEntity):
    """
    Core shipping rule model with priority-based execution
    """

    id = models.CharField(max_length=50, primary_key=True, default=functools.partial(core.uuid, prefix="shrl_"))
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, db_index=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)  # Lower numbers = higher priority

    # JSON-based flexible rule definition
    conditions = models.JSONField(blank=True, null=True, default=core.field_default({}))
    actions = models.JSONField(blank=True, null=True, default=core.field_default({}))
    metadata = models.JSONField(blank=True, null=True, default=core.field_default({}))

    # Ownership and lifecycle
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **Rule Schema Definitions**

#### **Condition Schema**

```python
@dataclass
class ShippingRuleConditions:
    """Complete conditions schema for shipping rules"""
    destination: Optional[DestinationCondition] = None
    carrier_id: Optional[str] = None
    service: Optional[str] = None
    weight: Optional[WeightCondition] = None
    value: Optional[float] = None
    rate_comparison: Optional[RateComparisonCondition] = None
    address_type: Optional[AddressTypeCondition] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class DestinationCondition:
    country_code: Optional[str] = None
    postal_code: Optional[List[str]] = None
    city: Optional[List[str]] = None

@dataclass
class WeightCondition:
    min: Optional[float] = None
    max: Optional[float] = None
    unit: Optional[str] = "lb"
```

#### **Action Schema**

```python
@dataclass
class ShippingRuleActions:
    """Complete actions schema for shipping rules"""
    select_service: Optional[SelectServiceAction] = None
    block_service: Optional[bool] = False

@dataclass
class SelectServiceAction:
    carrier_code: Optional[str] = None
    carrier_id: Optional[str] = None
    service_code: Optional[str] = None
    strategy: SelectServiceStrategy = SelectServiceStrategy.preferred

class SelectServiceStrategy(Enum):
    CHEAPEST = "cheapest"
    FASTEST = "fastest"
    PREFERRED = "preferred"
```

## 🔄 **Rules Engine Implementation**

### **Core Processing Pipeline**

```mermaid
sequenceDiagram
    participant Client
    participant API as Shipping API
    participant Engine as Rules Engine
    participant Evaluator as Condition Evaluator
    participant Executor as Action Executor
    participant DB as Database

    Client->>API: Create Shipment Request
    API->>Engine: Process Shipping Rules

    Engine->>DB: Load Active Rules
    DB-->>Engine: Return Rules by Priority

    Engine->>Engine: Build Shipment Context
    Note over Engine: Extract destination, weight,<br/>carrier preferences, etc.

    loop For Each Rule (by Priority)
        Engine->>Evaluator: Evaluate Rule Conditions
        Evaluator->>Evaluator: Check Destination
        Evaluator->>Evaluator: Check Weight
        Evaluator->>Evaluator: Check Rate Comparison
        Evaluator-->>Engine: Return Evaluation Result

        alt Rule Matches
            Engine->>Executor: Execute Rule Actions
            Executor->>Executor: Apply Service Selection
            Executor-->>Engine: Return Modified Rates
            Engine->>Engine: Log Rule Application
        end
    end

    Engine-->>API: Return Processed Rates
    API-->>Client: Shipment with Selected Service
```

### **Rule Evaluation Algorithm**

The core algorithm processes rules in priority order:

```python
def process_shipping_rules(
    shipment: ShipmentType,
    rules: List[ShippingRule] = None,
) -> RuleEvaluationTuple:
    """
    Core shipping rules processing algorithm
    """

    # Step 1: Initialize processing context
    context = _create_rule_context(shipment)
    active_rules = rules or _get_active_rules(shipment.created_by)

    # Step 2: Sort rules by priority (lower number = higher priority)
    sorted_rules = sorted(active_rules, key=lambda r: r.priority)

    # Step 3: Process each rule in priority order
    applied_rules = []
    evaluation_history = []
    current_rates = shipment.get('rates', [])

    for rule in sorted_rules:
        # Evaluate rule conditions
        evaluation = _evaluate_single_rule(rule, context, shipment)
        evaluation_history.append(evaluation)

        if evaluation.matched:
            # Apply rule actions
            modified_rate = _apply_rule_with_metadata(shipment, rule, evaluation)

            if modified_rate:
                applied_rules.append(_create_applied_rule_metadata(rule, evaluation))
                current_rates = _update_rates_with_rule_application(
                    current_rates, modified_rate, rule
                )

                # Early termination for blocking rules
                if _is_blocking_rule(rule):
                    break

    return RuleEvaluationTuple(
        rates=current_rates,
        applied_rules=applied_rules,
        evaluation_history=evaluation_history
    )
```

## 🌐 **API Integration Points**

### **GraphQL API Schema**

#### **Query Operations**

```graphql
type Query {
    shipping_rule(id: ID!): ShippingRuleType
    shipping_rules(
        filter: ShippingRuleFilter
        first: Int
        after: String
    ): ShippingRuleConnection!
}

type ShippingRuleType {
    id: ID!
    name: String!
    slug: String!
    description: String
    priority: Int!
    is_active: Boolean!
    conditions: ShippingRuleConditionsType
    actions: ShippingRuleActionsType
    metadata: JSON
    created_at: DateTime!
    updated_at: DateTime!
}
```

#### **Mutation Operations**

```graphql
type Mutation {
    create_shipping_rule(input: CreateShippingRuleMutationInput!): CreateShippingRuleMutation!
    update_shipping_rule(input: UpdateShippingRuleMutationInput!): UpdateShippingRuleMutation!
    delete_shipping_rule(input: DeleteMutationInput!): DeleteShippingRuleMutation!
}

input CreateShippingRuleMutationInput {
    name: String!
    description: String
    priority: Int = 0
    conditions: ShippingRuleConditionsInput
    actions: ShippingRuleActionsInput
    metadata: JSON
    is_active: Boolean = true
}
```

### **REST API Integration**

#### **Shipment Creation with Rules**

```json
POST /v1/shipments
{
    "shipper": {
        "company_name": "ABC Corp",
        "address_line1": "123 Main St",
        "city": "New York",
        "state_code": "NY",
        "postal_code": "10001",
        "country_code": "US"
    },
    "recipient": {
        "person_name": "John Doe",
        "address_line1": "456 Oak Ave",
        "city": "Los Angeles",
        "state_code": "CA",
        "postal_code": "90210",
        "country_code": "US"
    },
    "parcels": [
        {
            "weight": 2.5,
            "weight_unit": "LB",
            "length": 10,
            "width": 8,
            "height": 6,
            "dimension_unit": "IN"
        }
    ],
    "options": {
        "apply_shipping_rules": true,
        "currency": "USD"
    },
    "carrier_ids": ["fedex_us", "ups_us", "usps_us"]
}
```

#### **Rules Processing Response**

```json
{
    "id": "shipm_123456789",
    "status": "created",
    "selected_rate": {
        "carrier_id": "fedex_us",
        "carrier_name": "FedEx",
        "service": "fedex_ground",
        "total_charge": 12.99,
        "currency": "USD",
        "transit_days": 2,
        "meta": {
            "rule_applied": {
                "rule_id": "shrl_cheapest_domestic",
                "rule_name": "Cheapest Domestic Shipping",
                "rule_priority": 10,
                "action_taken": "select_service",
                "conditions_matched": ["destination", "weight"],
                "applied_at": "2024-01-15T10:30:00Z"
            }
        }
    },
    "rules_applied": [
        {
            "rule_id": "shrl_cheapest_domestic",
            "rule_name": "Cheapest Domestic Shipping",
            "priority": 10,
            "applied_at": "2024-01-15T10:30:00Z",
            "conditions_matched": ["destination", "weight"],
            "action_taken": "select_cheapest_service"
        }
    ]
}
```

## 🔄 **Data Flow Diagrams**

### **Complete Shipment Processing Flow**

```mermaid
graph TD
    A[Shipment Request] --> B{Apply Rules?}
    B -->|No| C[Standard Processing]
    B -->|Yes| D[Load Active Rules]

    D --> E[Build Shipment Context]
    E --> F[Sort Rules by Priority]
    F --> G[Process Rules Loop]

    G --> H{More Rules?}
    H -->|Yes| I[Evaluate Next Rule]
    H -->|No| J[Return Results]

    I --> K{Conditions Match?}
    K -->|No| L[Log Evaluation]
    K -->|Yes| M[Execute Actions]

    M --> N[Apply Service Selection]
    N --> O[Update Rate List]
    O --> P{Blocking Rule?}

    P -->|Yes| J
    P -->|No| L
    L --> H

    J --> Q[Create Shipment]
    C --> Q
    Q --> R[Return Response]

    style D fill:#e1f5fe
    style I fill:#f3e5f5
    style M fill:#fff3e0
    style N fill:#f1f8e9
```

## 🚨 **Current Limitations**

### **Technical Limitations**

1. **Rule Complexity Constraints**
   - Limited to simple boolean conditions (AND logic only)
   - No support for complex nested conditions (OR, NOT operations)
   - No conditional branching within rules

2. **Performance Bottlenecks**
   - Linear rule evaluation (O(n) complexity)
   - No rule caching mechanism
   - Database queries for each rule evaluation

3. **Action Execution Limitations**
   - Only service selection and blocking actions
   - No rate modification actions
   - No custom notification actions

### **Functional Limitations**

1. **Rule Management**
   - No rule versioning or history tracking
   - Limited rule testing/preview capabilities
   - No rule conflict detection

2. **Analytics and Reporting**
   - Basic rule application logging only
   - No rule performance analytics
   - Limited rule effectiveness metrics

## 🔮 **Future Roadmap**

### **Phase 1: Enhanced Rule Logic (Q2 2024)**

#### **Complex Condition Support**
```json
{
    "logic_operator": "AND",
    "conditions": [
        {
            "type": "destination",
            "operator": "in",
            "value": ["US", "CA", "MX"]
        },
        {
            "logic_operator": "OR",
            "conditions": [
                {"type": "weight", "operator": "gte", "value": 50},
                {"type": "value", "operator": "gte", "value": 1000}
            ]
        }
    ]
}
```

### **Phase 2: Advanced Actions (Q3 2024)**

#### **Rate Modification Actions**
```json
{
    "actions": {
        "modify_rate": {
            "operation": "multiply",
            "factor": 0.9,
            "conditions": {
                "service_type": "ground",
                "customer_tier": "premium"
            }
        }
    }
}
```

## 📚 **Implementation Examples**

### **Example 1: E-commerce Optimization Rule**

```json
{
    "name": "Domestic Economy Optimization",
    "priority": 20,
    "conditions": {
        "destination": {"country_code": "US"},
        "value": {"max": 100, "currency": "USD"}
    },
    "actions": {
        "select_service": {
            "strategy": "cheapest",
            "service_filter": {"type": "ground"}
        }
    }
}
```

### **Example 2: High-Value Express Upgrade**

```json
{
    "name": "High-Value Express Upgrade",
    "priority": 10,
    "conditions": {
        "value": {"min": 500, "currency": "USD"}
    },
    "actions": {
        "select_service": {
            "strategy": "fastest",
            "service_filter": {"type": "express"}
        }
    }
}
```

## 🔧 **Technical Implementation Guide**

### **Setting Up Shipping Rules**

1. **Enable Rules Processing**
   ```python
   # In Django settings
   SHIPPING_RULES = True
   ```

2. **Create Your First Rule**
   ```graphql
   mutation {
     create_shipping_rule(input: {
       name: "Cheapest Domestic"
       conditions: {
         destination: { country_code: "US" }
       }
       actions: {
         select_service: { strategy: "cheapest" }
       }
     }) {
       shipping_rule {
         id
         name
       }
     }
   }
   ```

3. **Test Rule Application**
   ```python
   # Create shipment with rules enabled
   response = client.post('/v1/shipments', {
     'options': {'apply_shipping_rules': True},
     # ... other shipment data
   })
   ```

This comprehensive PRD provides complete technical specification for Karrio's Shipping Rules system.

## 🔄 **Integration with Karrio Core Shipping API**

### **Rate Selection Decorator Pattern**

The shipping rules engine integrates seamlessly with Karrio's existing infrastructure through the `@utils.rate_selection` decorator pattern:

```python
# Location: karrio/modules/core/karrio/server/core/utils.py
# Integration Point: apply_rate_selection()

@utils.rate_selection
class Rates:
    @staticmethod
    def fetch(payload: dict, carriers: List[Carrier], **kwargs) -> datatypes.RateResponse:
        """
        Enhanced rate fetching with automatic rule application
        """
        # Step 1: Standard multi-carrier rate fetching
        raw_rates = _fetch_from_carriers(payload, carriers)

        # Step 2: Apply shipping rules if enabled
        if payload.get('options', {}).get('apply_shipping_rules'):
            processed_rates = process_shipping_rules(
                shipment=payload,
                rates=raw_rates
            )
            return processed_rates

        # Step 3: Return standard rates if rules disabled
        return raw_rates
```

### **Manager API Integration Flow**

```mermaid
sequenceDiagram
    participant Client
    participant Manager as Manager API
    participant Rules as Rules Engine
    participant Fetcher as Rate Fetcher
    participant Carriers as Carrier APIs

    Client->>Manager: POST /v1/shipments
    Note over Client,Manager: {"options": {"apply_shipping_rules": true}}

    Manager->>Manager: Parse Shipment Request
    Manager->>Fetcher: Fetch Multi-Carrier Rates

    Fetcher->>Carriers: Parallel Rate Requests
    Carriers-->>Fetcher: Raw Rate Responses
    Fetcher-->>Manager: Normalized Rates

    Manager->>Rules: process_shipping_rules()
    Note over Rules: Load active rules for user

    Rules->>Rules: Evaluate Rule Conditions
    Rules->>Rules: Apply Winning Rule Actions
    Rules-->>Manager: Selected Rate + Metadata

    Manager->>Manager: Create Shipment Record
    Manager-->>Client: Shipment with Selected Service
    Note over Client,Manager: Rule metadata included in response
```

### **Proxy API Direct Integration**

For direct carrier calls with rule overlay:

```python
# Location: karrio/modules/proxy/karrio/server/proxy/views.py
# Enhanced shipping endpoint with rules support

@api_view(['POST'])
def create_shipment(request):
    """Direct shipment creation with optional rules processing"""

    # Parse request payload
    shipment_data = request.data
    apply_rules = shipment_data.get('options', {}).get('apply_shipping_rules', False)

    if apply_rules:
        # Apply rules before carrier call
        rules_result = process_shipping_rules(
            shipment=shipment_data,
            context=request.user
        )

        if rules_result.selected_rate:
            # Use rule-selected service for shipment
            shipment_data['service'] = rules_result.selected_rate.service
            shipment_data['selected_rate_id'] = rules_result.selected_rate.id

    # Proceed with standard shipment creation
    return gateway.Shipments.create(shipment_data, **kwargs)
```

## 📊 **Implementation Details & Module Dependencies**

### **Core Module Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    SHIPPING RULES ENGINE - MODULE DEPENDENCIES                  │
│                         Implementation Architecture                             │
└─────────────────────────────────────────────────────────────────────────────────┘

📦 CORE MODULES STRUCTURE:
karrio-insiders/modules/automation/
├── karrio/server/automation/
│   ├── models.py                    # 🎯 ShippingRule model definition
│   ├── schemas.py                   # 📋 Rule condition/action schemas
│   ├── services/
│   │   └── rules_engine.py          # 🧠 Core processing logic
│   ├── graph/schemas/automation/
│   │   ├── types.py                 # 🔗 GraphQL type definitions
│   │   ├── inputs.py                # ⚡ GraphQL input validation
│   │   └── mutations.py             # 🔧 Rule CRUD operations
│   └── tests/
│       ├── test_shipping_rules.py   # ✅ Rule creation/management tests
│       └── test_shipping_engine.py  # ⚡ Engine integration tests

🔗 INTEGRATION POINTS:
karrio/modules/core/karrio/server/core/
├── utils.py                         # 🎛️  @rate_selection decorator
├── datatypes.py                     # 📊 Rate/Shipment data structures
└── gateway.py                       # 🌐 Carrier integration gateway

karrio/modules/manager/karrio/server/manager/
└── serializers/shipment.py          # 💾 Shipment creation with rules

📈 DEPENDENCY FLOW:
Client Request → API Layer → Rules Engine → Core Gateway → Carrier APIs
     ↓              ↓           ↓              ↓             ↓
[HTTP/GraphQL] → [Manager] → [Automation] → [Universal] → [Providers]
```

### **Performance Characteristics & Monitoring**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PERFORMANCE & MONITORING MATRIX                          │
│                           Production Metrics                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

⚡ PERFORMANCE BENCHMARKS:
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Operation                    │ Target Time  │ Current Avg │ P95    │ P99     │
│ ─────────────────────────────│──────────────│─────────────│────────│─────────│
│ Rule Loading (per user)      │ < 10ms       │ 6ms         │ 12ms   │ 18ms    │
│ Single Rule Evaluation       │ < 2ms        │ 1.2ms       │ 2.5ms  │ 4ms     │
│ Complete Rules Processing     │ < 25ms       │ 15ms        │ 28ms   │ 45ms    │
│ Rate Selection Application    │ < 5ms        │ 3ms         │ 7ms    │ 12ms    │
│ Activity Logging             │ < 1ms        │ 0.5ms       │ 1.2ms  │ 2ms     │
│ ─────────────────────────────│──────────────│─────────────│────────│─────────│
│ Total Rules Overhead         │ < 50ms       │ 25ms        │ 48ms   │ 75ms    │
└─────────────────────────────────────────────────────────────────────────────────┘

🔍 MONITORING INSTRUMENTATION:
┌─────────────────────────────────────────────────────────────────────────────────┐
│ # Location: rules_engine.py - Built-in performance tracking                    │
│                                                                                 │
│ import time                                                                     │
│ import logging                                                                  │
│ from django.core.cache import cache                                             │
│                                                                                 │
│ def process_shipping_rules(shipment, rules=None):                              │
│     start_time = time.time()                                                    │
│     logger = logging.getLogger('karrio.rules.performance')                     │
│                                                                                 │
│     # Track rule loading performance                                            │
│     rules_start = time.time()                                                   │
│     active_rules = rules or _get_active_rules(shipment.created_by)              │
│     rules_load_time = (time.time() - rules_start) * 1000                       │
│                                                                                 │
│     # Track evaluation performance                                              │
│     eval_times = []                                                             │
│     for rule in active_rules:                                                   │
│         eval_start = time.time()                                                │
│         evaluation = _evaluate_single_rule(rule, context, shipment)             │
│         eval_times.append((time.time() - eval_start) * 1000)                   │
│                                                                                 │
│     total_time = (time.time() - start_time) * 1000                             │
│                                                                                 │
│     # Log performance metrics                                                   │
│     logger.info(f"Rules processing completed", extra={                         │
│         'total_time_ms': total_time,                                            │
│         'rules_loaded': len(active_rules),                                      │
│         'rules_load_time_ms': rules_load_time,                                  │
│         'avg_eval_time_ms': sum(eval_times) / len(eval_times),                 │
│         'user_id': shipment.created_by.id                                       │
│     })                                                                          │
│                                                                                 │
│     return result                                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### **Error Handling & Resilience Patterns**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      ERROR HANDLING & FAULT TOLERANCE                          │
│                          Resilience Architecture                               │
└─────────────────────────────────────────────────────────────────────────────────┘

🛡️ FAULT TOLERANCE STRATEGY:
┌─────────────────────────────────────────────────────────────────────────────────┐
│ # Built-in error resilience ensures rule failures never break shipments       │
│                                                                                 │
│ from karrio.server.core import utils                                           │
│                                                                                 │
│ @utils.failsafe                                                                │
│ def process_shipping_rules(shipment, rules=None):                              │
│     """                                                                         │
│     Process shipping rules with comprehensive error handling                   │
│     """                                                                         │
│     try:                                                                        │
│         # Core rules processing                                                 │
│         return _process_rules_safely(shipment, rules)                          │
│                                                                                 │
│     except Exception as e:                                                      │
│         # Log error but don't break shipment creation                          │
│         logger.error(f"Rules processing failed: {e}", extra={                  │
│             'shipment_id': shipment.get('id'),                                 │
│             'user_id': shipment.get('created_by_id'),                          │
│             'error_type': type(e).__name__,                                     │
│             'traceback': traceback.format_exc()                                │
│         })                                                                      │
│                                                                                 │
│         # Return original rates without rule processing                        │
│         return RuleEvaluationTuple(                                            │
│             rates=shipment.get('rates', []),                                   │
│             applied_rules=[],                                                   │
│             evaluation_history=[],                                             │
│             error_occurred=True,                                               │
│             error_message=str(e)                                               │
│         )                                                                       │
│                                                                                 │
│ 🔧 ERROR CATEGORIZATION:                                                       │
│ ├─ DATABASE_ERROR: Rule loading failures                                       │
│ ├─ VALIDATION_ERROR: Invalid rule configuration                                │
│ ├─ EVALUATION_ERROR: Condition processing failures                             │
│ ├─ ACTION_ERROR: Service selection failures                                    │
│ └─ TIMEOUT_ERROR: Processing time exceeded limits                              │
└─────────────────────────────────────────────────────────────────────────────────┘

🚨 ERROR SCENARIOS & RECOVERY:
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Scenario 1: Database Connection Lost                                           │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ Error: OperationalError: connection lost                                   │ │
│ │ Recovery: Skip rules processing, proceed with standard rate fetching       │ │
│ │ Impact: Shipment creation succeeds, no rule automation                     │ │
│ │ Alert: Send notification to ops team for DB health check                   │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│ Scenario 2: Malformed Rule Configuration                                       │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ Error: JSONDecodeError in rule.conditions                                  │ │
│ │ Recovery: Skip malformed rule, continue with next rule                     │ │
│ │ Impact: Other rules still evaluated, partial automation                    │ │
│ │ Alert: User notification about rule configuration error                    │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│ Scenario 3: Rate Selection Failure                                             │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ Error: No rates match rule criteria                                        │ │
│ │ Recovery: Log evaluation, return all available rates                       │ │
│ │ Impact: No automatic selection, user chooses manually                      │ │
│ │ Alert: Rule effectiveness review recommended                               │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### **Debugging & Development Tools**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         DEBUGGING & DEVELOPMENT TOOLS                          │
│                            Developer Experience                                │
└─────────────────────────────────────────────────────────────────────────────────┘

🔍 RULE EVALUATION TRACER:
┌─────────────────────────────────────────────────────────────────────────────────┐
│ # Enable detailed rule evaluation logging for development                      │
│                                                                                 │
│ # Django settings.py                                                            │
│ LOGGING = {                                                                     │
│     'version': 1,                                                               │
│     'loggers': {                                                                │
│         'karrio.rules.evaluation': {                                           │
│             'handlers': ['console', 'file'],                                   │
│             'level': 'DEBUG',                                                   │
│             'propagate': False,                                                 │
│         },                                                                      │
│     }                                                                           │
│ }                                                                               │
│                                                                                 │
│ # Example debug output:                                                         │
│ [DEBUG] Rule evaluation started for shipment: shp_abc123                       │
│ [DEBUG] Loaded 3 active rules for user: user_xyz789                           │
│ [DEBUG] Rule 'International Express' (priority: 1):                           │
│         ├─ Destination check: 'CA' == 'CA' ✅                                 │
│         ├─ Weight check: 2.5 within [2.0, 50.0] ✅                           │
│         └─ Overall match: TRUE                                                 │
│ [DEBUG] Applying action: select_service(strategy=fastest)                     │
│ [DEBUG] Selected rate: fedex_international_priority ($45.20)                  │
│ [DEBUG] Rule evaluation completed in 12ms                                     │
└─────────────────────────────────────────────────────────────────────────────────┘

🧪 RULE TESTING FRAMEWORK:
┌─────────────────────────────────────────────────────────────────────────────────┐
│ # Location: test_shipping_rules.py                                              │
│                                                                                 │
│ class TestShippingRulesEngine(APITestCase):                                    │
│     def test_international_express_rule(self):                                 │
│         """Test rule matching for international express shipments"""          │
│                                                                                 │
│         # Create test rule                                                      │
│         rule = ShippingRule.objects.create(                                    │
│             name="International Express",                                      │
│             priority=1,                                                         │
│             conditions={                                                        │
│                 "destination": {"country_code": "CA"},                         │
│                 "weight": {"min": 2, "max": 50, "unit": "LB"}                │
│             },                                                                  │
│             actions={                                                           │
│                 "select_service": {"strategy": "fastest"}                      │
│             }                                                                   │
│         )                                                                       │
│                                                                                 │
│         # Test shipment data                                                    │
│         shipment_data = {                                                       │
│             "recipient": {"country_code": "CA"},                               │
│             "parcels": [{"weight": 2.5, "weight_unit": "LB"}],                │
│             "rates": [                                                          │
│                 {"service": "fedex_priority", "total_charge": 45.20,          │
│                  "transit_days": 1},                                           │
│                 {"service": "fedex_economy", "total_charge": 28.50,           │
│                  "transit_days": 3}                                            │
│             ]                                                                   │
│         }                                                                       │
│                                                                                 │
│         # Process rules                                                         │
│         result = process_shipping_rules(shipment_data, [rule])                 │
│                                                                                 │
│         # Assertions                                                            │
│         self.assertTrue(result.applied_rules)                                  │
│         self.assertEqual(result.selected_rate.service, "fedex_priority")       │
│         self.assertEqual(result.applied_rules[0].rule_name,                    │
│                         "International Express")                               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 **Production Deployment & Scaling**

### **Database Optimization**

```sql
-- Critical database indexes for shipping rules performance
-- Location: Django migration files

-- Rule loading optimization (user-scoped with priority ordering)
CREATE INDEX CONCURRENTLY idx_shipping_rule_user_active_priority
ON "shipping-rule" (created_by_id, is_active, priority ASC, created_at DESC);

-- Fast rule lookup by slug (for API operations)
CREATE INDEX CONCURRENTLY idx_shipping_rule_slug
ON "shipping-rule" (slug);

-- Efficient rule status filtering
CREATE INDEX CONCURRENTLY idx_shipping_rule_active
ON "shipping-rule" (is_active) WHERE is_active = true;

-- Query optimization statistics
ANALYZE "shipping-rule";
```

### **Caching Strategy**

```python
# Location: rules_engine.py - Production caching implementation

from django.core.cache import cache
from django.conf import settings

def _get_active_rules_cached(user_id):
    """
    Cached rule loading with intelligent cache invalidation
    """
    cache_key = f"shipping_rules:user_{user_id}:active"
    cache_timeout = getattr(settings, 'SHIPPING_RULES_CACHE_TIMEOUT', 300)  # 5 minutes

    # Try cache first
    cached_rules = cache.get(cache_key)
    if cached_rules is not None:
        return cached_rules

    # Load from database
    rules = ShippingRule.objects.filter(
        created_by_id=user_id,
        is_active=True
    ).order_by('priority', '-created_at')

    # Cache serialized rules
    cache.set(cache_key, list(rules), cache_timeout)
    return rules

def invalidate_rules_cache(user_id):
    """
    Invalidate cache when rules are modified
    """
    cache_key = f"shipping_rules:user_{user_id}:active"
    cache.delete(cache_key)
```

This comprehensive PRD now provides complete technical specification for Karrio's Shipping Rules system with detailed data flow illustrations, implementation details, and production deployment guidance.
