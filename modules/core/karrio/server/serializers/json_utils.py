"""JSON field mutation utilities for embedded data patterns.

This module provides reusable utilities for handling JSONField mutations
following Stripe's API patterns for array item management.

Key patterns:
- Single objects: deep merge with null removal
- Arrays: add/update/delete items with generated IDs
- Deletion: {"id": "x", "deleted": true} (Stripe pattern)
- Template resolution: convert template ID to JSON snapshot
"""

import typing
import uuid

import karrio.lib as lib


def generate_json_id(prefix: str = "id") -> str:
    """Generate unique ID for JSON array items.

    Args:
        prefix: ID prefix (e.g., 'pcl', 'itm', 'oli', 'cmd')

    Returns:
        Unique ID like 'pcl_abc123def456'

    Examples:
        >>> generate_json_id('pcl')
        'pcl_a1b2c3d4e5f6'
        >>> generate_json_id('itm')
        'itm_x9y8z7w6v5u4'
    """
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def deep_merge_remove_nulls(base: dict, updates: dict) -> dict:
    """Deep merge two dictionaries, removing keys with null values.

    Args:
        base: The base dictionary (existing data)
        updates: The updates dictionary (new data with potential nulls to remove)

    Returns:
        Merged dictionary with null values removed

    Examples:
        >>> base = {"a": 1, "b": {"c": 2, "d": 3}}
        >>> updates = {"b": {"c": None, "e": 4}}
        >>> deep_merge_remove_nulls(base, updates)
        {"a": 1, "b": {"d": 3, "e": 4}}  # c removed due to null
    """
    result = base.copy()

    for key, value in updates.items():
        if value is None:
            result.pop(key, None)
        elif isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge_remove_nulls(result[key], value)
        else:
            result[key] = value

    return result


def resolve_template_to_json(
    template_id: str,
    model_class: type,
    include_template_ref: bool = True,
    excluded_fields: typing.Optional[set] = None,
) -> typing.Optional[dict]:
    """Resolve a template ID to JSON data.

    Replaces @allow_model_id decorator with explicit resolution.

    Args:
        template_id: ID of the template to resolve
        model_class: Model class (Address, Parcel, Product)
        include_template_ref: Whether to include id in result (for single objects)
        excluded_fields: Fields to exclude from result

    Returns:
        JSON dict with template data, or None if not found
    """
    template = model_class.objects.filter(id=template_id).first()
    if template is None:
        return None

    default_excluded = {'created_at', 'updated_at', 'created_by', 'org', 'link'}
    excluded = default_excluded | (excluded_fields or set())

    data = lib.to_dict(template)
    result = {k: v for k, v in data.items() if k not in excluded and v is not None}

    if include_template_ref:
        result['id'] = template_id

    return result


def process_json_object_mutation(
    field_name: str,
    payload: dict,
    instance: typing.Any,
    model_class: typing.Optional[type] = None,
    object_type: typing.Optional[str] = None,
    id_prefix: typing.Optional[str] = None,
) -> typing.Optional[dict]:
    """Process mutation for a single JSON object field (shipper, recipient, etc.).

    Supports:
    - Full object replacement
    - Partial deep merge with null removal
    - Template ID resolution (string or {"id": "template_id"})
    - Explicit null to clear

    Args:
        field_name: Name of the JSON field
        payload: Input mutation data
        instance: Parent model instance (can be None for create)
        model_class: Optional model for template resolution
        object_type: Object type to add to result (e.g., 'address', 'parcel')
        id_prefix: Prefix for generated ID (e.g., 'adr' -> 'adr_xxxx')

    Returns:
        Updated JSON dict, or None if field should be cleared
    """
    if field_name not in payload:
        return getattr(instance, field_name, None) if instance else None

    new_data = payload.get(field_name)
    existing_data = (getattr(instance, field_name, None) or {}) if instance else {}

    # Explicit null = clear the field
    if new_data is None:
        return None

    result = None

    # String = template ID resolution
    if isinstance(new_data, str) and model_class:
        result = resolve_template_to_json(new_data, model_class)
    # Dict with only 'id' = template ID resolution
    elif isinstance(new_data, dict) and set(new_data.keys()) == {'id'} and model_class:
        result = resolve_template_to_json(new_data['id'], model_class)
    else:
        # Dict = deep merge with null removal
        result = deep_merge_remove_nulls(existing_data, new_data)

    # Add object_type if specified and result is a dict
    if result and isinstance(result, dict):
        if object_type:
            result.setdefault('object_type', object_type)
        # Generate ID if prefix specified and no existing ID
        if id_prefix and 'id' not in result:
            result['id'] = generate_json_id(id_prefix)

    return result


