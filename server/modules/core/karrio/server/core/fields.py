from django import forms
from django.db import models


class MultiChoiceField(models.JSONField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "widget": forms.SelectMultiple,
            "choices": self.choices,
        }
        defaults.update(kwargs)
        return super(models.JSONField, self).formfield(**defaults)
