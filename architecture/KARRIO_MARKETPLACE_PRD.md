# Karrio Marketplace PRD: Stripe Connect for Shipping

## Overview

Transform Karrio into a multi-organization shipping marketplace platform that enables platforms to facilitate shipping between organizations and their customers, similar to how Stripe Connect facilitates payments.

## Current Status

### ✅ **Complete: Frontend Connect Experience**
- **Shippers Overview Dashboard**: System-wide health metrics, operational analytics, top organizations
- **Organizations Management**: Enhanced table with summary cards, status badges, CRUD operations  
- **Connected Account Details**: Comprehensive organization dashboard with metrics, alerts, tabs
- **Sidebar Navigation**: Collapsible "Shippers" menu for superusers with multi-org enabled

### 🔧 **Implementation Phases**

## Implementation Status: ✅ Complete Frontend, 🔧 Backend Ready

### ✅ **Completed: Frontend Connect Experience**

The frontend implementation provides a complete Stripe Connect-inspired experience for managing organizations (shippers) on the Karrio platform.

#### **1. Sidebar Navigation Enhancement**
- **Location**: `/packages/ui/components/sidebar.tsx`
- **Features**:
  - New "Shippers" menu visible only to superusers when `MULTI_ORGANIZATIONS` is enabled
  - Collapsible submenu with "Overview" and "Accounts" options
  - Proper permission controls using `user?.is_superuser` and `metadata?.MULTI_ORGANIZATIONS`

#### **2. System Overview Dashboard**
- **Location**: `/packages/core/modules/Shippers/overview.tsx`
- **Features**:
  - System-wide health metrics (active organizations, members, API requests, system health)
  - Operational metrics (shipments, trackers, spending, orders)
  - Interactive charts showing organization status distribution
  - Top organizations ranking by shipments
  - Alert cards for errors and pending orders
  - Time-based filtering (7, 15, 30, 90 days)

#### **3. Organizations Management Table**
- **Location**: `/packages/core/modules/Shippers/index.tsx` 
- **Features**:
  - Enhanced organization table with visual icons and metadata
  - Summary cards showing aggregated metrics across all organizations
  - Status badges and usage metrics per organization
  - Column visibility controls
  - Pagination and search capabilities
  - Create/Edit/Disable/Delete organization workflows

#### **4. Connected Account Detail Page**
- **Location**: `/packages/core/modules/Shippers/detail.tsx`
- **Features**:
  - Comprehensive organization dashboard with Stripe Connect-style design
  - Key metrics cards with trend indicators
  - Alert system for errors and pending orders
  - Tabbed interface (Overview, Shipments, Team, Activity, Settings, Billing)
  - Account balances, capabilities, and quick actions
  - Recent shipments and team member management
  - Mock data structure ready for API integration

## Current Architecture Analysis

### 🔧 **Strong Marketplace Foundation Already Built**

#### **1. Multi-Organization Architecture**
- **PostgreSQL Schema-based Tenancy**: Complete tenant isolation
- **Organization Management**: Sophisticated team and role management via GraphQL
- **Access Control**: Role-based permissions (member, developer, admin)
- **Resource Isolation**: 20+ link models ensuring complete data separation

#### **2. Flexible Pricing Engine**
- **Surcharge System**: Organization-specific markups and pricing rules
- **Carrier Targeting**: Can apply to specific carriers or services
- **Dynamic Application**: Automatic application through post-processing signals
- **Multi-Tenant Aware**: Supports organization-specific pricing

#### **3. Comprehensive Shipping APIs**
- **REST API**: Complete shipping operations (rates, labels, tracking, pickups)
- **GraphQL API**: Organization management, usage analytics, OAuth apps
- **Carrier Network**: Both system-wide and organization-specific carriers
- **Multi-Carrier Support**: Unified API across multiple carriers

#### **4. Usage Analytics Infrastructure**
- **System-Level Tracking**: API requests, shipments, spend, errors
- **Organization-Level Metrics**: Per-org usage statistics and analytics
- **Real-time Data**: Live usage monitoring and health metrics

#### **5. OAuth App Ecosystem**
- **Third-Party Integrations**: Complete OAuth app infrastructure
- **App Store Framework**: Support for marketplace applications
- **API Key Management**: Comprehensive authentication and authorization

## Identified Gaps for Complete Marketplace Experience

### **1. Commission Tracking at Addon/Surcharge Level**
**Current State**: Robust surcharge system exists with carrier/service targeting
**Gap**: No commission attribution or revenue sharing tracking within surcharges

### **2. Advanced Analytics at Carrier Connection Level**
**Current State**: System-wide and organization-level usage analytics exist
**Gap**: No carrier connection-level metrics (API requests, errors, shipments, spends, addons)

### **3. Organization Addon Aggregation**
**Current State**: Individual surcharge tracking exists
**Gap**: No total addon/surcharge revenue tracking per organization

### **4. External Billing Integration Framework**
**Current State**: Payment tracking exists in shipments
**Gap**: No integration framework for external billing systems (Stripe, Lago, etc.)

## Focused Enhancement Recommendations (Leveraging Existing Architecture)

### **Phase 1: Enhance Existing Surcharge/Addon System** (2-3 days)

#### **1. Extend Existing Surcharge Model for Commission Tracking**
```python
# File: /modules/pricing/karrio/server/pricing/models.py
class Surcharge(core.Entity):
    # Existing fields (leverage what's already there):
    # - name, amount, surcharge_type, carriers, carrier_accounts, services
    
    # New commission tracking fields
    commission_enabled = models.BooleanField(
        default=False,
        help_text="Whether this addon generates commission for the platform"
    )
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=4, 
        default=0,
        help_text="Platform commission rate (0.0250 = 2.5%)"
    )
    commission_recipient = models.ForeignKey(
        'orgs.Organization',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='commission_addons',
        help_text="Organization that receives commission (null = platform)"
    )
    billing_metadata = models.JSONField(
        default=dict,
        help_text="External billing system integration data (Stripe, Lago, etc.)"
    )
```

