from rest_framework import permissions, exceptions

from karrio.server.conf import settings


class APIAccessPermissions(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        print(request.path)

        if ("/v1/data" in request.path) and (settings.DATA_IMPORT_EXPORT is False):
            raise exceptions.PermissionDenied()

        if ("/v1/orders" in request.path) and (settings.ORDERS_MANAGEMENT is False):
            raise exceptions.PermissionDenied()

        return super().has_permission(request, view)
