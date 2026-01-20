# Data migration: Transfer labels from Template model to meta.label
# This ensures backward compatibility by preserving existing template labels

from django.db import migrations


def transfer_template_labels(apps, schema_editor):
    """
    Transfer label and is_default from Template model to Address/Parcel meta field.

    The Template model (in graph module) stores:
    - label: The template name
    - is_default: Whether it's the default template
    - address: OneToOne FK to Address
    - parcel: OneToOne FK to Parcel

    We copy these to the meta.label and meta.is_default fields on the related models.
    Note: Customs templates are not migrated as the Customs model is being removed.
    """
    # Get models - Template is in graph module
    Template = apps.get_model("graph", "Template")
    Address = apps.get_model("manager", "Address")
    Parcel = apps.get_model("manager", "Parcel")

    # Process all templates
    for template in Template.objects.all():
        # Transfer to Address
        if template.address_id:
            try:
                address = Address.objects.get(pk=template.address_id)
                meta = address.meta or {}
                meta["label"] = template.label
                meta["is_default"] = template.is_default
                address.meta = meta
                address.save(update_fields=["meta"])
            except Address.DoesNotExist:
                pass

        # Transfer to Parcel
        if template.parcel_id:
            try:
                parcel = Parcel.objects.get(pk=template.parcel_id)
                meta = parcel.meta or {}
                meta["label"] = template.label
                meta["is_default"] = template.is_default
                parcel.meta = meta
                parcel.save(update_fields=["meta"])
            except Parcel.DoesNotExist:
                pass


def reverse_noop(apps, schema_editor):
    """Reverse migration is a no-op - we don't want to remove labels."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0074_clean_model_refactoring"),
        ("graph", "0002_auto_20210512_1353"),  # Ensure Template model exists
    ]

    operations = [
        migrations.RunPython(
            transfer_template_labels,
            reverse_noop,
        ),
    ]
