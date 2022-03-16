from functools import partial
from django.db import models
from oauth2_provider.models import Application

from karrio.server.core.utils import identity
from karrio.server.core.models import OwnedEntity, uuid
from karrio.server.orgs.models import Organization


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

    is_public = models.BooleanField(default=False)
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

    registration = models.OneToOneField(
        Application, on_delete=models.CASCADE, related_name="app"
    )
    org = models.ManyToManyField(Organization, related_name="apps", through="AppLink")

    @property
    def object_type(self):
        return "app"

    @property
    def client_id(self):
        return self.registration.client_id

    @property
    def client_secret(self):
        return self.registration.client_secret

    @property
    def redirect_uris(self):
        return self.registration.redirect_uris


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
