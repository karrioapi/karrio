from django.db import models


class Carrier(models.Model):
    class Meta:
        abstract = True

    carrier_id = models.CharField(max_length=200, unique=True)
    test = models.BooleanField(default=True)
