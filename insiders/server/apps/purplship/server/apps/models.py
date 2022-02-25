from functools import partial
from django.db import models
from django.contrib.postgres.fields import ArrayField

from purplship.server.core.utils import identity
from purplship.server.core.models import OwnedEntity, uuid
from purplship.server.orgs.models import Organization


class App(OwnedEntity):
    class Meta:
        db_table = "app"
        verbose_name = "App"
        verbose_name_plural = "Apps"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=partial(uuid, prefix="app_"),
    )

    display_name = models.CharField(max_length=50)
    developer_name = models.CharField(max_length=50)

    is_builtin = models.BooleanField(default=False)
    is_embedded = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    launch_url = models.CharField(max_length=100)

    features = models.JSONField(
        blank=True,
        null=True,
        default=partial(identity, value=[]),
    )
    metadata = models.JSONField(
        blank=True, null=True, default=partial(identity, value={})
    )

    org = models.ManyToManyField(Organization, related_name="apps", through="AppLink")

    @property
    def object_type(self):
        return "app"


class AppInstallation(OwnedEntity):
    class Meta:
        db_table = "app-installation"
        verbose_name = "App Installation"
        verbose_name_plural = "App Installations"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=partial(uuid, prefix="ins_"),
    )

    access_scopes = models.JSONField(
        blank=True,
        null=True,
        default=partial(identity, value=[]),
    )
    metadata = models.JSONField(
        blank=True, null=True, default=partial(identity, value={})
    )

    app = models.ForeignKey(
        App,
        null=False,
        on_delete=models.CASCADE,
        related_name="installations",
    )
    org = models.ManyToManyField(
        Organization, related_name="installations", through="AppInstallationLink"
    )

    @property
    def object_type(self):
        return "app_installation"

    @property
    def launch_url(self):
        return self.app.launch_url


class AppLink(models.Model):
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="app_links"
    )
    item = models.OneToOneField(App, on_delete=models.CASCADE, related_name="link")


class AppInstallationLink(models.Model):
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="app_installation_links"
    )
    item = models.OneToOneField(
        AppInstallation, on_delete=models.CASCADE, related_name="link"
    )
