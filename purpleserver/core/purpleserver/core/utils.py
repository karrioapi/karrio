from typing import List
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
