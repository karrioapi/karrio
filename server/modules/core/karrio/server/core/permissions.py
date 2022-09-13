import logging
import pydoc
import typing
from rest_framework import permissions, exceptions

import karrio.server.conf as conf

logger = logging.getLogger(__name__)
PERMISSION_CHECKS = getattr(
    conf.settings, "PERMISSION_CHECKS", ["karrio.server.core.permissions.check_feature_flags"]
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


def check_permissions(context, keys: typing.List[str]):
    for check in PERMISSION_CHECKS:
        pydoc.locate(check)(context=context, keys=keys) # type: ignore


def check_feature_flags(keys: typing.List[str] = [], **kwargs):
    flags = [flag for flag in keys if flag in conf.FEATURE_FLAGS]

    if any([conf.settings.get(flag) is False for flag in flags]):
        raise exceptions.PermissionDenied()
