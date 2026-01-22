import re
import yaml
import pydoc
import typing
from django.db import models
from django.conf import settings
from django.db import transaction
from django.forms.models import model_to_dict
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers, request

import karrio.lib as lib
from karrio.server.core.logging import logger

T = typing.TypeVar("T")

# Pattern for JSON-generated IDs: prefix_12hexchars (e.g., pcl_a1b2c3d4e5f6)
JSON_ID_PATTERN = re.compile(r'^[a-z]{2,4}_[a-f0-9]{12}$')


def is_json_generated_id(value: typing.Any) -> bool:
    """Check if a value is a JSON-generated ID (not a database ID).

    JSON-generated IDs have the format: prefix_12hexchars
    Examples: pcl_a1b2c3d4e5f6, adr_123abc456def, itm_x9y8z7w6v5u4
    """
    if not isinstance(value, str):
        return False
    return JSON_ID_PATTERN.match(value) is not None


class Context(typing.NamedTuple):
    user: typing.Any
    org: typing.Any = None
    test_mode: bool = None

    def __getitem__(self, item):
        return getattr(self, item)


RequestContext = typing.Union[Context, dict, request.Request]


class DecoratedSerializer:
    def __init__(
        self,
        instance: models.Model = None,
        serializer: "Serializer" = None,
    ):
        self._instance = instance
        self._serializer = serializer

    @property
    def data(self) -> typing.Optional[dict]:
        return self._serializer.validated_data if self._serializer is not None else None

    @property
    def instance(self) -> models.Model:
        return self._instance

    def save(self, **kwargs) -> "DecoratedSerializer":
        if self._serializer is not None:
            self._instance = self._serializer.save(**kwargs)

        return self


class AbstractSerializer:
    def create(self, validated_data, **kwargs):
        super().create(validated_data)

    def update(self, instance, validated_data, **kwargs):
        super().update(instance, validated_data, **kwargs)

    @classmethod
    def map(
        cls, instance=None, data: typing.Union[str, dict] = None, **kwargs
    ) -> "DecoratedSerializer":
        if data is None and instance is None:
            serializer = None
        else:
            serializer = (
                cls(data=data or {}, **kwargs)  # type:ignore
                if instance is None
                else cls(
                    instance, data=data or {}, **{**kwargs, "partial": True}
                )  # type:ignore
            )

            serializer.is_valid(raise_exception=True)  # type:ignore

        return DecoratedSerializer(
            instance=instance,
            serializer=serializer,  # type:ignore
        )


class Serializer(serializers.Serializer, AbstractSerializer):
    context: dict = {}


class ModelSerializer(serializers.ModelSerializer, AbstractSerializer):
    def create(self, data: dict, **kwargs):  # type: ignore
        return self.Meta.model.objects.create(**data)

    def update(self, instance, data: dict, **kwargs):  # type: ignore
        for name, value in data.items():
            if name != "created_by" and hasattr(instance, name):
                setattr(instance, name, value)

        instance.save()
        return instance


class StringListField(serializers.ListField):
    child = serializers.CharField()


class PlainDictField(serializers.DictField):
    class Meta:
        swagger_schema_fields = {
            "type": OpenApiTypes.OBJECT,
            "additional_properties": True,
        }


class FlagField(serializers.BooleanField):
    pass


class FlagsSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        data = kwargs.get("data", {})
        self.flags = [
            (label, label in data)
            for label, field in self.fields.items()
            if isinstance(field, FlagField)
        ]

        super().__init__(*args, **kwargs)

    def validate(self, data):
        validated = super().validate(data)
        for flag, specified in self.flags:
            if specified and validated[flag] is None:
                validated.update({flag: True})

        return validated


class EntitySerializer(serializers.Serializer):
    id = serializers.CharField(required=False, help_text="A unique identifier")


"""
Custom serializer utilities functions
"""


def PaginatedResult(serializer_name: str, content_serializer: typing.Type[Serializer]):
    return type(
        serializer_name,
        (Serializer,),
        dict(
            count=serializers.IntegerField(required=False, allow_null=True),
            next=serializers.URLField(
                required=False, allow_blank=True, allow_null=True
            ),
            previous=serializers.URLField(
                required=False, allow_blank=True, allow_null=True
            ),
            results=content_serializer(many=True),
        ),
    )


