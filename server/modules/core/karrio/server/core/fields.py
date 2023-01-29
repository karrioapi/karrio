from django import forms
from django.db import models


class MultiChoiceField(models.JSONField):
    def formfield(self, **kwargs):
        defaults = {"choices_form_class": forms.TypedMultipleChoiceField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def validate(self, value, model_instance):
        pass
