"""Karrio Chit Chats unit mappings and constants."""


def map_package_type(package_type: str) -> str:
    """Map Karrio package types to Chit Chats package types."""
    mapping = {
        "envelope": "envelope",
        "pak": "thick_envelope",
        "tube": "parcel",
        "box": "parcel",
        "small_box": "parcel",
        "medium_box": "parcel",
        "large_box": "parcel",
        "custom": "parcel",
    }
    return mapping.get(package_type.lower(), "parcel")


def map_weight_unit(unit: str) -> str:
    """Map Karrio weight units to Chit Chats weight units."""
    mapping = {
        "kg": "kg",
        "lb": "lb",
        "oz": "oz",
        "g": "g"
    }
    return mapping.get(unit.lower(), "g")


def map_dimension_unit(unit: str) -> str:
    """Map Karrio dimension units to Chit Chats dimension units."""
    mapping = {
        "cm": "cm",
        "in": "in",
        "m": "m",
    }
    return mapping.get(unit.lower(), "cm")


# Default country units preferences
COUNTRY_PREFERED_UNITS = {
    "CA": ("kg", "cm"),
    "US": ("lb", "in"),
} 