#### **2. Enhanced Usage Analytics System (Augmenting Existing OrgUsageType)**
```python
# File: /ee/insiders/modules/orgs/karrio/server/graph/schemas/orgs/types.py
# Enhance the existing OrgUsageType with marketplace metrics

@strawberry.type
class OrgUsageType:
    # Existing fields remain unchanged
    members: typing.Optional[int] = None
    total_errors: typing.Optional[int] = None
    order_volume: typing.Optional[float] = None
    total_requests: typing.Optional[int] = None
    total_trackers: typing.Optional[int] = None
    total_shipments: typing.Optional[int] = None
    unfulfilled_orders: typing.Optional[int] = None
    total_shipping_spend: typing.Optional[float] = None
    api_errors: typing.Optional[typing.List[utils.UsageStatType]] = None
    api_requests: typing.Optional[typing.List[utils.UsageStatType]] = None
    order_volumes: typing.Optional[typing.List[utils.UsageStatType]] = None
    shipment_count: typing.Optional[typing.List[utils.UsageStatType]] = None
    shipping_spend: typing.Optional[typing.List[utils.UsageStatType]] = None
    tracker_count: typing.Optional[typing.List[utils.UsageStatType]] = None
    
    # NEW marketplace metrics
    total_addon_applications: typing.Optional[int] = None
    total_addon_revenue: typing.Optional[float] = None
    total_commission_earned: typing.Optional[float] = None
    addon_spend: typing.Optional[typing.List[utils.UsageStatType]] = None
    commission_earned: typing.Optional[typing.List[utils.UsageStatType]] = None
    carrier_breakdown: typing.Optional[typing.List['CarrierUsageMetricsType']] = None
    addon_breakdown: typing.Optional[typing.List['AddonUsageMetricsType']] = None
    
    @staticmethod
    def resolve_usage(
        info,
        org: models.Organization,
        filter: utils.UsageFilter = strawberry.UNSET,
    ) -> "OrgUsageType":
        # ... existing implementation ...
        
        # NEW: Add addon and commission tracking
        addon_applications = (
            pricing.Surcharge.applications.filter(
                org=org,
                created_at__gte=_filter["date_after"],
                created_at__lte=_filter["date_before"],
                **_test_filter
            )
            .annotate(date=functions.TruncDay("created_at"))
            .values("date")
            .annotate(
                count=models.Count("id"),
                revenue=models.Sum("amount"),
                commission=models.Sum(
                    models.F("amount") * models.F("commission_rate")
                )
            )
            .order_by("-date")
        )
        
        # Carrier-level breakdown
        carrier_breakdown = (
            org.shipments.filter(
                created_at__gte=_filter["date_after"],
                created_at__lte=_filter["date_before"],
                **_test_filter
            )
            .values("selected_rate_carrier__carrier_id", "selected_rate_carrier__carrier_name")
            .annotate(
                requests=models.Count("logs__id", filter=models.Q(logs__endpoint__contains="/rates")),
                errors=models.Count("logs__id", filter=models.Q(logs__status="failed")),
                shipments=models.Count("id"),
                revenue=models.Sum("selected_rate__total_charge"),
                addon_revenue=models.Sum("addons__amount"),
                commission=models.Sum(
                    models.F("addons__amount") * models.F("addons__commission_rate")
                )
            )
        )
        
        # Addon breakdown
        addon_breakdown = (
            pricing.SurchargeApplication.objects.filter(
                shipment__org=org,
                created_at__gte=_filter["date_after"],
                created_at__lte=_filter["date_before"],
                **_test_filter
            )
            .values("surcharge__id", "surcharge__name")
            .annotate(
                applications=models.Count("id"),
                revenue=models.Sum("amount"),
                commission=models.Sum(
                    models.F("amount") * models.F("surcharge__commission_rate")
                )
            )
        )
        
        # Calculate totals
        total_addon_applications = sum([item["count"] for item in addon_applications], 0)
        total_addon_revenue = lib.to_money(sum([item["revenue"] for item in addon_applications], 0.0))
        total_commission_earned = lib.to_money(sum([item["commission"] for item in addon_applications], 0.0))
        
        return dict(
            # ... existing fields ...
            total_addon_applications=total_addon_applications,
            total_addon_revenue=total_addon_revenue,
            total_commission_earned=total_commission_earned,
            addon_spend=[utils.UsageStatType.parse(item) for item in addon_applications],
            commission_earned=[
                utils.UsageStatType(date=item["date"], count=item["commission"]) 
                for item in addon_applications
            ],
            carrier_breakdown=[
                CarrierUsageMetricsType(**item) for item in carrier_breakdown
            ],
            addon_breakdown=[
                AddonUsageMetricsType(**item) for item in addon_breakdown
            ],
        )

# Helper function to track addon applications
def track_addon_application(surcharge, shipment, amount):
    """Track addon application for usage analytics"""
    from karrio.server.pricing.models import SurchargeApplication
    
    # Create surcharge application record for tracking
    application = SurchargeApplication.objects.create(
        surcharge=surcharge,
        shipment=shipment,
        amount=amount,
        org=shipment.org,
        test_mode=shipment.test_mode,
    )
    
    return application
```

