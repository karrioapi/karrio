from django.db import models


class Carrier(models.Model):
    name = models.CharField(max_length=200)
    test = models.BooleanField()


class CanadaPostSettings(models.Model):
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    customer_number = models.CharField(max_length=200)
    contract_id = models.CharField(max_length=200)


class FedexSettings(models.Model):
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    user_key = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    meter_number = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
