from rest_framework import permissions, exceptions
import karrio.server.core.utils as utils


class IsOrgOwner(permissions.BasePermission):
    """Allows access only to owner or billing users.
    """

    def has_permission(self, request, view):
        user_id = request.user.id
        owner_id = utils.failsafe(
            lambda: request.org.owner.organization_user.user.id
        )

        if (user_id != owner_id):
            exceptions.PermissionDenied()

        return super().has_permission(request, view)
