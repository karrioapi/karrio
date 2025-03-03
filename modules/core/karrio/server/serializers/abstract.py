import yaml
import pydoc
import typing
import logging
from django.db import models
from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from django.forms.models import model_to_dict
from drf_spectacular.types import OpenApiTypes

import karrio.lib as lib

logger = logging.getLogger(__name__)
T = typing.TypeVar("T")


class Context(typing.NamedTuple):
    user: typing.Any
    org: typing.Any = None
    test_mode: bool = None

    def __getitem__(self, item):
        return getattr(self, item)


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


def owned_model_serializer(serializer: typing.Type[Serializer]):
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
                logger.exception(e)
                raise e

            return instance

        def update(self, instance, data: dict, **kwargs):
            payload = {k: v for k, v in data.items()}

            return super().update(instance, payload, context=self.__context)

    return type(serializer.__name__, (MetaSerializer,), {})


def link_org(entity: ModelSerializer, context: Context):
    if (
        context.org is not None
        and hasattr(entity, "org")
        and hasattr(entity.org, "exists")
        and not entity.org.exists()
    ):
        entity.link = entity.__class__.link.related.related_model.objects.create(
            org=context.org, item=entity
        )
        entity.save(
            update_fields=(["created_at"] if hasattr(entity, "created_at") else [])
        )

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


def process_dictionaries_mutations(
    keys: typing.List[str], payload: dict, entity
) -> dict:
    """This function checks if the payload contains dictionary with the keys and if so, it
    mutate the values content by removing any null values and adding the new one.
    """
    data = payload.copy()

    for key in [k for k in keys if k in payload]:
        value = lib.to_dict({**getattr(entity, key, {}), **payload.get(key, {})})
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
            **(dict(default=default) if not required else {}),
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
