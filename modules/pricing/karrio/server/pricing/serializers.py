"""
Pricing module serializers.

This module provides simple constants and enums for markup types.
The old enum-based CARRIERS and SERVICES are no longer used - markups
now use plain string lists for carrier_codes and service_codes.
"""

import enum


class MarkupType(enum.Enum):
    """Type of markup to apply."""
    AMOUNT = "AMOUNT"
    PERCENTAGE = "PERCENTAGE"


# Markup type choices for Django model field
MARKUP_TYPE = [(c.name, c.name) for c in list(MarkupType)]

# Legacy aliases for backward compatibility
SurchargeType = MarkupType
SURCHAGE_TYPE = MARKUP_TYPE
