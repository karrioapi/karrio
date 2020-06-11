import inspect
from django.contrib import admin
import purpleserver.core.models as models

for name, model in inspect.getmembers(models):
    if inspect.isclass(model) and issubclass(model, models.Carrier) and name not in ['Carrier']:
        admin.site.register(model)
