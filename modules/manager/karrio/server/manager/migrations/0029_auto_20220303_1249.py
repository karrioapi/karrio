# Generated by Django 3.2.11 on 2022-03-03 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0026_auto_20220208_0132'),
        ('manager', '0028_auto_20220303_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customs',
            name='commodities',
            field=models.ManyToManyField(blank=True, related_name='commodity_customs', to='manager.Commodity'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='commodity_parcel', to='manager.Commodity'),
        ),
        migrations.AlterField(
            model_name='pickup',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address_pickup', to='manager.address'),
        ),
        migrations.AlterField(
            model_name='pickup',
            name='shipments',
            field=models.ManyToManyField(related_name='shipment_pickup', to='manager.Shipment'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='customs',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customs_shipment', to='manager.customs'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='parcels',
            field=models.ManyToManyField(related_name='parcel_shipment', to='manager.Parcel'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='selected_rate_carrier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carrier_shipments', to='providers.carrier'),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='shipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipment_tracker', to='manager.shipment'),
        ),
    ]
