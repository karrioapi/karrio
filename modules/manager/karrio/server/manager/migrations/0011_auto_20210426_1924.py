# Generated by Django 3.2 on 2021-04-26 19:24

from django.db import migrations
import jsonfield.fields
from django.forms.models import model_to_dict


def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Customs = apps.get_model("manager", "Customs")
    Shipment = apps.get_model("manager", "Shipment")

    for customs in Customs.objects.using(db_alias).all().iterator():
        if customs.duty is not None:
            customs.duty = model_to_dict(customs.duty)
            customs.save()

    for shipment in Shipment.objects.using(db_alias).all().iterator():
        if shipment.payment is not None:
            shipment.payment = model_to_dict(shipment.payment)
            shipment.save()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0010_auto_20210403_1404"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customs",
            name="duty",
            field=jsonfield.fields.JSONField(blank=True, default={}, null=True),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="payment",
            field=jsonfield.fields.JSONField(blank=True, default={}, null=True),
        ),
        migrations.RunPython(forwards_func, reverse_func),
        migrations.DeleteModel(
            name="Payment",
        ),
    ]
