from functools import partial
from django.db import models
from oauth2_provider.models import Application

import karrio.server.core.utils as utils
import karrio.server.core.models as core


@core.register_model
class App(core.OwnedEntity):
    class Meta:
        db_table = "app"
        verbose_name = "App"
        verbose_name_plural = "Apps"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=partial(core.uuid, prefix="app_"),
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
        default=partial(utils.identity, value=[]),
    )
    metadata = models.JSONField(
        blank=True, null=True, default=partial(utils.identity, value={})
    )

    registration = models.OneToOneField(
        Application, on_delete=models.CASCADE, related_name="app"
    )

    def delete(self, *args, **kwargs):
        self.registration.delete()
        return super().delete(*args, **kwargs)

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


@core.register_model
class AppInstallation(core.OwnedEntity):
    class Meta:
        db_table = "app-installation"
        verbose_name = "App Installation"
        verbose_name_plural = "App Installations"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=partial(core.uuid, prefix="ins_"),
    )

    access_scopes = models.JSONField(
        blank=True,
        null=True,
        default=partial(utils.identity, value=[]),
    )
    metadata = models.JSONField(
        blank=True, null=True, default=partial(utils.identity, value={})
    )

    app = models.ForeignKey(
        App,
        null=False,
        on_delete=models.CASCADE,
        related_name="installations",
    )

    @property
    def object_type(self):
        return "app_installation"

    @property
    def launch_url(self):
        return self.app.launch_url
