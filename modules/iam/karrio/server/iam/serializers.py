import typing
import karrio.lib as lib


class PermissionGroup(lib.StrEnum):
    manage_apps = "manage_apps"
    manage_team = "manage_team"
    manage_system = "manage_system"
    manage_orders = "manage_orders"
    manage_data = "manage_data"
    manage_pickups = "manage_pickups"
    manage_carriers = "manage_carriers"
    manage_trackers = "manage_trackers"
    manage_webhooks = "manage_webhooks"
    manage_shipments = "manage_shipments"
    manage_org_owner = "manage_org_owner"


PERMISSION_GROUPS = [(p.name, p.name) for p in list(PermissionGroup)]
ROLES_GROUPS: typing.Dict[str, typing.List[str]] = {
    "owner": [
        PermissionGroup.manage_org_owner.value,
    ],
    "admin": [
        PermissionGroup.manage_team.value,
        PermissionGroup.manage_apps.value,
        PermissionGroup.manage_carriers.value,
    ],
    "developer": [
        PermissionGroup.manage_webhooks.value,
    ],
    "member": [
        PermissionGroup.manage_data.value,
        PermissionGroup.manage_orders.value,
        PermissionGroup.manage_pickups.value,
        PermissionGroup.manage_trackers.value,
        PermissionGroup.manage_shipments.value,
    ],
}