def owned_model_serializer(
    serializer: typing.Type[typing.Union[Serializer, ModelSerializer]],
):
    class MetaSerializer(serializer):  # type: ignore
        context: dict = {}

        def __init__(self, *args, **kwargs):
            if "context" in kwargs:
                context = kwargs.get("context") or {}
                user = (
                    context.get("user") if isinstance(context, dict) else context.user
                )
                org = context.get("org") if isinstance(context, dict) else context.org
                test_mode = (
                    context.get("test_mode")
                    if isinstance(context, dict)
                    else context.test_mode
                )

                if settings.MULTI_ORGANIZATIONS and org is None:
                    import karrio.server.orgs.models as orgs

                    org = orgs.Organization.objects.filter(
                        users__id=getattr(user, "id", None)
                    ).first()

                self.__context: Context = Context(user, org, test_mode)
            else:
                self.__context: Context = getattr(self, "__context", None)
                kwargs.update({"context": self.__context})

            super().__init__(*args, **kwargs)

        @transaction.atomic
        def create(self, data: dict, **kwargs):
            payload = {"created_by": self.__context.user, **data}

            try:
                instance = super().create(payload, context=self.__context)
                link_org(instance, self.__context)  # Link to organization if supported
            except Exception as e:
                # Log exception with full traceback for debugging
                meta = getattr(self.__class__, "Meta", None)
                model_name = getattr(
                    getattr(meta, "model", None), "__name__", "Unknown"
                )
                logger.exception(
                    f"Failed to create {model_name} instance using {self.__class__.__name__}: {str(e)}"
                )
                raise

            return instance

        def update(self, instance, data: dict, **kwargs):
            payload = {k: v for k, v in data.items()}

            return super().update(instance, payload, context=self.__context)

    return type(serializer.__name__, (MetaSerializer,), {})


def link_org(entity: ModelSerializer, context: Context):
    from django.utils.functional import SimpleLazyObject

    # Evaluate org from context (handles SimpleLazyObject)
    org = (
        context.org if not isinstance(context.org, SimpleLazyObject)
        else (context.org if context.org else None)
    )

    # Check if entity can be linked to org
    entity_org = getattr(entity, "org", None)
    has_org_relation = entity_org is not None and hasattr(entity_org, "exists")
    should_link = org is not None and has_org_relation and not entity_org.exists()

    if should_link:
        entity.link = entity.__class__.link.related.related_model.objects.create(org=org, item=entity)
        entity.save(update_fields=(["created_at"] if hasattr(entity, "created_at") else []))


def bulk_link_org(entities: typing.List[models.Model], context: Context):
    if len(entities) == 0 or settings.MULTI_ORGANIZATIONS is False:
        return

    EntityLinkModel = entities[0].__class__.link.related.related_model
    links = []

    for entity in entities:
        entity.link = EntityLinkModel(org=context.org, item=entity)
        links.append(entity.link)

    EntityLinkModel.objects.bulk_create(links)


def get_object_context(entity) -> Context:
    org = lib.failsafe(
        lambda: (
            entity.org.first()
            if (hasattr(entity, "org") and entity.org.exists())
            else None
        )
    )

    return Context(
        org=org,
        user=getattr(entity, "created_by", None),
        test_mode=getattr(entity, "test_mode", None),
    )


def save_many_to_many_data(
    name: str,
    serializer: ModelSerializer,
    parent: models.Model,
    payload: dict = None,
    remove_if_missing: bool = False,
    **kwargs,
):
    if not any((key in payload for key in [name])):
        return None

    collection_data = payload.get(name)
    collection = getattr(parent, name)

    if collection_data is None and any(collection.all()):
        for item in collection.all():
            item.delete()

    if remove_if_missing and collection.exists():
        collection.exclude(id__in=[item.get("id") for item in collection_data]).delete()

    for data in collection_data:
        item_instance = (
            collection.filter(id=data.pop("id")).first() if "id" in data else None
        )

        if item_instance is None:
            item = serializer.map(data=data, **kwargs).save().instance
            getattr(parent, name).add(item)
        else:
            item = (
                serializer.map(
                    data=data,
                    instance=item_instance,
                    **{**kwargs, "partial": True},
                )
                .save()
                .instance
            )


