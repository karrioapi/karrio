import inspect
from django.contrib import admin
from purpleserver.core.models import Entity
import purpleserver.manager.models as models

for name, model in inspect.getmembers(models):
    if inspect.isclass(model) and issubclass(model, Entity) and name not in ['Entity', 'OwnedEntity', 'Carrier']:
        admin.site.register(model)
