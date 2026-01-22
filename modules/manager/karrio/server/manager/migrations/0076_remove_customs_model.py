from django.db import migrations


def cleanup_orgs_customs_links(apps, schema_editor):
    """
    Clean up any orgs link tables that reference Customs before deleting the model.
    This handles the case where the database was created in insiders mode but migrations
    are running in OSS mode.

    In insiders mode, orgs.0024_remove_organization_customs runs first (via run_before)
    and handles this cleanup properly. This is a fallback for OSS mode with insiders DB.
    """
    # Try to get orgs link models and clean them up using Django ORM
    try:
        CustomsLink = apps.get_model("orgs", "CustomsLink")
        CustomsLink.objects.all().delete()
    except LookupError:
        # Model not registered - check if table exists using Django introspection
        connection = schema_editor.connection
        table_names = connection.introspection.table_names()
        if "orgs_customslink" in table_names:
            # Table exists but model isn't registered - use Django's cursor
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM orgs_customslink")

    # Also try to clear any M2M relationship
    try:
        Organization = apps.get_model("orgs", "Organization")
        for org in Organization.objects.all():
            if hasattr(org, "customs"):
                org.customs.clear()
    except LookupError:
        pass  # Model doesn't exist in OSS mode


def noop(apps, schema_editor):
    """Reverse migration is a no-op since we can't restore deleted links."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0075_populate_template_meta"),
        ("graph", "0003_remove_template_customs"),  # Remove template.customs FK first
        # Note: orgs.0024_remove_organization_customs (insiders) uses run_before to ensure proper ordering
    ]

    operations = [
        # Clean up any orgs link tables first (handles insiders DB in OSS mode)
        migrations.RunPython(cleanup_orgs_customs_links, noop),
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