#### **3. Supporting GraphQL Types for Marketplace Metrics**
```python
# File: /ee/insiders/modules/orgs/karrio/server/graph/schemas/orgs/types.py
@strawberry.type
class CarrierUsageMetricsType:
    """Carrier-specific usage metrics"""
    carrier_id: str
    carrier_name: str
    requests: int
    errors: int
    error_rate: float
    shipments: int
    revenue: float
    addon_revenue: float
    commission_earned: float

@strawberry.type
class AddonUsageMetricsType:
    """Addon-specific usage metrics"""
    addon_id: str
    addon_name: str
    applications: int
    revenue: float
    commission: float

# File: /ee/insiders/modules/pricing/karrio/server/pricing/models.py
class SurchargeApplication(core.Entity):
    """Track individual surcharge applications for analytics"""
    id = models.CharField(max_length=50, primary_key=True, default=partial(core.uuid, prefix="suapp_"))
    
    surcharge = models.ForeignKey(
        'Surcharge',
        on_delete=models.CASCADE,
        related_name='applications'
    )
    shipment = models.ForeignKey(
        'manager.Shipment',
        on_delete=models.CASCADE,
        related_name='addon_applications'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    org = models.ForeignKey(
        'orgs.Organization',
        on_delete=models.CASCADE,
        related_name='addon_applications'
    )
    test_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['org', 'created_at']),
            models.Index(fields=['surcharge', 'created_at']),
        ]
```

### **Phase 2: GraphQL Schema Enhancements** (1 day)

#### **1. Enhanced Analytics Queries (Building on Usage System)**
```python
# File: /ee/insiders/modules/admin/karrio/server/admin/schemas/base/__init__.py
@strawberry.type
class Query:
    # ... existing queries ...
    
    @strawberry.field
    def carrier_connection_analytics(
        self,
        info: Info,
        carrier_id: typing.Optional[str] = None,
        organization_id: typing.Optional[str] = None,
        date_range: typing.Optional[inputs.DateRangeInput] = None
    ) -> typing.List[types.CarrierConnectionAnalyticsType]:
        """Get detailed analytics for carrier connections"""
        return types.CarrierConnectionAnalyticsType.resolve_list(
            info, carrier_id=carrier_id, organization_id=organization_id, date_range=date_range
        )
    
    @strawberry.field
    def organization_addon_summary(
        self,
        info: Info,
        organization_id: str
    ) -> types.OrganizationAddonSummaryType:
        """Get addon revenue and commission summary for an organization"""
        return types.OrganizationAddonSummaryType.resolve(info, organization_id=organization_id)
    
    @strawberry.field
    def marketplace_analytics(
        self,
        info: Info,
        date_range: typing.Optional[inputs.DateRangeInput] = None
    ) -> types.MarketplaceAnalyticsType:
        """Get system-wide marketplace analytics"""
        return types.MarketplaceAnalyticsType.resolve(info, date_range=date_range)

# File: /ee/insiders/modules/admin/karrio/server/admin/schemas/base/types.py
@strawberry.type
class CarrierConnectionAnalyticsType:
    """Analytics for a specific carrier connection"""
    carrier_id: str
    carrier_name: str
    organization_id: typing.Optional[str]
    organization_name: typing.Optional[str]
    
    # Metrics from enhanced usage tracking
    api_requests: int
    api_errors: int
    error_rate: float
    shipments_created: int
    shipments_purchased: int
    total_revenue: float
    addon_revenue: float
    commission_earned: float
    
    @staticmethod
    def resolve_list(
        info,
        carrier_id: typing.Optional[str] = None,
        organization_id: typing.Optional[str] = None,
        date_range: typing.Optional[inputs.DateRangeInput] = None
    ) -> typing.List["CarrierConnectionAnalyticsType"]:
        """Aggregate carrier metrics from usage statistics"""
        from karrio.server.admin.models import UsageStatistics
        
        query = UsageStatistics.objects.all()
        if organization_id:
            query = query.filter(organization_id=organization_id)
        if date_range:
            query = query.filter(
                period_start__gte=date_range.date_from,
                period_end__lte=date_range.date_to
            )
        
        # Aggregate by carrier
        carrier_analytics = {}
        for usage in query:
            for cid, metrics in usage.carrier_metrics.items():
                if carrier_id and cid != carrier_id:
                    continue
                    
                if cid not in carrier_analytics:
                    carrier_analytics[cid] = {
                        'carrier_id': cid,
                        'carrier_name': metrics.get('name', cid),
                        'api_requests': 0,
                        'api_errors': 0,
                        'shipments_created': 0,
                        'shipments_purchased': 0,
                        'total_revenue': 0,
                        'addon_revenue': 0,
                        'commission_earned': 0
                    }
                
                # Aggregate metrics
                carrier_analytics[cid]['api_requests'] += metrics.get('requests', 0)
                carrier_analytics[cid]['api_errors'] += metrics.get('errors', 0)
                carrier_analytics[cid]['shipments_created'] += metrics.get('shipments', 0)
                carrier_analytics[cid]['total_revenue'] += metrics.get('revenue', 0)
                carrier_analytics[cid]['addon_revenue'] += metrics.get('addon_revenue', 0)
                carrier_analytics[cid]['commission_earned'] += metrics.get('commission', 0)
        
        # Convert to list and calculate error rate
        results = []
        for analytics in carrier_analytics.values():
            analytics['error_rate'] = (
                analytics['api_errors'] / analytics['api_requests']
                if analytics['api_requests'] > 0 else 0
            )
            results.append(CarrierConnectionAnalyticsType(**analytics))
        
        return results

@strawberry.type
class OrganizationAddonSummaryType:
    """Addon revenue and commission summary for an organization"""
    organization_id: str
    total_addon_revenue: float
    total_commission_paid: float
    active_addons_count: int
    
    @strawberry.field
    def addon_breakdown(self) -> typing.List[AddonUsageMetricsType]:
        """Detailed breakdown by addon"""
        from karrio.server.admin.models import UsageStatistics
        
        # Aggregate addon metrics across all periods
        addon_totals = {}
        usage_stats = UsageStatistics.objects.filter(
            organization_id=self.organization_id
        )
        
        for usage in usage_stats:
            for addon_id, metrics in usage.addon_metrics.items():
                if addon_id not in addon_totals:
                    addon_totals[addon_id] = {
                        'addon_id': addon_id,
                        'addon_name': metrics.get('name', addon_id),
                        'applications': 0,
                        'revenue': 0,
                        'commission': 0
                    }
                
                addon_totals[addon_id]['applications'] += metrics.get('applications', 0)
                addon_totals[addon_id]['revenue'] += metrics.get('revenue', 0)
                addon_totals[addon_id]['commission'] += metrics.get('commission', 0)
        
        return [AddonUsageMetricsType(**data) for data in addon_totals.values()]
    
    @staticmethod
    def resolve(info, organization_id: str) -> "OrganizationAddonSummaryType":
        """Calculate organization addon summary"""
        from karrio.server.admin.models import UsageStatistics
        
        # Aggregate totals
        totals = UsageStatistics.objects.filter(
            organization_id=organization_id
        ).aggregate(
            total_addon_revenue=models.Sum('addon_revenue'),
            total_commission_paid=models.Sum('commission_earned')
        )
        
        # Count active addons
        active_addons = pricing.Surcharge.objects.filter(
            carrier_accounts__org_id=organization_id,
            active=True
        ).distinct().count()
        
        return OrganizationAddonSummaryType(
            organization_id=organization_id,
            total_addon_revenue=totals['total_addon_revenue'] or 0,
            total_commission_paid=totals['total_commission_paid'] or 0,
            active_addons_count=active_addons
        )

@strawberry.type
class MarketplaceAnalyticsType:
    """System-wide marketplace analytics"""
    total_organizations: int
    active_organizations: int
    total_shipments: int
    total_revenue: float
    total_addon_revenue: float
    total_commission_earned: float
    
    @strawberry.field
    def top_organizations(self) -> typing.List[types.TopOrganizationType]:
        """Get top performing organizations"""
        from karrio.server.admin.models import UsageStatistics
        
        # Aggregate by organization
        org_totals = UsageStatistics.objects.values('organization_id').annotate(
            shipment_count=models.Sum('shipments'),
            revenue=models.Sum('spend'),
            commission=models.Sum('commission_earned')
        ).order_by('-revenue')[:10]
        
        results = []
        for org in org_totals:
            org_obj = orgs.Organization.objects.get(id=org['organization_id'])
            results.append(types.TopOrganizationType(
                organization_id=org_obj.id,
                name=org_obj.name,
                shipment_count=org['shipment_count'],
                revenue=org['revenue'],
                commission=org['commission']
            ))
        
        return results
    
    @staticmethod
    def resolve(info, date_range: typing.Optional[inputs.DateRangeInput] = None) -> "MarketplaceAnalyticsType":
        """Calculate marketplace-wide analytics"""
        from karrio.server.admin.models import UsageStatistics
        
        query = UsageStatistics.objects.all()
        if date_range:
            query = query.filter(
                period_start__gte=date_range.date_from,
                period_end__lte=date_range.date_to
            )
        
        # Aggregate totals
        totals = query.aggregate(
            total_shipments=models.Sum('shipments'),
            total_revenue=models.Sum('spend'),
            total_addon_revenue=models.Sum('addon_revenue'),
            total_commission_earned=models.Sum('commission_earned')
        )
        
        # Count organizations
        total_orgs = orgs.Organization.objects.count()
        active_orgs = orgs.Organization.objects.filter(is_active=True).count()
        
        return MarketplaceAnalyticsType(
            total_organizations=total_orgs,
            active_organizations=active_orgs,
            total_shipments=totals['total_shipments'] or 0,
            total_revenue=totals['total_revenue'] or 0,
            total_addon_revenue=totals['total_addon_revenue'] or 0,
            total_commission_earned=totals['total_commission_earned'] or 0
        )
```

