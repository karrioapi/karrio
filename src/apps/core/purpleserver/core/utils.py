import functools
from typing import Type, TypeVar, Generic, Optional, Union, Callable, Any, List
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import models

T = TypeVar('T')
User = get_user_model


def identity(value: Union[Any, Callable]) -> T:
    """
    :param value: function or value desired to be wrapped
    :return: value or callable return
    """
    return value() if callable(value) else value


def post_processing(methods: List[str] = None):

    def class_wrapper(klass):
        setattr(klass, 'post_process_functions', getattr(klass, 'post_process_functions') or [])

        for name in methods:
            method = getattr(klass, name)

            def wrapper(*args, **kwargs):
                result = method(*args, **kwargs)
                processes = klass.post_process_functions
                return functools.reduce(
                    lambda processed_result, process: process(processed_result), processes, result
                )

            setattr(klass, name, wrapper)

        return klass

    return class_wrapper


def PaginatedResult(serializer_name: str, content_serializer: Type[serializers.Serializer]):
    return type(serializer_name, (serializers.Serializer,), dict(
        next=serializers.URLField(required=False),
        previous=serializers.URLField(required=False),
        results=content_serializer(many=True)
    ))


class _SerializerDecoratorInitializer(Generic[T]):

    def __getitem__(self, serializer_type: Type[serializers.Serializer]):
        class Decorator:
            def __init__(self, instance=None, data: Union[str, dict] = None, **kwargs):
                self._instance = instance

                if data is None and instance is None:
                    self._serializer = None

                else:
                    self._serializer: serializer_type = (
                        serializer_type(data=data, **kwargs) if instance is None else
                        serializer_type(instance, data=data, **{**kwargs, 'partial': True})
                    )

                    self._serializer.is_valid(raise_exception=True)

            @property
            def data(self) -> Optional[dict]:
                return self._serializer.validated_data if self._serializer is not None else None

            @property
            def instance(self):
                return self._instance

            def save(self, **kwargs) -> 'Decorator':
                if self._serializer is not None:
                    self._instance = self._serializer.save(**kwargs)

                return self

        return Decorator


SerializerDecorator = _SerializerDecoratorInitializer()


def save_many_to_many_data(
        serializer: Type[serializers.ModelSerializer],
        name: str,
        instance: models.Model,
        collection_data: List[dict] = None,
        **kwargs):

    current = getattr(instance, name, [])

    if not any(collection_data) and any(current):
        for item in current:
            item.delete()

    for data in collection_data:
        item_instance = next((i for i in current if i.id == data.get('id')), None)
        item = save_one_to_one_data(serializer, item_instance, data=data, **kwargs)

        getattr(instance, name).add(item)


def save_one_to_one_data(
        serializer: Type[serializers.ModelSerializer],
        instance: models.Model = None,
        data: dict = None,
        **kwargs):

    if data is None and instance is not None:
        instance.delete()
        return None

    if instance is None:
        return SerializerDecorator[serializer](data=data, **kwargs).save().instance

    return SerializerDecorator[serializer](instance=instance, data=data, **kwargs).save().instance


def Access(model: models.Model, with_user: User, **kwargs):

    return model.objects.filter(created_by_id=with_user.id, **kwargs)
