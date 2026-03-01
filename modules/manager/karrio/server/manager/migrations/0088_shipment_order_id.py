from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0087_shipment_is_return_nullable"),
    ]

    operations = [
        migrations.AddField(
            model_name="shipment",
            name="order_id",
            field=models.CharField(
                max_length=50,
                null=True,
                blank=True,
                db_index=True,
                help_text="The order identifier associated with this shipment",
            ),
        ),
    ]
