from django import forms
from django.db import models
from django.contrib.postgres.fields import ArrayField


class MultiChoiceField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class MultiChoiceJSONField(models.JSONField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "widget": forms.SelectMultiple,
            "choices": self.choices,
        }
        defaults.update(kwargs)
        return super(models.JSONField, self).formfield(**defaults)
