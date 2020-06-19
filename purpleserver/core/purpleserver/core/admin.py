from django.contrib import admin
import purpleserver.core.models as models

for name, model in models.MODELS.items():
    admin.site.register(model)