#### **2. External Billing Integration Framework**
```python
# File: /ee/insiders/modules/integrations/karrio/server/integrations/schemas.py
@strawberry.type
class BillingIntegrationType:
    """External billing system integration"""
    provider: str  # stripe, lago, custom
    organization_id: str
    external_account_id: str
    integration_status: str
    
    # Sync capabilities
    supports_commission_tracking: bool
    supports_credit_management: bool
    last_sync: typing.Optional[datetime.datetime]

@strawberry.input
class ConfigureBillingIntegrationInput:
    organization_id: str
    provider: str
    external_account_id: str
    api_credentials: typing.Dict[str, str]  # Encrypted storage
    
@strawberry.type
class ConfigureBillingIntegrationMutation:
    integration: typing.Optional[BillingIntegrationType]
    errors: typing.List[str]
```

#### **3. Enhanced Queries (Building on Existing Usage Analytics)**
```python
# Add to existing Query class
def carrier_connection_analytics(
    self,
    carrier_id: typing.Optional[str] = None,
    organization_id: typing.Optional[str] = None,
    date_range: typing.Optional[DateRangeInput] = None
) -> typing.List[CarrierConnectionAnalyticsType]:
    """Get advanced analytics at carrier + connection level"""
    pass

def organization_addon_summary(
    self, 
    organization_id: str
) -> OrganizationAddonSummaryType:
    """Get total addon revenue and commission for an organization"""
    pass

def billing_integrations(
    self,
    organization_id: typing.Optional[str] = None
) -> typing.List[BillingIntegrationType]:
    """Get external billing system integrations"""
    pass
```

### **Phase 3: Integration with Existing Systems** (1 day)

