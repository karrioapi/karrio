from django.contrib import admin
from karrio.server.apps import models


admin.site.register(models.App)
admin.site.register(models.AppInstallation)