def process_json_array_mutation(
    field_name: str,
    payload: dict,
    instance: typing.Any,
    id_prefix: str = "id",
    model_class: typing.Optional[type] = None,
    nested_arrays: typing.Optional[dict] = None,
    object_type: typing.Optional[str] = None,
    data_field_name: typing.Optional[str] = None,
) -> typing.Optional[list]:
    """Process mutation for a JSON array field (parcels, items, line_items, etc.).

    Follows Stripe's API pattern for array mutations.

    Supports:
    - Add new items (no id -> generate one)
    - Update existing items (by id match + deep merge)
    - Delete items via {"id": "x", "deleted": true} (Stripe pattern)
    - Clear entire array via null
    - Template ID resolution for new items
    - Nested array processing (e.g., parcel.items)

    Args:
        field_name: Name of the field in payload
        payload: Input mutation data
        instance: Parent model instance (can be None for create)
        id_prefix: Prefix for generated IDs (e.g., 'pcl', 'itm')
        model_class: Optional model for template resolution
        nested_arrays: Dict of {field_name: (prefix, model_class)} for nested arrays
        object_type: Object type to add to each item (e.g., 'parcel', 'commodity')
        data_field_name: Name of the JSON field on instance to read existing data from
                         (defaults to field_name if not specified)

    Returns:
        Updated JSON array, or empty list if cleared

    Examples:
        # Delete a parcel
        {"parcels": [{"id": "pcl_123", "deleted": true}]}

        # Delete nested item from parcel
        {"parcels": [{"id": "pcl_123", "items": [{"id": "itm_456", "deleted": true}]}]}

        # Combined: delete one, update one, add one
        {"parcels": [
            {"id": "pcl_111", "deleted": true},
            {"id": "pcl_222", "weight": 5.0},
            {"weight": 1.0}  # new, id will be generated
        ]}
    """
    # Use data_field_name for reading from instance, fall back to field_name
    instance_field = data_field_name or field_name

    if field_name not in payload:
        return getattr(instance, instance_field, None) if instance else []

    new_items = payload.get(field_name)
    existing_items = (getattr(instance, instance_field, None) or []) if instance else []

    # Explicit null = clear the array
    if new_items is None:
        return []

    # Build lookup of existing items by ID
    existing_by_id = {
        item.get('id'): item
        for item in existing_items
        if isinstance(item, dict) and item.get('id')
    }

    # Determine nested array field names to exclude from deep merge
    nested_field_names = set(nested_arrays.keys()) if nested_arrays else set()

    result = []
    for item_data in new_items:
        # Skip items marked for deletion (Stripe pattern)
        if isinstance(item_data, dict) and item_data.get('deleted') is True:
            continue

        # Handle template ID resolution (string or {'id': ...} with only id key)
        if isinstance(item_data, str) and model_class:
            resolved = resolve_template_to_json(
                item_data, model_class, include_template_ref=False
            )
            if resolved:
                item_data = {**resolved, 'template_id': item_data}

        elif (
            isinstance(item_data, dict)
            and set(item_data.keys()) == {'id'}
            and model_class
        ):
            resolved = resolve_template_to_json(
                item_data['id'], model_class, include_template_ref=False
            )
            if resolved:
                item_data = {**resolved, 'template_id': item_data['id']}

        item_id = item_data.get('id') if isinstance(item_data, dict) else None

        if item_id and item_id in existing_by_id:
            # Update existing item - deep merge (exclude 'deleted' and nested arrays)
            clean_data = {
                k: v
                for k, v in item_data.items()
                if k != 'deleted' and k not in nested_field_names
            }
            merged = deep_merge_remove_nulls(existing_by_id[item_id], clean_data)
            # Add object_type if specified
            if object_type:
                merged.setdefault('object_type', object_type)
            result.append(merged)
        else:
            # New item - generate ID and reference_number
            clean_data = {
                k: v
                for k, v in item_data.items()
                if k != 'deleted' and k not in nested_field_names
            }
            new_id = generate_json_id(id_prefix)
            new_item = {**clean_data, 'id': new_id}
            # Add object_type if specified
            if object_type:
                new_item.setdefault('object_type', object_type)
            # Add reference_number for parcels (use last part of ID)
            if id_prefix == 'pcl' and 'reference_number' not in new_item:
                new_item['reference_number'] = new_id.replace('pcl_', '')
            result.append(new_item)

        # Process nested arrays AFTER adding to result
        if nested_arrays and isinstance(item_data, dict):
            for nested_field, (nested_prefix, nested_model) in nested_arrays.items():
                if nested_field in item_data:
                    # Get existing nested items from the ORIGINAL existing item
                    existing_nested = (
                        existing_by_id.get(item_id, {}).get(nested_field, [])
                        if item_id
                        else []
                    )

                    # Create a simple object to pass existing nested items
                    class NestedInstance:
                        pass

                    nested_instance = NestedInstance()
                    setattr(nested_instance, nested_field, existing_nested)

                    result[-1][nested_field] = process_json_array_mutation(
                        nested_field,
                        {nested_field: item_data[nested_field]},
                        nested_instance,
                        id_prefix=nested_prefix,
                        model_class=nested_model,
                    )
                else:
                    # Initialize nested arrays to empty list if not present
                    result[-1].setdefault(nested_field, [])

    return result


