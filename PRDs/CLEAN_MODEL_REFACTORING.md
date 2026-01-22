# Product Requirements Document: Clean Model Refactoring

**Project**: Migration to Clean JSON-Native Models
**Version**: 1.0
**Date**: 2026-01-16
**Status**: Planning
**Owner**: Engineering Team

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Success Criteria](#3-goals--success-criteria)
4. [Proposed Architecture](#4-proposed-architecture)
5. [Data Models](#5-data-models)
6. [Migration Strategy](#6-migration-strategy)
7. [Serializer Design (Option C)](#7-serializer-design-option-c)
8. [Implementation Plan](#8-implementation-plan)
9. [Testing Strategy](#9-testing-strategy)
10. [Risk Assessment](#10-risk-assessment)
11. [Appendix](#11-appendix)

---

## 1. Executive Summary

### 1.1 Overview

This PRD outlines a **complete model replacement approach** for refactoring Shipment, Order, Pickup, and Manifest models from FK/M2M-based relations to clean JSON-native fields. Instead of adding `_data` suffix fields alongside existing FKs, we create **entirely new models** with:

- **Direct JSON fields** (e.g., `shipper` as `JSONField`, not `shipper_data`)
- **Clean table naming** (e.g., `shipments` instead of `shipment`)
- **Seamless data migration** with zero data loss

### 1.2 Key Design Principles

| Principle | Description |
|-----------|-------------|
| **Clean Field Names** | `shipper = JSONField()` not `shipper_data = JSONField()` |
| **Direct JSON Access** | No `_info` properties or proxy classes needed |
| **Seamless Migration** | Data migrated in-place with no API disruption |
| **Option C Serializers** | Nested serializers that handle dict data directly |
| **Template ID Reference** | `id` field in JSON can reference a template for resolution |

### 1.3 Models to Refactor

| Current Model | New Model | DB Table |
|---------------|-----------|----------|
| `Shipment` | `Shipment` (rebuilt) | `shipments` |
| `Order` | `Order` (rebuilt) | `orders` |
| `Pickup` | `Pickup` (rebuilt) | `pickups` |
| `Manifest` | `Manifest` (rebuilt) | `manifests` |

### 1.4 Benefits

- **Simplicity**: Clean model with `shipper`, `recipient`, `parcels` as direct JSON fields
- **No suffix confusion**: No `_data` or `_info` naming complexity
- **Better developer experience**: Fields work as expected (`instance.shipper` returns dict)
- **No proxy classes**: JSONField returns dict directly, serializers handle conversion
- **Clean table names**: `shipments`, `orders`, `pickups`, `manifests`

---

## 2. Problem Statement

### 2.1 Current Architecture Issues

The current implementation (Phase 3 of ADDRESS_PARCEL_PRODUCT_REFACTORING) has introduced:

```
Current Shipment Model:
├── shipper (OneToOneField)           # Legacy FK - nullable
├── shipper_data (JSONField)          # New JSON field
├── shipper_info (property)           # Accessor that returns JSONDataProxy
├── recipient (OneToOneField)         # Legacy FK - nullable
├── recipient_data (JSONField)        # New JSON field
├── recipient_info (property)         # Accessor that returns JSONDataProxy
└── ... similar pattern for all fields
```

**Problems:**
1. **Confusing naming**: `shipper`, `shipper_data`, `shipper_info` - three ways to access same data
2. **Proxy complexity**: JSONDataProxy/JSONArrayProxy classes add abstraction layer
3. **Technical debt**: `_data` suffix fields meant to be temporary but become permanent
4. **Serializer complexity**: `source="shipper_info"` redirections hard to follow
5. **Table naming**: `shipment` instead of `shipments` (inconsistent with conventions)

### 2.2 Desired End State

```
New Shipment Model:
├── shipper (JSONField)               # Direct JSON - returns dict
├── recipient (JSONField)             # Direct JSON - returns dict
├── parcels (JSONField)               # Direct JSON - returns list[dict]
├── customs (JSONField)               # Direct JSON - returns dict
└── ... clean, direct fields
```

---

## 3. Goals & Success Criteria

### 3.1 Goals

1. **Clean model structure** with direct JSON fields (no suffixes)
2. **Zero data loss** during migration
3. **API backward compatibility** - responses remain identical
4. **Improved developer experience** - simpler model access patterns
5. **Clean database schema** - proper table naming conventions

### 3.2 Success Criteria

| Criteria | Metric |
|----------|--------|
| All tests pass | 100% test pass rate |
| No data loss | All records migrated with full data integrity |
| API compatibility | Response JSON structure unchanged |
| Performance | Query performance maintained or improved |
| Code clarity | No proxy classes, no `_info` properties |

---

## 4. Proposed Architecture

### 4.1 Architecture Comparison

**Before (Current Complex State):**
```python
class Shipment(OwnedEntity):
    # FK (legacy)
    shipper = models.OneToOneField("Address", null=True, ...)
    # JSON (new)
    shipper_data = models.JSONField(null=True, ...)

    @property
    def shipper_info(self):
        if self.shipper_data:
            return JSONDataProxy(self.shipper_data)
        return self.shipper

# Serializer uses:
shipper = AddressSerializer(source="shipper_info", ...)
```

**After (Clean State):**
```python
class Shipment(OwnedEntity):
    shipper = models.JSONField(null=True, ...)  # Direct, clean

# Serializer uses:
shipper = AddressSerializer()  # Works with dict directly
```

### 4.2 Model Field Mapping

#### Shipment Fields

| Current FK/M2M | New JSON Field | Type |
|----------------|----------------|------|
| `shipper` (OneToOne) | `shipper` | `JSONField` |
| `recipient` (OneToOne) | `recipient` | `JSONField` |
| `return_address` (OneToOne) | `return_address` | `JSONField` |
| `billing_address` (OneToOne) | `billing_address` | `JSONField` |
| `parcels` (M2M) | `parcels` | `JSONField` (list) |
| `customs` (OneToOne) | `customs` | `JSONField` |

#### Order Fields

| Current FK/M2M | New JSON Field | Type |
|----------------|----------------|------|
| `shipping_to` (OneToOne) | `shipping_to` | `JSONField` |
| `shipping_from` (OneToOne) | `shipping_from` | `JSONField` |
| `billing_address` (OneToOne) | `billing_address` | `JSONField` |
| `line_items` (M2M) | `line_items` | `JSONField` (list) |

#### Pickup Fields

| Current FK | New JSON Field | Type |
|------------|----------------|------|
| `address` (FK) | `address` | `JSONField` |

#### Manifest Fields

| Current FK | New JSON Field | Type |
|------------|----------------|------|
| `address` (OneToOne) | `address` | `JSONField` |

---

## 5. Data Models

### 5.1 New Shipment Model

```python
@core.register_model
class Shipment(core.OwnedEntity):
    """Shipment model with embedded JSON data for addresses, parcels, and customs."""

    DIRECT_PROPS = [
        "options", "services", "status", "meta", "label_type",
        "tracking_number", "tracking_url", "shipment_identifier",
        "test_mode", "messages", "rates", "payment", "metadata",
        "created_by", "reference",
    ]

    class Meta:
        db_table = "shipments"  # Clean plural table name
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="shp_"),
        editable=False,
    )

    # Status and tracking
    status = models.CharField(
        max_length=50,
        choices=serializers.SHIPMENT_STATUS,
        default=serializers.SHIPMENT_STATUS[0][0],
        db_index=True,
    )
    tracking_number = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    shipment_identifier = models.CharField(max_length=100, null=True, blank=True)
    tracking_url = models.TextField(null=True, blank=True)
    label_type = models.CharField(max_length=25, null=True, blank=True)
    test_mode = models.BooleanField(null=False)
    reference = models.CharField(max_length=100, null=True, blank=True)

    # Document storage
    label = models.TextField(null=True, blank=True)
    invoice = models.TextField(null=True, blank=True)

    # ─────────────────────────────────────────────────────────────────
    # EMBEDDED JSON FIELDS (direct, no _data suffix)
    # ─────────────────────────────────────────────────────────────────

    shipper = models.JSONField(
        blank=True,
        null=True,
        help_text="Shipper address (embedded JSON)",
    )
    recipient = models.JSONField(
        blank=True,
        null=True,
        help_text="Recipient address (embedded JSON)",
    )
    return_address = models.JSONField(
        blank=True,
        null=True,
        help_text="Return address (embedded JSON)",
    )
    billing_address = models.JSONField(
        blank=True,
        null=True,
        help_text="Billing address (embedded JSON)",
    )
    parcels = models.JSONField(
        blank=True,
        null=True,
        default=list,
        help_text="Parcels array with nested items (embedded JSON)",
    )
    customs = models.JSONField(
        blank=True,
        null=True,
        help_text="Customs information (embedded JSON)",
    )

    # ─────────────────────────────────────────────────────────────────
    # OPERATIONAL JSON FIELDS (existing)
    # ─────────────────────────────────────────────────────────────────

    selected_rate = models.JSONField(blank=True, null=True)
    rates = models.JSONField(blank=True, null=True, default=list)
    payment = models.JSONField(blank=True, null=True)
    options = models.JSONField(blank=True, null=True, default=dict)
    services = models.JSONField(blank=True, null=True, default=list)
    messages = models.JSONField(blank=True, null=True, default=list)
    meta = models.JSONField(blank=True, null=True, default=dict)
    metadata = models.JSONField(blank=True, null=True, default=dict)
    extra_documents = models.JSONField(blank=True, null=True, default=list)

    # ─────────────────────────────────────────────────────────────────
    # CARRIER RELATIONS (kept as FK - operational necessity)
    # ─────────────────────────────────────────────────────────────────

    carriers = models.ManyToManyField(
        providers.Carrier, blank=True, related_name="related_shipments"
    )
    selected_rate_carrier = models.ForeignKey(
        providers.Carrier,
        on_delete=models.CASCADE,
        related_name="carrier_shipments",
        blank=True,
        null=True,
    )
    manifest = models.ForeignKey(
        "Manifest",
        on_delete=models.SET_NULL,
        related_name="shipments",
        blank=True,
        null=True,
    )

    @property
    def object_type(self):
        return "shipment"
```

### 5.2 New Order Model

```python
@register_model
class Order(OwnedEntity):
    """Order model with embedded JSON data for addresses and line items."""

    DIRECT_PROPS = [
        "order_id", "order_date", "source", "status",
        "options", "metadata", "test_mode", "created_by",
    ]

    class Meta:
        db_table = "orders"  # Clean plural table name
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=partial(uuid, prefix="ord_"),
        editable=False,
    )
    order_id = models.CharField(max_length=50, db_index=True)
    order_date = models.DateField(default=datetime.date.today)
    source = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    status = models.CharField(
        max_length=25, choices=ORDER_STATUS, default=ORDER_STATUS[0][0], db_index=True
    )
    test_mode = models.BooleanField()

    # ─────────────────────────────────────────────────────────────────
    # EMBEDDED JSON FIELDS (direct, no _data suffix)
    # ─────────────────────────────────────────────────────────────────

    shipping_to = models.JSONField(
        blank=True,
        null=True,
        help_text="Shipping destination address (embedded JSON)",
    )
    shipping_from = models.JSONField(
        blank=True,
        null=True,
        help_text="Shipping origin address (embedded JSON)",
    )
    billing_address = models.JSONField(
        blank=True,
        null=True,
        help_text="Billing address (embedded JSON)",
    )
    line_items = models.JSONField(
        blank=True,
        null=True,
        default=list,
        help_text="Line items array with fulfillment tracking (embedded JSON)",
    )

    # ─────────────────────────────────────────────────────────────────
    # OPERATIONAL JSON FIELDS
    # ─────────────────────────────────────────────────────────────────

    options = models.JSONField(blank=True, null=True, default=dict)
    metadata = models.JSONField(blank=True, null=True, default=dict)
    meta = models.JSONField(blank=True, null=True, default=dict)

    # ─────────────────────────────────────────────────────────────────
    # SHIPMENT RELATION (kept as M2M - operational necessity)
    # ─────────────────────────────────────────────────────────────────

    shipments = models.ManyToManyField(
        "manager.Shipment", related_name="shipment_order"
    )

    @property
    def object_type(self):
        return "order"
```

### 5.3 New Pickup Model

```python
@core.register_model
class Pickup(core.OwnedEntity):
    """Pickup model with embedded JSON address."""

    DIRECT_PROPS = [
        "confirmation_number", "pickup_date", "instruction",
        "package_location", "ready_time", "closing_time",
        "test_mode", "pickup_charge", "created_by", "metadata", "meta",
    ]

    class Meta:
        db_table = "pickups"  # Clean plural table name
        verbose_name = "Pickup"
        verbose_name_plural = "Pickups"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="pck_"),
        editable=False,
    )
    confirmation_number = models.CharField(max_length=100, blank=False, db_index=True)
    test_mode = models.BooleanField(null=False)
    pickup_date = models.DateField(blank=False)
    ready_time = models.CharField(max_length=5, blank=False)
    closing_time = models.CharField(max_length=5, blank=False)
    instruction = models.CharField(max_length=250, null=True, blank=True)
    package_location = models.CharField(max_length=250, null=True, blank=True)

    # ─────────────────────────────────────────────────────────────────
    # EMBEDDED JSON FIELD (direct, no _data suffix)
    # ─────────────────────────────────────────────────────────────────

    address = models.JSONField(
        blank=True,
        null=True,
        help_text="Pickup address (embedded JSON)",
    )

    # ─────────────────────────────────────────────────────────────────
    # OPERATIONAL JSON FIELDS
    # ─────────────────────────────────────────────────────────────────

    options = models.JSONField(blank=True, null=True, default=dict)
    pickup_charge = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True, default=dict)
    meta = models.JSONField(blank=True, default=dict)

    # ─────────────────────────────────────────────────────────────────
    # CARRIER/SHIPMENT RELATIONS (kept - operational necessity)
    # ─────────────────────────────────────────────────────────────────

    pickup_carrier = models.ForeignKey(providers.Carrier, on_delete=models.CASCADE)
    shipments = models.ManyToManyField("Shipment", related_name="shipment_pickup")

    @property
    def object_type(self):
        return "pickup"
```

### 5.4 New Manifest Model

```python
@core.register_model
class Manifest(core.OwnedEntity):
    """Manifest model with embedded JSON address."""

    DIRECT_PROPS = [
        "meta", "options", "metadata", "messages", "created_by", "reference",
    ]

    class Meta:
        db_table = "manifests"  # Clean plural table name
        verbose_name = "Manifest"
        verbose_name_plural = "Manifests"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="manf_"),
        editable=False,
    )
    reference = models.CharField(max_length=100, null=True, blank=True)
    manifest = models.TextField(null=True, blank=True)
    test_mode = models.BooleanField(null=False)

    # ─────────────────────────────────────────────────────────────────
    # EMBEDDED JSON FIELD (direct, no _data suffix)
    # ─────────────────────────────────────────────────────────────────

    address = models.JSONField(
        blank=True,
        null=True,
        help_text="Manifest address (embedded JSON)",
    )

    # ─────────────────────────────────────────────────────────────────
    # OPERATIONAL JSON FIELDS
    # ─────────────────────────────────────────────────────────────────

    metadata = models.JSONField(blank=True, null=True, default=dict)
    meta = models.JSONField(blank=True, null=True, default=dict)
    options = models.JSONField(blank=True, null=True, default=dict)
    messages = models.JSONField(blank=True, null=True, default=list)

    # ─────────────────────────────────────────────────────────────────
    # CARRIER RELATION (kept - operational necessity)
    # ─────────────────────────────────────────────────────────────────

    manifest_carrier = models.ForeignKey(providers.Carrier, on_delete=models.CASCADE)

    @property
    def object_type(self):
        return "manifest"
```

### 5.5 JSON Field Structure Examples

#### Address JSON Structure
```json
{
  "id": "adr_abc123def456",
  "object_type": "address",
  "template_id": "adr_template_xyz",
  "person_name": "John Doe",
  "company_name": "Acme Inc",
  "address_line1": "123 Main St",
  "city": "Montreal",
  "state_code": "QC",
  "postal_code": "H3A 1A1",
  "country_code": "CA",
  "phone_number": "+1-514-555-0123",
  "email": "john@example.com"
}
```

#### Parcel JSON Structure
```json
{
  "id": "pcl_abc123def456",
  "object_type": "parcel",
  "weight": 2.5,
  "weight_unit": "KG",
  "width": 30,
  "height": 20,
  "length": 40,
  "dimension_unit": "CM",
  "packaging_type": "your_packaging",
  "items": [
    {
      "id": "itm_abc123def456",
      "object_type": "commodity",
      "parent_id": "oli_order_item_123",
      "title": "T-Shirt",
      "quantity": 2,
      "weight": 0.3,
      "value_amount": 25.00,
      "value_currency": "CAD",
      "origin_country": "CA"
    }
  ]
}
```

#### Line Item JSON Structure
```json
{
  "id": "oli_abc123def456",
  "object_type": "commodity",
  "sku": "TSHIRT-BLU-L",
  "title": "Blue T-Shirt Large",
  "quantity": 3,
  "unfulfilled_quantity": 1,
  "weight": 0.3,
  "weight_unit": "KG",
  "value_amount": 29.99,
  "value_currency": "CAD"
}
```

---

## 6. Migration Strategy

### 6.1 Migration Approach: In-Place Table Rename + Field Migration

Instead of creating entirely new models and copying data, we use a more efficient approach:

1. **Rename existing tables** to new names (`shipment` → `shipments`)
2. **Rename FK fields** to remove `_data` suffix where applicable
3. **Drop legacy FK/M2M fields** after data migration
4. **Update Django model** `Meta.db_table` to match

### 6.2 Migration Phases

#### Phase 1: Add New JSON Fields (Already Done)
- ✅ Added `*_data` JSON fields to existing models
- ✅ Made FK fields nullable
- ✅ Created data migration to copy FK data to JSON

#### Phase 2: Rename Fields and Tables (This Phase)

```python
# Migration: rename_shipment_to_shipments

from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('manager', 'previous_migration'),
    ]

    operations = [
        # 1. Rename table
        migrations.AlterModelTable(
            name='shipment',
            table='shipments',
        ),

        # 2. Rename JSON fields (remove _data suffix)
        migrations.RenameField(
            model_name='shipment',
            old_name='shipper_data',
            new_name='shipper_json',  # Temporary name to avoid conflict
        ),

        # 3. Drop legacy FK field
        migrations.RemoveField(
            model_name='shipment',
            name='shipper',  # Legacy FK
        ),

        # 4. Rename JSON field to final name
        migrations.RenameField(
            model_name='shipment',
            old_name='shipper_json',
            new_name='shipper',
        ),

        # Repeat for other fields...
    ]
```

#### Phase 3: Update Models and Serializers
- Update `Meta.db_table` to new table names
- Remove legacy FK/M2M field definitions from models
- Update serializers to use direct field access (no `source` redirection)
- Remove JSONDataProxy/JSONArrayProxy classes
- Remove `*_info` properties

#### Phase 4: Cleanup
- Remove any remaining legacy code
- Update documentation
- Run comprehensive tests

### 6.3 Data Migration Script

```python
def migrate_shipment_data(apps, schema_editor):
    """Migrate FK/M2M data to JSON fields."""
    Shipment = apps.get_model('manager', 'Shipment')

    for shipment in Shipment.objects.select_related(
        'shipper', 'recipient', 'return_address',
        'billing_address', 'customs'
    ).prefetch_related('parcels', 'parcels__items'):

        updates = {}

        # Migrate shipper FK to JSON
        if shipment.shipper and not shipment.shipper_data:
            updates['shipper_data'] = serialize_address(shipment.shipper)

        # Migrate recipient FK to JSON
        if shipment.recipient and not shipment.recipient_data:
            updates['recipient_data'] = serialize_address(shipment.recipient)

        # Migrate parcels M2M to JSON
        if shipment.parcels.exists() and not shipment.parcels_data:
            updates['parcels_data'] = [
                serialize_parcel(p) for p in shipment.parcels.all()
            ]

        # Migrate customs FK to JSON
        if shipment.customs and not shipment.customs_data:
            updates['customs_data'] = serialize_customs(shipment.customs)

        if updates:
            Shipment.objects.filter(pk=shipment.pk).update(**updates)


def serialize_address(address):
    """Convert Address model to JSON dict."""
    return {
        'id': f"adr_{uuid.uuid4().hex[:12]}",
        'object_type': 'address',
        'template_id': address.pk if address.is_template else None,
        'person_name': address.person_name,
        'company_name': address.company_name,
        'address_line1': address.address_line1,
        'address_line2': address.address_line2,
        'city': address.city,
        'state_code': address.state_code,
        'postal_code': address.postal_code,
        'country_code': address.country_code,
        'phone_number': address.phone_number,
        'email': address.email,
        'federal_tax_id': address.federal_tax_id,
        'state_tax_id': address.state_tax_id,
        'residential': address.residential,
    }


def serialize_parcel(parcel):
    """Convert Parcel model to JSON dict."""
    return {
        'id': f"pcl_{uuid.uuid4().hex[:12]}",
        'object_type': 'parcel',
        'weight': parcel.weight,
        'width': parcel.width,
        'height': parcel.height,
        'length': parcel.length,
        'weight_unit': parcel.weight_unit,
        'dimension_unit': parcel.dimension_unit,
        'packaging_type': parcel.packaging_type,
        'package_preset': parcel.package_preset,
        'is_document': parcel.is_document,
        'description': parcel.description,
        'content': parcel.content,
        'items': [serialize_commodity(c) for c in parcel.items.all()],
    }
```

### 6.4 Rollback Strategy

If issues arise during migration:

1. **Backup before migration**: Full database backup
2. **Reversible migrations**: All Django migrations are reversible
3. **Feature flag**: Can toggle between FK and JSON access during transition
4. **Parallel read**: During transition, read from JSON with FK fallback

---

## 7. Serializer Design (Option C)

### 7.1 Option C: Nested Serializers Handle Dicts Directly

The key insight is that DRF nested serializers can work with dict data directly when properly configured. The serializer's `to_representation` method can handle both model instances and dicts.

### 7.2 Address Serializer

```python
class AddressSerializer(serializers.Serializer):
    """Address serializer that handles both model instances and dicts."""

    id = serializers.CharField(required=False, allow_null=True)
    object_type = serializers.CharField(default="address", read_only=True)
    template_id = serializers.CharField(required=False, allow_null=True)

    person_name = serializers.CharField(required=False, allow_null=True)
    company_name = serializers.CharField(required=False, allow_null=True)
    address_line1 = serializers.CharField(required=False, allow_null=True)
    address_line2 = serializers.CharField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)
    state_code = serializers.CharField(required=False, allow_null=True)
    postal_code = serializers.CharField(required=False, allow_null=True)
    country_code = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
    federal_tax_id = serializers.CharField(required=False, allow_null=True)
    state_tax_id = serializers.CharField(required=False, allow_null=True)
    residential = serializers.BooleanField(required=False, allow_null=True)

    def to_representation(self, instance):
        """Handle both model instances and dict data."""
        if isinstance(instance, dict):
            return {
                key: instance.get(key)
                for key in self.fields.keys()
                if key in instance or key == 'object_type'
            }
        return super().to_representation(instance)
```

### 7.3 Shipment Response Serializer

```python
class ShipmentSerializer(serializers.Serializer):
    """Shipment response serializer using Option C pattern."""

    id = serializers.CharField(read_only=True)
    object_type = serializers.CharField(default="shipment", read_only=True)
    status = serializers.CharField()
    tracking_number = serializers.CharField(allow_null=True)

    # Nested serializers work with JSON field data directly
    shipper = AddressSerializer(allow_null=True)
    recipient = AddressSerializer(allow_null=True)
    return_address = AddressSerializer(allow_null=True)
    billing_address = AddressSerializer(allow_null=True)
    parcels = ParcelSerializer(many=True)
    customs = CustomsSerializer(allow_null=True)

    # Other fields...
    selected_rate = RateSerializer(allow_null=True)
    rates = RateSerializer(many=True)
    messages = MessageSerializer(many=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        """Serialize shipment with JSON field data."""
        data = {
            'id': instance.id,
            'object_type': 'shipment',
            'status': instance.status,
            'tracking_number': instance.tracking_number,
            # ... other direct fields
        }

        # Nested serializers handle dict data from JSON fields
        if instance.shipper:
            data['shipper'] = AddressSerializer(instance.shipper).data

        if instance.recipient:
            data['recipient'] = AddressSerializer(instance.recipient).data

        if instance.parcels:
            data['parcels'] = ParcelSerializer(instance.parcels, many=True).data

        if instance.customs:
            data['customs'] = CustomsSerializer(instance.customs).data

        return data
```

### 7.4 Input Serializer with Template Resolution

```python
class ShipmentWriteSerializer(serializers.Serializer):
    """Shipment create/update serializer with template resolution."""

    shipper = serializers.DictField(required=True)
    recipient = serializers.DictField(required=True)
    parcels = serializers.ListField(child=serializers.DictField(), required=True)
    customs = serializers.DictField(required=False, allow_null=True)

    # Other input fields...

    def validate_shipper(self, value):
        """Resolve template if id provided."""
        return self._resolve_address(value)

    def validate_recipient(self, value):
        """Resolve template if id provided."""
        return self._resolve_address(value)

    def _resolve_address(self, data):
        """Resolve address template or validate inline data."""
        if isinstance(data, str):
            # Just an ID - resolve template
            template = Address.objects.get(pk=data)
            return serialize_address(template)

        if 'id' in data and data['id'].startswith('adr_'):
            # Has template ID - merge with template data
            try:
                template = Address.objects.get(pk=data['id'])
                merged = {**serialize_address(template), **data}
                merged['template_id'] = data['id']
                merged['id'] = f"adr_{uuid.uuid4().hex[:12]}"
                return merged
            except Address.DoesNotExist:
                pass

        # Inline data - generate ID
        if 'id' not in data:
            data['id'] = f"adr_{uuid.uuid4().hex[:12]}"
        data['object_type'] = 'address'
        return data
```

---

## 8. Implementation Plan

### 8.1 Phase 1: Preparation (1 day)

1. **Create backup of existing database**
2. **Review and update existing JSON field migrations**
3. **Ensure all FK data is already migrated to JSON fields**
4. **Write comprehensive tests for current state**

### 8.2 Phase 2: Model Updates (2 days)

1. **Update Meta.db_table** to new table names
2. **Create migration to rename tables**
3. **Create migration to rename fields** (remove `_data` suffix)
4. **Create migration to drop legacy FK/M2M fields**
5. **Remove JSONDataProxy/JSONArrayProxy classes**
6. **Remove `*_info` property methods**

### 8.3 Phase 3: Serializer Updates (2 days)

1. **Update response serializers** to use direct field access
2. **Remove `source="*_info"` redirections**
3. **Update input serializers** for Option C pattern
4. **Update template resolution logic**

### 8.4 Phase 4: Signal and Logic Updates (1 day)

1. **Update signals** (order status, fulfillment tracking)
2. **Update gateway/shipping logic** to use JSON fields
3. **Update any queries** that referenced FK fields

### 8.5 Phase 5: Testing and Cleanup (2 days)

1. **Run full test suite**
2. **Fix any failing tests**
3. **Performance testing**
4. **Documentation updates**
5. **Remove any remaining legacy code**

---

## 9. Testing Strategy

### 9.1 Test Categories

| Category | Description |
|----------|-------------|
| Unit Tests | JSON field serialization/deserialization |
| Integration Tests | Full API request/response cycles |
| Migration Tests | Data integrity after migration |
| Performance Tests | Query performance comparison |

### 9.2 Critical Test Cases

```python
class TestShipmentJSONFields(APITestCase):
    """Test shipment with embedded JSON data."""

    def test_create_shipment_with_embedded_addresses(self):
        """Create shipment with inline address data."""
        response = self.client.post('/api/shipments', data={
            'shipper': {
                'person_name': 'John Doe',
                'address_line1': '123 Main St',
                'city': 'Montreal',
                'state_code': 'QC',
                'postal_code': 'H3A 1A1',
                'country_code': 'CA',
            },
            'recipient': {
                'person_name': 'Jane Smith',
                'address_line1': '456 Oak Ave',
                'city': 'Toronto',
                'state_code': 'ON',
                'postal_code': 'M5V 1A1',
                'country_code': 'CA',
            },
            'parcels': [{
                'weight': 2.5,
                'weight_unit': 'KG',
            }],
        })

        print(response)
        self.assertResponseNoErrors(response)
        self.assertDictEqual(response.data, {
            'id': mock.ANY,
            'object_type': 'shipment',
            'status': 'draft',
            'shipper': {
                'id': mock.ANY,
                'object_type': 'address',
                'person_name': 'John Doe',
                # ...
            },
            'recipient': {
                'id': mock.ANY,
                'object_type': 'address',
                'person_name': 'Jane Smith',
                # ...
            },
            'parcels': [{
                'id': mock.ANY,
                'object_type': 'parcel',
                'weight': 2.5,
                'weight_unit': 'KG',
                # ...
            }],
            'created_at': mock.ANY,
            'updated_at': mock.ANY,
        })

    def test_create_shipment_with_template_reference(self):
        """Create shipment referencing address template."""
        # Create template first
        template = Address.objects.create(
            person_name='Warehouse',
            address_line1='789 Industrial Blvd',
            city='Montreal',
            country_code='CA',
            meta={'label': 'Main Warehouse', 'usage': ['sender']},
        )

        response = self.client.post('/api/shipments', data={
            'shipper': template.pk,  # Just the ID
            'recipient': {
                'person_name': 'Customer',
                'address_line1': '123 Customer St',
                'city': 'Toronto',
                'country_code': 'CA',
            },
            'parcels': [{'weight': 1.0, 'weight_unit': 'KG'}],
        })

        print(response)
        self.assertResponseNoErrors(response)
        self.assertEqual(
            response.data['shipper']['template_id'],
            template.pk
        )
        self.assertEqual(
            response.data['shipper']['person_name'],
            'Warehouse'
        )
```

---

## 10. Risk Assessment

### 10.1 Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Data loss during migration | High | Low | Pre-migration backup, reversible migrations |
| API breaking changes | High | Low | Extensive test coverage, staging environment |
| Performance regression | Medium | Medium | Performance benchmarks before/after |
| Third-party integrations break | Medium | Low | API response structure unchanged |
| Rollback complexity | Medium | Low | Feature flags, parallel access during transition |

### 10.2 Monitoring

1. **Error rate monitoring** during and after deployment
2. **Query performance monitoring**
3. **Data integrity checks** post-migration
4. **User feedback channels** for issue reporting

---

## 11. Appendix

### 11.1 Field Mapping Reference

#### Shipment Field Mapping

| Legacy Field | Type | New Field | Type |
|--------------|------|-----------|------|
| `shipper` | OneToOneField | `shipper` | JSONField |
| `shipper_data` | JSONField | (removed) | - |
| `recipient` | OneToOneField | `recipient` | JSONField |
| `recipient_data` | JSONField | (removed) | - |
| `return_address` | OneToOneField | `return_address` | JSONField |
| `return_address_data` | JSONField | (removed) | - |
| `billing_address` | OneToOneField | `billing_address` | JSONField |
| `billing_address_data` | JSONField | (removed) | - |
| `parcels` | ManyToManyField | `parcels` | JSONField |
| `parcels_data` | JSONField | (removed) | - |
| `customs` | OneToOneField | `customs` | JSONField |
| `customs_data` | JSONField | (removed) | - |

#### Order Field Mapping

| Legacy Field | Type | New Field | Type |
|--------------|------|-----------|------|
| `shipping_to` | OneToOneField | `shipping_to` | JSONField |
| `shipping_to_data` | JSONField | (removed) | - |
| `shipping_from` | OneToOneField | `shipping_from` | JSONField |
| `shipping_from_data` | JSONField | (removed) | - |
| `billing_address` | OneToOneField | `billing_address` | JSONField |
| `billing_address_data` | JSONField | (removed) | - |
| `line_items` | ManyToManyField | `line_items` | JSONField |
| `line_items_data` | JSONField | (removed) | - |

### 11.2 Table Naming Changes

| Current Table | New Table |
|---------------|-----------|
| `shipment` | `shipments` |
| `order` | `orders` |
| `pickup` | `pickups` |
| `manifest` | `manifests` |

### 11.3 Files to Modify

| File | Changes |
|------|---------|
| `modules/manager/karrio/server/manager/models.py` | Update Shipment, Pickup, Manifest models |
| `modules/orders/karrio/server/orders/models.py` | Update Order model |
| `modules/manager/karrio/server/manager/serializers/shipment.py` | Update serializers |
| `modules/orders/karrio/server/orders/serializers/` | Update serializers |
| `modules/core/karrio/server/core/serializers.py` | Update ShipmentContent |
| `modules/orders/karrio/server/orders/signals.py` | Update for JSON fields |
| `modules/manager/karrio/server/manager/signals.py` | Update for JSON fields |

### 11.4 Code Cleanup Checklist

- [ ] Remove `JSONDataProxy` class from `models.py`
- [ ] Remove `JSONArrayProxy` class from `models.py`
- [ ] Remove `*_info` property methods from models
- [ ] Remove `*_data` field definitions (renamed to direct fields)
- [ ] Remove `source="*_info"` from serializers
- [ ] Remove legacy FK/M2M field definitions
- [ ] Update `DIRECT_PROPS`, `RELATIONAL_PROPS`, `JSON_PROPS` lists
- [ ] Update model managers (remove FK prefetch)
- [ ] Update signals for JSON-only access
