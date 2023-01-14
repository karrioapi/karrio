import typing
import operator
import functools
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.contenttypes import models as contenttypes
from rest_framework import permissions, exceptions
from rest_framework import exceptions

import karrio.server.iam.serializers as iam_serializers
import karrio.server.core.utils as utils
import karrio.server.user.models as users
import karrio.server.orgs.models as orgs
import karrio.server.iam.models as iam

User = get_user_model()


class IsOrgOwner(permissions.BasePermission):
    """Allows access only to owner or billing users."""

    def has_permission(self, request, view):
        user_id = request.user.id
        owner_id = utils.failsafe(lambda: request.org.owner.organization_user.user.id)

        if user_id != owner_id:
            exceptions.PermissionDenied()

        return super().has_permission(request, view)


@utils.skip_on_loadata
@utils.async_wrapper
@utils.tenant_aware
def apply_for_org_users(**_):
    """This function will create context permissions for all organization users based on their roles."""
    org_user_permissions = iam.ContextPermission.objects.filter(
        content_type__model="OrganizationUser".lower()
    ).values_list("object_pk", flat=True)
    org_users_without_permissions = orgs.OrganizationUser.objects.all().exclude(
        pk__in=list(org_user_permissions)
    )

    for user in org_users_without_permissions:
        sync_permissions(user)


def sync_permissions(org_user):
    org_owner_id = utils.failsafe(
        lambda: org_user.organization.owner.organization_user.id
    )
    group_names = set(
        sum(
            [iam_serializers.ROLES_GROUPS.get(role) or [] for role in org_user.roles],
            start=[],
        )
    )

    if org_owner_id == org_user.id:
        group_names.add("manage_org_owner")

    groups = users.Group.objects.filter(name__in=group_names)

    permission, _ = iam.ContextPermission.objects.get_or_create(
        content_type=contenttypes.ContentType.objects.get_for_model(org_user),
        object_pk=org_user.pk,
    )
    permission.groups.set(groups)
    permission.save()


def check_context_permissions(context=None, keys: typing.List[str] = [], **kwargs):
    groups = [group for group, _ in iam_serializers.PERMISSION_GROUPS if group in keys]

    if any(groups) and users.Group.objects.exists():
        org_user = context.org.organization_users.filter(
            user__id=context.user.id
        ).first()
        token = getattr(context, "token", None)
        group_filters = functools.reduce(
            operator.and_, (Q(groups__name=x) for x in groups)
        )
        token_permission = iam.ContextPermission.objects.filter(
            Q(object_pk=getattr(token, "pk", None))
        )

        if token_permission.exists():
            permission_groups = token_permission.filter(group_filters)
        else:
            permission_groups = iam.ContextPermission.objects.filter(
                Q(object_pk=org_user.pk) & group_filters
            )

        if not permission_groups.exists():
            raise exceptions.PermissionDenied()
