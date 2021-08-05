from django.db import models
from django.contrib import admin
from django import forms

import purpleserver.providers.models as carriers


def model_admin(model):
    class _Admin(admin.ModelAdmin):
        exclude = ['active_users']
        formfield_overrides = {
            models.CharField: {
                'widget': forms.TextInput(attrs={'autocomplete': 'off', 'class':'vTextField', 'type': 'text'})
            }
        }

        def get_queryset(self, request):
            query = super().get_queryset(request)
            return query.filter(created_by=None)

    return type(f'{model.__class__.__name__}Admin', (_Admin, ), {})


for name, model in carriers.MODELS.items():
    admin.site.register(model, model_admin(model))