def process_customs_mutation(
    payload: dict,
    instance: typing.Any,
    address_model: typing.Optional[type] = None,
    product_model: typing.Optional[type] = None,
) -> typing.Optional[dict]:
    """Process mutation for customs JSON field with nested duty_billing_address and commodities.

    Args:
        payload: Input mutation data containing 'customs' key
        instance: Parent model instance (Shipment)
        address_model: Address model for template resolution
        product_model: Product model for commodity template resolution

    Returns:
        Updated customs JSON dict, or None if cleared
    """
    if 'customs' not in payload:
        return getattr(instance, 'customs', None) if instance else None

    customs_data = payload.get('customs')

    # Explicit null = clear customs
    if customs_data is None:
        return None

    existing_customs = (getattr(instance, 'customs', None) or {}) if instance else {}

    # Process duty_billing_address
    if 'duty_billing_address' in customs_data:
        # Create a simple object for the nested call
        class CustomsInstance:
            pass

        customs_instance = CustomsInstance()
        customs_instance.duty_billing_address = existing_customs.get(
            'duty_billing_address'
        )

        customs_data['duty_billing_address'] = process_json_object_mutation(
            'duty_billing_address',
            customs_data,
            customs_instance,
            model_class=address_model,
            object_type='address',
        )

    # Process commodities array
    if 'commodities' in customs_data:

        class CustomsInstance:
            pass

        customs_instance = CustomsInstance()
        customs_instance.commodities = existing_customs.get('commodities', [])

        customs_data['commodities'] = process_json_array_mutation(
            'commodities',
            customs_data,
            customs_instance,
            id_prefix='cmd',
            model_class=product_model,
            object_type='commodity',
        )

    # Deep merge the rest of customs fields
    fields_to_exclude = {'duty_billing_address', 'commodities'}
    other_fields = {k: v for k, v in customs_data.items() if k not in fields_to_exclude}

    result = deep_merge_remove_nulls(
        {k: v for k, v in existing_customs.items() if k not in fields_to_exclude},
        other_fields,
    )

    # Add back processed nested fields
    if 'duty_billing_address' in customs_data:
        result['duty_billing_address'] = customs_data['duty_billing_address']
    elif 'duty_billing_address' in existing_customs:
        result['duty_billing_address'] = existing_customs['duty_billing_address']

    if 'commodities' in customs_data:
        result['commodities'] = customs_data['commodities']
    elif 'commodities' in existing_customs:
        result['commodities'] = existing_customs['commodities']

    return result