#### **1. Track Addon Applications via Signals**
```python
# File: /modules/pricing/karrio/server/pricing/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from karrio.server.pricing.models import Surcharge, SurchargeApplication

@receiver(post_save, sender=Surcharge)
def track_surcharge_application(sender, instance, created, **kwargs):
    """Track surcharge applications when applied to shipments"""
    if not created and hasattr(instance, '_applied_to_shipment'):
        shipment = instance._applied_to_shipment
        amount = instance._applied_amount
        
        # Create application record for analytics
        SurchargeApplication.objects.create(
            surcharge=instance,
            shipment=shipment,
            amount=amount,
            org=shipment.org,
            test_mode=shipment.test_mode
        )
        
        # Trigger webhook if commission enabled
        if instance.commission_enabled:
            from karrio.server.events.billing import trigger_billing_event, BillingWebhookEvents
            
            commission_amount = amount * instance.commission_rate
            
            trigger_billing_event(
                BillingWebhookEvents.ADDON_APPLIED,
                shipment.org.id,
                {
                    "addon_id": instance.id,
                    "addon_name": instance.name,
                    "addon_amount": float(amount),
                    "commission_amount": float(commission_amount),
                    "shipment_id": shipment.id,
                    "carrier": shipment.selected_rate_carrier_name
                }
            )

# Update existing surcharge application logic
def apply_surcharge_to_shipment(surcharge, shipment, amount):
    """Apply surcharge and track for analytics"""
    # Set tracking attributes
    surcharge._applied_to_shipment = shipment
    surcharge._applied_amount = amount
    surcharge.save()
    
    return amount
```

#### **2. Webhook Events for External Billing Integration**
```python
# File: /ee/insiders/modules/events/karrio/server/events/billing.py
class BillingWebhookEvents:
    """Webhook events for external billing system integration"""
    
    # Commission and addon events
    ADDON_APPLIED = "addon.applied"
    COMMISSION_EARNED = "commission.earned"
    ORGANIZATION_ADDON_TOTAL_UPDATED = "organization.addon_total.updated"
    
    # Usage events for PAUG (Pay As You Go)
    API_REQUEST_MADE = "usage.api_request.made"
    SHIPMENT_CREATED = "usage.shipment.created"
    SHIPMENT_PURCHASED = "usage.shipment.purchased"
    TRACKING_REQUEST_MADE = "usage.tracking.made"
    
    # Subscription-related events
    ORGANIZATION_CREATED = "organization.created"
    ORGANIZATION_ACTIVATED = "organization.activated"
    ORGANIZATION_SUSPENDED = "organization.suspended"
    
    # Credit-related events
    CREDIT_THRESHOLD_REACHED = "credit.threshold.reached"
    CREDIT_EXHAUSTED = "credit.exhausted"
    CREDIT_TOPPED_UP = "credit.topped_up"

def trigger_billing_event(event_type: str, organization_id: str, data: dict):
    """Trigger webhook event for billing systems"""
    event_data = {
        "event": event_type,
        "created": timezone.now().isoformat(),
        "data": {
            "organization_id": organization_id,
            "timestamp": timezone.now().isoformat(),
            **data
        }
    }
    
    # Send to configured webhook endpoints
    send_webhook_event.delay("billing", event_data)
```

#### **3. Enhanced Webhook Event Triggers**
```python
# File: /modules/pricing/karrio/server/pricing/signals.py (enhanced)
def track_addon_commission(sender, instance, **kwargs):
    """Track commission and trigger webhook events for billing integration"""
    if hasattr(instance, 'commission_enabled') and instance.commission_enabled:
        commission_amount = instance.amount * (instance.commission_rate)
        
        # Update analytics (existing code)
        # ... existing analytics code ...
        
        # Trigger webhook events for external billing systems
        from karrio.server.events.billing import trigger_billing_event, BillingWebhookEvents
        
        # Addon applied event (for PAUG billing)
        trigger_billing_event(
            BillingWebhookEvents.ADDON_APPLIED,
            getattr(instance, 'org_id', None),
            {
                "addon_id": instance.id,
                "addon_name": instance.name,
                "addon_amount": instance.amount,
                "addon_type": instance.surcharge_type,
                "carrier": getattr(instance, 'applied_carrier', None),
                "service": getattr(instance, 'applied_service', None),
                "shipment_id": getattr(instance, 'shipment_id', None)
            }
        )
        
        # Commission earned event
        if commission_amount > 0:
            trigger_billing_event(
                BillingWebhookEvents.COMMISSION_EARNED,
                getattr(instance, 'org_id', None),
                {
                    "commission_amount": commission_amount,
                    "commission_rate": instance.commission_rate,
                    "base_amount": instance.amount,
                    "addon_id": instance.id,
                    "addon_name": instance.name
                }
            )
        
        # Organization addon total updated event
        trigger_billing_event(
            BillingWebhookEvents.ORGANIZATION_ADDON_TOTAL_UPDATED,
            getattr(instance, 'org_id', None),
            {
                "total_addon_revenue": summary.total_addon_revenue,
                "total_commission_paid": summary.total_commission_paid,
                "active_addons_count": summary.active_addons_count
            }
        )
```

#### **4. API Endpoints for Billing System Integration**
```python
# File: /ee/insiders/modules/integrations/karrio/server/integrations/views.py
class BillingIntegrationViewSet(viewsets.ViewSet):
    """API endpoints for external billing system integration"""
    
    @action(detail=False, methods=['get'])
    def organization_usage(self, request):
        """Get organization usage data for billing calculations"""
        org_id = request.query_params.get('organization_id')
        date_range = request.query_params.get('date_range', 'current_month')
        
        usage_data = {
            "organization_id": org_id,
            "period": date_range,
            "api_requests": 0,  # from analytics
            "shipments_created": 0,  # from analytics  
            "shipments_purchased": 0,  # from analytics
            "addon_revenue": 0,  # from addon summary
            "commission_earned": 0,  # from addon summary
            "carrier_connections": []  # carrier-level breakdown
        }
        
        return Response(usage_data)
    
    @action(detail=False, methods=['post'])
    def credit_status_update(self, request):
        """Receive credit status updates from external billing systems"""
        org_id = request.data.get('organization_id')
        credit_balance = request.data.get('credit_balance')
        credit_limit = request.data.get('credit_limit')
        status = request.data.get('status')  # active, suspended, etc.
        
        # Update organization status based on credit information
        # Trigger internal events if needed
        
        return Response({"status": "updated"})
    
    @action(detail=False, methods=['get'])
    def billing_events(self, request):
        """Get recent billing events for an organization"""
        org_id = request.query_params.get('organization_id')
        event_types = request.query_params.getlist('event_types')
        
        # Return recent billing events for the organization
        events = get_recent_billing_events(org_id, event_types)
        
        return Response({"events": events})
```

