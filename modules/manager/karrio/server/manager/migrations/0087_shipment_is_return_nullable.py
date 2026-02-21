from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0086_shipment_is_return"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shipment",
            name="is_return",
            field=models.BooleanField(
                null=True,
                default=False,
                db_index=True,
                help_text="Whether this shipment is a return shipment",
            ),
        ),
    ]
