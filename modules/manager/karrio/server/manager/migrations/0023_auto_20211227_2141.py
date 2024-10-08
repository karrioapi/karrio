# Generated by Django 3.2.10 on 2021-12-27 21:41

from django.db import migrations, models
import django.db.models.deletion
import functools
import karrio.server.core.utils


class Migration(migrations.Migration):

    dependencies = [
        ("providers", "0020_genericsettings_labeltemplate"),
        ("manager", "0022_auto_20211122_2100"),
    ]

    operations = [
        migrations.AddField(
            model_name="commodity",
            name="metadata",
            field=models.JSONField(
                blank=True,
                default=functools.partial(
                    karrio.server.core.utils.identity, *(), **{"value": {}}
                ),
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="commodity",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children",
                to="manager.commodity",
            ),
        ),
        migrations.AddField(
            model_name="parcel",
            name="items",
            field=models.ManyToManyField(
                blank=True, related_name="parcels", to="manager.Commodity"
            ),
        ),
        migrations.AddField(
            model_name="shipment",
            name="metadata",
            field=models.JSONField(
                blank=True,
                default=functools.partial(
                    karrio.server.core.utils.identity, *(), **{"value": {}}
                ),
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="customs",
            name="commodities",
            field=models.ManyToManyField(
                blank=True, related_name="customs", to="manager.Commodity"
            ),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="carriers",
            field=models.ManyToManyField(
                blank=True,
                related_name="related_shipments",
                to="providers.Carrier",
            ),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="customs",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="shipment",
                to="manager.customs",
            ),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="parcels",
            field=models.ManyToManyField(related_name="shipment", to="manager.Parcel"),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="recipient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipient_shipment",
                to="manager.address",
            ),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="selected_rate_carrier",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shipments",
                to="providers.carrier",
            ),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="shipper",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shipper_shipment",
                to="manager.address",
            ),
        ),
    ]