## Key Benefits of This Approach

### **1. Leverages Existing Infrastructure**
- **Builds on UsageType**: Extends the existing usage tracking system
- **No New Models**: Uses enhanced `UsageStatistics` instead of creating new event models
- **Preserves Compatibility**: All existing usage queries continue to work

### **2. Efficient Analytics Strategy**
- **Pre-Aggregated Metrics**: Usage statistics already aggregated by period
- **JSONB Flexibility**: Carrier, service, and addon breakdowns in flexible JSON fields
- **Fast Queries**: Indexed by organization and time period for performance

### **3. Flexible External Billing Integration (Webhook + API Approach)**
- **Webhook Events**: Rich billing events for PAUG, subscription, and credit-based pricing
- **API Endpoints**: Integration APIs for external billing systems to query usage data
- **No Hardcoded Billing**: Generic webhook/API approach works with any billing system
- **Flexible Pricing Models**: Supports PAUG, subscription, credit, and hybrid pricing models

### **4. Preserves Existing Architecture**
- **No Breaking Changes**: All existing surcharge/addon functionality unchanged
- **Additive Features**: New commission and analytics features are purely additive
- **Existing API Compatibility**: All current APIs continue to work unchanged

### **5. Marketplace-Focused Enhancements**
- **Commission Tracking**: Real commission revenue tracking at the addon level
- **Advanced Analytics**: Detailed carrier connection performance metrics  
- **Flexible Billing Integration**: Webhook events + APIs enable any pricing model (PAUG, subscription, credit)
- **Event-Driven Architecture**: Rich billing events for real-time billing system integration

## Current API Capabilities Supporting Marketplace

### **REST API Endpoints (from OpenAPI schema)**
- **Shipments**: `/v1/shipments` - Complete shipment lifecycle
- **Rates**: `/v1/proxy/rates` - Multi-carrier rate shopping
- **Tracking**: `/v1/trackers` - Package tracking across carriers
- **Organizations**: Admin endpoints for organization management
- **Batch Operations**: `/v1/batches` - Bulk processing capabilities
- **Webhooks**: `/v1/webhooks` - Event-driven integrations

### **GraphQL Capabilities**
- **Organization Management**: Create, update, delete organizations
- **User Management**: Roles, permissions, invitations
- **Usage Analytics**: System and organization-level metrics
- **OAuth Apps**: Third-party application integration
- **API Key Management**: Secure access control

## Architecture Strengths for Marketplace Scenarios

### **1. Multi-Tenant Design**
- Complete data isolation using PostgreSQL schemas
- Organization-level access control
- Configurable carrier access per organization
- Role-based team management

### **2. Carrier Network Management**
- System carriers (available to all organizations)
- Organization-specific carriers
- Flexible access control and capability filtering
- Multi-carrier abstraction layer

### **3. Pricing Flexibility**
- Organization-specific surcharge rules
- Percentage and fixed amount markups
- Carrier and service-specific pricing
- Automatic application through middleware

### **4. Extensibility**
- OAuth app framework for third-party integrations
- Webhook system for event notifications
- Metadata support on major entities
- Document management and templating

## Implementation Roadmap

### **🎯 Goals**
Transform Karrio into a comprehensive shipping marketplace platform that enables platforms to facilitate shipping between organizations and their customers, similar to how Stripe Connect facilitates payments.

### **✅ Completed: Frontend Connect Experience**
The complete Stripe Connect-inspired frontend experience is ready for use with existing APIs:
- System overview dashboard with health metrics and analytics
- Organizations management with enhanced table and summary cards  
- Connected account detail pages with comprehensive dashboards
- Proper navigation and access controls

### **📋 Implementation Phases**

#### **Phase 1: Commission Tracking at Addon/Surcharge Level (2-3 days)**
**Objective**: Enable commission revenue tracking within the existing surcharge system

**Tasks**:
1. Extend `Surcharge` model with commission tracking fields:
   - `commission_enabled` (Boolean)
   - `commission_rate` (Decimal - e.g., 0.0250 = 2.5%)
   - `commission_recipient` (ForeignKey to Organization)
   - `billing_metadata` (JSONField for external billing integration)

2. Update existing pricing signals to track commission events
3. Test commission calculation with existing surcharge application logic

**Success Criteria**: Commission revenue tracked at individual addon application level without breaking existing functionality

#### **Phase 2: Event-Driven Analytics System (1-2 days)**  
**Objective**: Create unified analytics system for carrier connection metrics and organization totals

**Tasks**:
1. Implement `AnalyticsEvent` model for flexible event tracking
2. Implement `AnalyticsSnapshot` model for materialized view performance
3. Create `AnalyticsEngine` with smart query strategy (snapshots vs live computation)
4. Add analytics event tracking to shipment and addon lifecycle signals
5. Build GraphQL schema for flexible analytics queries

**Success Criteria**: 
- Carrier connection level metrics (API requests, errors, shipments, revenue)
- Organization addon revenue totals
- Fast dashboard queries via pre-computed snapshots

#### **Phase 3: Webhook + API Billing Integration (2-3 days)**
**Objective**: Enable external billing system integration via events and APIs

**Tasks**:
1. Define comprehensive webhook event types for billing systems:
   - PAUG events (addon.applied, api_request.made, shipment.created)
   - Subscription events (organization.created, organization.activated)
   - Credit events (credit.threshold.reached, credit.exhausted)
