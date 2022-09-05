import pydoc
import typing
from rest_framework import permissions, exceptions

import karrio.server.conf as conf

PERMISSION_CHECKS = getattr(
    conf.settings, "PERMISSION_CHECKS", ["karrio.server.core.permissions.feature_enabled"]
)


class AllowEnabledAPI(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        if ("/v1/data" in request.path) and (conf.settings.DATA_IMPORT_EXPORT is False):
            raise exceptions.PermissionDenied()

        if ("/v1/orders" in request.path) and (conf.settings.ORDERS_MANAGEMENT is False):
            raise exceptions.PermissionDenied()

        return super().has_permission(request, view)


def check_permissions(keys: typing.List[str]):
    for check in PERMISSION_CHECKS:
        pydoc.locate(check)(keys) # type: ignore


def feature_enabled(features: typing.List[str]):
    keys = [key for key in features if key in conf.FEATURE_FLAGS]

    if any([conf.settings.get(key) is False for key in keys]):
        raise exceptions.PermissionDenied()

    return True
