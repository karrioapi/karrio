import inspect
from django.contrib import admin
import purpleserver.manager.models as models

for name, model in inspect.getmembers(models):
    if inspect.isclass(model) and issubclass(model, models.Entity) and name not in ['Entity', 'OwnedEntity', 'Carrier']:
        admin.site.register(model)