2. Implement webhook event triggers in existing signal pipeline
3. Create REST API endpoints for billing system integration:
   - Organization usage data queries
   - Credit status updates from external systems
   - Recent billing events retrieval
4. Test webhook delivery and API integration workflows

**Success Criteria**: External billing systems can integrate via webhooks and APIs to implement any pricing model (PAUG, subscription, credit, hybrid)

### **🎯 Key Benefits**

1. **✅ Commission at Addon Level**: Real commission tracking where it belongs - at the individual surcharge application
2. **✅ Carrier Connection Analytics**: Detailed performance metrics at the carrier + connection level
3. **✅ Organization Addon Totals**: Aggregated addon revenue tracking per organization  
4. **✅ Event-Driven Architecture**: Modern, scalable analytics approach used by top companies
5. **✅ Flexible Billing Integration**: Webhook + API approach works with any external billing system
6. **✅ No Breaking Changes**: All existing functionality preserved and enhanced

### **📊 Success Metrics**

**Technical**:
- Commission tracking accuracy: 100% of addon applications tracked
- Analytics query performance: <200ms for dashboard queries
- Webhook delivery reliability: >99.9% success rate

**Business**:
- Platform commission revenue tracking and reporting
- Organization performance insights for marketplace operators
- Seamless billing system integration for any pricing model

## GraphQL Admin API Analysis

### **✅ Existing Queries/Mutations for Marketplace**

After analyzing the GraphQL admin schemas, here's what we already have:

#### **Organization Management (Admin Orgs Schema)**
- **Queries:**
  - `account(id: String)`: Get single organization (OrganizationAccountType)
  - `accounts(filter: AccountFilter)`: List organizations with filtering
  - `usage(filter: OrgUsageFilter)`: Organization usage statistics (returns AccountUsageType)

- **Mutations:**
  - `createOrganizationAccount`: Create new organization
  - `updateOrganizationAccount`: Update organization details
  - `disableOrganizationAccount`: Disable an organization
  - `deleteOrganizationAccount`: Delete an organization
  - `inviteOrganizationUser`: Invite users to organization

#### **AccountUsageType Fields (from Schema)**
- Basic Metrics:
  - `members`: Int
  - `total_errors`: Int
  - `order_volume`: Float
  - `total_requests`: Int
  - `total_trackers`: Int
  - `total_shipments`: Int
  - `unfulfilled_orders`: Int
  - `total_shipping_spend`: Float
  - `total_addons_charges`: Float (addon revenue)
  - `total_commission`: Float (commission tracking)
- Time Series Data:
  - `api_errors`: [UsageStatType]
  - `api_requests`: [UsageStatType]
  - `order_volumes`: [UsageStatType]
  - `shipment_count`: [UsageStatType]
  - `shipping_spend`: [UsageStatType]
  - `tracker_count`: [UsageStatType]
  - `addons_charges`: [AddonUsageStatType]

#### **Addon/Surcharge System (Admin Base Schema)**
- **Queries:**
  - `addon(id: String)`: Get single addon (AddonType)
  - `addons(filter: AddonFilter)`: List addons with filtering
  
- **Mutations:**
  - `createAddon`: Create new addon
  - `updateAddon`: Update addon
  - `deleteAddon`: Delete addon

- **AddonType Fields (from Schema):**
  - Basic: `id`, `name`, `active`, `amount`, `surcharge_type`
  - Targeting: `services`, `carriers`, `carrier_accounts`
  - Commission tracking fields would need to be added

#### **System-Level Resources**
- **Queries:**
  - `system_carrier_connections`: List system carriers (SystemCarrierConnectionType)
  - `carrier_connections`: List user carrier connections (UserCarrierConnectionType)
  - `carrier_connection(id: String)`: Get single carrier connection
  - `shipments`: List shipments with account context (SystemShipmentType)
  - `shipment(id: String)`: Get single shipment
  - `trackers`: List trackers with account context (SystemTrackerType) 
  - `tracker(id: String)`: Get single tracker
  - `orders`: List orders with account context (SystemOrderType)
  - `order(id: String)`: Get single order

### **🔧 Missing Fields & Queries for Complete Marketplace**

#### **1. Missing Commission Fields in AddonType**
The AddonType in the schema needs these fields added:
```python
# Fields to add to AddonType:
commission_enabled: Boolean
commission_rate: Float
commission_amount: Float  # calculated field
commission_recipient: String  # org ID
billing_metadata: JSON
```

#### **2. Missing Carrier Connection Analytics**
Need to add carrier-level breakdown to AccountUsageType:
```graphql
# Add to AccountUsageType:
carrier_breakdown: [CarrierUsageMetricsType]

# New type needed:
type CarrierUsageMetricsType {
  carrier_id: String!
  carrier_name: String!
  api_requests: Int
  api_errors: Int
  error_rate: Float
  shipments: Int
  revenue: Float
  addon_revenue: Float
  commission_earned: Float
}

# Missing organization addon summary
query organizationAddonSummary($organizationId: String!) {
  organizationAddonSummary(organizationId: $organizationId) {
    totalAddonRevenue
    totalCommissionPaid
    activeAddonsCount
    addonBreakdown {
      addonId
      addonName
      totalApplications
      totalRevenue
      totalCommission
    }
  }
}

# Missing system-wide marketplace analytics
query marketplaceAnalytics($dateRange: DateRangeInput) {
  marketplaceAnalytics(dateRange: $dateRange) {
    totalOrganizations
    activeOrganizations
    totalShipments
    totalRevenue
    totalAddonRevenue
    totalCommissionEarned
    topOrganizations {
      organizationId
      name
      shipmentCount
      revenue
      commission
    }
  }
}
```

