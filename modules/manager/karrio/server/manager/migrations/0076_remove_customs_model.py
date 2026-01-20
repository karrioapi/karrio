from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0075_populate_template_meta"),
        ("graph", "0003_remove_template_customs"),  # Remove template.customs FK first
        ("orgs", "0024_remove_organization_customs"),  # Remove orgs customs M2M first
    ]

    operations = [
        # Remove M2M relationship first (customs_commodities junction table)
        migrations.RemoveField(
            model_name="customs",
            name="commodities",
        ),
        # Remove FK to Address
        migrations.RemoveField(
            model_name="customs",
            name="duty_billing_address",
        ),
        # Then delete the model (drops the customs table)
        migrations.DeleteModel(
            name="Customs",
        ),
    ]
