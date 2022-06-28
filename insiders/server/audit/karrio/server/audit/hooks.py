import typing
from django.db import models
from auditlog.registry import auditlog


def register_model(model: models.Model) -> models.Model:

    exclude_fields = ["link"]

    auditlog.register(model, exclude_fields=exclude_fields)

    return model
