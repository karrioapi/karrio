import typing
from django.db import models
from auditlog.registry import auditlog


def register_model(model: models.Model) -> models.Model:

    auditlog.register(model)

    return model
