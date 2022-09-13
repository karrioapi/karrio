import pydoc
import logging
import drf_yasg.openapi as openapi
from typing import Generic, Type, Optional, Union, TypeVar, Any, NamedTuple, List
from django.db import models
from django.conf import settings
from django.db import transaction
from django.forms.models import model_to_dict
from rest_framework import serializers

from karrio.core.utils import DP

logger = logging.getLogger(__name__)
T = TypeVar("T")


class AbstractSerializer:
    def create(self, validated_data, **kwargs):
        super().create(validated_data)

    def update(self, instance, validated_data, **kwargs):
        super().update(instance, validated_data, **kwargs)


class Context(NamedTuple):
    user: Any
    org: Any = None
    test_mode: bool = None

    def __getitem__(self, item):
        return getattr(self, item)


class Serializer(serializers.Serializer, AbstractSerializer):
    pass


class ModelSerializer(serializers.ModelSerializer, AbstractSerializer):
    def create(self, data: dict, **kwargs):
        return self.Meta.model.objects.create(**data)

    def update(self, instance, data: dict, **kwargs):
        for name, value in data.items():
            if name != "created_by":
                setattr(instance, name, value)

        instance.save()
        return instance


class StringListField(serializers.ListField):
    child = serializers.CharField()


class PlainDictField(serializers.DictField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
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


def PaginatedResult(serializer_name: str, content_serializer: Type[Serializer]):
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


class _SerializerDecoratorInitializer(Generic[T]):
    def __getitem__(self, serializer_type: Type[Serializer]):
        class Decorator:
            def __init__(self, instance=None, data: Union[str, dict] = None, **kwargs):
                self._instance = instance

                if data is None and instance is None:
                    self._serializer = None

                else:
                    self._serializer: serializer_type = (
                        serializer_type(data=data, **kwargs)
                        if instance is None
                        else serializer_type(
                            instance, data=data, **{**kwargs, "partial": True}
                        )
                    )

                    self._serializer.is_valid(raise_exception=True)

            @property
            def data(self) -> Optional[dict]:
                return (
                    self._serializer.validated_data
                    if self._serializer is not None
                    else None
                )

            @property
            def instance(self):
                return self._instance

            def save(self, **kwargs) -> "Decorator":
                if self._serializer is not None:
                    self._instance = self._serializer.save(**kwargs)

                return self

        return Decorator


SerializerDecorator = _SerializerDecoratorInitializer()


def owned_model_serializer(serializer: Type[Serializer]):
    class MetaSerializer(serializer):
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
    if hasattr(entity, "org") and context.org is not None and not entity.org.exists():
        entity.link = entity.__class__.link.related.related_model.objects.create(
            org=context.org, item=entity
        )
        entity.save(
            update_fields=(["created_at"] if hasattr(entity, "created_at") else [])
        )


def save_many_to_many_data(
    name: str,
    serializer: ModelSerializer,
    parent: models.Model,
    payload: dict = None,
    **kwargs,
):

    if not any((key in payload for key in [name])):
        return None

    collection_data = payload.get(name)
    collection = getattr(parent, name)

    if collection_data is None and any(collection.all()):
        for item in collection.all():
            item.delete()

    for data in collection_data:
        item_instance = (
            collection.filter(id=data.pop("id")).first() if "id" in data else None
        )

        if item_instance is None:
            item = SerializerDecorator[serializer](data=data, **kwargs).save().instance
        else:
            item = (
                SerializerDecorator[serializer](
                    instance=item_instance, data=data, **{**kwargs, "partial": True}
                )
                .save()
                .instance
            )

        getattr(parent, name).add(item)


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
        new_instance = (
            SerializerDecorator[serializer](data=data, **kwargs).save().instance
        )
        parent and setattr(parent, name, new_instance)
        return new_instance

    return (
        SerializerDecorator[serializer](
            instance=instance, data=data, partial=True, **kwargs
        )
        .save()
        .instance
    )


def allow_model_id(model_paths: []):
    def _decorator(serializer: Type[Serializer]):
        class ModelIdSerializer(serializer):
            def __init__(self, *args, **kwargs):
                for param, model_path in model_paths:
                    content = kwargs.get("data", {}).get(param)
                    values = content if isinstance(content, list) else [content]
                    model = pydoc.locate(model_path)

                    if any([isinstance(val, str) for val in values]):
                        new_content = []
                        for value in values:
                            if isinstance(value, str) and (model is not None):
                                data = model_to_dict(model.objects.get(pk=value))
                                ("id" in data) and data.pop("id")
                                new_content.append(data)

                        kwargs.update(
                            data={
                                **kwargs["data"],
                                param: new_content
                                if isinstance(content, list)
                                else next(iter(new_content)),
                            }
                        )

                super().__init__(*args, **kwargs)

        return type(serializer.__name__, (ModelIdSerializer,), {})

    return _decorator


def make_fields_optional(serializer: Type[ModelSerializer]):
    _name = f"Partial{serializer.__name__}"

    class _Meta(serializer.Meta):
        extra_kwargs = {
            **getattr(serializer.Meta, "extra_kwargs", {}),
            **{
                field.name: {"required": False}
                for field in serializer.Meta.model._meta.fields
            },
        }

    return type(_name, (serializer,), dict(Meta=_Meta))


def exclude_id_field(serializer: Type[ModelSerializer]):
    class _Meta(serializer.Meta):
        exclude = [*getattr(serializer.Meta, "exclude", []), "id"]

    return type(serializer.__name__, (serializer,), dict(Meta=_Meta))


def process_dictionaries_mutations(keys: List[str], payload: dict, entity) -> dict:
    """This function checks if the payload contains dictionary with the keys and if so, it
    mutate the values content by removing any null values and adding the new one.
    """
    data = payload.copy()

    for key in [k for k in keys if k in payload]:
        options = DP.to_dict({**getattr(entity, key, {}), **payload.get(key, {})})
        data.update({key: options})

    return data
