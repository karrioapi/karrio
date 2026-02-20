from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0085_fix_stale_tracker_carrier_snapshots"),
    ]

    operations = [
        migrations.AddField(
            model_name="shipment",
            name="is_return",
            field=models.BooleanField(
                default=False,
                db_index=True,
                help_text="Whether this shipment is a return shipment",
            ),
        ),
    ]
