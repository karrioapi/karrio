"""Service-level tags registry.

Single source of truth for tag definitions used by:
- ``ServiceLevel.tags`` (storage validation)
- ``rate_sheets`` importer (``<key>_tag`` column dispatch)
- Base + admin GraphQL (``tagDefinitions`` query, ``derivedBadges`` resolver)
- Live rates REST (``?tag=k:v`` filter, ``display_priority`` sort)

Adding a new tag is a one-line registry entry — no model migration required.
See ``PRDs/RATE_SHEET_SERVICE_TAGS.md`` for the design rationale.
"""

import typing

import attr

# ─────────────────────────────────────────────────────────────────────────────
# REGISTRY DATATYPES
# ─────────────────────────────────────────────────────────────────────────────


@attr.s(auto_attribs=True)
class TagBadge:
    """Render config for an enum value that should appear as a badge."""

    priority: int
    style: str
    label_key: str


@attr.s(auto_attribs=True)
class TagSpec:
    """Declarative specification for a tag in the registry."""

    kind: str  # "bool" | "enum" | "int"
    values: list[str] | None = None
    range: tuple[int, int] | None = None
    default: typing.Any = None
    label_key: str = ""
    value_label_key_prefix: str = ""
    badges: dict[str, TagBadge] = attr.Factory(dict)
    filterable: bool = True
    sortable: bool = False


# ─────────────────────────────────────────────────────────────────────────────
# REGISTRY
# ─────────────────────────────────────────────────────────────────────────────


TAG_REGISTRY: dict[str, TagSpec] = {
    "recommended": TagSpec(
        kind="bool",
        default=False,
        label_key="tags.recommended.label",
    ),
    "recommendation_category": TagSpec(
        kind="enum",
        values=[
            "most_popular",
            "home_delivery",
            "service_point",
            "international",
            "bulky",
            "economy",
            "express",
        ],
        label_key="tags.recommendation_category.label",
        value_label_key_prefix="tags.recommendation_category.values.",
    ),
    "recommendation_type": TagSpec(
        kind="enum",
        values=["recommended", "best_price", "fastest", "eco", "new"],
        label_key="tags.recommendation_type.label",
        value_label_key_prefix="tags.recommendation_type.values.",
        badges={
            "recommended": TagBadge(priority=50, style="yellow", label_key="tags.badge.recommended"),
            "best_price": TagBadge(priority=60, style="green", label_key="tags.badge.best_price"),
            "fastest": TagBadge(priority=55, style="purple", label_key="tags.badge.fastest"),
            "eco": TagBadge(priority=45, style="green", label_key="tags.badge.eco"),
            "new": TagBadge(priority=30, style="blue", label_key="tags.badge.new"),
        },
    ),
    "display_priority": TagSpec(
        kind="int",
        range=(0, 100),
        default=50,
        label_key="tags.display_priority.label",
        filterable=False,
        sortable=True,
    ),
    "surface_visibility": TagSpec(
        kind="enum",
        values=["default", "hidden", "internal_only"],
        default="default",
        label_key="tags.surface_visibility.label",
        value_label_key_prefix="tags.surface_visibility.values.",
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# COERCION + VALIDATION
# ─────────────────────────────────────────────────────────────────────────────


_TRUTHY = {"1", "true", "t", "yes", "y", "on"}
_FALSY = {"0", "false", "f", "no", "n", "off", ""}


def _coerce_bool(raw: typing.Any) -> tuple[bool | None, str | None]:
    if isinstance(raw, bool):
        return raw, None
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return bool(raw), None
    if isinstance(raw, str):
        normalized = raw.strip().lower()
        if normalized in _TRUTHY:
            return True, None
        if normalized in _FALSY:
            return False, None
    return None, f"expected boolean, got {raw!r}"


def _coerce_int(
    raw: typing.Any,
    range_: tuple[int, int] | None,
) -> tuple[int | None, str | None]:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return None, f"expected integer, got {raw!r}"
    if range_ is not None:
        low, high = range_
        if value < low or value > high:
            return None, f"value {value} out of range [{low}, {high}]"
    return value, None


def _coerce_enum(
    raw: typing.Any,
    values: list[str],
) -> tuple[str | None, str | None]:
    if not isinstance(raw, str):
        return None, f"expected one of {values}, got {raw!r}"
    normalized = raw.strip().lower()
    if normalized in values:
        return normalized, None
    return None, f"expected one of {values}, got {raw!r}"


def coerce_tag_value(
    key: str,
    raw: typing.Any,
) -> tuple[typing.Any, str | None]:
    """Coerce a raw value into the registry-typed value for ``key``.

    Returns ``(value, None)`` on success, ``(None, error)`` on failure.
    """
    spec = TAG_REGISTRY.get(key)
    if spec is None:
        return None, f"unknown tag key {key!r}"
    if spec.kind == "bool":
        return _coerce_bool(raw)
    if spec.kind == "enum":
        return _coerce_enum(raw, spec.values or [])
    if spec.kind == "int":
        return _coerce_int(raw, spec.range)
    return None, f"unsupported tag kind {spec.kind!r} for key {key!r}"


def validate_tags(
    tags: dict[str, typing.Any] | None,
) -> tuple[dict[str, typing.Any], list[str]]:
    """Coerce and validate a tag dict against ``TAG_REGISTRY``.

    Returns ``(cleaned, warnings)``. Unknown keys and invalid values produce
    warnings; valid pairs land in ``cleaned``. An empty input maps to an empty
    cleaned dict, never raises.
    """
    cleaned: dict[str, typing.Any] = {}
    warnings: list[str] = []
    for key, raw in (tags or {}).items():
        if key not in TAG_REGISTRY:
            warnings.append(f"unknown tag key {key!r}")
            continue
        value, error = coerce_tag_value(key, raw)
        if error is not None:
            warnings.append(f"tag {key!r}: {error}")
            continue
        cleaned[key] = value
    return cleaned, warnings


# ─────────────────────────────────────────────────────────────────────────────
# DERIVED BADGES
# ─────────────────────────────────────────────────────────────────────────────


def derive_badges(
    tags: dict[str, typing.Any] | None,
) -> list[dict[str, typing.Any]]:
    """Compute the badges that should render for a given tag dict.

    Walks every registry entry with a ``badges`` map, looks up the value on
    ``tags``, and selects the highest-priority match. Returns a list (0 or 1
    today; list shape leaves room for future multi-badge scenarios without an
    API change).
    """
    if not tags:
        return []

    candidates = [
        spec.badges[tags[key]] for key, spec in TAG_REGISTRY.items() if spec.badges and tags.get(key) in spec.badges
    ]
    if not candidates:
        return []

    winner = max(candidates, key=lambda b: b.priority)
    return [
        {
            "label_key": winner.label_key,
            "style": winner.style,
            "priority": winner.priority,
        }
    ]


# ─────────────────────────────────────────────────────────────────────────────
# COLUMN-NAME HELPERS (for the rate-sheet importer)
# ─────────────────────────────────────────────────────────────────────────────


TAG_COLUMN_SUFFIX = "_tag"


def column_to_tag_key(column: str) -> str | None:
    """Return the tag key for a column name ending in ``_tag``.

    Returns ``None`` when the column does not end with the suffix, when it ends
    with only the suffix (no key), or when the resulting key is not in the
    registry. The importer treats ``None`` as "this column is not a tag column"
    and falls through to its existing dispatch.
    """
    if not column.endswith(TAG_COLUMN_SUFFIX):
        return None
    key = column[: -len(TAG_COLUMN_SUFFIX)]
    if not key or key not in TAG_REGISTRY:
        return None
    return key
