import typing
from django.db import models
from auditlog.registry import auditlog


def register_model(model: models.Model) -> models.Model:

    exclude_fields = ["link"]

    if "Parcel" in model.__name__:
        exclude_fields += ["reference_number"]

    if "Shipment" in model.__name__:
        exclude_fields += ["tracking_url"]

    auditlog.register(model, exclude_fields=exclude_fields)

    return model
