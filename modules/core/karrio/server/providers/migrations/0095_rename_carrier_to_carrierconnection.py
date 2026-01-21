# Rename Carrier model to CarrierConnection and update table names to CamelCase

from django.db import migrations


class Migration(migrations.Migration):
    """
    Rename Carrier model to CarrierConnection and update all table names to CamelCase.

    Changes:
    - Rename Carrier model to CarrierConnection
    - Rename 'carrier' table to 'CarrierConnection'
    - Rename 'system_connection' table to 'SystemConnection'
    - Rename 'brokered_connection' table to 'BrokeredConnection'
    """

    dependencies = [
        ("providers", "0094_remove_carrier_legacy_fields"),
    ]

    operations = [
        # Rename the model
        migrations.RenameModel(
            old_name="Carrier",
            new_name="CarrierConnection",
        ),
        # Rename tables to CamelCase
        migrations.AlterModelTable(
            name="carrierconnection",
            table="CarrierConnection",
        ),
        migrations.AlterModelTable(
            name="systemconnection",
            table="SystemConnection",
        ),
        migrations.AlterModelTable(
            name="brokeredconnection",
            table="BrokeredConnection",
        ),
    ]
