from django.db import migrations, models


def rename_purchased_to_created(apps, schema_editor):
    Shipment = apps.get_model("manager", "Shipment")
    Shipment.objects.filter(status="purchased").update(status="created")


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0088_shipment_order_id"),
    ]

    operations = [
        migrations.RunPython(
            rename_purchased_to_created,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="shipment",
            name="status",
            field=models.CharField(
                max_length=50,
                db_index=True,
                default="draft",
            ),
        ),
    ]
