from django.contrib import admin

import purpleserver.carriers.models as models

for name, model in models.MODELS.items():
    admin.site.register(model)
