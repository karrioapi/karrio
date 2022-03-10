from django.contrib import admin
from purplship.server.apps import models


admin.site.register(models.App)
admin.site.register(models.AppInstallation)
