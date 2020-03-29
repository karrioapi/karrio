from django.contrib import admin
from purpleserver.core.models import MODELS

for model in MODELS.values():
    admin.site.register(model)
