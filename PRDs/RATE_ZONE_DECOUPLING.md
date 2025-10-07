# Product Requirements Document: Rate/Zone Decoupling Architecture Upgrade

**Project**: Complete Migration to Decoupled Rate Calculation System
**Version**: 1.0
**Date**: 2025-10-04
**Status**: Planning
**Owner**: Engineering Team

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Goals & Success Criteria](#goals--success-criteria)
4. [Technical Architecture](#technical-architecture)
5. [Database Changes](#database-changes)
6. [SDK/Core Changes](#sdkcore-changes)
7. [Carrier Integration Changes](#carrier-integration-changes)
8. [GraphQL API Changes](#graphql-api-changes)
9. [Frontend Changes](#frontend-changes)
10. [Migration Strategy](#migration-strategy)
11. [Implementation Plan](#implementation-plan)
12. [Testing Strategy](#testing-strategy)
13. [Risk Assessment](#risk-assessment)
14. [Rollout Plan](#rollout-plan)

---

## Executive Summary

This document outlines a **complete architectural upgrade** to decouple rate calculation from zone definitions in the Karrio shipping platform. This is **not** a backward-compatible change - it's a full system migration that will:

✅ **Remove** all legacy code supporting the old zone-with-rate model
✅ **Replace** with DEFAULT_RATESHEET architecture (pricing logic in SDK, rates from CSV)
✅ **Migrate** all existing database records to new rate_config JSON format
✅ **Update** all 9 carrier integrations to define DEFAULT_RATESHEET with CSV data loading
✅ **Upgrade** the full stack: SDK (define logic) → CSV (provide rates) → Database (store config) → API → Frontend

### Key Architecture Decisions

1. **Pricing Logic Lives in SDK**: Calculators (weight tiers, dimensional weight) and accessorial charges (fuel surcharge, residential fee) are defined once per carrier in `DEFAULT_RATESHEET`
2. **Rates Live in CSV**: Only the numbers (rates, weight ranges, zone mappings) are stored in CSV files
3. **Runtime Config in Database**: The populated DEFAULT_RATESHEET (logic + rates) is stored as JSON in `rate_config` field
4. **No New Database Tables**: Everything stored in single `rate_config` JSONField per RateSheet/ServiceLevel
5. **User Editable**: Rates, weight ranges, accessorial charge percentages (via GraphQL/Frontend)
6. **Not User Editable**: Calculator logic, accessorial charge logic (defined in carrier code)

**Timeline**: 8-10 weeks
**Risk Level**: HIGH (breaking changes to core pricing system)
**User Impact**: Zero (if migration successful) / Critical (if migration fails)
**Migration Requirement**: All 9 carriers must have DEFAULT_RATESHEET implemented before migration

---

## Problem Statement

### Current State

**Zone Definition** (Current):
```python
{
    "label": "United States",
    "country_codes": ["US"],
    "min_weight": 0.5,
    "max_weight": 1.0,
    "rate": 8.78,  # ❌ Rate hardcoded in zone
    "transit_days": 7
}
```

**Problems**:
1. **Inflexible**: Cannot apply dynamic pricing (fuel surcharges, discounts)
2. **Inefficient**: Same zones duplicated across services with different rates
3. **Complex**: Updating rates requires modifying zone definitions
4. **Limited**: Cannot support complex pricing models (distance-based, dimensional weight, etc.)
5. **Messy**: Backward compatibility code scattered throughout codebase

### Desired State

**DEFAULT_RATESHEET** (Defined in SDK - Carrier Code):

```python
# modules/connectors/landmark/karrio/providers/landmark/units.py

from karrio.core.models import (
    RateSheet,
    Zone,
    WeightTieredRate,
    FuelSurcharge,
    ResidentialDeliveryFee,
)

DEFAULT_RATESHEET = RateSheet(
    carrier_name="landmark",

    # Zone definitions (eligibility only)
    zones=[
        Zone(id="zone_us", label="United States", country_codes=["US"]),
        Zone(id="zone_eu1", label="EU Zone 1", country_codes=["DE", "FR", "BE", "NL"]),
    ],

    # Calculator definitions (pricing logic)
    rates=[
        WeightTieredRate(
            rate_id="landmark_maxipak_intl",
            currency="GBP",
            weight_unit="KG",
            config={
                "tiers": []  # Populated from CSV at runtime
            }
        )
    ],

    # Accessorial charge definitions (surcharges/discounts)
    accessorial_charges=[
        FuelSurcharge(
            accessorial_id="fuel_2025q1",
            percentage=8.5,  # Default, can be edited in rate_config
            applies_to_services=["*"]  # All services
        ),
        ResidentialDeliveryFee(
            accessorial_id="residential_surcharge",
            amount=3.95,  # Default, can be edited in rate_config
            applies_to_services=["*"]
        )
    ],

    # Services populated from CSV
    services=[]  # Loaded from services.csv
)
```

**CSV Files** (Just the Numbers):

```csv
# services.csv
service_code,service_name,max_weight,dim_factor,rate_id,accessorial_charge_ids
LGINTSTD,MaxiPak Scan DDP,30.0,6000,landmark_maxipak_intl,"fuel_2025q1,residential_surcharge"

# rate_tiers.csv
rate_id,zone_id,min_weight,max_weight,rate
landmark_maxipak_intl,zone_us,0.5,1.0,8.78
landmark_maxipak_intl,zone_us,1.0,2.0,10.81
landmark_maxipak_intl,zone_eu1,0.5,1.0,5.50
```

**Database Storage**:

**RateSheet.rate_config** (Complete structure):

```json
{
  "zones": [
    {
      "id": "zone_us",
      "label": "United States",
      "country_codes": ["US"],
      "cities": [],
      "postal_codes": [],
      "transit_days": 7,
      "metadata": {}
    },
    {
      "id": "zone_eu1",
      "label": "EU Zone 1",
      "country_codes": ["DE", "FR", "BE", "NL", "AT", "DK"],
      "cities": [],
      "postal_codes": [],
      "transit_days": 3,
      "metadata": {}
    }
  ],
  "rates": [
    {
      "rate_id": "landmark_maxipak_intl",
      "rate_type": "weight_tiered",
      "currency": "GBP",
      "weight_unit": "KG",
      "dimension_unit": "CM",
      "config": {
        "tiers": [
          {
            "zone_id": "zone_us",
            "min_weight": 0.0,
            "max_weight": 0.25,
            "rate": 5.71
          },
          {
            "zone_id": "zone_us",
            "min_weight": 0.25,
            "max_weight": 0.5,
            "rate": 6.86
          },
          {
            "zone_id": "zone_us",
            "min_weight": 0.5,
            "max_weight": 1.0,
            "rate": 8.78
          },
          {
            "zone_id": "zone_eu1",
            "min_weight": 0.5,
            "max_weight": 1.0,
            "rate": 5.16
          }
        ]
      },
      "is_active": true,
      "metadata": {}
    }
  ],
  "accessorial_charges": [
    {
      "accessorial_id": "fuel_2025q1",
      "accessorial_type": "fuel_surcharge",
      "config": {
        "percent": 8.5
      },
      "applies_to_services": ["LGINTSTD", "LGINTSTDU"],
      "priority": 10,
      "is_active": true
    },
    {
      "accessorial_id": "residential",
      "accessorial_type": "residential_delivery_fee",
      "config": {
        "amount": 3.95
      },
      "applies_to_services": ["*"],
      "priority": 20,
      "is_active": true
    }
  ]
}
```

**ServiceLevel.rate_config** (Simplified structure - references RateSheet):

```json
{
  "zone_ids": ["zone_us", "zone_eu1"],
  "rate_id": "landmark_maxipak_intl",
  "accessorial_charge_ids": ["fuel_2025q1", "residential"],
  "dim_factor": 6000
}
```

**Key insights**:
- `RateSheet.rate_config`: Defines ALL zones, rates, and accessorial charges (the "library")
- `ServiceLevel.rate_config`: References which zones/rates/accessorials apply to THIS service (the "selection")
- User edits rates/accessorial percentages in RateSheet, not in ServiceLevel
- Avoids data duplication - single source of truth in RateSheet

---

## Goals & Success Criteria

### Primary Goals

1. **Complete Decoupling**: Separate eligibility (zones) from pricing (rates)
2. **Clean Codebase**: Remove ALL backward compatibility code
3. **Zero Data Loss**: Migrate all existing rate sheets without losing data
4. **Full Stack Upgrade**: Update database, SDK, API, and frontend
5. **Carrier Migration**: Convert all 9 carriers to new CSV format

### Success Criteria

- [ ] All existing rate sheets migrated to new format (100% success rate)
- [ ] All 9 carriers using new CSV-based rate_definition format
- [ ] Zero backward compatibility code in codebase
- [ ] All GraphQL mutations working with new schema
- [ ] Frontend UI functional with new data structure
- [ ] Performance equal or better than current system
- [ ] All existing tests passing + new tests added
- [ ] Production deployment with zero downtime

### Non-Goals (Out of Scope)

- Machine learning pricing (future phase)
- Multi-currency rate sheets (future phase)
- Historical rate versioning (future phase)
- Rate sheet templates/marketplace (future phase)

---

## Technical Architecture

### New Data Model

```
┌──────────────────────────────────────────────────────────────┐
│                        RateSheet                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • id, name, carrier_name                             │   │
│  │ • zones: [Zone]          (shared zone definitions)   │   │
│  │ • rates: [Calculator]  (rate calculation logic)│   │
│  │ • accessorial_charges: [Modifier]  (surcharges, discounts)     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Service    │  │   Service    │  │   Service    │      │
│  │   Level 1    │  │   Level 2    │  │   Level 3    │      │
│  │              │  │              │  │              │      │
│  │ • zones_ids  │  │ • zones_ids  │  │ • zones_ids  │      │
│  │ • rate_id    │  │ • rate_id    │  │ • rate_id    │      │
│  │ • mod_ids    │  │ • mod_ids    │  │ • mod_ids    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

### Rate Calculation Flow

```
┌─────────────┐
│ Rate Request│
│ • package   │
│ • origin    │
│ • dest      │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ 1. Find Service │  (Based on service_code, domestic/intl)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Find Zone    │  (Match location: postal > city > country)
│    (Eligibility)│  (Match weight: min <= weight < max)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Get          │  (Lookup by zone.rate_id)
│    Calculator   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Calculate    │  (Execute: rate_definition.calculate(package, zone))
│    Base Rate    │  → Returns base_rate (e.g., $10.00)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Apply        │  (For each accessorial_charge in service.accessorial_charges:)
│    Modifiers    │    → fuel: +$0.85 (8.5%)
└────────┬────────┘    → residential: +$3.95
         │             → total: $14.80
         ▼
┌─────────────────┐
│ 6. Return Rate  │  → RateDetails(base=10.00, surcharges=[...], total=14.80)
└─────────────────┘
```

---

## Database Changes

### Design Principles

This schema design follows three key optimization principles:

1. **JSONField consolidation**: Use JSONField to group related configuration, reducing field proliferation
2. **Minimal tables**: Store rates/accessorial_charges as JSON in RateSheet, avoiding separate tables
3. **No database-level enums**: Use CharField, enforce validation at GraphQL/input layer

### Schema Changes

#### 1. Updated RateSheet Table

```sql
-- REMOVE legacy fields
ALTER TABLE "rate-sheet" DROP COLUMN IF EXISTS metadata;
ALTER TABLE "rate-sheet" DROP COLUMN IF EXISTS service_rates;

-- ADD new field (consolidated configuration)
ALTER TABLE "rate-sheet" ADD COLUMN rate_config JSONB DEFAULT '{}';

-- rate_config structure:
-- {
--   "zones": [
--     {
--       "id": "zone_us",
--       "label": "United States",
--       "country_codes": ["US"],
--       "cities": [],
--       "postal_codes": [],
--       "transit_days": 7
--     }
--   ],
--   "rates": [
--     {
--       "rate_id": "landmark_maxipak_intl",
--       "rate_type": "weight_tiered",  -- No enum at DB level!
--       "config": {
--         "currency": "GBP",
--         "weight_unit": "KG",
--         "dimension_unit": "CM",
--         "tiers": [
--           {
--             "zone_id": "zone_us",
--             "min_weight": 0.5,
--             "max_weight": 1.0,
--             "rate": 8.78
--           },
--           {
--             "zone_id": "zone_us",
--             "min_weight": 1.0,
--             "max_weight": 2.0,
--             "rate": 10.81
--           }
--         ]
--       },
--       "is_active": true,
--       "created_at": "2025-01-01T00:00:00Z"
--     }
--   ],
--   "accessorial_charges": [
--     {
--       "accessorial_id": "fuel_2025q1",
--       "accessorial_type": "fuel",  -- No enum at DB level!
--       "config": {
--         "percentage": 8.5,
--         "applies_to_services": ["LGINTSTD", "LGINTSTDU"],
--         "priority": 10
--       },
--       "is_active": true,
--       "created_at": "2025-01-01T00:00:00Z"
--     },
--     {
--       "accessorial_id": "residential_surcharge",
--       "accessorial_type": "residential",
--       "config": {
--         "amount": 3.95,
--         "applies_to_services": ["*"],  -- All services
--         "priority": 20
--       },
--       "is_active": true
--     }
--   ]
-- }

-- Create GIN index for efficient JSON querying
CREATE INDEX idx_ratesheet_rate_config ON "rate-sheet" USING GIN (rate_config);
```

**Benefits**:
- ✅ Zero new tables
- ✅ All rate configuration in one JSON field
- ✅ Atomic updates (entire config versioned together)
- ✅ Easy to backup/restore/duplicate rate sheets
- ✅ No foreign key constraints to manage

#### 2. Updated ServiceLevel Table

```sql
-- REMOVE legacy field
ALTER TABLE "service-level" DROP COLUMN IF EXISTS zones;

-- ADD new field (consolidated configuration)
ALTER TABLE "service-level" ADD COLUMN rate_config JSONB DEFAULT '{}';

-- rate_config structure:
-- {
--   "zone_ids": ["zone_us", "zone_eu1", "zone_eu2"],
--   "rate_id": "landmark_maxipak_intl",
--   "accessorial_ids": ["fuel_2025q1", "residential_surcharge"],
--   "dim_factor": 6000  -- Dimensional weight factor (optional)
-- }

-- Create GIN index for efficient JSON querying
CREATE INDEX idx_servicelevel_rate_config ON "service-level" USING GIN (rate_config);

-- Add expression index for rate_id lookups (frequently queried)
CREATE INDEX idx_servicelevel_rate_id ON "service-level"
    ((rate_config->>'rate_id'));
```

**Benefits**:
- ✅ Single JSON field instead of 4 separate fields
- ✅ Reduced schema complexity
- ✅ Easy to add new config options without migrations
- ✅ Atomic updates of service rate configuration

### Database Schema Summary

**Before Optimization**:
- 2 new tables (RateDefinition, AccessorialCharge)
- 1 junction table (ServiceLevel_Modifiers)
- 4 new fields on ServiceLevel (zone_ids, rate_id, accessorial_ids, dim_factor)
- 2 new fields on RateSheet (rates, accessorial_charges)
- Multiple enum constraints
- Foreign key constraints

**After Optimization**:
- **0 new tables** ✅
- **0 junction tables** ✅
- **1 new field on ServiceLevel** (rate_config) ✅
- **1 new field on RateSheet** (rate_config) ✅
- **0 enum constraints** ✅
- **0 foreign key constraints** ✅

### Performance Considerations

**JSON Indexing**:
```sql
-- GIN indexes support efficient querying of JSON fields
CREATE INDEX idx_ratesheet_rate_config ON "rate-sheet" USING GIN (rate_config);
CREATE INDEX idx_servicelevel_rate_config ON "service-level" USING GIN (rate_config);

-- Expression indexes for frequently accessed JSON keys
CREATE INDEX idx_servicelevel_rate_id ON "service-level"
    ((rate_config->>'rate_id'));

CREATE INDEX idx_servicelevel_zone_ids ON "service-level"
    USING GIN ((rate_config->'zone_ids'));
```

**Query Examples**:
```sql
-- Find all services using a specific rate_definition
SELECT * FROM "service-level"
WHERE rate_config->>'rate_id' = 'landmark_maxipak_intl';

-- Find all services covering zone_us
SELECT * FROM "service-level"
WHERE rate_config->'zone_ids' @> '"zone_us"'::jsonb;

-- Find all rate sheets with fuel surcharge accessorial_charge
SELECT * FROM "rate-sheet"
WHERE rate_config->'accessorial_charges' @> '[{"accessorial_id": "fuel_2025q1"}]'::jsonb;
```

**Trade-offs**:
- ✅ **Pro**: Fewer tables, simpler schema, easier migrations
- ✅ **Pro**: Atomic updates, better versioning
- ✅ **Pro**: No foreign key cascade issues
- ⚠️ **Con**: Slightly more complex queries (JSONB operations)
- ⚠️ **Con**: Data validation must happen at application layer (not DB constraints)

### Migration Strategy

The migration strategy follows Django's standard approach: update models first, then let Django auto-generate migration files, and finally add manual data transformations where needed.

#### Step 1: Update Django Models

Update the following model files to add new fields:

**modules/core/karrio/server/providers/models.py**

Update existing `ServiceLevel` model:

```python
class ServiceLevel(models.Model):
    # ... existing fields ...

    # NEW FIELD - Add this single JSON field
    rate_config = models.JSONField(default=dict, blank=True)
    # Structure:
    # {
    #   "zone_ids": ["zone_us", "zone_eu1"],
    #   "rate_id": "landmark_maxipak_intl",
    #   "accessorial_ids": ["fuel_2025q1", "residential_surcharge"],
    #   "dim_factor": 6000
    # }

    # DEPRECATED FIELD - Will be removed in cleanup migration
    # zones = models.JSONField(...)  # Keep for now during transition

    class Meta:
        # ... existing meta ...
        indexes = [
            # ... existing indexes ...
            # Add GIN index for rate_config
            models.Index(fields=['rate_config'], name='idx_servicelevel_rate_config'),
        ]
```

Update existing `RateSheet` model:

```python
class RateSheet(models.Model):
    # ... existing fields ...

    # NEW FIELD - Add this single JSON field
    rate_config = models.JSONField(default=dict, blank=True)
    # Structure:
    # {
    #   "zones": [...],
    #   "rates": [...],
    #   "accessorial_charges": [...]
    # }

    # DEPRECATED FIELDS - Will be removed in cleanup migration
    # metadata = models.JSONField(...)  # Keep for now during transition
    # service_rates = models.JSONField(...)  # Keep for now during transition

    class Meta:
        # ... existing meta ...
        indexes = [
            # ... existing indexes ...
            # Add GIN index for rate_config
            models.Index(fields=['rate_config'], name='idx_ratesheet_rate_config'),
        ]
```

**Note**: No new models needed! All rates and accessorial_charges stored as JSON.

#### Step 2: Generate Migration Files

Run Django's makemigrations command to auto-generate schema migration files:

```bash
# From project root
cd modules/core
python manage.py makemigrations providers --name add_rate_config_fields
```

This will generate migration file like:
- `0XXX_add_rate_config_fields.py` - Adds rate_config JSONField to RateSheet and ServiceLevel

Expected auto-generated migration:
```python
# Auto-generated by Django - DO NOT EDIT MANUALLY

from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('providers', '0XXX_previous_migration'),
    ]

    operations = [
        # Add rate_config to RateSheet
        migrations.AddField(
            model_name='ratesheet',
            name='rate_config',
            field=models.JSONField(blank=True, default=dict),
        ),

        # Add rate_config to ServiceLevel
        migrations.AddField(
            model_name='servicelevel',
            name='rate_config',
            field=models.JSONField(blank=True, default=dict),
        ),

        # Add GIN indexes for JSON querying
        migrations.AddIndex(
            model_name='ratesheet',
            index=models.Index(fields=['rate_config'], name='idx_ratesheet_rate_config'),
        ),
        migrations.AddIndex(
            model_name='servicelevel',
            index=models.Index(fields=['rate_config'], name='idx_servicelevel_rate_config'),
        ),
    ]
```

#### Step 3: Create Manual Data Migration

After schema migrations are generated, create a manual data migration to transform legacy data to new format.

**Pattern Reference**: Based on `modules/core/karrio/server/providers/migrations/0076_rename_customer_registration_id_uspsinternationalsettings_account_number_and_more.py`

Create migration file:

```bash
python manage.py makemigrations providers --empty --name migrate_legacy_rates_to_rate_config
```

Edit the generated file:

```python
# modules/core/karrio/server/providers/migrations/0XXX_migrate_legacy_rates_to_rate_config.py

from django.db import migrations
from datetime import datetime
import json


def migrate_legacy_rate_sheets_forward(apps, schema_editor):
    """
    Migrate all existing rate sheets from legacy format to new rate_config structure.

    Migration steps:
    1. Extract unique zones from all services (deduplicate)
    2. Create rate_definition definitions from zone rate + weight data
    3. Store everything in rate_config JSON field
    4. Update ServiceLevel.rate_config with zone_ids and rate_id
    """
    db_alias = schema_editor.connection.alias
    RateSheet = apps.get_model('providers', 'RateSheet')
    ServiceLevel = apps.get_model('providers', 'ServiceLevel')

    for rate_sheet in RateSheet.objects.using(db_alias).all().iterator():
        # Step 1: Extract unique zones across all services
        all_zones = {}
        zone_counter = 1

        for service in rate_sheet.services.all():
            legacy_zones = service.zones or []

            for zone_data in legacy_zones:
                # Create zone signature for deduplication (excluding rate/weight)
                zone_sig = {
                    'label': zone_data.get('label', ''),
                    'country_codes': sorted(zone_data.get('country_codes', [])),
                    'cities': sorted(zone_data.get('cities', [])),
                    'postal_codes': sorted(zone_data.get('postal_codes', [])),
                }

                sig_key = json.dumps(zone_sig, sort_keys=True)

                if sig_key not in all_zones:
                    zone_id = f"zone_{zone_counter}"
                    all_zones[sig_key] = {
                        'id': zone_id,
                        **zone_sig,
                        'transit_days': zone_data.get('transit_days'),
                    }
                    zone_counter += 1

        # Step 2: Create rate_definition definitions for each service
        rates = []

        for service in rate_sheet.services.all():
            legacy_zones = service.zones or []

            # Extract weight tiers from zones
            tiers = []
            service_zone_ids = []

            for zone_data in legacy_zones:
                # Find matching zone ID
                zone_sig = {
                    'label': zone_data.get('label', ''),
                    'country_codes': sorted(zone_data.get('country_codes', [])),
                    'cities': sorted(zone_data.get('cities', [])),
                    'postal_codes': sorted(zone_data.get('postal_codes', [])),
                }
                sig_key = json.dumps(zone_sig, sort_keys=True)
                zone_id = all_zones[sig_key]['id']

                if zone_id not in service_zone_ids:
                    service_zone_ids.append(zone_id)

                # Extract tier data (rate + weight range)
                tier = {
                    'zone_id': zone_id,
                    'rate': zone_data.get('rate', 0),
                }

                # Add weight range if defined
                if zone_data.get('min_weight') is not None:
                    tier['min_weight'] = zone_data['min_weight']
                if zone_data.get('max_weight') is not None:
                    tier['max_weight'] = zone_data['max_weight']

                tiers.append(tier)

            # Create rate_definition definition
            rate_id = f"{rate_sheet.carrier_name}_{service.service_code}_{rate_sheet.id}".lower().replace(' ', '_')

            # Determine rate_definition type based on tier structure
            has_weight_tiers = any(
                t.get('min_weight') is not None or t.get('max_weight') is not None
                for t in tiers
            )
            rate_type = 'weight_tiered' if has_weight_tiers else 'flat'

            rate_def = {
                'rate_id': rate_id,
                'rate_type': rate_type,
                'config': {
                    'currency': getattr(service, 'currency', 'USD') or 'USD',
                    'weight_unit': getattr(service, 'weight_unit', 'KG') or 'KG',
                    'dimension_unit': getattr(service, 'dimension_unit', 'CM') or 'CM',
                    'tiers': tiers,
                },
                'is_active': True,
                'created_at': datetime.utcnow().isoformat(),
            }

            rates.append(rate_def)

            # Update service.rate_config
            service.rate_config = {
                'zone_ids': service_zone_ids,
                'rate_id': rate_id,
                'accessorial_ids': [],
                'dim_factor': None,  # No dimensional weight in legacy data
            }
            service.save(using=db_alias)

        # Step 3: Update rate_sheet.rate_config with zones and rates
        rate_sheet.rate_config = {
            'zones': list(all_zones.values()),
            'rates': rates,
            'accessorial_charges': [],  # No accessorial_charges in legacy data
        }
        rate_sheet.save(using=db_alias)


def migrate_legacy_rate_sheets_reverse(apps, schema_editor):
    """
    Reverse migration - convert rate_config back to legacy zones format.

    NOTE: This is a safety measure but will lose accessorial_charge data if any exists.
    """
    db_alias = schema_editor.connection.alias
    RateSheet = apps.get_model('providers', 'RateSheet')
    ServiceLevel = apps.get_model('providers', 'ServiceLevel')

    for service in ServiceLevel.objects.using(db_alias).all().iterator():
        rate_config = service.rate_config or {}
        rate_id = rate_config.get('rate_id')

        if not rate_id:
            continue

        # Find service's rate sheet
        rate_sheet = getattr(service, 'rate_sheet', None)
        if not rate_sheet:
            # Try to find via services relation
            rate_sheets = RateSheet.objects.using(db_alias).filter(
                services__id=service.id
            )
            if rate_sheets.exists():
                rate_sheet = rate_sheets.first()
            else:
                continue

        sheet_config = rate_sheet.rate_config or {}
        zones_def = sheet_config.get('zones', [])
        rates = sheet_config.get('rates', [])

        # Find matching rate_definition
        rate_definition = next(
            (c for c in rates if c.get('rate_id') == rate_id),
            None
        )

        if not rate_definition:
            continue

        # Reconstruct legacy zones from rate_definition tiers
        legacy_zones = []
        tiers = rate_definition.get('config', {}).get('tiers', [])

        for tier in tiers:
            zone_id = tier.get('zone_id')
            zone_def = next(
                (z for z in zones_def if z.get('id') == zone_id),
                None
            )

            if zone_def:
                legacy_zone = {
                    **zone_def,
                    'rate': tier.get('rate', 0),
                }

                # Add weight range if defined
                if tier.get('min_weight') is not None:
                    legacy_zone['min_weight'] = tier['min_weight']
                if tier.get('max_weight') is not None:
                    legacy_zone['max_weight'] = tier['max_weight']

                # Remove new fields that didn't exist in legacy
                legacy_zone.pop('id', None)

                legacy_zones.append(legacy_zone)

        service.zones = legacy_zones
        service.save(using=db_alias)


class Migration(migrations.Migration):
    dependencies = [
        ('providers', '0XXX_add_rate_config_fields'),  # Replace with actual previous migration
    ]

    operations = [
        migrations.RunPython(
            migrate_legacy_rate_sheets_forward,
            migrate_legacy_rate_sheets_reverse,
        ),
    ]
```

#### Step 4: Apply Migrations

```bash
# Apply all migrations
python manage.py migrate providers

# Verify migration succeeded
python manage.py showmigrations providers
```

#### Step 5: Cleanup Migration (Optional - After Verification)

After verifying the new system works in production for a reasonable period (e.g., 2-4 weeks), create a final cleanup migration to remove deprecated fields:

**Update models first** - Remove/comment out deprecated fields:

```python
class ServiceLevel(models.Model):
    # ... existing fields ...
    rate_config = models.JSONField(default=dict, blank=True)

    # REMOVE THIS LINE:
    # zones = models.JSONField(...)


class RateSheet(models.Model):
    # ... existing fields ...
    rate_config = models.JSONField(default=dict, blank=True)

    # REMOVE THESE LINES:
    # metadata = models.JSONField(...)
    # service_rates = models.JSONField(...)
```

**Generate cleanup migration**:

```bash
python manage.py makemigrations providers --name remove_legacy_rate_fields
```

Expected auto-generated migration:

```python
# Auto-generated by Django

class Migration(migrations.Migration):
    dependencies = [
        ('providers', '0XXX_migrate_legacy_rates_to_rate_config'),
    ]

    operations = [
        # Remove deprecated ServiceLevel fields
        migrations.RemoveField(
            model_name='servicelevel',
            name='zones',
        ),

        # Remove deprecated RateSheet fields
        migrations.RemoveField(
            model_name='ratesheet',
            name='metadata',
        ),
        migrations.RemoveField(
            model_name='ratesheet',
            name='service_rates',
        ),
    ]
```

---

## Coding Standards & Style Guidelines

All code changes must follow Karrio's functional programming style and documentation standards.

### Code Style Principles

1. **No Nested If Statements**
   ```python
   # ❌ BAD: Nested ifs
   def check_zone_match(zone, recipient):
       if zone.postal_codes:
           if recipient.postal_code:
               if recipient.postal_code in zone.postal_codes:
                   return True
       return False

   # ✅ GOOD: Early returns, guard clauses
   def check_zone_match(zone, recipient):
       """Check if recipient matches zone postal codes."""
       if not zone.postal_codes:
           return True  # No restrictions = matches all

       if not recipient.postal_code:
           return False

       return recipient.postal_code in zone.postal_codes
   ```

2. **Functional Programming Over Loops**
   ```python
   # ❌ BAD: For loops with mutation
   def extract_zone_ids(zones):
       zone_ids = []
       for zone in zones:
           if zone.country_codes:
               if 'US' in zone.country_codes:
                   zone_ids.append(zone.id)
       return zone_ids

   # ✅ GOOD: List comprehension
   def extract_zone_ids(zones):
       """Extract IDs of zones covering US."""
       return [
           zone.id
           for zone in zones
           if zone.country_codes and 'US' in zone.country_codes
       ]

   # ✅ GOOD: Filter + map
   def extract_zone_ids(zones):
       """Extract IDs of zones covering US."""
       us_zones = filter(
           lambda z: z.country_codes and 'US' in z.country_codes,
           zones
       )
       return list(map(lambda z: z.id, us_zones))
   ```

3. **Reusable Functions & karrio.lib Utilities**
   ```python
   # ❌ BAD: Duplicate logic, hardcoded conversions
   def calculate_rate(package, zone):
       weight = package.weight
       if package.weight_unit == 'LB':
           weight = package.weight * 0.453592  # Convert to KG

       if weight >= zone.min_weight and weight < zone.max_weight:
           return zone.rate
       return None

   # ✅ GOOD: Reuse karrio.lib, extract utilities
   import karrio.core.units as units

   def calculate_rate(package, zone, weight_unit='KG'):
       """Calculate rate if package fits zone weight range."""
       package_weight = package.weight[weight_unit]  # Units handles conversion

       return zone.rate if _fits_weight_range(
           package_weight,
           zone.min_weight,
           zone.max_weight
       ) else None

   def _fits_weight_range(weight, min_weight, max_weight):
       """Check if weight falls within range (inclusive min, exclusive max)."""
       min_ok = min_weight is None or weight >= min_weight
       max_ok = max_weight is None or weight < max_weight
       return min_ok and max_ok
   ```

4. **Compact, Declarative Code**
   ```python
   # ❌ BAD: Verbose, imperative
   def find_matching_zones(zones, recipient, package_weight):
       matching_zones = []
       for zone in zones:
           country_match = False
           if zone.country_codes:
               if recipient.country_code in zone.country_codes:
                   country_match = True
           else:
               country_match = True

           weight_match = False
           if zone.min_weight is not None:
               if package_weight >= zone.min_weight:
                   if zone.max_weight is not None:
                       if package_weight < zone.max_weight:
                           weight_match = True
                   else:
                       weight_match = True
           else:
               weight_match = True

           if country_match and weight_match:
               matching_zones.append(zone)

       return matching_zones

   # ✅ GOOD: Declarative, compact
   def find_matching_zones(zones, recipient, package_weight):
       """Find all zones matching recipient location and package weight."""
       return [
           zone for zone in zones
           if _matches_location(zone, recipient)
           and _matches_weight(zone, package_weight)
       ]

   def _matches_location(zone, recipient):
       """Check if recipient location matches zone."""
       return (
           not zone.country_codes
           or recipient.country_code in zone.country_codes
       )

   def _matches_weight(zone, weight):
       """Check if weight fits zone range."""
       return (
           (zone.min_weight is None or weight >= zone.min_weight)
           and (zone.max_weight is None or weight < zone.max_weight)
       )
   ```

### Documentation Standards

#### Module-Level Documentation

Every module must have comprehensive module-level docstring with:
- **Purpose statement**: What the module does
- **Architecture diagram**: ASCII art showing data flow
- **Core functionality**: Key features with emojis
- **Usage examples**: Practical code examples
- **Key functions overview**: Brief summary of main functions

**Template**:

```python
"""Module Title - Brief Description

Detailed description of what this module does and why it exists.

🎯 **Core Functionality**

What the module provides to the system.

📊 **Data Flow Architecture**

```
┌──────────────────────────────────────────────────────────────────┐
│                        MODULE NAME                                │
│                   Complete Data Flow Illustration                 │
└──────────────────────────────────────────────────────────────────┘

INPUT LAYER - What comes in
┌──────────────────────────────────────────────────────────────────┐
│ Input structure here                                             │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
PROCESSING LAYER - What happens
┌──────────────────────────────────────────────────────────────────┐
│ Processing steps here                                            │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
OUTPUT LAYER - What comes out
┌──────────────────────────────────────────────────────────────────┐
│ Output structure here                                            │
└──────────────────────────────────────────────────────────────────┘
```

🔧 **Usage Examples**

```python
# Example usage
```

🎯 **Key Functions Overview**

- function_name(): Brief description
- another_function(): Brief description
"""
```

#### Function-Level Documentation

Every function must have:
- **Purpose**: One-line summary
- **Flow diagram**: ASCII art for non-trivial functions
- **Args/Returns**: Type hints + descriptions
- **Examples**: Usage examples for public functions

**Example** (based on `rules_engine.py` style):

```python
def find_best_matching_zone(
    zones: List[ServiceZone],
    package: Package,
    recipient: Address,
    service: ServiceLevel,
) -> Optional[ServiceZone]:
    """Find the most specific zone that matches package and destination.

    This function implements a sophisticated zone matching algorithm that prioritizes
    specificity (postal code > city > country) and tightness of weight ranges to
    select the single best matching zone from a list of candidates.

    📊 **Processing Flow**

    ```
    INPUT: zones=[(zone_1, specificity=1000), (zone_2, specificity=100)]
    │
    ├─ STEP 1: Filter by location match
    │  ├─ Check postal codes (most specific)
    │  ├─ Check cities (medium specific)
    │  └─ Check country codes (least specific)
    │  Result: [zone_1, zone_2] → [zone_1]
    │
    ├─ STEP 2: Filter by weight range
    │  ├─ Check min_weight <= package.weight < max_weight
    │  └─ Exclude non-matching zones
    │  Result: [zone_1]
    │
    └─ STEP 3: Select best match
       ├─ Sort by: specificity (desc), weight_range (asc), rate (asc)
       └─ Return: zone_1 (highest specificity, tightest range)
    ```

    Args:
        zones: List of candidate zones to evaluate
        package: Package with weight/dimensions to match
        recipient: Destination address for location matching
        service: Service level for weight unit reference

    Returns:
        Best matching zone, or None if no matches found

    Examples:
        >>> zones = [
        ...     ServiceZone(id="us", country_codes=["US"], min_weight=0, max_weight=1),
        ...     ServiceZone(id="us_ca", country_codes=["US"], cities=["San Francisco"]),
        ... ]
        >>> package = Package(weight=Weight(0.5, "KG"))
        >>> recipient = Address(country_code="US", city="San Francisco")
        >>> zone = find_best_matching_zone(zones, package, recipient, service)
        >>> zone.id
        'us_ca'  # City match (specificity=100) beats country match (specificity=10)
    """
    # Calculate zone scores using functional approach
    scored_zones = [
        {
            'zone': zone,
            'specificity': _calculate_specificity(zone),
            'weight_range': _calculate_weight_range(zone),
            'rate': zone.rate or 0,
        }
        for zone in zones
        if _matches_location(zone, recipient)
        and _matches_weight(zone, package, service)
    ]

    # Early return if no matches
    if not scored_zones:
        return None

    # Sort by priority and return best
    best = sorted(
        scored_zones,
        key=lambda z: (-z['specificity'], z['weight_range'], z['rate'])
    )[0]

    return best['zone']
```

### Reference Files

Study these files for documentation style examples:
- `ee/insiders/modules/automation/karrio/server/automation/services/rules_engine.py`
- `ee/insiders/modules/automation/karrio/server/automation/services/scheduler.py`

---

## Error Handling & Validation

### Nullable Field Safety

All code must handle nullable fields safely to prevent 500 errors while maintaining data integrity.

#### Safe JSON Access Patterns

```python
# ❌ BAD: Direct access can cause KeyError or AttributeError
def get_rate_id(service):
    return service.rate_config['rate_id']  # KeyError if rate_config is {}

def get_zone_countries(zone):
    return zone.country_codes[0]  # IndexError if empty, TypeError if None

# ✅ GOOD: Safe access with defaults
def get_rate_id(service):
    """Get rate_definition ID from service rate config."""
    rate_config = service.rate_config or {}
    return rate_config.get('rate_id')

def get_zone_countries(zone):
    """Get zone country codes safely."""
    return (zone.country_codes or [])[0] if zone.country_codes else None

# ✅ BETTER: Use karrio.lib utilities
import karrio.lib as lib

def get_rate_id(service):
    """Get rate_definition ID from service rate config."""
    return lib.to_dict(service.rate_config).get('rate_id')
```

#### Failsafe Rate Calculation

```python
def calculate_rate_with_zone(
    package: Package,
    zone: ServiceZone,
    rate_definition: dict,
) -> Optional[float]:
    """Calculate rate with comprehensive error handling.

    Args:
        package: Package to rate
        zone: Zone definition
        rate_definition: Calculator configuration from rate_config

    Returns:
        Calculated rate or None if calculation fails
    """
    # Validate required data exists
    if not rate_definition:
        logger.warning("No rate_definition provided for rate calculation")
        return None

    rate_type = rate_definition.get('rate_type')
    if not rate_type:
        logger.warning("Calculator missing type field")
        return None

    config = rate_definition.get('config') or {}
    tiers = config.get('tiers') or []

    # Handle empty tiers
    if not tiers and rate_type == 'weight_tiered':
        logger.warning(f"Weight-tiered rate_definition has no tiers: {rate_definition.get('rate_id')}")
        return None

    # Safe tier matching
    matching_tier = _find_matching_tier(
        tiers=tiers,
        zone_id=zone.get('id') if isinstance(zone, dict) else getattr(zone, 'id', None),
        package_weight=_get_package_weight(package, config.get('weight_unit', 'KG')),
    )

    return matching_tier.get('rate') if matching_tier else None


def _get_package_weight(package, weight_unit='KG'):
    """Safely extract package weight in specified unit."""
    if not package:
        return 0.0

    try:
        # Use karrio units for safe conversion
        return package.weight[weight_unit]
    except (AttributeError, KeyError, TypeError) as e:
        logger.warning(f"Could not extract package weight: {e}")
        return 0.0


def _find_matching_tier(tiers, zone_id, package_weight):
    """Find tier matching zone and weight range."""
    if not tiers or package_weight is None:
        return None

    # Use functional approach with safe comparisons
    return next(
        (
            tier for tier in tiers
            if _tier_matches_zone(tier, zone_id)
            and _tier_matches_weight(tier, package_weight)
        ),
        None,  # Default if no match
    )


def _tier_matches_zone(tier, zone_id):
    """Check if tier matches zone (None zone_id = matches all)."""
    tier_zone = tier.get('zone_id')
    return tier_zone is None or tier_zone == zone_id


def _tier_matches_weight(tier, weight):
    """Check if weight fits tier range (handles None bounds)."""
    min_weight = tier.get('min_weight')
    max_weight = tier.get('max_weight')

    min_ok = min_weight is None or weight >= min_weight
    max_ok = max_weight is None or weight < max_weight

    return min_ok and max_ok
```

### Input Validation

All GraphQL inputs and API endpoints must validate data before database writes.

#### GraphQL Input Validation

```python
# modules/graph/karrio/server/graph/schemas/rate_sheets.py

import graphene
from karrio.server.core.validators import validate_rate_config


class CalculatorConfigInput(graphene.InputObjectType):
    """Calculator configuration input with validation."""

    rate_id = graphene.String(required=True)
    rate_type = graphene.String(required=True)
    config = graphene.JSONString(required=True)
    is_active = graphene.Boolean(default_value=True)


class RateConfigInput(graphene.InputObjectType):
    """Rate configuration input."""

    zones = graphene.List(graphene.NonNull(ZoneInput))
    rates = graphene.List(graphene.NonNull(CalculatorConfigInput))
    accessorial_charges = graphene.List(graphene.NonNull(ModifierConfigInput))


class UpdateServiceLevelInput(graphene.InputObjectType):
    """Service level update with validation."""

    rate_config = graphene.Field(RateConfigInput)

    @staticmethod
    def validate(data):
        """Validate service level input data.

        Raises:
            ValidationError: If data is invalid
        """
        rate_config = data.get('rate_config') or {}

        # Validate rate_id exists if specified
        rate_id = rate_config.get('rate_id')
        if rate_id:
            # Check rate_definition exists in rate sheet
            rates = rate_config.get('rates') or []
            rate_ids = [c.get('rate_id') for c in rates]

            if rate_id not in rate_ids:
                raise ValidationError(
                    f"rate_id '{rate_id}' not found in rate sheet rates"
                )

        # Validate zone_ids reference existing zones
        zone_ids = rate_config.get('zone_ids') or []
        zones = rate_config.get('zones') or []
        zone_id_set = {z.get('id') for z in zones if z.get('id')}

        invalid_refs = [zid for zid in zone_ids if zid not in zone_id_set]
        if invalid_refs:
            raise ValidationError(
                f"zone_ids reference non-existent zones: {invalid_refs}"
            )

        # Validate rate_definition type is valid
        rate_type = rate_config.get('rate_type')
        if rate_type:
            valid_types = ['flat', 'weight_tiered', 'distance', 'dimensional', 'composite']
            if rate_type not in valid_types:
                raise ValidationError(
                    f"Invalid rate_type '{rate_type}'. Must be one of: {valid_types}"
                )

        # Validate accessorial_charge types
        accessorial_charges = rate_config.get('accessorial_charges') or []
        valid_accessorial_types = ['fuel', 'residential', 'insurance', 'discount', 'peak_season', 'custom']

        for accessorial_charge in accessorial_charges:
            mod_type = accessorial_charge.get('accessorial_type')
            if mod_type and mod_type not in valid_accessorial_types:
                raise ValidationError(
                    f"Invalid accessorial_type '{mod_type}'. Must be one of: {valid_accessorial_types}"
                )

        return True
```

#### Model-Level Validation

```python
# modules/core/karrio/server/providers/models.py

class ServiceLevel(models.Model):
    # ... fields ...
    rate_config = models.JSONField(default=dict, blank=True)

    def clean(self):
        """Validate service level data."""
        super().clean()

        # Validate rate_config structure
        rate_config = self.rate_config or {}

        # Ensure zone_ids is a list
        zone_ids = rate_config.get('zone_ids')
        if zone_ids is not None and not isinstance(zone_ids, list):
            raise ValidationError({
                'rate_config': 'zone_ids must be a list'
            })

        # Ensure accessorial_ids is a list
        accessorial_ids = rate_config.get('accessorial_ids')
        if accessorial_ids is not None and not isinstance(accessorial_ids, list):
            raise ValidationError({
                'rate_config': 'accessorial_ids must be a list'
            })

        # Validate dim_factor is numeric if provided
        dim_factor = rate_config.get('dim_factor')
        if dim_factor is not None:
            try:
                float(dim_factor)
            except (TypeError, ValueError):
                raise ValidationError({
                    'rate_config': 'dim_factor must be a number'
                })

    def save(self, *args, **kwargs):
        """Save with validation."""
        self.full_clean()  # Run validation
        super().save(*args, **kwargs)


class RateSheet(models.Model):
    # ... fields ...
    rate_config = models.JSONField(default=dict, blank=True)

    def clean(self):
        """Validate rate sheet data."""
        super().clean()

        rate_config = self.rate_config or {}

        # Validate zones structure
        zones = rate_config.get('zones') or []
        if not isinstance(zones, list):
            raise ValidationError({
                'rate_config': 'zones must be a list'
            })

        # Validate each zone has required fields
        for idx, zone in enumerate(zones):
            if not isinstance(zone, dict):
                raise ValidationError({
                    'rate_config': f'zones[{idx}] must be an object'
                })

            if not zone.get('id'):
                raise ValidationError({
                    'rate_config': f'zones[{idx}] missing required field: id'
                })

        # Validate rates structure
        rates = rate_config.get('rates') or []
        if not isinstance(rates, list):
            raise ValidationError({
                'rate_config': 'rates must be a list'
            })

        # Validate each rate_definition
        for idx, calc in enumerate(rates):
            if not isinstance(calc, dict):
                raise ValidationError({
                    'rate_config': f'rates[{idx}] must be an object'
                })

            required_fields = ['rate_id', 'rate_type', 'config']
            for field in required_fields:
                if not calc.get(field):
                    raise ValidationError({
                        'rate_config': f'rates[{idx}] missing required field: {field}'
                    })
```

### Error Handling Best Practices

1. **Never expose internal errors to users**
   - Catch all exceptions in GraphQL resolvers
   - Log detailed errors with context
   - Return user-friendly error messages

2. **Use try-except sparingly**
   - Prefer validation and guard clauses
   - Only catch specific exceptions you can handle
   - Re-raise if you can't recover

3. **Log with context**
   ```python
   logger.error(
       f"Rate calculation failed for service {service.service_code}",
       extra={
           'service_id': service.id,
           'rate_id': rate_definition.get('rate_id'),
           'package_weight': package_weight,
           'zone_id': zone_id,
       }
   )
   ```

4. **Fail gracefully**
   - Return None for optional calculations
   - Return empty list for collection operations
   - Raise ValidationError for user input errors
   - Raise specific exceptions (ValueError, TypeError) for programming errors

---

## Testing Strategy

### Test Coverage Requirements

All new code must have comprehensive test coverage:

- **Unit tests**: 90%+ coverage for rate_definition logic, zone matching, accessorial_charges
- **Integration tests**: GraphQL API, database migrations, carrier integrations
- **End-to-end tests**: Full rate request → response flow for each carrier

### Test Files to Update

#### 1. GraphQL API Tests

**File**: `modules/graph/karrio/server/graph/tests/test_rate_sheets.py`

Add tests for new rate_config structure:

```python
class TestRateConfigMigration(GraphTestCase):
    """Test rate_config JSON structure for rate sheets and services."""

    def test_create_rate_sheet_with_rate_config(self):
        """Test creating rate sheet with new rate_config structure."""
        response = self.query(
            """
            mutation create_rate_sheet($data: CreateRateSheetMutationInput!) {
              create_rate_sheet(input: $data) {
                rate_sheet {
                  id
                  name
                  rate_config
                }
              }
            }
            """,
            variables={
                'data': {
                    'name': 'Test Rate Sheet',
                    'carrier_name': 'landmark',
                    'rate_config': {
                        'zones': [
                            {
                                'id': 'zone_us',
                                'label': 'United States',
                                'country_codes': ['US'],
                            }
                        ],
                        'rates': [
                            {
                                'rate_id': 'landmark_maxipak_us',
                                'rate_type': 'weight_tiered',
                                'config': {
                                    'currency': 'GBP',
                                    'weight_unit': 'KG',
                                    'tiers': [
                                        {
                                            'zone_id': 'zone_us',
                                            'min_weight': 0.5,
                                            'max_weight': 1.0,
                                            'rate': 8.78,
                                        }
                                    ],
                                },
                                'is_active': True,
                            }
                        ],
                        'accessorial_charges': [],
                    },
                }
            },
        )

        self.assertResponseNoErrors(response)
        rate_sheet = response.data['create_rate_sheet']['rate_sheet']

        # Verify rate_config structure
        self.assertIn('zones', rate_sheet['rate_config'])
        self.assertEqual(len(rate_sheet['rate_config']['zones']), 1)
        self.assertEqual(rate_sheet['rate_config']['zones'][0]['id'], 'zone_us')

        self.assertIn('rates', rate_sheet['rate_config'])
        self.assertEqual(len(rate_sheet['rate_config']['rates']), 1)

    def test_update_service_rate_config(self):
        """Test updating service level with rate_config."""
        # Setup: Create service with legacy zones
        service = ServiceLevel.objects.create(
            service_name='MaxiPak DDP',
            service_code='LGINTSTD',
            zones=[{'rate': 10.0, 'label': 'Old Zone'}],
        )

        # Update with new rate_config
        response = self.query(
            """
            mutation update_service($id: String!, $data: UpdateServiceLevelInput!) {
              update_service_level(id: $id, input: $data) {
                service_level {
                  id
                  rate_config
                }
              }
            }
            """,
            variables={
                'id': service.id,
                'data': {
                    'rate_config': {
                        'zone_ids': ['zone_us'],
                        'rate_id': 'landmark_maxipak_us',
                        'accessorial_ids': ['fuel_2025q1'],
                        'dim_factor': 6000,
                    }
                },
            },
        )

        self.assertResponseNoErrors(response)
        updated_config = response.data['update_service_level']['service_level']['rate_config']

        self.assertEqual(updated_config['zone_ids'], ['zone_us'])
        self.assertEqual(updated_config['rate_id'], 'landmark_maxipak_us')
        self.assertEqual(updated_config['dim_factor'], 6000)

    def test_rate_config_validation_errors(self):
        """Test validation errors for invalid rate_config."""
        response = self.query(
            """
            mutation create_rate_sheet($data: CreateRateSheetMutationInput!) {
              create_rate_sheet(input: $data) {
                rate_sheet { id }
              }
            }
            """,
            variables={
                'data': {
                    'name': 'Invalid Rate Sheet',
                    'carrier_name': 'test',
                    'rate_config': {
                        'rates': [
                            {
                                'rate_id': 'test_calc',
                                'rate_type': 'invalid_type',  # Invalid!
                                'config': {},
                            }
                        ],
                    },
                }
            },
        )

        # Should return validation error
        self.assertResponseHasErrors(response)
        self.assertIn('Invalid rate_type', str(response.errors))

    def test_dimensional_weight_calculation(self):
        """Test rate calculation with dimensional weight."""
        # Setup rate sheet with dim_factor
        rate_sheet = self.create_rate_sheet_with_dim_weight(dim_factor=6000)

        # Request rate for package with dimensions
        response = self.query(
            """
            query get_rates($data: RateRequestInput!) {
              get_rates(input: $data) {
                rates {
                  service
                  total_charge
                  meta {
                    billable_weight
                    actual_weight
                    dimensional_weight
                  }
                }
              }
            }
            """,
            variables={
                'data': {
                    'recipient': {'country_code': 'US', 'postal_code': '10001'},
                    'parcels': [
                        {
                            'weight': 1.0,
                            'weight_unit': 'KG',
                            'length': 30,
                            'width': 20,
                            'height': 15,
                            'dimension_unit': 'CM',
                        }
                    ],
                }
            },
        )

        self.assertResponseNoErrors(response)
        rate = response.data['get_rates']['rates'][0]

        # Verify dimensional weight calculation
        # (30 * 20 * 15) / 6000 = 1.5 kg
        # Billable weight = max(1.0, 1.5) = 1.5 kg
        self.assertEqual(rate['meta']['dimensional_weight'], 1.5)
        self.assertEqual(rate['meta']['billable_weight'], 1.5)
```

#### 2. Rating Proxy Tests

**File**: `modules/sdk/tests/core/test_universal_rate.py`

Add tests for new zone/rate_definition separation:

```python
def test_rate_config_zone_matching(self):
    """Test zone matching with new rate_config structure."""
    settings_with_rate_config = RatingMixinSettings(**rate_config_settings_data)
    proxy = RatingMixinProxy(settings_with_rate_config)

    request = Serializable(
        RateRequest(
            shipper={'postal_code': 'H8Z 2Z3', 'country_code': 'CA'},
            recipient={'postal_code': '10001', 'country_code': 'US'},
            parcels=[{'weight': 0.75, 'weight_unit': 'KG'}],
        )
    )

    response = proxy.get_rates(request)
    rates = parse_rate_response(response, settings_with_rate_config)

    # Should find matching zone and rate_definition
    self.assertEqual(len(rates[0]), 1)
    self.assertEqual(rates[0][0]['service'], 'landmark_maxipak')


def test_calculator_not_found_returns_no_rate(self):
    """Test that missing rate_definition returns no rate instead of error."""
    settings = RatingMixinSettings(**{
        'carrier_id': 'test',
        'services': [
            {
                'service_name': 'Test Service',
                'service_code': 'test_service',
                'rate_config': {
                    'zone_ids': ['zone_us'],
                    'rate_id': 'nonexistent_calculator',  # Doesn't exist!
                },
            }
        ],
        'rate_config': {
            'zones': [{'id': 'zone_us', 'country_codes': ['US']}],
            'rates': [],  # Empty!
        },
    })
    proxy = RatingMixinProxy(settings)

    request = Serializable(RateRequest(
        recipient={'country_code': 'US'},
        parcels=[{'weight': 1.0}],
    ))

    response = proxy.get_rates(request)
    rates, errors = parse_rate_response(response, settings)

    # Should return empty rates, not crash
    self.assertEqual(len(rates), 0)
    self.assertEqual(len(errors), 0)  # No errors, just no matching rate


def test_null_rate_config_fallback_to_legacy(self):
    """Test that null rate_config falls back to legacy zones."""
    settings = RatingMixinSettings(**{
        'carrier_id': 'test',
        'services': [
            {
                'service_name': 'Legacy Service',
                'service_code': 'legacy',
                'zones': [  # Old format
                    {
                        'rate': 10.0,
                        'country_codes': ['US'],
                        'min_weight': 0,
                        'max_weight': 5,
                    }
                ],
                'rate_config': None,  # Not migrated yet
            }
        ],
    })
    proxy = RatingMixinProxy(settings)

    request = Serializable(RateRequest(
        recipient={'country_code': 'US'},
        parcels=[{'weight': 1.0}],
    ))

    response = proxy.get_rates(request)
    rates = parse_rate_response(response, settings)

    # Should still work with legacy zones
    self.assertEqual(len(rates[0]), 1)
    self.assertEqual(rates[0][0]['total_charge'], 10.0)
```

#### 3. Carrier-Specific Tests

For each migrated carrier, add tests in:
- `modules/connectors/{carrier}/tests/{carrier}/test_rate.py`

**Template** (using Landmark as example):

```python
class TestLandmarkRateConfig(unittest.TestCase):
    """Test Landmark rate calculation with new rate_config structure."""

    def setUp(self):
        """Load services from new rate_config format."""
        from karrio.providers.landmark import units
        self.services = units.DEFAULT_SERVICES

    def test_rate_config_structure(self):
        """Test that services have rate_config populated."""
        service = next(
            (s for s in self.services if s.service_code == 'LGINTSTD'),
            None
        )

        self.assertIsNotNone(service)
        self.assertIsNotNone(service.rate_config)

        # Check rate_config structure
        self.assertIn('zone_ids', service.rate_config)
        self.assertIn('rate_id', service.rate_config)
        self.assertIsInstance(service.rate_config['zone_ids'], list)

    def test_calculator_zone_tier_matching(self):
        """Test rate calculation with rate_definition + zone + weight tier."""
        service = self.services[0]
        rate_config = service.rate_config

        # Find rate_definition from rate sheet
        rate_id = rate_config.get('rate_id')
        self.assertIsNotNone(rate_id)

        # Verify rate_definition can be resolved
        # (This would use the actual rating proxy in real test)
        self.assertIsNotNone(rate_id)

    def test_dim_factor_configuration(self):
        """Test dimensional weight factor is configured."""
        service = next(
            (s for s in self.services if s.service_code == 'LGINTSTD'),
            None
        )

        dim_factor = service.rate_config.get('dim_factor')
        # Landmark uses metric, so default should be 6000
        self.assertEqual(dim_factor, 6000)

    def test_modifier_application(self):
        """Test rate accessorial_charges are applied correctly."""
        # This test would verify fuel surcharge, residential fee, etc.
        # are properly applied from rate_config.accessorial_charges
        pass
```

### Testing Checklist

For each carrier migration:

- [ ] Unit tests for CSV loading
- [ ] Unit tests for rate_config structure validation
- [ ] Integration tests for zone matching
- [ ] Integration tests for weight tier matching
- [ ] Integration tests for dimensional weight (if applicable)
- [ ] Integration tests for accessorial_charges (fuel, residential, etc.)
- [ ] End-to-end GraphQL API tests
- [ ] Migration data integrity tests (legacy → new format)
- [ ] Backward compatibility tests (during transition period)
- [ ] Error handling tests (null/missing data)

### Test Data Requirements

Each carrier test suite must include:

1. **Minimal valid request**: Simplest possible rate request that works
2. **Complex multi-tier request**: Package matching multiple weight tiers
3. **Boundary cases**: Weights exactly on tier boundaries
4. **Invalid requests**: Missing data, invalid countries, overweight packages
5. **Edge cases**: Empty zones, null rates, missing accessorial_charges

---

## SDK/Core Changes

### 1. New Models (modules/sdk/karrio/core/models.py)

```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass
class RateDefinition(ABC):
    """Abstract base class for rate calculation strategies."""

    rate_id: str
    rate_type: str
    currency: str
    weight_unit: str = "KG"
    dimension_unit: str = "CM"
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @abstractmethod
    def calculate(
        self,
        package: "Package",
        origin: "Address",
        destination: "Address",
        zone: "ServiceZone",
        context: Dict[str, Any]
    ) -> float:
        """Calculate base rate for shipment."""
        pass


@dataclass
class FlatRate(RateDefinition):
    """Simple flat rate pricing."""

    def __post_init__(self):
        self.rate_type = "flat"

    @property
    def rate(self) -> float:
        return self.config.get("rate", 0.0)

    def calculate(self, package, origin, destination, zone, context):
        return self.rate


@dataclass
class WeightTieredRate(RateDefinition):
    """Weight-based tiered pricing."""

    def __post_init__(self):
        self.rate_type = "weight_tiered"

    @property
    def tiers(self) -> List[Dict[str, Any]]:
        return self.config.get("tiers", [])

    def calculate(self, package, origin, destination, zone, context):
        import karrio.core.units as units

        package_weight = package.weight[self.weight_unit]

        # Find matching tier for this zone
        for tier in self.tiers:
            # Skip if tier doesn't match this zone
            if tier.get("zone_id") and tier["zone_id"] != zone.id:
                continue

            min_weight = tier.get("min_weight")
            max_weight = tier.get("max_weight")

            # Check weight match (inclusive min, exclusive max)
            if min_weight is not None and package_weight < min_weight:
                continue
            if max_weight is not None and package_weight >= max_weight:
                continue

            return tier.get("rate", 0.0)

        # No matching tier
        raise ValueError(
            f"No rate tier found for {package_weight}{self.weight_unit} "
            f"to zone {zone.label}"
        )


@dataclass
class DimensionalWeightRate(RateDefinition):
    """
    Dimensional weight-based pricing.

    Uses the greater of actual weight or dimensional weight (volumetric weight).
    Formula: (width × height × length) / dim_factor

    Industry standard:
    - Metric (cm/kg): dim_factor = 6000 (1 m³ = 166.67 kg)
    - Imperial (in/lb): dim_factor = 166 (1 ft³ = 10.4 lb)

    Reference: https://en.wikipedia.org/wiki/Dimensional_weight
    """

    def __post_init__(self):
        self.rate_type = "dimensional_weight"

    @property
    def dim_factor(self) -> float:
        """
        Dimensional weight divisor.

        Default values:
        - Metric (cm³/kg): 6000
        - Imperial (in³/lb): 166
        """
        return self.config.get("dim_factor", 6000)

    @property
    def tiers(self) -> List[Dict[str, Any]]:
        """Weight tiers to apply after calculating billable weight."""
        return self.config.get("tiers", [])

    def calculate_dimensional_weight(
        self,
        package: "Package",
    ) -> float:
        """
        Calculate dimensional weight.

        Formula: (length × width × height) / dim_factor

        Args:
            package: Package with dimensions

        Returns:
            Dimensional weight in service's weight unit
        """
        import karrio.core.units as units

        # Get dimensions in service's dimension unit
        length = package.length[self.dimension_unit]
        width = package.width[self.dimension_unit]
        height = package.height[self.dimension_unit]

        # Calculate volume
        volume = length * width * height

        # Calculate dimensional weight
        dim_weight = volume / self.dim_factor

        return dim_weight

    def calculate_billable_weight(
        self,
        package: "Package",
    ) -> float:
        """
        Calculate billable weight (max of actual or dimensional).

        Args:
            package: Package with weight and dimensions

        Returns:
            Billable weight in service's weight unit
        """
        # Get actual weight
        actual_weight = package.weight[self.weight_unit]

        # Calculate dimensional weight
        dim_weight = self.calculate_dimensional_weight(package)

        # Return the greater of the two
        billable_weight = max(actual_weight, dim_weight)

        return billable_weight

    def calculate(self, package, origin, destination, zone, context):
        """
        Calculate rate using billable weight (max of actual or dimensional).

        Args:
            package: Package with weight and dimensions
            origin: Origin address
            destination: Destination address
            zone: Service zone
            context: Additional context

        Returns:
            Rate based on billable weight tier
        """
        # Calculate billable weight
        billable_weight = self.calculate_billable_weight(package)

        # Store billable weight in context for reference
        context["billable_weight"] = billable_weight
        context["actual_weight"] = package.weight[self.weight_unit]
        context["dimensional_weight"] = self.calculate_dimensional_weight(package)
        context["dim_factor"] = self.dim_factor

        # Find matching tier based on billable weight
        for tier in self.tiers:
            # Skip if tier doesn't match this zone
            if tier.get("zone_id") and tier["zone_id"] != zone.id:
                continue

            min_weight = tier.get("min_weight")
            max_weight = tier.get("max_weight")

            # Check weight match (inclusive min, exclusive max)
            if min_weight is not None and billable_weight < min_weight:
                continue
            if max_weight is not None and billable_weight >= max_weight:
                continue

            return tier.get("rate", 0.0)

        # No matching tier
        raise ValueError(
            f"No rate tier found for billable weight {billable_weight}{self.weight_unit} "
            f"(actual: {package.weight[self.weight_unit]}{self.weight_unit}, "
            f"dimensional: {self.calculate_dimensional_weight(package)}{self.weight_unit}) "
            f"to zone {zone.label}"
        )


@dataclass
class AccessorialCharge(ABC):
    """Abstract base class for accessorial charges (surcharges, fees, discounts)."""

    accessorial_id: str
    accessorial_type: str
    config: Dict[str, Any] = field(default_factory=dict)
    applies_to_services: List[str] = field(default_factory=list)
    priority: int = 0

    @abstractmethod
    def apply(
        self,
        base_rate: float,
        package: "Package",
        origin: "Address",
        destination: "Address",
        context: Dict[str, Any]
    ) -> float:
        """Apply accessorial charge and return adjusted rate."""
        pass

    def applies_to_service(self, service_code: str) -> bool:
        """Check if this accessorial charge applies to a service."""
        if "*" in self.applies_to_services:
            return True
        return service_code in self.applies_to_services


@dataclass
class FuelSurcharge(AccessorialCharge):
    """Fuel surcharge accessorial (percentage-based)."""

    def __post_init__(self):
        self.accessorial_type = "fuel_surcharge"

    @property
    def surcharge_percent(self) -> float:
        return self.config.get("percent", 0.0)

    def apply(self, base_rate, package, origin, destination, context):
        surcharge = base_rate * (self.surcharge_percent / 100)
        return base_rate + surcharge


@dataclass
class ResidentialDeliveryFee(AccessorialCharge):
    """Residential delivery fee accessorial (flat fee)."""

    def __post_init__(self):
        self.accessorial_type = "residential_delivery_fee"

    @property
    def surcharge_amount(self) -> float:
        return self.config.get("amount", 0.0)

    def apply(self, base_rate, package, origin, destination, context):
        if getattr(destination, 'residential', False):
            return base_rate + self.surcharge_amount
        return base_rate


@dataclass
class ServiceZone:
    """Zone definition - eligibility criteria only (NO rate)."""

    id: str  # NEW: Unique zone identifier
    label: Optional[str] = None
    rate: Optional[float] = None  # DEPRECATED - will be removed

    # Geographic criteria
    cities: List[str] = field(default_factory=list)
    postal_codes: List[str] = field(default_factory=list)
    country_codes: List[str] = field(default_factory=list)

    # Physical restrictions (optional - can be in rate_definition)
    min_weight: Optional[float] = None
    max_weight: Optional[float] = None

    # Service attributes
    transit_days: Optional[int] = None
    transit_time: Optional[float] = None

    # Metadata
    radius: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class ServiceLevel:
    """Shipping service with decoupled pricing."""

    # Service identity
    service_code: str
    service_name: str
    carrier_id: Optional[str] = None
    carrier_service_code: Optional[str] = None

    # Zones (eligibility)
    zone_ids: List[str] = field(default_factory=list)  # NEW
    zones: List[ServiceZone] = field(default_factory=list)  # DEPRECATED

    # Pricing (NEW)
    rate_id: Optional[str] = None
    rate_definition: Optional["RateDefinition"] = None
    accessorial_charge_ids: List[str] = field(default_factory=list)
    accessorial_charges: List[AccessorialCharge] = field(default_factory=list)

    # Service restrictions
    currency: Optional[str] = None
    active: bool = True
    max_weight: Optional[float] = None
    max_length: Optional[float] = None
    max_height: Optional[float] = None
    max_width: Optional[float] = None
    min_weight: Optional[float] = None
    weight_unit: Optional[str] = None
    dimension_unit: Optional[str] = None
    domicile: Optional[bool] = None
    international: Optional[bool] = None
    transit_days: Optional[int] = None

    # NEW: Dimensional weight configuration
    dim_factor: Optional[float] = None  # Default: 6000 for metric, 166 for imperial

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RateSheet:
    """
    Complete rate sheet definition with zones, rates, accessorial charges, and services.

    This is a RUNTIME-ONLY dataclass, NOT a database model.
    Each carrier defines DEFAULT_RATESHEET in their SDK code.
    """

    carrier_name: str
    zones: List[ServiceZone] = field(default_factory=list)
    rates: List["RateDefinition"] = field(default_factory=list)
    accessorial_charges: List[AccessorialCharge] = field(default_factory=list)
    services: List[ServiceLevel] = field(default_factory=list)

    def get_zone(self, zone_id: str) -> Optional[ServiceZone]:
        """Get zone by ID."""
        return next((z for z in self.zones if z.id == zone_id), None)

    def get_rate(self, rate_id: str) -> Optional["RateDefinition"]:
        """Get rate definition by ID."""
        return next((r for r in self.rates if r.rate_id == rate_id), None)

    def get_accessorial_charge(self, accessorial_id: str) -> Optional[AccessorialCharge]:
        """Get accessorial charge by ID."""
        return next((a for a in self.accessorial_charges if a.accessorial_id == accessorial_id), None)
```

**IMPORTANT**: These classes (`RateDefinition`, `AccessorialCharge`, `ServiceZone`, `RateSheet`) are **runtime-only dataclasses**, not Django database models. They are:

- Defined in `modules/sdk/karrio/core/models.py`
- Used at runtime for rate calculation
- Stored as JSON in the `rate_config` field of the database
- **Never** queried with `.objects.get()` or `.objects.filter()`

Each carrier defines a `DEFAULT_RATESHEET` constant that populates these structures from CSV files at module import time.

### 2. DEFAULT_RATESHEET Pattern (Per-Carrier SDK Implementation)

Each carrier defines their DEFAULT_RATESHEET in their units module. Example for Landmark:

**modules/connectors/landmark/karrio/providers/landmark/units.py**

```python
import csv
import os
from pathlib import Path
from typing import List
from karrio.core.models import (
    RateSheet,
    ServiceZone,
    WeightTieredRate,
    FuelSurcharge,
    ResidentialDeliveryFee,
    ServiceLevel,
)

# --- CSV Loading Functions ---

def load_services_from_csv() -> List[ServiceLevel]:
    """
    Load service definitions from CSV.

    CSV structure (services.csv):
    service_code,service_name,max_weight,dim_factor,rate_id,accessorial_ids
    LGINTSTD,MaxiPak Scan DDP,30.0,6000,landmark_maxipak_intl,"fuel_2025q1,residential"
    """
    csv_path = Path(__file__).parent / "services.csv"
    services = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            accessorial_ids = [
                m.strip()
                for m in row.get('accessorial_ids', '').split(',')
                if m.strip()
            ]

            services.append(ServiceLevel(
                service_code=row['service_code'],
                service_name=row['service_name'],
                max_weight=float(row.get('max_weight', 0)) if row.get('max_weight') else None,
                rate_id=row.get('rate_id'),
                accessorial_ids=accessorial_ids,
                dim_factor=float(row.get('dim_factor', 6000)) if row.get('dim_factor') else None,
            ))

    return services


def load_rate_tiers_from_csv() -> dict:
    """
    Load rate tiers from CSV and group by rate_id.

    CSV structure (rate_tiers.csv):
    rate_id,zone_id,min_weight,max_weight,rate
    landmark_maxipak_intl,zone_us,0.5,1.0,8.78
    landmark_maxipak_intl,zone_us,1.0,2.0,10.81
    """
    csv_path = Path(__file__).parent / "rate_tiers.csv"
    tiers_by_calculator = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rate_id = row['rate_id']

            if rate_id not in tiers_by_calculator:
                tiers_by_calculator[rate_id] = []

            tier = {
                'zone_id': row['zone_id'],
                'rate': float(row['rate']),
            }

            if row.get('min_weight'):
                tier['min_weight'] = float(row['min_weight'])
            if row.get('max_weight'):
                tier['max_weight'] = float(row['max_weight'])

            tiers_by_calculator[rate_id].append(tier)

    return tiers_by_calculator


# --- DEFAULT_RATESHEET Definition ---

# Load rate tiers from CSV
_RATE_TIERS = load_rate_tiers_from_csv()

DEFAULT_RATESHEET = RateSheet(
    carrier_name="landmark",

    # Zone definitions (hardcoded logic)
    zones=[
        ServiceZone(id="zone_us", label="United States", country_codes=["US"], transit_days=7),
        ServiceZone(id="zone_eu1", label="EU Zone 1", country_codes=["DE", "FR", "BE", "NL"], transit_days=5),
        ServiceZone(id="zone_eu2", label="EU Zone 2", country_codes=["ES", "IT", "PL", "PT"], transit_days=6),
        # ... more zones ...
    ],

    # Calculator definitions (logic hardcoded, tiers from CSV)
    rates=[
        WeightTieredRate(
            rate_id="landmark_maxipak_intl",
            rate_type="weight_tiered",
            currency="GBP",
            weight_unit="KG",
            dimension_unit="CM",
            config={
                "tiers": _RATE_TIERS.get("landmark_maxipak_intl", [])  # Loaded from CSV
            },
        ),
        # ... more rates ...
    ],

    # Modifier definitions (logic hardcoded, percentages have defaults)
    accessorial_charges=[
        FuelSurcharge(
            accessorial_id="fuel_2025q1",
            accessorial_type="fuel",
            config={"percent": 8.5},  # Default value, can be overridden in rate_config
            applies_to_services=["LGINTSTD", "LGINTSTDU"],
            priority=10,
        ),
        ResidentialDeliveryFee(
            accessorial_id="residential",
            accessorial_type="residential",
            config={"amount": 3.95},  # Default value, can be overridden
            applies_to_services=["*"],  # All services
            priority=20,
        ),
    ],

    # Service definitions (loaded from CSV)
    services=load_services_from_csv(),
)

# Deprecate DEFAULT_SERVICES (replaced by DEFAULT_RATESHEET)
# DEFAULT_SERVICES = [...]  # REMOVED
```

**Key Points**:

1. **Logic in Code**: Zone definitions, rate_definition types, accessorial_charge types are hardcoded in DEFAULT_RATESHEET
2. **Rates from CSV**: Only numbers (rates, weight ranges) come from CSV files
3. **CSV Structure**:
   - `services.csv`: service definitions (name, code, max_weight, rate_id, accessorial_ids)
   - `rate_tiers.csv`: rate tiers (rate_id, zone_id, min_weight, max_weight, rate)
4. **Defaults**: Modifiers have default percentages/amounts but can be overridden in rate_config
5. **Runtime Loading**: CSVs are loaded at module import time, once per process

### 3. Updated Rating Proxy (modules/sdk/karrio/universal/mappers/rating_proxy.py)

```python
def get_available_rates(
    package: units.Package,
    shipper: units.ComputedAddress,
    recipient: units.ComputedAddress,
    settings: RatingMixinSettings,
    is_domicile: bool = None,
    is_international: bool = None,
    selected_services: typing.List[str] = [],
    context: dict = None,
) -> PackageRates:
    """
    Get available rates using new rate_definition-based system.
    """
    errors: typing.List[models.Message] = []
    rates: typing.List[models.RateDetails] = []
    services = [svc for svc in settings.shipping_services if svc.active]
    context = context or {}

    for service in services:
        # Check service eligibility (same as before)
        explicitly_requested = service.service_code in selected_services
        implicitly_requested = len(selected_services or []) == 0
        excluded = len(selected_services or []) > 0 and not explicitly_requested

        if not service.active or excluded:
            continue

        # Check destination coverage
        cover_domestic_shipment = (
            service.domicile is True and service.domicile == is_domicile
        )
        cover_international_shipment = (
            service.international is True and service.international == is_international
        )
        cover_all_destination = (
            service.domicile is None and service.international is None
        )

        destination_covered = (
            cover_domestic_shipment
            or cover_international_shipment
            or cover_all_destination
        )

        if not destination_covered:
            if explicitly_requested:
                errors.append(
                    models.Message(
                        carrier_id=settings.carrier_id,
                        code="destination_not_supported",
                        message=f"Service {service.service_code} does not cover destination"
                    )
                )
            continue

        # Validate package dimensions and weight against SERVICE level restrictions
        # (same as before)

        # NEW: Find matching zone (eligibility only)
        selected_zone: typing.Optional[models.ServiceZone] = find_best_matching_zone(
            zones=service.zones or [],
            package=package,
            recipient=recipient,
            service=service,
        )

        if selected_zone is None:
            if explicitly_requested:
                errors.append(
                    models.Message(
                        carrier_id=settings.carrier_id,
                        code="no_matching_zone",
                        message=f"No zone found for destination"
                    )
                )
            continue

        # NEW: Calculate base rate using rate_definition
        try:
            if not service.rate_definition:
                errors.append(
                    models.Message(
                        carrier_id=settings.carrier_id,
                        code="no_calculator",
                        message=f"Service {service.service_code} has no rate rate_definition"
                    )
                )
                continue

            base_rate = service.rate_definition.calculate(
                package=package,
                origin=shipper,
                destination=recipient,
                zone=selected_zone,
                context=context,
            )

        except ValueError as e:
            if explicitly_requested:
                errors.append(
                    models.Message(
                        carrier_id=settings.carrier_id,
                        code="calculation_error",
                        message=str(e)
                    )
                )
            continue

        # NEW: Apply accessorial_charges
        final_rate = base_rate
        surcharges = []

        for accessorial_charge in sorted(service.accessorial_charges, key=lambda m: m.priority):
            if not accessorial_charge.applies_to_service(service.service_code):
                continue

            try:
                adjusted_rate = accessorial_charge.apply(
                    base_rate=final_rate,
                    package=package,
                    origin=shipper,
                    destination=recipient,
                    context=context,
                )

                # Track surcharge
                surcharge_amount = adjusted_rate - final_rate
                if surcharge_amount != 0:
                    surcharges.append({
                        "type": accessorial_charge.accessorial_type,
                        "name": accessorial_charge.accessorial_id,
                        "amount": surcharge_amount,
                    })

                final_rate = adjusted_rate

            except Exception as e:
                # Log warning but don't fail the rate
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(
                    f"Failed to apply accessorial_charge {accessorial_charge.accessorial_id}: {e}"
                )

        # Create rate details
        carrier_name = getattr(settings, "custom_carrier_name", settings.carrier_name)
        transit_days = (
            service.transit_days
            if selected_zone.transit_days is None
            else selected_zone.transit_days
        )

        rates.append(
            models.RateDetails(
                carrier_name=carrier_name,
                carrier_id=settings.carrier_id,
                service=service.service_code,
                currency=service.currency or service.rate_definition.currency,
                transit_days=transit_days,
                base_charge=base_rate,
                extra_charges=surcharges,
                total_charge=final_rate,
                meta=dict(
                    service_name=service.service_name,
                    zone=selected_zone.label,
                ),
            )
        )

    return rates, errors
```

### 3. Calculator Factory (modules/sdk/karrio/core/calculator_factory.py)

```python
"""Factory for creating rate rates from config."""

import karrio.core.models as models
from typing import Dict, Any

RATE_REGISTRY = {
    "flat": models.FlatRate,
    "weight_tiered": models.WeightTieredRate,
    "dimensional": models.DimensionalWeightRate,
    # Add more as implemented: distance, composite, etc.
}

def create_rate_definition(config: Dict[str, Any]) -> models.RateDefinition:
    """
    Create a rate_definition instance from config dict.

    Args:
        config: Calculator configuration
            {
                "rate_id": "landmark_us",
                "rate_type": "weight_tiered",
                "currency": "GBP",
                "weight_unit": "KG",
                "config": {"tiers": [...]},
                ...
            }

    Returns:
        RateDefinition instance
    """
    rate_type = config.get("rate_type")

    if rate_type not in RATE_REGISTRY:
        raise ValueError(f"Unknown rate_definition type: {rate_type}")

    rate_class = RATE_REGISTRY[rate_type]

    return rate_class(
        rate_id=config["rate_id"],
        rate_type=rate_type,
        currency=config.get("currency", "USD"),
        weight_unit=config.get("weight_unit", "KG"),
        dimension_unit=config.get("dimension_unit", "CM"),
        config=config.get("config", {}),
        metadata=config.get("metadata", {}),
    )


def create_accessorial_charge(config: Dict[str, Any]) -> models.AccessorialCharge:
    """Create a accessorial_charge instance from config dict."""

    ACCESSORIAL_CHARGE_REGISTRY = {
        "fuel": models.FuelSurcharge,
        "residential": models.ResidentialDeliveryFee,
        # Add more as implemented
    }

    accessorial_type = config.get("accessorial_type")

    if accessorial_type not in ACCESSORIAL_CHARGE_REGISTRY:
        raise ValueError(f"Unknown accessorial_charge type: {accessorial_type}")

    accessorial_class = ACCESSORIAL_CHARGE_REGISTRY[accessorial_type]

    return accessorial_class(
        accessorial_id=config["accessorial_id"],
        accessorial_type=accessorial_type,
        config=config.get("config", {}),
        applies_to_services=config.get("applies_to_services", []),
        priority=config.get("priority", 0),
    )
```

---

## Carrier Integration Changes

### DEFAULT_RATESHEET Architecture

Each of the 9 carriers must define a `DEFAULT_RATESHEET` in their `units.py` module. This replaces the legacy `DEFAULT_SERVICES` pattern.

**Key principles**:
1. **Pricing logic in code**: Zone definitions, rate_definition types, accessorial_charge types are hardcoded in DEFAULT_RATESHEET
2. **Rates in CSV**: Only the numbers (rates, weight ranges) come from CSV files
3. **Two CSV files**: `services.csv` (service definitions) + `rate_tiers.csv` (rate data)
4. **No zones.csv, rates/, or accessorial_charges.csv** - this logic is in DEFAULT_RATESHEET

### File Structure

```
modules/connectors/{carrier}/karrio/providers/{carrier}/
├── services.csv      # Service definitions
├── rate_tiers.csv    # Rate tiers (rates + weight ranges)
└── units.py          # DEFAULT_RATESHEET definition
```

### CSV Format

#### 1. services.csv

```csv
service_code,service_name,max_weight,dim_factor,rate_id,accessorial_ids
LGINTSTD,MaxiPak Scan DDP,30.0,6000,landmark_maxipak_intl,"fuel_2025q1,residential"
LGINTSTDU,MaxiPak Scan DDU,30.0,6000,landmark_maxipak_intl,"fuel_2025q1"
LGINTBPIP,MiniPak Scan DDP,2.0,,landmark_minipak_eu,"fuel_2025q1"
LGINTBPIU,MiniPak Scan DDU,2.0,,landmark_minipak_eu,"fuel_2025q1"
```

**Fields**:
- `service_code`: Unique service identifier
- `service_name`: Human-readable service name
- `max_weight`: Maximum package weight (optional)
- `dim_factor`: Dimensional weight divisor (optional - 6000 for metric, 166 for imperial)
- `rate_id`: ID of rate_definition defined in DEFAULT_RATESHEET
- `accessorial_ids`: Comma-separated list of accessorial_charge IDs (defined in DEFAULT_RATESHEET)

#### 2. rate_tiers.csv

```csv
rate_id,zone_id,min_weight,max_weight,rate
landmark_maxipak_intl,zone_us,0.0,0.25,5.71
landmark_maxipak_intl,zone_us,0.25,0.5,6.86
landmark_maxipak_intl,zone_us,0.5,1.0,8.78
landmark_maxipak_intl,zone_us,1.0,2.0,10.81
landmark_maxipak_intl,zone_us,2.0,5.0,15.39
landmark_maxipak_intl,zone_us,5.0,10.0,28.82
landmark_maxipak_intl,zone_us,10.0,20.0,87.80
landmark_maxipak_intl,zone_us,20.0,30.0,165.76
landmark_maxipak_intl,zone_eu1,0.0,0.25,3.35
landmark_maxipak_intl,zone_eu1,0.25,0.5,4.02
landmark_maxipak_intl,zone_eu1,0.5,1.0,5.16
```

**Fields**:
- `rate_id`: References rate_definition defined in DEFAULT_RATESHEET
- `zone_id`: References zone defined in DEFAULT_RATESHEET
- `min_weight`: Tier minimum weight (inclusive)
- `max_weight`: Tier maximum weight (exclusive)
- `rate`: Price for this tier/zone

### Complete Implementation Example (Landmark)

**modules/connectors/landmark/karrio/providers/landmark/units.py**

```python
import csv
from pathlib import Path
from typing import List, Dict
from karrio.core.models import (
    RateSheet,
    ServiceZone,
    ServiceLevel,
    WeightTieredRate,
    FuelSurcharge,
    ResidentialDeliveryFee,
)

# --- Helper Functions ---

def load_rate_tiers_from_csv() -> Dict[str, List[dict]]:
    """
    Load rate tiers from CSV and group by rate_id.

    Returns:
        Dictionary mapping rate_id to list of tier dicts
    """
    csv_path = Path(__file__).parent / "rate_tiers.csv"
    tiers_by_calculator = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rate_id = row['rate_id']

            if rate_id not in tiers_by_calculator:
                tiers_by_calculator[rate_id] = []

            tier = {
                'zone_id': row['zone_id'],
                'rate': float(row['rate']),
            }

            if row.get('min_weight'):
                tier['min_weight'] = float(row['min_weight'])
            if row.get('max_weight'):
                tier['max_weight'] = float(row['max_weight'])

            tiers_by_calculator[rate_id].append(tier)

    return tiers_by_calculator


def load_services_from_csv() -> List[ServiceLevel]:
    """
    Load service definitions from CSV.

    Returns:
        List of ServiceLevel objects
    """
    csv_path = Path(__file__).parent / "services.csv"
    services = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            accessorial_ids = [
                m.strip()
                for m in row.get('accessorial_ids', '').split(',')
                if m.strip()
            ]

            services.append(ServiceLevel(
                service_code=row['service_code'],
                service_name=row['service_name'],
                max_weight=float(row['max_weight']) if row.get('max_weight') else None,
                rate_id=row.get('rate_id'),
                accessorial_ids=accessorial_ids,
                dim_factor=float(row['dim_factor']) if row.get('dim_factor') else None,
            ))

    return services


# --- DEFAULT_RATESHEET Definition ---

# Load rate tiers from CSV at module import time
_RATE_TIERS = load_rate_tiers_from_csv()

DEFAULT_RATESHEET = RateSheet(
    carrier_name="landmark",

    # Zone definitions - HARDCODED LOGIC (not in CSV)
    zones=[
        ServiceZone(
            id="zone_us",
            label="United States",
            country_codes=["US"],
            transit_days=7
        ),
        ServiceZone(
            id="zone_eu1",
            label="EU Zone 1",
            country_codes=["DE", "FR", "BE", "NL", "AT", "DK"],
            transit_days=3
        ),
        ServiceZone(
            id="zone_eu2",
            label="EU Zone 2",
            country_codes=["ES", "IT", "PT", "SE", "FI", "NO", "IE"],
            transit_days=5
        ),
        ServiceZone(
            id="zone_au",
            label="Australia",
            country_codes=["AU"],
            transit_days=12
        ),
        ServiceZone(
            id="zone_ca",
            label="Canada",
            country_codes=["CA"],
            transit_days=5
        ),
    ],

    # Calculator definitions - HARDCODED LOGIC + CSV RATES
    rates=[
        WeightTieredRate(
            rate_id="landmark_maxipak_intl",
            rate_type="weight_tiered",
            currency="GBP",
            weight_unit="KG",
            dimension_unit="CM",
            config={
                "tiers": _RATE_TIERS.get("landmark_maxipak_intl", [])
            },
        ),
        WeightTieredRate(
            rate_id="landmark_minipak_eu",
            rate_type="weight_tiered",
            currency="GBP",
            weight_unit="KG",
            dimension_unit="CM",
            config={
                "tiers": _RATE_TIERS.get("landmark_minipak_eu", [])
            },
        ),
    ],

    # Modifier definitions - HARDCODED LOGIC + DEFAULT VALUES
    accessorial_charges=[
        FuelSurcharge(
            accessorial_id="fuel_2025q1",
            accessorial_type="fuel",
            config={"percent": 8.5},  # Default - can be overridden in rate_config
            applies_to_services=["LGINTSTD", "LGINTSTDU"],
            priority=10,
        ),
        ResidentialDeliveryFee(
            accessorial_id="residential",
            accessorial_type="residential",
            config={"amount": 3.95},  # Default - can be overridden
            applies_to_services=["*"],  # All services
            priority=20,
        ),
    ],

    # Service definitions - LOADED FROM CSV
    services=load_services_from_csv(),
)

# DEPRECATED - Remove DEFAULT_SERVICES
# DEFAULT_SERVICES = [...]
```

### Carrier Migration Checklist

Each of the 9 carriers must implement DEFAULT_RATESHEET **before** the database migration runs.

**Carriers to migrate**:

- [ ] **bpost** (`community/plugins/bpost`)
  - [ ] Define zones in DEFAULT_RATESHEET
  - [ ] Define rates in DEFAULT_RATESHEET
  - [ ] Define accessorial_charges in DEFAULT_RATESHEET (if applicable)
  - [ ] Create services.csv
  - [ ] Create rate_tiers.csv
  - [ ] Remove DEFAULT_SERVICES
  - [ ] Update MANIFEST.in to include CSV files
  - [ ] Create/update tests

- [ ] **colissimo** (`community/plugins/colissimo`)
  - [ ] (same steps as bpost)

- [ ] **dhl_parcel_de** (`modules/connectors/dhl_parcel_de`)
  - [ ] (same steps as bpost)

- [ ] **dhl_poland** (`modules/connectors/dhl_poland`)
  - [ ] (same steps as bpost)

- [ ] **dtdc** (`ee/insiders/modules/connectors/dtdc`)
  - [ ] (same steps as bpost)

- [ ] **generic** (`modules/connectors/generic`)
  - [ ] (same steps as bpost)

- [ ] **geodis** (`community/plugins/geodis`)
  - [ ] (same steps as bpost)

- [ ] **landmark** (`modules/connectors/landmark`) ✅ REFERENCE IMPLEMENTATION
  - [x] DEFAULT_RATESHEET defined
  - [x] services.csv created
  - [x] rate_tiers.csv created
  - [x] Tests updated

- [ ] **locate2u** (`community/plugins/locate2u`)
  - [ ] (same steps as bpost)

**Migration blockers**: Database migration cannot proceed until all 9 carriers have DEFAULT_RATESHEET implemented. This ensures backward compatibility migration can populate rate_config from DEFAULT_RATESHEET.

---

## GraphQL API Changes

### 1. New Input Types (modules/graph/karrio/server/graph/schemas/base/inputs.py)

```python
import strawberry
import typing

@strawberry.input
class RateDefinitionInput(utils.BaseInput):
    """Input for creating/updating a rate rate_definition."""

    rate_id: str
    rate_type: str  # "flat", "weight_tiered", "distance", "dimensional"
    currency: utils.CurrencyCodeEnum
    weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET
    dimension_unit: typing.Optional[utils.DimensionUnitEnum] = strawberry.UNSET
    config: utils.JSON  # Calculator-specific config
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class AccessorialChargeInput(utils.BaseInput):
    """Input for creating/updating a rate accessorial_charge."""

    accessorial_id: str
    accessorial_type: str  # "fuel", "residential", "insurance", "discount"
    config: utils.JSON  # Modifier-specific config
    applies_to_services: typing.Optional[typing.List[str]] = strawberry.UNSET
    priority: typing.Optional[int] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class ServiceZoneInput(utils.BaseInput):
    """Updated zone input - NO rate field."""

    id: str  # NEW: Required zone ID
    label: typing.Optional[str] = strawberry.UNSET

    # Geographic criteria
    cities: typing.Optional[typing.List[str]] = strawberry.UNSET
    postal_codes: typing.Optional[typing.List[str]] = strawberry.UNSET
    country_codes: typing.Optional[typing.List[str]] = strawberry.UNSET

    # Service attributes
    transit_days: typing.Optional[int] = strawberry.UNSET
    transit_time: typing.Optional[float] = strawberry.UNSET

    # Metadata
    radius: typing.Optional[float] = strawberry.UNSET
    latitude: typing.Optional[float] = strawberry.UNSET
    longitude: typing.Optional[float] = strawberry.UNSET

    # REMOVED: rate, min_weight, max_weight (moved to rate_definition)


@strawberry.input
class CreateServiceLevelInput(utils.BaseInput):
    """Updated service input with rate_definition + accessorial_charges."""

    service_name: str
    service_code: str
    currency: utils.CurrencyCodeEnum

    # NEW: Calculator and accessorial_charges
    zone_ids: typing.List[str]  # References to zone IDs
    rate_id: str  # References a RateDefinition
    accessorial_ids: typing.Optional[typing.List[str]] = strawberry.UNSET

    # Rest same as before
    carrier_service_code: typing.Optional[str] = strawberry.UNSET
    description: typing.Optional[str] = strawberry.UNSET
    active: typing.Optional[bool] = strawberry.UNSET

    transit_days: typing.Optional[int] = strawberry.UNSET
    transit_time: typing.Optional[float] = strawberry.UNSET

    max_width: typing.Optional[float] = strawberry.UNSET
    max_height: typing.Optional[float] = strawberry.UNSET
    max_length: typing.Optional[float] = strawberry.UNSET
    dimension_unit: typing.Optional[utils.DimensionUnitEnum] = strawberry.UNSET

    min_weight: typing.Optional[float] = strawberry.UNSET
    max_weight: typing.Optional[float] = strawberry.UNSET
    weight_unit: typing.Optional[utils.WeightUnitEnum] = strawberry.UNSET

    domicile: typing.Optional[bool] = strawberry.UNSET
    international: typing.Optional[bool] = strawberry.UNSET

    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class CreateRateSheetMutationInput(utils.BaseInput):
    """Updated rate sheet input with rates + accessorial_charges."""

    name: str
    carrier_name: utils.CarrierNameEnum

    # NEW: Shared resources
    zones: typing.Optional[typing.List[ServiceZoneInput]] = strawberry.UNSET
    rates: typing.Optional[typing.List[RateDefinitionInput]] = strawberry.UNSET
    accessorial_charges: typing.Optional[typing.List[AccessorialChargeInput]] = strawberry.UNSET

    # Services reference the above by ID
    services: typing.Optional[typing.List[CreateServiceLevelInput]] = strawberry.UNSET

    carriers: typing.Optional[typing.List[str]] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


@strawberry.input
class UpdateRateSheetMutationInput(utils.BaseInput):
    """Updated rate sheet update input."""

    id: str
    name: typing.Optional[str] = strawberry.UNSET

    # NEW: Update zones/rates/accessorial_charges
    zones: typing.Optional[typing.List[ServiceZoneInput]] = strawberry.UNSET
    rates: typing.Optional[typing.List[RateDefinitionInput]] = strawberry.UNSET
    accessorial_charges: typing.Optional[typing.List[AccessorialChargeInput]] = strawberry.UNSET

    services: typing.Optional[typing.List[UpdateServiceLevelInput]] = strawberry.UNSET
    carriers: typing.Optional[typing.List[str]] = strawberry.UNSET
    remove_missing_services: typing.Optional[bool] = strawberry.UNSET
    metadata: typing.Optional[utils.JSON] = strawberry.UNSET


# REMOVED: UpdateRateSheetZoneCellMutationInput (zones don't have rates anymore)
# REMOVED: BatchUpdateRateSheetCellsMutationInput (zones don't have rates anymore)

@strawberry.input
class UpdateCalculatorTierInput(utils.BaseInput):
    """Update a specific tier in a rate_definition."""

    rate_id: str
    zone_id: str
    min_weight: typing.Optional[float] = strawberry.UNSET
    max_weight: typing.Optional[float] = strawberry.UNSET
    rate: typing.Optional[float] = strawberry.UNSET


@strawberry.input
class BatchUpdateCalculatorTiersInput(utils.BaseInput):
    """Batch update rate_definition tiers."""

    rate_sheet_id: str
    updates: typing.List[UpdateCalculatorTierInput]
```

### 2. Mutations - Working with rate_config JSON

**IMPORTANT**: Rates and accessorial charges are NOT separate database models. They're stored as JSON in `RateSheet.rate_config`. Mutations update the JSON structure directly.

```python
# modules/graph/karrio/server/graph/schemas/base/mutations.py

@strawberry.mutation
@utils.authentication_required
def update_rate_definition(
    info,
    rate_sheet_id: str,
    input: inputs.RateDefinitionInput,
) -> types.RateSheetType:
    """
    Add or update a rate definition in RateSheet.rate_config.

    NOTE: Rates are stored as JSON in rate_config, not as separate database objects.
    """
    rate_sheet = providers.RateSheet.objects.get(id=rate_sheet_id)
    rate_config = rate_sheet.rate_config or {}
    rates = rate_config.get("rates", [])

    # Find existing rate or create new one
    rate_def = next(
        (r for r in rates if r.get("rate_id") == input.rate_id),
        None
    )

    if rate_def:
        # Update existing
        rate_def.update({
            "rate_type": input.rate_type,
            "currency": input.currency,
            "weight_unit": input.weight_unit or "KG",
            "dimension_unit": input.dimension_unit or "CM",
            "config": input.config,
            "metadata": input.metadata or {},
        })
    else:
        # Create new
        rates.append({
            "rate_id": input.rate_id,
            "rate_type": input.rate_type,
            "currency": input.currency,
            "weight_unit": input.weight_unit or "KG",
            "dimension_unit": input.dimension_unit or "CM",
            "config": input.config,
            "is_active": True,
            "metadata": input.metadata or {},
        })

    rate_config["rates"] = rates
    rate_sheet.rate_config = rate_config
    rate_sheet.save()

    return rate_sheet


@strawberry.mutation
@utils.authentication_required
def update_accessorial_charge(
    info,
    rate_sheet_id: str,
    input: inputs.AccessorialChargeInput,
) -> types.RateSheetType:
    """
    Add or update an accessorial charge in RateSheet.rate_config.

    NOTE: Accessorial charges are stored as JSON in rate_config, not as separate database objects.
    """
    rate_sheet = providers.RateSheet.objects.get(id=rate_sheet_id)
    rate_config = rate_sheet.rate_config or {}
    accessorial_charges = rate_config.get("accessorial_charges", [])

    # Find existing or create new
    accessorial = next(
        (a for a in accessorial_charges if a.get("accessorial_id") == input.accessorial_id),
        None
    )

    if accessorial:
        # Update existing
        accessorial.update({
            "accessorial_type": input.accessorial_type,
            "config": input.config,
            "applies_to_services": input.applies_to_services or [],
            "priority": input.priority or 0,
            "metadata": input.metadata or {},
        })
    else:
        # Create new
        accessorial_charges.append({
            "accessorial_id": input.accessorial_id,
            "accessorial_type": input.accessorial_type,
            "config": input.config,
            "applies_to_services": input.applies_to_services or [],
            "priority": input.priority or 0,
            "is_active": True,
        })

    rate_config["accessorial_charges"] = accessorial_charges
    rate_sheet.rate_config = rate_config
    rate_sheet.save()

    return rate_sheet


@strawberry.mutation
@utils.authentication_required
def update_rate_tier(
    info,
    rate_sheet_id: str,
    input: inputs.UpdateCalculatorTierInput,
) -> types.RateSheetType:
    """
    Update a specific tier in a rate definition's config.

    Updates the JSON structure in RateSheet.rate_config.
    """
    rate_sheet = providers.RateSheet.objects.get(id=rate_sheet_id)
    rate_config = rate_sheet.rate_config or {}
    rates = rate_config.get("rates", [])

    # Find the rate definition
    rate_def = next(
        (r for r in rates if r.get("rate_id") == input.rate_id),
        None
    )

    if not rate_def:
        raise ValueError(f"Rate definition '{input.rate_id}' not found")

    config = rate_def.get("config", {})
    tiers = config.get("tiers", [])

    # Find and update the tier
    tier_found = False
    for tier in tiers:
        if tier.get("zone_id") == input.zone_id:
            if input.min_weight is not None:
                tier["min_weight"] = input.min_weight
            if input.max_weight is not None:
                tier["max_weight"] = input.max_weight
            if input.rate is not None:
                tier["rate"] = input.rate
            tier_found = True
            break

    if not tier_found:
        # Create new tier
        tiers.append({
            "zone_id": input.zone_id,
            "min_weight": input.min_weight,
            "max_weight": input.max_weight,
            "rate": input.rate,
        })

    config["tiers"] = tiers
    rate_def["config"] = config

    rate_config["rates"] = rates
    rate_sheet.rate_config = rate_config
    rate_sheet.save()

    return rate_sheet


@strawberry.mutation
@utils.authentication_required
def batch_update_rate_tiers(
    info,
    input: inputs.BatchUpdateCalculatorTiersInput,
) -> types.RateSheetType:
    """
    Batch update rate tiers in a single transaction.

    All updates are applied to RateSheet.rate_config JSON.
    """
    rate_sheet = providers.RateSheet.objects.get(id=input.rate_sheet_id)
    rate_config = rate_sheet.rate_config or {}
    rates = rate_config.get("rates", [])

    # Group updates by rate_id
    updates_by_rate = {}
    for update in input.updates:
        if update.rate_id not in updates_by_rate:
            updates_by_rate[update.rate_id] = []
        updates_by_rate[update.rate_id].append(update)

    # Apply all updates
    for rate_def in rates:
        rate_id = rate_def.get("rate_id")
        if rate_id not in updates_by_rate:
            continue

        config = rate_def.get("config", {})
        tiers = config.get("tiers", [])

        for update in updates_by_rate[rate_id]:
            # Find and update tier
            for tier in tiers:
                if tier.get("zone_id") == update.zone_id:
                    if update.min_weight is not None:
                        tier["min_weight"] = update.min_weight
                    if update.max_weight is not None:
                        tier["max_weight"] = update.max_weight
                    if update.rate is not None:
                        tier["rate"] = update.rate
                    break

        config["tiers"] = tiers
        rate_def["config"] = config

    rate_config["rates"] = rates
    rate_sheet.rate_config = rate_config
    rate_sheet.save()

    return rate_sheet
```

**Key Differences from Legacy Approach**:

1. ❌ **DON'T**: `providers.RateDefinition.objects.create()` - RateDefinition is NOT a database model
2. ❌ **DON'T**: `providers.AccessorialCharge.objects.get()` - AccessorialCharge is NOT a database model
3. ✅ **DO**: Update `RateSheet.rate_config` JSON field directly
4. ✅ **DO**: Return `RateSheet` from mutations (not individual rates/accessorial charges)
5. ✅ **DO**: Use list comprehensions to find/update items in JSON arrays

### 3. New Types (modules/graph/karrio/server/graph/schemas/base/types.py)

```python
@strawberry.type
class RateDefinitionType:
    """GraphQL type for rate rate_definition."""

    id: str
    rate_id: str
    rate_type: str
    currency: str
    weight_unit: str
    dimension_unit: str
    config: utils.JSON
    metadata: utils.JSON
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


@strawberry.type
class AccessorialChargeType:
    """GraphQL type for rate accessorial_charge."""

    id: str
    accessorial_id: str
    accessorial_type: str
    config: utils.JSON
    applies_to_services: typing.List[str]
    priority: int
    metadata: utils.JSON
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


@strawberry.type
class ServiceZoneType:
    """Updated zone type - NO rate field."""

    id: str
    label: typing.Optional[str]

    cities: typing.List[str]
    postal_codes: typing.List[str]
    country_codes: typing.List[str]

    transit_days: typing.Optional[int]
    transit_time: typing.Optional[float]

    radius: typing.Optional[float]
    latitude: typing.Optional[float]
    longitude: typing.Optional[float]

    # REMOVED: rate, min_weight, max_weight


@strawberry.type
class ServiceLevelType:
    """Updated service type with rate_definition + accessorial_charges."""

    id: str
    service_name: str
    service_code: str
    carrier_service_code: typing.Optional[str]
    currency: str

    # NEW: References
    zone_ids: typing.List[str]
    rate_id: typing.Optional[str]
    accessorial_ids: typing.List[str]

    # Resolved fields
    @strawberry.field
    def zones(self: providers.ServiceLevel) -> typing.List[ServiceZoneType]:
        """Resolve zones from rate_config JSON."""
        rate_sheet = self.service_sheet.first()
        if rate_sheet and rate_sheet.rate_config:
            zones = rate_sheet.rate_config.get('zones', [])
            return [
                ServiceZoneType(**zone)
                for zone in zones
                if zone.get('id') in self.zone_ids
            ]
        return []

    @strawberry.field
    def rate_definition(self: providers.ServiceLevel) -> typing.Optional[RateDefinitionType]:
        """
        Resolve rate_definition from rate_config JSON.

        NOTE: RateDefinition is NOT a database model - it's stored as JSON.
        """
        if not self.rate_id:
            return None

        rate_sheet = self.service_sheet.first()
        if not rate_sheet or not rate_sheet.rate_config:
            return None

        rates = rate_sheet.rate_config.get('rates', [])
        rate_def = next(
            (r for r in rates if r.get('rate_id') == self.rate_id),
            None
        )

        if rate_def:
            return RateDefinitionType(**rate_def)
        return None

    @strawberry.field
    def accessorial_charges(self: providers.ServiceLevel) -> typing.List[AccessorialChargeType]:
        """
        Resolve accessorial_charges from rate_config JSON.

        NOTE: AccessorialCharge is NOT a database model - it's stored as JSON.
        """
        if not self.accessorial_ids:
            return []

        rate_sheet = self.service_sheet.first()
        if not rate_sheet or not rate_sheet.rate_config:
            return []

        accessorial_charges = rate_sheet.rate_config.get('accessorial_charges', [])
        matched = [
            AccessorialChargeType(**ac)
            for ac in accessorial_charges
            if ac.get('accessorial_id') in self.accessorial_ids
        ]

        return matched

    # Rest of fields same as before
    active: bool
    max_weight: typing.Optional[float]
    max_length: typing.Optional[float]
    # ...
```

---

## Frontend Changes

### 1. TypeScript Types (packages/types/graphql/types.ts)

```typescript
export interface RateDefinition {
  id: string;
  rate_id: string;
  rate_type: 'flat' | 'weight_tiered' | 'distance' | 'dimensional';
  currency: string;
  weight_unit: string;
  dimension_unit: string;
  config: CalculatorConfig;
  metadata: Record<string, any>;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CalculatorConfig {
  // Flat rate
  rate?: number;

  // Weight tiered
  tiers?: WeightTier[];

  // Distance based
  base_rate?: number;
  rate_per_km?: number;
}

export interface WeightTier {
  zone_id?: string;
  min_weight?: number;
  max_weight?: number;
  rate: number;
}

export interface AccessorialCharge {
  id: string;
  accessorial_id: string;
  accessorial_type: 'fuel' | 'residential' | 'insurance' | 'discount' | 'peak_season';
  config: ModifierConfig;
  applies_to_services: string[];
  priority: number;
  metadata: Record<string, any>;
  is_active: boolean;
}

export interface ModifierConfig {
  // Fuel
  percent?: number;

  // Residential/Insurance
  amount?: number;

  // Insurance
  rate_per_100?: number;
  min_charge?: number;

  // Volume discount
  tiers?: {
    min_shipments: number;
    discount: number;
  }[];
}

export interface ServiceZone {
  id: string;  // NEW
  label?: string;
  cities?: string[];
  postal_codes?: string[];
  country_codes?: string[];
  transit_days?: number;
  transit_time?: number;
  radius?: number;
  latitude?: number;
  longitude?: number;

  // REMOVED: rate, min_weight, max_weight
}

export interface ServiceLevel {
  id: string;
  service_name: string;
  service_code: string;
  carrier_service_code?: string;
  currency: string;

  // NEW
  zone_ids: string[];
  rate_id?: string;
  accessorial_ids: string[];

  // Resolved
  zones?: ServiceZone[];
  rate_definition?: RateDefinition;
  accessorial_charges?: AccessorialCharge[];

  // Rest same as before
  active: boolean;
  max_weight?: number;
  // ...
}

export interface RateSheet {
  id: string;
  name: string;
  slug: string;
  carrier_name: string;
  is_system: boolean;

  // NEW
  zones: ServiceZone[];
  rates: RateDefinition[];
  accessorial_charges: AccessorialCharge[];

  services: ServiceLevel[];
  carriers: Carrier[];

  created_at: string;
  updated_at: string;
}
```

### 2. GraphQL Queries (packages/types/graphql/queries.ts)

```typescript
export const GET_RATE_CALCULATORS = gql`
  query GetRateDefinitions($filter: RateDefinitionFilter) {
    rate_calculators(filter: $filter) {
      edges {
        node {
          id
          rate_id
          rate_type
          currency
          weight_unit
          dimension_unit
          config
          metadata
          is_active
          created_at
          updated_at
        }
      }
      page_info {
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
    }
  }
`;

export const GET_RATE_MODIFIERS = gql`
  query GetAccessorialCharges($filter: AccessorialChargeFilter) {
    rate_modifiers(filter: $filter) {
      edges {
        node {
          id
          accessorial_id
          accessorial_type
          config
          applies_to_services
          priority
          metadata
          is_active
          created_at
          updated_at
        }
      }
      page_info {
        has_next_page
        has_previous_page
        start_cursor
        end_cursor
      }
    }
  }
`;

export const CREATE_RATE_CALCULATOR = gql`
  mutation CreateRateDefinition($input: RateDefinitionInput!) {
    create_rate_calculator(input: $input) {
      id
      rate_id
      rate_type
      currency
      config
    }
  }
`;

export const UPDATE_CALCULATOR_TIER = gql`
  mutation UpdateCalculatorTier($input: UpdateCalculatorTierInput!) {
    update_calculator_tier(input: $input) {
      id
      rate_id
      config
    }
  }
`;

export const BATCH_UPDATE_CALCULATOR_TIERS = gql`
  mutation BatchUpdateCalculatorTiers($input: BatchUpdateCalculatorTiersInput!) {
    batch_update_calculator_tiers(input: $input) {
      id
      rate_id
      config
    }
  }
`;
```

### 3. React Hooks (packages/hooks/rate-sheet.ts)

```typescript
// Add new hooks for rates and accessorial_charges

export function useRateDefinitions(filter?: RateDefinitionFilter) {
  const karrio = useKarrio();

  const query = useAuthenticatedQuery({
    queryKey: ['rate-rates', filter],
    queryFn: () => karrio.graphql.request<GetRateDefinitions>(
      gqlstr(GET_RATE_CALCULATORS),
      { variables: { filter } }
    ),
    onError,
  });

  return {
    query,
    rates: query.data?.rate_calculators,
  };
}

export function useRateDefinitionMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();

  const createCalculator = useMutation({
    mutationFn: (input: RateDefinitionInput) =>
      karrio.graphql.request<CreateRateDefinition>(
        gqlstr(CREATE_RATE_CALCULATOR),
        { variables: { input } }
      ),
    onSuccess: () => {
      queryClient.invalidateQueries(['rate-rates']);
    },
    onError,
  });

  const updateTier = useMutation({
    mutationFn: (input: UpdateCalculatorTierInput) =>
      karrio.graphql.request<UpdateCalculatorTier>(
        gqlstr(UPDATE_CALCULATOR_TIER),
        { variables: { input } }
      ),
    onSuccess: () => {
      queryClient.invalidateQueries(['rate-rates']);
      queryClient.invalidateQueries(['rate-sheets']);
    },
    onError,
  });

  const batchUpdateTiers = useMutation({
    mutationFn: (input: BatchUpdateCalculatorTiersInput) =>
      karrio.graphql.request<BatchUpdateCalculatorTiers>(
        gqlstr(BATCH_UPDATE_CALCULATOR_TIERS),
        { variables: { input } }
      ),
    onSuccess: () => {
      queryClient.invalidateQueries(['rate-rates']);
      queryClient.invalidateQueries(['rate-sheets']);
    },
    onError,
  });

  return {
    createCalculator,
    updateTier,
    batchUpdateTiers,
  };
}

// Similar hooks for accessorial_charges...
export function useAccessorialCharges(filter?: AccessorialChargeFilter) {
  // ... similar pattern
}

export function useAccessorialChargeMutation() {
  // ... similar pattern
}
```

### 4. UI Components

#### RateSheetEditor Component Updates

```tsx
// packages/admin/modules/carriers/rate-sheet-editor.tsx

import { RateSheet, ServiceLevel, RateDefinition, ServiceZone } from '@karrio/types';
import { useRateSheet, useRateSheetMutation, useRateDefinitionMutation } from '@karrio/hooks';

export function RateSheetEditor({ rateSheetId }: { rateSheetId: string }) {
  const { query } = useRateSheet({ id: rateSheetId });
  const { updateRateSheet } = useRateSheetMutation();
  const { updateTier, batchUpdateTiers } = useRateDefinitionMutation();

  const rateSheet = query.data?.rate_sheet;

  if (!rateSheet) return <Loading />;

  return (
    <div className="rate-sheet-editor">
      {/* Zone Management Section */}
      <ZonesPanel zones={rateSheet.zones} />

      {/* Calculator Management Section */}
      <CalculatorsPanel
        rates={rateSheet.rates}
        zones={rateSheet.zones}
        onUpdateTier={(update) => {
          updateTier.mutate({
            rate_id: update.rate_id,
            zone_id: update.zone_id,
            rate: update.rate,
            min_weight: update.min_weight,
            max_weight: update.max_weight,
          });
        }}
      />

      {/* Modifier Management Section */}
      <ModifiersPanel accessorial_charges={rateSheet.accessorial_charges} />

      {/* Services Section */}
      <ServicesPanel
        services={rateSheet.services}
        zones={rateSheet.zones}
        rates={rateSheet.rates}
        accessorial_charges={rateSheet.accessorial_charges}
      />
    </div>
  );
}
```

#### CalculatorsPanel Component (NEW)

```tsx
// packages/core/modules/ShippingRules/rates-panel.tsx

export function CalculatorsPanel({
  rates,
  zones,
  onUpdateTier,
}: {
  rates: RateDefinition[];
  zones: ServiceZone[];
  onUpdateTier: (update: UpdateCalculatorTierInput) => void;
}) {
  return (
    <div className="rates-panel">
      <h3>Rate Calculators</h3>

      {rates.map((rate_definition) => (
        <CalculatorCard
          key={rate_definition.id}
          rate_definition={rate_definition}
          zones={zones}
          onUpdateTier={onUpdateTier}
        />
      ))}
    </div>
  );
}

function CalculatorCard({
  rate_definition,
  zones,
  onUpdateTier,
}: {
  rate_definition: RateDefinition;
  zones: ServiceZone[];
  onUpdateTier: (update: UpdateCalculatorTierInput) => void;
}) {
  const tiers = rate_definition.config.tiers || [];

  return (
    <div className="rate_definition-card">
      <div className="rate_definition-header">
        <h4>{rate_definition.rate_id}</h4>
        <span className="badge">{rate_definition.rate_type}</span>
        <span className="badge">{rate_definition.currency}</span>
      </div>

      {rate_definition.rate_type === 'weight_tiered' && (
        <table className="tiers-table">
          <thead>
            <tr>
              <th>Zone</th>
              <th>Min Weight ({rate_definition.weight_unit})</th>
              <th>Max Weight ({rate_definition.weight_unit})</th>
              <th>Rate ({rate_definition.currency})</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {tiers.map((tier, index) => {
              const zone = zones.find(z => z.id === tier.zone_id);

              return (
                <tr key={index}>
                  <td>{zone?.label || tier.zone_id}</td>
                  <td>
                    <input
                      type="number"
                      value={tier.min_weight || ''}
                      onChange={(e) => {
                        onUpdateTier({
                          rate_id: rate_definition.rate_id,
                          zone_id: tier.zone_id!,
                          min_weight: parseFloat(e.target.value),
                          max_weight: tier.max_weight,
                          rate: tier.rate,
                        });
                      }}
                    />
                  </td>
                  <td>
                    <input
                      type="number"
                      value={tier.max_weight || ''}
                      onChange={(e) => {
                        onUpdateTier({
                          rate_id: rate_definition.rate_id,
                          zone_id: tier.zone_id!,
                          min_weight: tier.min_weight,
                          max_weight: parseFloat(e.target.value),
                          rate: tier.rate,
                        });
                      }}
                    />
                  </td>
                  <td>
                    <input
                      type="number"
                      step="0.01"
                      value={tier.rate}
                      onChange={(e) => {
                        onUpdateTier({
                          rate_id: rate_definition.rate_id,
                          zone_id: tier.zone_id!,
                          min_weight: tier.min_weight,
                          max_weight: tier.max_weight,
                          rate: parseFloat(e.target.value),
                        });
                      }}
                    />
                  </td>
                  <td>
                    <button onClick={() => {/* delete tier */}}>
                      Delete
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}

      {rate_definition.rate_type === 'flat' && (
        <div className="flat-rate-display">
          <label>Rate:</label>
          <span>{rate_definition.config.rate} {rate_definition.currency}</span>
        </div>
      )}
    </div>
  );
}
```

#### ModifiersPanel Component (NEW)

```tsx
// packages/core/modules/ShippingRules/accessorial_charges-panel.tsx

export function ModifiersPanel({
  accessorial_charges,
}: {
  accessorial_charges: AccessorialCharge[];
}) {
  return (
    <div className="accessorial_charges-panel">
      <h3>Rate Modifiers</h3>

      <div className="accessorial_charges-list">
        {accessorial_charges.map((accessorial_charge) => (
          <ModifierCard key={accessorial_charge.id} accessorial_charge={accessorial_charge} />
        ))}
      </div>

      <button onClick={() => {/* add new accessorial_charge */}}>
        Add Modifier
      </button>
    </div>
  );
}

function ModifierCard({ accessorial_charge }: { accessorial_charge: AccessorialCharge }) {
  return (
    <div className="accessorial_charge-card">
      <div className="accessorial_charge-header">
        <h4>{accessorial_charge.accessorial_id}</h4>
        <span className="badge">{accessorial_charge.accessorial_type}</span>
        {accessorial_charge.is_active && <span className="badge success">Active</span>}
      </div>

      <div className="accessorial_charge-config">
        {accessorial_charge.accessorial_type === 'fuel' && (
          <div>
            <label>Surcharge:</label>
            <span>{accessorial_charge.config.percent}%</span>
          </div>
        )}

        {accessorial_charge.accessorial_type === 'residential' && (
          <div>
            <label>Fee:</label>
            <span>${accessorial_charge.config.amount}</span>
          </div>
        )}

        {/* More accessorial_charge types... */}
      </div>

      <div className="accessorial_charge-applies-to">
        <label>Applies to:</label>
        <span>{accessorial_charge.applies_to_services.join(', ') || 'All services'}</span>
      </div>
    </div>
  );
}
```

---

## Migration Strategy

### Pre-Migration Checklist

- [ ] **Backup Production Database**
  ```bash
  pg_dump karrio_production > backup_pre_migration.sql
  ```

- [ ] **Create Migration Environment**
  - Clone production database to staging
  - Test full migration on staging
  - Validate all data migrated correctly

- [ ] **Communication Plan**
  - Notify users of scheduled maintenance window
  - Prepare rollback plan
  - Document breaking changes

### Migration Execution Plan

#### Phase 1: Database Migration (Estimated: 30 minutes downtime)

**NOTE**: No new tables created - only adding `rate_config` JSONField to existing models.

```bash
# Step 1: Run migration to add rate_config JSONField
python manage.py migrate providers 0XXX_add_rate_config_field

# Step 2: Run data migration to populate rate_config from legacy zones
python manage.py migrate providers 0XXX_migrate_zones_to_rate_config

# Step 3: Verify migration
python manage.py shell
>>> from karrio.server.providers.models import RateSheet
>>> print(f"Rate Sheets: {RateSheet.objects.count()}")
>>> # Spot check a few rate sheets
>>> rs = RateSheet.objects.first()
>>> print(f"rate_config zones: {len(rs.rate_config.get('zones', []))}")
>>> print(f"rate_config rates: {len(rs.rate_config.get('rates', []))}")
>>> print(f"rate_config accessorial_charges: {len(rs.rate_config.get('accessorial_charges', []))}")
```

**Key Migration Points**:

1. ✅ **DO**: Add `rate_config` JSONField to RateSheet model
2. ✅ **DO**: Migrate legacy zone data into rate_config JSON structure
3. ✅ **DO**: Keep legacy `zones` field for backward compatibility during transition
4. ❌ **DON'T**: Create new RateDefinition or AccessorialCharge tables
5. ❌ **DON'T**: Drop legacy columns immediately (wait for next major version)

#### Phase 2: Deploy Backend (API + SDK)

**SDK Changes**: All 9 carriers now have DEFAULT_RATESHEET with CSV data loaded at module import.

```bash
# Step 1: Verify DEFAULT_RATESHEET loaded for all carriers
python -c "
from karrio.providers.landmark import units as landmark_units
from karrio.providers.bpost import units as bpost_units
from karrio.providers.colissimo import units as colissimo_units
# ... (all 9 carriers)

print(f'Landmark services: {len(landmark_units.DEFAULT_RATESHEET.services)}')
print(f'Bpost services: {len(bpost_units.DEFAULT_RATESHEET.services)}')
# ... verify all carriers loaded successfully
"

# Step 2: Deploy updated SDK with DEFAULT_RATESHEET
cd modules/sdk
python setup.py sdist bdist_wheel
pip install --upgrade dist/karrio-*.whl

# Step 3: Deploy API
# (Kubernetes/Docker deployment commands)

# Step 4: Verify API with rate_config JSONField
curl -X POST https://api.karrio.com/graphql \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query": "{ rate_sheets { edges { node { id rate_config } } } }"}'
```

**Key Deployment Points**:

1. ✅ **All 9 Carriers Updated**: landmark, bpost, colissimo, dhl_parcel_de, dhl_poland, dtdc, generic, geodis, locate2u
2. ✅ **DEFAULT_RATESHEET Pattern**: Each carrier has `DEFAULT_RATESHEET` loaded from CSV at import time
3. ✅ **CSV Files**: `services.csv` and `rate_tiers.csv` in each carrier's directory
4. ✅ **Backward Compatible**: Legacy DEFAULT_SERVICES still works during transition period

#### Phase 3: Deploy Frontend

```bash
# Step 1: Build frontend with new types
cd packages
npm run build

# Step 2: Deploy
# (Vercel/Netlify deployment commands)

# Step 3: Verify UI
# - Open rate sheet editor
# - Verify zones display
# - Verify rate_definition tiers editable
# - Test rate updates
```

### Rollback Plan

If migration fails:

```sql
-- Rollback to previous migration
python manage.py migrate providers 0XXX_previous_migration

-- Restore from backup
psql karrio_production < backup_pre_migration.sql

-- Redeploy previous version
git checkout <previous-commit>
./deploy.sh
```

---

## Implementation Plan

### Phase 1: Foundation (Weeks 1-2)

**Week 1: Database & SDK Core**
- [ ] Day 1-2: Add `rate_config` JSONField to RateSheet/ServiceLevel models
- [ ] Day 3-4: Implement RateDefinition and AccessorialCharge dataclasses (NOT models)
- [ ] Day 5: Create data migration to populate rate_config from legacy zones

**Week 2: SDK Rating Engine**
- [ ] Day 1-2: Update rating_proxy.py with zone matching algorithm
- [ ] Day 3-4: Implement rate calculation logic (FlatRate, WeightTieredRate)
- [ ] Day 5: Unit tests for zone matching and rate calculations

**Deliverables**:
- ✅ `rate_config` JSONField added (NO new tables)
- ✅ RateDefinition/AccessorialCharge dataclasses implemented
- ✅ Zone matching algorithm working
- ✅ Unit tests passing

### Phase 2: Carrier Migration (Weeks 3-5)

**Week 3: CSV Format & Landmark**
- [ ] Day 1-2: Design CSV format (services.csv, rate_tiers.csv)
- [ ] Day 3-4: Implement CSV loader + DEFAULT_RATESHEET for Landmark
- [ ] Day 5: Test Landmark end-to-end with real rates

**Week 4: Migrate Carriers 2-6**
- [ ] Day 1: bpost
- [ ] Day 2: colissimo
- [ ] Day 3: dhl_parcel_de
- [ ] Day 4: dhl_poland
- [ ] Day 5: dtdc

**Week 5: Migrate Carriers 7-9**
- [ ] Day 1-2: generic
- [ ] Day 3-4: geodis
- [ ] Day 5: locate2u

**Deliverables**:
- ✅ CSV format finalized (services.csv, rate_tiers.csv)
- ✅ **All 9 carriers** have DEFAULT_RATESHEET + CSV files
- ✅ Integration tests passing for all carriers

### Phase 3: API Layer (Weeks 6-7)

**Week 6: GraphQL Schema**
- [ ] Day 1-2: Update GraphQL types for rate_config JSON
- [ ] Day 3-4: Implement mutations (update_rate_definition, update_accessorial_charge)
- [ ] Day 5: Remove old zone cell mutations

**Week 7: Final Testing**
- [ ] Day 1-2: Test rate_config updates via GraphQL
- [ ] Day 3-4: Test all 9 carriers with real shipment requests
- [ ] Day 5: Performance testing on large rate sheets

**Deliverables**:
- GraphQL schema updated
- All 9 carriers migrated
- API tests passing

### Phase 4: Frontend (Weeks 7-8)

**Week 7: UI Components**
- [ ] Day 1-2: Update TypeScript types
- [ ] Day 3-4: Implement CalculatorsPanel component
- [ ] Day 5: Implement ModifiersPanel component

**Week 8: Integration & Polish**
- [ ] Day 1-2: Update RateSheetEditor
- [ ] Day 3-4: Update hooks (rate-sheet.ts)
- [ ] Day 5: E2E testing

**Deliverables**:
- Frontend UI functional
- All CRUD operations working
- E2E tests passing

### Phase 5: Testing & Migration (Weeks 9-10)

**Week 9: Testing**
- [ ] Day 1-2: Integration testing (full stack)
- [ ] Day 3-4: Performance testing
- [ ] Day 5: Security review

**Week 10: Staging Migration**
- [ ] Day 1-2: Migrate staging database
- [ ] Day 3-4: User acceptance testing
- [ ] Day 5: Fix bugs

**Deliverables**:
- All tests passing
- Staging environment validated
- Production deployment plan finalized

---

## Testing Strategy

### 1. Unit Tests

**DEFAULT_RATESHEET Loading**:
```python
# modules/connectors/landmark/tests/test_default_ratesheet.py

def test_default_ratesheet_loads_from_csv():
    """Test that DEFAULT_RATESHEET loads correctly from CSV at module import."""
    from karrio.providers.landmark import units

    # Verify DEFAULT_RATESHEET exists
    assert units.DEFAULT_RATESHEET is not None
    assert units.DEFAULT_RATESHEET.carrier_name == "landmark"

    # Verify services loaded
    assert len(units.DEFAULT_RATESHEET.services) > 0

    # Verify zones loaded
    assert len(units.DEFAULT_RATESHEET.zones) > 0

    # Verify rates loaded
    assert len(units.DEFAULT_RATESHEET.rates) > 0

    # Verify accessorial charges loaded
    assert len(units.DEFAULT_RATESHEET.accessorial_charges) >= 0

def test_all_nine_carriers_have_default_ratesheet():
    """Test that all 9 carriers have DEFAULT_RATESHEET loaded."""
    carriers = [
        "landmark", "bpost", "colissimo", "dhl_parcel_de",
        "dhl_poland", "dtdc", "generic", "geodis", "locate2u"
    ]

    for carrier in carriers:
        module = __import__(f"karrio.providers.{carrier}.units", fromlist=["DEFAULT_RATESHEET"])
        assert hasattr(module, "DEFAULT_RATESHEET"), f"{carrier} missing DEFAULT_RATESHEET"
        assert module.DEFAULT_RATESHEET is not None, f"{carrier} DEFAULT_RATESHEET is None"
```

**Zone Matching Algorithm**:
```python
# modules/sdk/tests/test_zone_matching.py

def test_zone_specificity_postal_over_city():
    """Test that postal code match is preferred over city match."""
    from karrio.universal.mappers.rating_proxy import find_best_matching_zone

    zones = [
        ServiceZone(id="zone_city", cities=["Toronto"], rate=15.00),
        ServiceZone(id="zone_postal", postal_codes=["M5H"], rate=12.00),
    ]

    recipient = Address(city="Toronto", postal_code="M5H 2N2", country_code="CA")
    package = Package(weight=1.0, weight_unit="KG")
    service = ServiceLevel(currency="USD", weight_unit="KG")

    best_zone = find_best_matching_zone(zones, package, recipient, service)

    assert best_zone.id == "zone_postal"  # More specific wins
    assert best_zone.rate == 12.00

def test_zone_weight_tier_matching():
    """Test weight tier selection (inclusive min, exclusive max)."""
    from karrio.universal.mappers.rating_proxy import check_weight_match

    zone = ServiceZone(id="zone_us", min_weight=0.5, max_weight=1.0)
    service = ServiceLevel(weight_unit="KG")

    # 0.5kg should match (inclusive min)
    package_min = Package(weight=0.5, weight_unit="KG")
    assert check_weight_match(zone, package_min, service) == True

    # 1.0kg should NOT match (exclusive max)
    package_max = Package(weight=1.0, weight_unit="KG")
    assert check_weight_match(zone, package_max, service) == False

    # 0.75kg should match (within range)
    package_mid = Package(weight=0.75, weight_unit="KG")
    assert check_weight_match(zone, package_mid, service) == True
```

**Rate Calculation with Zone Matching**:
```python
# tests/test_rating_proxy.py

def test_rate_calculation_with_zone_matching():
    """Test that zone matching selects correct tier and applies rates."""
    from karrio.universal.mappers.rating_proxy import get_available_rates

    # Setup rate_config structure
    rate_config = {
        "zones": [
            {
                "id": "zone_us",
                "label": "United States",
                "country_codes": ["US"],
                "transit_days": 7
            }
        ],
        "rates": [
            {
                "rate_id": "landmark_maxipak",
                "rate_type": "weight_tiered",
                "currency": "GBP",
                "weight_unit": "KG",
                "config": {
                    "tiers": [
                        {"zone_id": "zone_us", "min_weight": 0.0, "max_weight": 0.5, "rate": 6.86},
                        {"zone_id": "zone_us", "min_weight": 0.5, "max_weight": 1.0, "rate": 8.78},
                        {"zone_id": "zone_us", "min_weight": 1.0, "max_weight": 2.0, "rate": 10.81},
                    ]
                }
            }
        ],
        "accessorial_charges": [
            {
                "accessorial_id": "fuel_2025q1",
                "accessorial_type": "fuel_surcharge",
                "config": {"percent": 8.5},
                "applies_to_services": ["LGINTSTD"]
            }
        ]
    }

    service = ServiceLevel(
        service_code="LGINTSTD",
        rate_config={
            "zone_ids": ["zone_us"],
            "rate_id": "landmark_maxipak",
            "accessorial_charge_ids": ["fuel_2025q1"]
        }
    )

    # Test 0.3kg package to US
    package = Package(weight=0.3, weight_unit="KG")
    recipient = Address(country_code="US")

    rates, errors = get_available_rates(package, shipper, recipient, settings)

    assert len(rates) == 1
    assert rates[0].total_charge == 6.86  # Matches 0-0.5kg tier

    # Test 0.75kg package to US
    package = Package(weight=0.75, weight_unit="KG")
    rates, errors = get_available_rates(package, shipper, recipient, settings)

    assert rates[0].total_charge == 8.78  # Matches 0.5-1.0kg tier
```

### 2. Integration Tests

**GraphQL API Tests (rate_config JSON)**:
```python
# modules/graph/tests/test_rate_config_mutations.py

def test_update_rate_definition_in_rate_config(graphql_client):
    """Test updating rate definition within rate_config JSONField."""

    mutation = """
        mutation {
            update_rate_definition(
                rate_sheet_id: "rsht_123"
                input: {
                    rate_id: "test_calc"
                    rate_type: WEIGHT_TIERED
                    currency: "USD"
                    config: {
                        tiers: [
                            {zone_id: "zone_us", min_weight: 0, max_weight: 1, rate: 10.00}
                        ]
                    }
                }
            ) {
                id
                rate_config
            }
        }
    """

    result = graphql_client.execute(mutation)

    # Verify rate_config JSON was updated
    rate_config = result["update_rate_definition"]["rate_config"]
    rates = rate_config["rates"]

    matching_rate = next(r for r in rates if r["rate_id"] == "test_calc")
    assert matching_rate["rate_type"] == "weight_tiered"
    assert len(matching_rate["config"]["tiers"]) == 1
    assert matching_rate["config"]["tiers"][0]["rate"] == 10.00

def test_update_accessorial_charge_in_rate_config(graphql_client):
    """Test updating accessorial charge within rate_config JSONField."""

    mutation = """
        mutation {
            update_accessorial_charge(
                rate_sheet_id: "rsht_123"
                input: {
                    accessorial_id: "fuel_2025q1"
                    accessorial_type: FUEL_SURCHARGE
                    config: {percent: 9.5}
                }
            ) {
                id
                rate_config
            }
        }
    """

    result = graphql_client.execute(mutation)

    # Verify rate_config JSON was updated
    rate_config = result["update_accessorial_charge"]["rate_config"]
    accessorial_charges = rate_config["accessorial_charges"]

    matching_ac = next(ac for ac in accessorial_charges if ac["accessorial_id"] == "fuel_2025q1")
    assert matching_ac["config"]["percent"] == 9.5
```

### 3. E2E Tests

**Frontend E2E**:
```typescript
// packages/admin/tests/e2e/rate-sheet-editor.spec.ts

describe('Rate Sheet Editor', () => {
  it('should display rates panel', async () => {
    await page.goto('/admin/rate-sheets/rsht_123');

    const calculatorsPanel = await page.$('.rates-panel');
    expect(calculatorsPanel).toBeTruthy();

    const calculatorCards = await page.$$('.rate_definition-card');
    expect(calculatorCards.length).toBeGreaterThan(0);
  });

  it('should update rate_definition tier', async () => {
    await page.goto('/admin/rate-sheets/rsht_123');

    // Find rate input for first tier
    const rateInput = await page.$('input[name="tier-rate-0"]');
    await rateInput.clear();
    await rateInput.type('15.50');

    // Save
    await page.click('button.save-tier');

    // Verify update
    await page.waitForSelector('.success-message');
    const savedValue = await rateInput.value();
    expect(savedValue).toBe('15.50');
  });

  it('should add new accessorial_charge', async () => {
    await page.goto('/admin/rate-sheets/rsht_123');

    await page.click('button.add-accessorial_charge');

    // Fill form
    await page.select('select[name="accessorial_charge-type"]', 'fuel');
    await page.type('input[name="accessorial_charge-id"]', 'fuel_2025q2');
    await page.type('input[name="surcharge-percent"]', '10.5');

    // Save
    await page.click('button.save-accessorial_charge');

    // Verify
    await page.waitForSelector('.accessorial_charge-card:contains("fuel_2025q2")');
  });
});
```

### 4. Migration Tests

**Data Migration Validation (rate_config JSON)**:
```python
# modules/core/karrio/server/providers/tests/test_migration.py

def test_legacy_zones_to_rate_config_migration():
    """Test that legacy zones migrate correctly into rate_config JSON."""

    # Create legacy rate sheet with zones in ServiceLevel
    legacy_sheet = RateSheet.objects.create(
        name="Legacy Sheet",
        carrier_name="landmark",
    )

    legacy_service = ServiceLevel.objects.create(
        service_code="LGINTSTD",
        service_name="MaxiPak",
        currency="GBP",
        zones=[  # Legacy format - zones in ServiceLevel
            {
                "label": "United States",
                "country_codes": ["US"],
                "min_weight": 0.0,
                "max_weight": 1.0,
                "rate": 8.78,
            },
            {
                "label": "United States",
                "country_codes": ["US"],
                "min_weight": 1.0,
                "max_weight": 2.0,
                "rate": 10.81,
            },
        ]
    )

    legacy_sheet.services.add(legacy_service)

    # Run migration
    from karrio.server.providers.migrations.0XXX_migrate_zones_to_rate_config import migrate_to_rate_config
    migrate_to_rate_config(None, None)

    # Verify results
    legacy_sheet.refresh_from_db()

    # Should have rate_config populated
    assert legacy_sheet.rate_config is not None
    assert "zones" in legacy_sheet.rate_config
    assert "rates" in legacy_sheet.rate_config

    # Verify zones extracted and deduplicated
    zones = legacy_sheet.rate_config["zones"]
    assert len(zones) == 1  # Deduplicated (same country)
    assert zones[0]["label"] == "United States"
    assert zones[0]["country_codes"] == ["US"]

    # Verify rates created with weight tiers
    rates = legacy_sheet.rate_config["rates"]
    assert len(rates) >= 1

    rate_def = rates[0]
    assert rate_def["rate_type"] == "weight_tiered"
    assert len(rate_def["config"]["tiers"]) == 2
    assert rate_def["config"]["tiers"][0]["rate"] == 8.78
    assert rate_def["config"]["tiers"][1]["rate"] == 10.81

    # Service should reference rate via rate_id
    legacy_service.refresh_from_db()
    assert legacy_service.rate_config is not None
    assert "rate_id" in legacy_service.rate_config
    assert "zone_ids" in legacy_service.rate_config
```

---

## Risk Assessment

### High Risks

1. **Data Loss During Migration** 🔴
   - **Mitigation**: Full database backup, staging migration first, rollback plan
   - **Impact**: Critical - loss of customer rate sheets
   - **Likelihood**: Low (with proper testing)

2. **Breaking API Changes** 🔴
   - **Mitigation**: Version API, maintain compatibility layer for 1 month
   - **Impact**: High - third-party integrations break
   - **Likelihood**: Medium (if not coordinated)

3. **Performance Degradation** 🟡
   - **Mitigation**: Database indexing, query optimization, load testing
   - **Impact**: Medium - slower rate calculations
   - **Likelihood**: Low (new system should be faster)

### Medium Risks

4. **Incomplete Carrier Migration** 🟡
   - **Mitigation**: Carrier-by-carrier migration with testing
   - **Impact**: Medium - some carriers unavailable
   - **Likelihood**: Low (controlled rollout)

5. **Frontend UI Bugs** 🟡
   - **Mitigation**: E2E testing, beta testing with select users
   - **Impact**: Medium - rate sheet editing broken
   - **Likelihood**: Medium (complex UI changes)

### Low Risks

6. **Calculator Logic Bugs** 🟢
   - **Mitigation**: Comprehensive unit tests, compare old vs new rates
   - **Impact**: Medium - incorrect rates returned
   - **Likelihood**: Low (well-tested algorithms)

### Risk Mitigation Checklist

- [ ] Full database backup before migration
- [ ] Staging environment migration test
- [ ] Rollback plan documented and tested
- [ ] API versioning implemented
- [ ] Performance benchmarks established
- [ ] User communication plan
- [ ] Support team trained on new system
- [ ] Monitoring and alerting configured

---

## Rollout Plan

### Pre-Launch (Week -1)

- [ ] **Final Testing**
  - All unit tests passing
  - Integration tests passing
  - E2E tests passing
  - Performance benchmarks met

- [ ] **Staging Deployment**
  - Deploy to staging environment
  - Run full migration on staging database
  - User acceptance testing with 5 beta users

- [ ] **Documentation**
  - Migration guide published
  - API documentation updated
  - Admin user guide updated

- [ ] **Communication**
  - Email users about upcoming changes
  - Blog post explaining new features
  - Support team briefing

### Launch Day (Production Deployment)

**Maintenance Window**: 2-4 hours (off-peak time)

#### Hour 1: Database Migration

```bash
# 1. Take final backup
pg_dump karrio_production > final_backup.sql

# 2. Enable maintenance mode
python manage.py maintenance on

# 3. Run migrations
python manage.py migrate providers 0XXX_create_rate_definition_tables
python manage.py migrate providers 0XXX_update_ratesheet_servicelevel
python manage.py migrate providers 0XXX_migrate_legacy_data

# 4. Verify migration
python manage.py validate_migration
```

#### Hour 2: Backend Deployment

```bash
# 1. Deploy SDK
./deploy_sdk.sh

# 2. Deploy API
kubectl apply -f k8s/api-deployment.yaml

# 3. Verify health
curl https://api.karrio.com/health
```

#### Hour 3: Frontend Deployment

```bash
# 1. Build frontend
npm run build

# 2. Deploy
vercel deploy --prod

# 3. Verify
# - Rate sheet editor loads
# - Calculators panel displays
# - Rate updates work
```

#### Hour 4: Post-Deployment Verification

- [ ] Run smoke tests
- [ ] Check error logs
- [ ] Monitor performance metrics
- [ ] Test a few customer rate sheets manually

### Post-Launch

**Day 1-7**: Intensive Monitoring
- Monitor error rates hourly
- Watch performance metrics
- Respond to support tickets immediately

**Week 2-4**: Stabilization
- Fix any bugs discovered
- Optimize performance if needed
- Gather user feedback

**Month 2+**: Enhancement
- Implement additional rate_definition types
- Add more accessorial_charge types
- Build rate sheet templates

---

## Success Metrics

### Technical Metrics

- [ ] **Migration Success Rate**: 100% of rate sheets migrated
- [ ] **API Response Time**: ≤ 200ms (same or better than before)
- [ ] **Error Rate**: < 0.1% (same or better than before)
- [ ] **Test Coverage**: ≥ 80% for new code
- [ ] **Database Query Performance**: No N+1 queries

### Business Metrics

- [ ] **Zero Downtime**: Maintenance window ≤ 4 hours
- [ ] **User Satisfaction**: ≥ 4/5 stars in feedback
- [ ] **Support Tickets**: < 10 related to migration
- [ ] **Feature Adoption**: 50% of users update a rate within 30 days

### Code Quality Metrics

- [ ] **Lines of Code Removed**: > 500 (backward compat code)
- [ ] **Code Duplication**: Reduced by 30%
- [ ] **Cyclomatic Complexity**: Average ≤ 10

---

## Conclusion

This PRD outlines a **complete architectural upgrade** to decouple rate calculation from zone definitions. The migration is complex but necessary to enable:

✅ Flexible pricing (surcharges, discounts, complex models)
✅ Clean codebase (no backward compatibility noise)
✅ Better performance (optimized database structure)
✅ Future extensibility (easy to add new rate_definition/accessorial_charge types)

**Estimated Timeline**: 10 weeks
**Estimated Effort**: 2-3 full-time engineers
**Risk Level**: High (but manageable with proper planning)
**User Impact**: Zero (if successful) / High (if unsuccessful)

**Recommendation**: Proceed with phased implementation, starting with foundation work (database + SDK), then carrier migration, then full-stack deployment.

---

## Appendix

### A. Database Schema Diagrams

```
┌─────────────────────────────────────────────────────────────────┐
│                     karrio_rate_calculator                       │
├─────────────────────────────────────────────────────────────────┤
│ id (UUID, PK)                                                   │
│ rate_id (VARCHAR, UNIQUE)                                 │
│ rate_type (VARCHAR) - "flat", "weight_tiered", etc.       │
│ currency (VARCHAR)                                              │
│ weight_unit (VARCHAR)                                           │
│ dimension_unit (VARCHAR)                                        │
│ config (JSONB) - Calculator-specific configuration              │
│ metadata (JSONB)                                                │
│ is_active (BOOLEAN)                                             │
│ created_at (TIMESTAMP)                                          │
│ updated_at (TIMESTAMP)                                          │
│ created_by_id (FK → auth_user)                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Referenced by
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       service-level                              │
├─────────────────────────────────────────────────────────────────┤
│ id (VARCHAR, PK)                                                │
│ service_code (VARCHAR)                                          │
│ service_name (VARCHAR)                                          │
│ currency (VARCHAR)                                              │
│ zone_ids (JSONB) - ["zone_1", "zone_2", ...]                   │
│ rate_id (VARCHAR, FK → karrio_rate_calculator)            │
│ accessorial_ids (JSONB) - ["mod_1", "mod_2", ...]                 │
│ ... (other service attributes)                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Many-to-many
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         rate-sheet                               │
├─────────────────────────────────────────────────────────────────┤
│ id (VARCHAR, PK)                                                │
│ name (VARCHAR)                                                  │
│ carrier_name (VARCHAR)                                          │
│ zones (JSONB) - Shared zone definitions                        │
│ rates (JSONB) - Calculator references                     │
│ accessorial_charges (JSONB) - Modifier references                         │
└─────────────────────────────────────────────────────────────────┘
```

### B. Example Calculator Configs

**Flat Rate**:
```json
{
  "rate": 10.00
}
```

**Weight Tiered**:
```json
{
  "tiers": [
    {"zone_id": "zone_us", "min_weight": 0.0, "max_weight": 1.0, "rate": 5.00},
    {"zone_id": "zone_us", "min_weight": 1.0, "max_weight": 2.0, "rate": 8.00},
    {"zone_id": "zone_eu", "min_weight": 0.0, "max_weight": 1.0, "rate": 4.00}
  ]
}
```

**Distance Based**:
```json
{
  "base_rate": 5.00,
  "rate_per_km": 0.25,
  "max_distance": 1000
}
```

**Dimensional Weight**:
```json
{
  "dim_factor": 6000,
  "tiers": [
    {"zone_id": "zone_us", "min_weight": 0.0, "max_weight": 5.0, "rate": 25.00},
    {"zone_id": "zone_us", "min_weight": 5.0, "max_weight": 10.0, "rate": 45.00},
    {"zone_id": "zone_us", "min_weight": 10.0, "max_weight": 20.0, "rate": 85.00}
  ]
}
```

Note: Dimensional weight uses billable weight = max(actual_weight, (L×W×H)/dim_factor)

### C. Example Modifier Configs

**Fuel Surcharge**:
```json
{
  "percent": 8.5
}
```

**Residential Fee**:
```json
{
  "amount": 3.95
}
```

**Volume Discount**:
```json
{
  "tiers": [
    {"min_shipments": 100, "discount": 5},
    {"min_shipments": 500, "discount": 10},
    {"min_shipments": 1000, "discount": 15}
  ]
}
```

### D. Migration Validation Queries

```sql
-- Verify all rate sheets have zones
SELECT id, name,
       CASE WHEN zones IS NULL OR zones = '[]' THEN 'MISSING' ELSE 'OK' END as zones_status
FROM "rate-sheet";

-- Verify all services have rate_definition
SELECT id, service_code,
       CASE WHEN rate_id IS NULL THEN 'MISSING' ELSE 'OK' END as calculator_status
FROM "service-level";

-- Count rates created
SELECT rate_type, COUNT(*)
FROM karrio_rate_calculator
GROUP BY rate_type;

-- Verify tier counts
SELECT rate_id,
       jsonb_array_length(config->'tiers') as tier_count
FROM karrio_rate_calculator
WHERE rate_type = 'weight_tiered';
```

### E. Dimensional Weight Reference

#### Industry Standard Dim Factors

| Unit System | Dimension Unit | Weight Unit | Dim Factor | Calculation |
|------------|----------------|-------------|------------|-------------|
| **Metric** | cm | kg | **6000** | (L × W × H in cm³) / 6000 = kg |
| **Metric** | cm | kg | 5000 | Alternative (denser) |
| **Imperial** | in | lb | **166** | (L × W × H in in³) / 166 = lb |
| **Imperial** | in | lb | 139 | Alternative (denser) |

**Reference**: [Dimensional Weight - Wikipedia](https://en.wikipedia.org/wiki/Dimensional_weight)

#### Common Carrier Dim Factors

| Carrier | Domestic | International | Units |
|---------|----------|---------------|-------|
| **FedEx** | 139 (in³/lb) | 139 (in³/lb) | Imperial |
| **UPS** | 139 (in³/lb) | 139 (in³/lb) | Imperial |
| **DHL** | 5000 (cm³/kg) | 5000 (cm³/kg) | Metric |
| **USPS** | 166 (in³/lb) | N/A | Imperial |
| **Canada Post** | 6000 (cm³/kg) | 6000 (cm³/kg) | Metric |

#### Dimensional Weight Examples

**Example 1: Large lightweight box (Metric)**
- Package: 50cm × 40cm × 30cm, 5kg
- Dim factor: 6000
- Volume: 50 × 40 × 30 = 60,000 cm³
- Dimensional weight: 60,000 / 6000 = 10 kg
- **Billable weight: max(5kg, 10kg) = 10kg**

**Example 2: Small heavy box (Metric)**
- Package: 20cm × 15cm × 10cm, 8kg
- Dim factor: 6000
- Volume: 20 × 15 × 10 = 3,000 cm³
- Dimensional weight: 3,000 / 6000 = 0.5 kg
- **Billable weight: max(8kg, 0.5kg) = 8kg**

**Example 3: Large lightweight box (Imperial)**
- Package: 20in × 16in × 12in, 10lb
- Dim factor: 166
- Volume: 20 × 16 × 12 = 3,840 in³
- Dimensional weight: 3,840 / 166 = 23.1 lb
- **Billable weight: max(10lb, 23.1lb) = 23.1lb**

#### Configuration Examples

**Dimensional Weight Calculator Config (Metric)**:
```json
{
  "rate_id": "fedex_express_intl",
  "rate_type": "dimensional",
  "currency": "USD",
  "weight_unit": "KG",
  "dimension_unit": "CM",
  "config": {
    "dim_factor": 5000,
    "tiers": [
      {"zone_id": "zone_us", "min_weight": 0.0, "max_weight": 1.0, "rate": 25.00},
      {"zone_id": "zone_us", "min_weight": 1.0, "max_weight": 5.0, "rate": 45.00},
      {"zone_id": "zone_us", "min_weight": 5.0, "max_weight": 10.0, "rate": 75.00}
    ]
  }
}
```

**Dimensional Weight Calculator Config (Imperial)**:
```json
{
  "rate_id": "ups_ground_dom",
  "rate_type": "dimensional",
  "currency": "USD",
  "weight_unit": "LB",
  "dimension_unit": "IN",
  "config": {
    "dim_factor": 139,
    "tiers": [
      {"zone_id": "zone_domestic", "min_weight": 0.0, "max_weight": 10.0, "rate": 15.00},
      {"zone_id": "zone_domestic", "min_weight": 10.0, "max_weight": 50.0, "rate": 35.00},
      {"zone_id": "zone_domestic", "min_weight": 50.0, "max_weight": 150.0, "rate": 85.00}
    ]
  }
}
```

#### Testing Dimensional Weight

```python
# Test case 1: Dimensional weight exceeds actual weight
def test_dimensional_weight_exceeds_actual():
    rate_definition = DimensionalWeightRate(
        rate_id="test_dim",
        weight_unit="KG",
        dimension_unit="CM",
        currency="USD",
        config={
            "dim_factor": 6000,
            "tiers": [
                {"zone_id": "zone_us", "min_weight": 0, "max_weight": 15, "rate": 50.00},
            ]
        }
    )

    # Large lightweight package
    package = Package(
        length=50,  # cm
        width=40,   # cm
        height=30,  # cm
        weight=5,   # kg (actual)
        weight_unit="KG",
        dimension_unit="CM"
    )

    zone = ServiceZone(id="zone_us", label="US")
    context = {}

    rate = rate_definition.calculate(package, None, None, zone, context)

    # Volume: 50 × 40 × 30 = 60,000 cm³
    # Dim weight: 60,000 / 6000 = 10 kg
    # Billable: max(5kg, 10kg) = 10kg
    assert context["actual_weight"] == 5.0
    assert context["dimensional_weight"] == 10.0
    assert context["billable_weight"] == 10.0
    assert rate == 50.00


# Test case 2: Actual weight exceeds dimensional weight
def test_actual_weight_exceeds_dimensional():
    rate_definition = DimensionalWeightRate(
        rate_id="test_dim",
        weight_unit="KG",
        dimension_unit="CM",
        currency="USD",
        config={
            "dim_factor": 6000,
            "tiers": [
                {"zone_id": "zone_us", "min_weight": 0, "max_weight": 15, "rate": 50.00},
            ]
        }
    )

    # Small heavy package
    package = Package(
        length=20,  # cm
        width=15,   # cm
        height=10,  # cm
        weight=8,   # kg (actual)
        weight_unit="KG",
        dimension_unit="CM"
    )

    zone = ServiceZone(id="zone_us", label="US")
    context = {}

    rate = rate_definition.calculate(package, None, None, zone, context)

    # Volume: 20 × 15 × 10 = 3,000 cm³
    # Dim weight: 3,000 / 6000 = 0.5 kg
    # Billable: max(8kg, 0.5kg) = 8kg
    assert context["actual_weight"] == 8.0
    assert context["dimensional_weight"] == 0.5
    assert context["billable_weight"] == 8.0
    assert rate == 50.00


# Test case 3: Imperial units
def test_dimensional_weight_imperial():
    rate_definition = DimensionalWeightRate(
        rate_id="test_dim",
        weight_unit="LB",
        dimension_unit="IN",
        currency="USD",
        config={
            "dim_factor": 166,
            "tiers": [
                {"zone_id": "zone_us", "min_weight": 0, "max_weight": 50, "rate": 25.00},
            ]
        }
    )

    # Package: 20×16×12 inches, 10 lb
    package = Package(
        length=20,  # in
        width=16,   # in
        height=12,  # in
        weight=10,  # lb (actual)
        weight_unit="LB",
        dimension_unit="IN"
    )

    zone = ServiceZone(id="zone_us", label="US")
    context = {}

    rate = rate_definition.calculate(package, None, None, zone, context)

    # Volume: 20 × 16 × 12 = 3,840 in³
    # Dim weight: 3,840 / 166 = 23.13 lb
    # Billable: max(10lb, 23.13lb) = 23.13lb
    assert context["actual_weight"] == 10.0
    assert abs(context["dimensional_weight"] - 23.13) < 0.01
    assert abs(context["billable_weight"] - 23.13) < 0.01
    assert rate == 25.00
```

#### Frontend UI for Dimensional Weight

**Service Configuration Form**:
```tsx
<div className="service-config-form">
  {/* ... other fields ... */}

  <div className="form-group">
    <label>Dimensional Weight Configuration</label>

    <div className="checkbox-group">
      <input
        type="checkbox"
        checked={useDimensionalWeight}
        onChange={(e) => setUseDimensionalWeight(e.target.checked)}
      />
      <span>Use dimensional weight pricing</span>
    </div>

    {useDimensionalWeight && (
      <>
        <div className="input-group">
          <label>Dim Factor</label>
          <input
            type="number"
            value={dimFactor}
            onChange={(e) => setDimFactor(parseFloat(e.target.value))}
            placeholder="6000 for metric, 166 for imperial"
          />
          <select value={units} onChange={(e) => {
            setUnits(e.target.value);
            // Auto-set dim_factor based on units
            if (e.target.value === 'metric') {
              setDimFactor(6000);
            } else {
              setDimFactor(166);
            }
          }}>
            <option value="metric">Metric (cm/kg)</option>
            <option value="imperial">Imperial (in/lb)</option>
          </select>
        </div>

        <div className="info-box">
          <p><strong>Formula:</strong> (Length × Width × Height) / {dimFactor} = Dimensional Weight</p>
          <p><strong>Billable Weight:</strong> max(Actual Weight, Dimensional Weight)</p>
        </div>
      </>
    )}
  </div>
</div>
```

**Rate Calculation Display**:
```tsx
<div className="rate-details">
  <h4>Rate: ${rate.total_charge.toFixed(2)}</h4>

  {rate.meta?.billable_weight && (
    <div className="weight-breakdown">
      <table>
        <tr>
          <td>Actual Weight:</td>
          <td>{rate.meta.actual_weight} {rate.meta.weight_unit}</td>
        </tr>
        <tr>
          <td>Dimensional Weight:</td>
          <td>{rate.meta.dimensional_weight.toFixed(2)} {rate.meta.weight_unit}</td>
          <td className="muted">
            ({rate.meta.dimensions.length}×{rate.meta.dimensions.width}×{rate.meta.dimensions.height} {rate.meta.dimension_unit} / {rate.meta.dim_factor})
          </td>
        </tr>
        <tr className="billable-row">
          <td><strong>Billable Weight:</strong></td>
          <td><strong>{rate.meta.billable_weight.toFixed(2)} {rate.meta.weight_unit}</strong></td>
          <td className="info-icon" title="Greater of actual or dimensional weight">ℹ️</td>
        </tr>
      </table>
    </div>
  )}
</div>
```

---

**END OF PRD**
