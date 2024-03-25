import os
import binascii
import functools
from django.db import models
from django.conf import settings
from django.contrib.auth import models as auth
from rest_framework.authtoken import models as authtoken
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

import karrio.server.core.models as core


class UserManager(auth.UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


@core.register_model
class User(auth.AbstractUser):
    full_name = models.CharField(_("full name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list = []

    objects = UserManager()

    username = None
    first_name = None
    last_name = None

    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs):
        self.tokens.all().delete()
        super().delete(*args, **kwargs)

    @property
    def object_type(self):
        return "user"

    @property
    def permissions(self):
        import karrio.server.conf as conf
        import karrio.server.iam.models as iam
        import karrio.server.core.middleware as middleware

        ctx = middleware.SessionContext.get_current_request()
        _permissions = []

        if conf.settings.MULTI_ORGANIZATIONS and ctx.org is not None:
            org_user = ctx.org.organization_users.filter(user_id=self.pk)
            _permissions = (
                iam.ContextPermission.objects.get(
                    object_pk=org_user.first().pk,
                    content_type=ContentType.objects.get_for_model(org_user.first()),
                )
                .groups.all()
                .values_list("name", flat=True)
                if org_user.exists()
                else []
            )

        if not any(_permissions):
            _permissions = self.groups.all().values_list("name", flat=True)

        if not any(_permissions) and self.is_superuser:
            return Group.objects.all().values_list("name", flat=True)

        if not any(_permissions) and self.is_staff:
            return Group.objects.exclude(
                name__in=["manage_system", "manage_team", "manage_org_owner"]
            ).values_list("name", flat=True)

        return _permissions


@core.register_model
class Token(authtoken.Token, core.ControlledAccessModel):
    label = models.CharField(_("label"), max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tokens"
    )
    test_mode = models.BooleanField(null=False, default=core.field_default(False))

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    @property
    def pk(self):
        return self.key

    @classmethod
    def generate_key(cls):
        return f"key_{binascii.hexlify(os.urandom(16)).decode()}"

    @property
    def organization(self):
        return self.org.first() if hasattr(self, "org") else None

    @property
    def object_type(self):
        return "token"

    @property
    def permissions(self):
        import karrio.server.conf as conf
        import karrio.server.iam.models as iam

        _permissions = []

        if iam.ContextPermission.objects.filter(object_pk=self.pk).exists():
            _permissions = (
                iam.ContextPermission.objects.get(
                    object_pk=self.pk,
                    content_type=ContentType.objects.get_for_model(Token),
                )
                .groups.all()
                .values_list("name", flat=True)
            )

        if (
            not any(_permissions)
            and conf.settings.MULTI_ORGANIZATIONS
            and self.org.exists()
        ):
            org_user = self.org.first().organization_users.filter(user_id=self.user_id)
            _permissions = (
                iam.ContextPermission.objects.get(
                    object_pk=org_user.first().pk,
                    content_type=ContentType.objects.get_for_model(org_user.first()),
                )
                .groups.all()
                .values_list("name", flat=True)
                if org_user.exists()
                else []
            )

        return _permissions if any(_permissions) else self.user.permissions


@core.register_model
class Group(auth.Group):
    pass


@core.register_model
class WorkspaceConfig(core.OwnedEntity):
    class Meta:
        db_table = "workspace-config"
        verbose_name = "Workspace Config"
        verbose_name_plural = "Workspace Configs"

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="wcfg_"),
    )
    config = models.JSONField(
        null=False,
        blank=False,
        default=core.field_default({}),
    )
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )

    @property
    def object_type(self):
        return "workspace-config"