#### **2. Billing Integration Queries/Mutations**
```graphql
# Missing billing integration management
query billingIntegrations($organizationId: String) {
  billingIntegrations(organizationId: $organizationId) {
    id
    provider
    organizationId
    externalAccountId
    integrationStatus
    supportsCommissionTracking
    supportsCreditManagement
    lastSync
  }
}

mutation configureBillingIntegration($input: ConfigureBillingIntegrationInput!) {
  configureBillingIntegration(input: $input) {
    integration {
      id
      provider
      integrationStatus
    }
    errors
  }
}

# Missing credit management
query organizationCreditStatus($organizationId: String!) {
  organizationCreditStatus(organizationId: $organizationId) {
    creditBalance
    creditLimit
    creditUsed
    status
    thresholdAlerts {
      threshold
      triggered
      message
    }
  }
}

mutation updateOrganizationCredit($input: UpdateOrganizationCreditInput!) {
  updateOrganizationCredit(input: $input) {
    organization {
      id
      creditBalance
      creditLimit
    }
    errors
  }
}
```

#### **3. Event-Driven Analytics Queries**
```graphql
# Flexible analytics query (as proposed in PRD)
query analytics(
  $organizationId: String
  $carrierId: String
  $eventTypes: [String]
  $dateFrom: DateTime
  $dateTo: DateTime
  $groupBy: [String]
  $timeBucket: String
) {
  analytics(
    organizationId: $organizationId
    carrierId: $carrierId
    eventTypes: $eventTypes
    dateFrom: $dateFrom
    dateTo: $dateTo
    groupBy: $groupBy
    timeBucket: $timeBucket
  ) {
    periodStart
    periodEnd
    dimensions
    apiRequests
    apiErrors
    errorRate
    shipmentsCreated
    shipmentsPurchased
    shipmentsValue
    addonRevenue
    commissionEarned
    carrierBreakdown {
      carrierName
      carrierId
      metrics
    }
    timeSeries {
      timestamp
      value
    }
  }
}
```

#### **4. Commission Management Mutations**
```graphql
# Configure platform commission settings
mutation configurePlatformCommission($input: ConfigurePlatformCommissionInput!) {
  configurePlatformCommission(input: $input) {
    settings {
      defaultCommissionRate
      minimumCommissionAmount
      commissionTiers {
        volumeThreshold
        rate
      }
    }
    errors
  }
}

# Override commission for specific organization
mutation setOrganizationCommission($input: SetOrganizationCommissionInput!) {
  setOrganizationCommission(input: $input) {
    organization {
      id
      customCommissionRate
      commissionOverride
    }
    errors
  }
}
```

### **📋 Implementation Priorities**

Based on the actual schema analysis:

#### **Priority 1: Leverage Existing Infrastructure** ✅
- **AccountUsageType** already has:
  - `total_addons_charges` for addon revenue tracking
  - `total_commission` for commission tracking
  - `addons_charges` time series with AddonUsageStatType
- **OrganizationAccountType** has usage query returning AccountUsageType
- **UserCarrierConnectionType** exists for carrier connection data

#### **Priority 2: Add Missing Fields & Enhance Existing Types** 🔧
1. **Add commission fields to AddonType**: Enable commission tracking at addon level
2. **Add carrier_breakdown to AccountUsageType**: Carrier-level performance metrics
3. **Create new analytics aggregation queries**: Build on existing usage infrastructure

#### **Priority 3: Billing Integration Framework** 🔧
1. **billingIntegrations** query and mutations
2. **organizationCreditStatus** for credit management
3. Webhook event system for external billing

#### **Priority 4: Advanced Features** 📅
1. Flexible **analytics** query for custom reporting
2. Commission management mutations
3. Revenue sharing configuration

## Next Steps

Ready to proceed with **Phase 1: Commission Tracking** implementation. The approach is:
1. Small, focused enhancements building on existing architecture
2. No reinventing of wheels - leveraging proven Karrio systems
3. Clean, step-by-step implementation without overwhelming complexity
4. Event-driven architecture following best practices from leading companies

### **Key Advantage**: 
The GraphQL admin API already has strong foundations:
- AccountUsageType has `total_commission` and `total_addons_charges` fields
- Organization usage tracking with time series data exists
- Account management mutations are complete
- AddonUsageStatType tracks addon applications
- Need to add commission fields to AddonType and carrier breakdown analytics

## Summary of Approach: Augmenting Existing Systems

Instead of creating new models and systems, this approach leverages and extends what Karrio already has:

### **1. Enhanced OrgUsageType**
- **No New Models**: Augments the existing `OrgUsageType` with marketplace metrics
- **Existing Queries Work**: All current usage queries continue functioning
- **New Fields Added**: `total_addon_revenue`, `total_commission_earned`, `carrier_breakdown`, `addon_breakdown`

### **2. SurchargeApplication Tracking**
- **Minimal New Model**: Only adds `SurchargeApplication` to track individual addon applications
- **Links Existing Models**: Connects surcharges to shipments for analytics
- **Enables Aggregation**: Allows querying addon performance by time, carrier, organization

### **3. Commission in Existing Surcharge Model**
- **Fields Already Added**: `commission_enabled`, `commission_rate`, `billing_metadata`
- **No Schema Changes**: Works with existing surcharge application logic
- **Backward Compatible**: Non-commission surcharges work exactly as before

### **4. GraphQL Query Extensions**
- **New Queries Added**: `carrierConnectionAnalytics`, `organizationAddonSummary`, `marketplaceAnalytics`
- **Builds on OrgUsageType**: Extends existing usage patterns
- **Consistent Pattern**: Follows Karrio's existing GraphQL design

This approach ensures:
- **Minimal Disruption**: No breaking changes to existing APIs
- **Fast Implementation**: Builds on proven infrastructure
- **Production Ready**: Uses battle-tested Karrio patterns
- **Scalable Design**: JSONB fields allow flexible metric expansion