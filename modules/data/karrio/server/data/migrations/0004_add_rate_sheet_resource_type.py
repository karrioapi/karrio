from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0003_datatemplate_metadata_alter_batchoperation_resources"),
    ]

    operations = [
        migrations.AlterField(
            model_name="batchoperation",
            name="resource_type",
            field=models.CharField(
                choices=[
                    ("orders", "orders"),
                    ("shipments", "shipments"),
                    ("trackers", "trackers"),
                    ("billing", "billing"),
                    ("rate_sheet", "rate_sheet"),
                ],
                default="orders",
                max_length=25,
            ),
        ),
        migrations.AlterField(
            model_name="datatemplate",
            name="resource_type",
            field=models.CharField(
                choices=[
                    ("orders", "orders"),
                    ("shipments", "shipments"),
                    ("trackers", "trackers"),
                    ("billing", "billing"),
                    ("rate_sheet", "rate_sheet"),
                ],
                max_length=25,
            ),
        ),
    ]
