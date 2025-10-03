from django.db import models
from django.contrib.auth.models import PermissionsMixin, Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _

import karrio.server.user.models as user

User = user.User
Group = user.Group


class ContextPermission(PermissionsMixin):
    class Meta:
        verbose_name = _("context permission")
        verbose_name_plural = _("context permission")

    def __str__(self) -> str:
        return f"{self.object_pk} - {self.content_type}"

    content_type = models.ForeignKey(
        to="contenttypes.ContentType",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("content type"),
    )
    object_pk = models.CharField(
        db_index=True, max_length=50, verbose_name=_("object pk")
    )
    content_object = GenericForeignKey("content_type", "object_pk")
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user context belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="context",
        related_query_name="context",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user context permissions"),
        blank=True,
        help_text=_("Specific permissions for this user context."),
        related_name="context",
        related_query_name="context",
    )
