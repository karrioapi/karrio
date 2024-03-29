# Generated by Django 4.1.3 on 2022-11-28 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0040_parcel_freight_class"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="commodity",
            options={
                "ordering": ["created_at"],
                "verbose_name": "Commodity",
                "verbose_name_plural": "Commodities",
            },
        ),
        migrations.AlterModelOptions(
            name="parcel",
            options={
                "ordering": ["created_at"],
                "verbose_name": "Parcel",
                "verbose_name_plural": "Parcels",
            },
        ),
    ]
