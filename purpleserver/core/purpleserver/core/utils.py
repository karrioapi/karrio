from typing import List, Type
from django.db.models import Model
from rest_framework.serializers import Serializer


def update_model(instance: Model, serializer: Serializer, exclude: List[str] = None) -> Model:
    if exclude is None:
        exclude = ['id']

    serializer.is_valid(raise_exception=True)
    for key, val in serializer.data.items():
        if key not in exclude and hasattr(instance, key):
            setattr(instance, key, val)
    return instance


def validate_and_save(serializer_type: Type, data, instance=None, **kwargs):
    if data is None:
        return None

    serializer = serializer_type(data=data) if instance is None else serializer_type(instance, data=data, partial=True)

    # We are not raising an exception nor checking the validation result because it was already done.
    serializer.is_valid(raise_exception=True)
    return serializer.save(**kwargs)
