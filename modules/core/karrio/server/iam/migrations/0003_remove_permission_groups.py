# Generated migration to remove permission groups

from django.db import migrations


def remove_permission_groups(apps, schema_editor):
    """
    Remove all permission groups that were created by setup_groups().

    This migration removes the following groups:
    - manage_apps
    - manage_carriers (deprecated)
    - read_carriers
    - write_carriers
    - manage_orders
    - manage_team
    - manage_org_owner
    - manage_webhooks
    - manage_data
    - manage_shipments
    - manage_system
    """
    Group = apps.get_model("user", "Group")
    ContextPermission = apps.get_model("iam", "ContextPermission")

    # List of groups to remove
    groups_to_remove = [
        "manage_apps",
        "manage_carriers",
        "read_carriers",
        "write_carriers",
        "manage_orders",
        "manage_team",
        "manage_org_owner",
        "manage_webhooks",
        "manage_data",
        "manage_shipments",
        "manage_system",
        "manage_pickups",
        "manage_trackers",
    ]

    # First, remove the groups from all ContextPermissions
    for group_name in groups_to_remove:
        group = Group.objects.filter(name=group_name).first()
        if group:
            # Remove this group from all context permissions
            for ctx_perm in ContextPermission.objects.filter(groups=group):
                ctx_perm.groups.remove(group)

    # Then delete the groups themselves
    Group.objects.filter(name__in=groups_to_remove).delete()


def reverse_migration(apps, schema_editor):
    """
    Reverse migration - recreate groups (without permissions, which were set dynamically).
    Note: This won't restore the full permission setup, only creates empty groups.
    """
    Group = apps.get_model("user", "Group")

    groups_to_create = [
        "manage_apps",
        "manage_carriers",
        "read_carriers",
        "write_carriers",
        "manage_orders",
        "manage_team",
        "manage_org_owner",
        "manage_webhooks",
        "manage_data",
        "manage_shipments",
        "manage_system",
        "manage_pickups",
        "manage_trackers",
    ]

    for group_name in groups_to_create:
        Group.objects.get_or_create(name=group_name)


class Migration(migrations.Migration):

    dependencies = [
        ("iam", "0002_setup_carrier_permission_groups"),
        ("user", "0004_group"),
    ]

    operations = [
        migrations.RunPython(remove_permission_groups, reverse_migration),
    ]