def save_one_to_one_data(
    name: str,
    serializer: ModelSerializer,
    parent: models.Model = None,
    payload: dict = None,
    **kwargs,
):
    if name not in payload:
        return None

    data = payload.get(name)
    instance = getattr(parent, name, None)

    if data is None and instance is not None:
        instance.delete()
        setattr(parent, name, None)

    if instance is None:
        new_instance = serializer.map(data=data, **kwargs).save().instance
        parent and setattr(parent, name, new_instance)  # type: ignore
        return new_instance

    return (
        serializer.map(instance=instance, data=data, **{**kwargs, "partial": True})
        .save()
        .instance
    )


def allow_model_id(model_paths: []):  # type: ignore
    def _decorator(serializer: typing.Type[Serializer]):
        class ModelIdSerializer(serializer):  # type: ignore
            def __init__(self, *args, **kwargs):
                for param, model_path in model_paths:
                    content = kwargs.get("data", {}).get(param)
                    values = content if isinstance(content, list) else [content]
                    model = pydoc.locate(model_path)

                    if any([isinstance(val, dict) and "id" in val for val in values]):
                        new_content = []
                        for value in values:
                            if (
                                isinstance(value, dict)
                                and ("id" in value)
                                and (model is not None)
                            ):
                                # Skip database lookup for JSON-generated IDs (pcl_xxx, adr_xxx, etc.)
                                # These are embedded JSON data, not database references
                                if is_json_generated_id(value["id"]):
                                    new_content.append(value)
                                    continue

                                data = model_to_dict(model.objects.get(pk=value["id"]))

                                for field, field_data in data.items():
                                    if isinstance(field_data, list):
                                        data[field] = [
                                            (
                                                model_to_dict(item)
                                                if hasattr(item, "_meta")
                                                else item
                                            )
                                            for item in field_data
                                        ]

                                    if hasattr(field_data, "_meta"):
                                        data[field] = model_to_dict(field_data)

                                ("id" in data) and data.pop("id")
                                new_content.append(data)

                        kwargs.update(
                            data={
                                **kwargs["data"],
                                param: (
                                    new_content
                                    if isinstance(content, list)
                                    else next(iter(new_content))
                                ),
                            }
                        )

                super().__init__(*args, **kwargs)

        return type(serializer.__name__, (ModelIdSerializer,), {})

    return _decorator


def make_fields_optional(serializer: typing.Type[ModelSerializer]):
    _name = f"Partial{serializer.__name__}"

    class _Meta(serializer.Meta):  # type: ignore
        extra_kwargs = {
            **getattr(serializer.Meta, "extra_kwargs", {}),
            **{
                field.name: {"required": False}
                for field in serializer.Meta.model._meta.fields
            },
        }

    return type(_name, (serializer,), dict(Meta=_Meta))


def exclude_id_field(serializer: typing.Type[ModelSerializer]):
    class _Meta(serializer.Meta):  # type: ignore
        exclude = [*getattr(serializer.Meta, "exclude", []), "id"]

    return type(serializer.__name__, (serializer,), dict(Meta=_Meta))


def is_field_optional(model, field_name: str) -> bool:
    field = getattr(model, field_name)

    if hasattr(field, "field"):
        return field.field.null

    return False


def deep_merge_remove_nulls(base: dict, updates: dict) -> dict:
    """Deep merge two dictionaries, removing keys with null values from updates.

    Args:
        base: The base dictionary (existing data)
        updates: The updates dictionary (new data with potential nulls to remove)

    Returns:
        Merged dictionary with null values removed

    Examples:
        >>> base = {"a": 1, "b": {"c": 2, "d": 3}}
        >>> updates = {"b": {"c": null, "e": 4}}
        >>> deep_merge_remove_nulls(base, updates)
        {"a": 1, "b": {"d": 3, "e": 4}}  # c removed due to null
    """
    result = base.copy()

    for key, value in updates.items():
        if value is None:
            # Explicit null means remove the key
            result.pop(key, None)
        elif isinstance(value, dict) and isinstance(result.get(key), dict):
            # Both are dicts: recursively merge
            result[key] = deep_merge_remove_nulls(result[key], value)
        else:
            # Overwrite with new value
            result[key] = value

    return result


def process_nested_dictionaries_mutations(
    keys: typing.List[str], payload: dict, entity
) -> dict:
    """Process nested dictionary mutations with deep merge and null removal.

    This function is designed for complex nested JSON fields where you need:
    - Deep merging of nested objects
    - Removal of keys when explicit null is sent
    - Preservation of unaffected nested keys

    Use this for fields like shipping rule actions/conditions that have nested extensions.
    For simple flat dictionaries, use process_dictionaries_mutations instead.

    Args:
        keys: List of field names to process
        payload: Input data from mutation
        entity: Existing entity instance

    Returns:
        Updated payload with deep merged values

    Examples:
        Existing: {"actions": {"select_service": {"carrier": "ups"}, "extensions": {"old": "data"}}}
        Update: {"actions": {"extensions": {"new": "data"}}}
        Result: {"actions": {"select_service": {"carrier": "ups"}, "extensions": {"old": "data", "new": "data"}}}
    """
    data = payload.copy()

    for key in [k for k in keys if k in payload]:
        existing_value = getattr(entity, key, None) or {}
        new_value = payload.get(key)

        if new_value is None:
            # Explicit null means clear the entire field
            data[key] = {}
        else:
            # Deep merge with null removal
            data[key] = deep_merge_remove_nulls(existing_value, new_value)

    return data


def process_dictionaries_mutations(
    keys: typing.List[str], payload: dict, entity
) -> dict:
    """This function checks if the payload contains dictionary with the keys and if so, it
    mutate the values content by removing any null values and adding the new one.
    """
    data = payload.copy()

    for key in [k for k in keys if k in payload and payload.get(k) is not None]:
        value = lib.to_dict(
            {**(getattr(entity, key, None) or {}), **(payload.get(key, None) or {})}
        )
        data.update({key: value})

    return data


def get_query_flag(
    key: str,
    query_params: dict,
    nullable: bool = True,
) -> typing.Optional[bool]:
    _value = yaml.safe_load(query_params.get(key) or "")

    if key in query_params and _value is not False:
        return True

    if nullable:
        return _value

    return False


def field_to_serializer(args: dict):
    [type, name, required, default, enum] = [
        args.get("type"),
        args.get("name"),
        args.get("required"),
        args.get("default"),
        args.get("enum"),
    ]

    if enum:
        return serializers.ChoiceField(
            choices=enum,
            required=required,
            help_text=f"Indicates a {name} {type}",
        )
    if type == "string":
        return serializers.CharField(
            required=required,
            **(
                dict(default=default, allow_blank=True, allow_null=True)
                if not required
                else {}
            ),
        )
    if type == "integer":
        return serializers.IntegerField(
            required=required,
            **(dict(default=default) if not required else {}),
        )
    if type == "boolean":
        return serializers.BooleanField(
            required=required,
            **(dict(default=default) if not required else {}),
        )
    if type == "float":
        return serializers.FloatField(
            required=required,
            **(dict(default=default) if not required else {}),
        )
    if type == "datetime":
        return serializers.DateTimeField(
            required=required,
            **(dict(default=default) if not required else {}),
        )
    if type == "date":
        return serializers.DateField(
            required=required,
            **(dict(default=default) if not required else {}),
        )
    if type == "decimal":
        return serializers.DecimalField(
            required=required,
            **(dict(default=default) if not required else {}),
        )
    if type == "uuid":
        return serializers.UUIDField(
            required=required,
            **(dict(default=default) if not required else {}),
        )
    if type == "email":
        return serializers.EmailField(
            required=required,
            **(dict(default=default) if not required else {}),
        )
    if type == "url":
        return serializers.URLField(
            required=required,
            **(dict(default=default) if not required else {}),
        )
