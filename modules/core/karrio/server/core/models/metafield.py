import json
import re
import functools
from datetime import datetime, date
import django.conf as conf
import django.db.models as models
import django.utils.translation as translation
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

import karrio.server.core.models.base as core
import karrio.server.core.models.entity as entity

_ = translation.gettext_lazy


@core.register_model
class Metafield(entity.OwnedEntity):
    class Meta:
        db_table = "metafield"
        verbose_name = "Metafield"
        verbose_name_plural = "Metafields"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    id = models.CharField(
        max_length=50,
        editable=False,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="metaf_"),
    )
    key = models.CharField(_("name"), max_length=50, db_index=True)
    value = models.JSONField(null=True, blank=True)
    type = models.CharField(
        _("type"),
        max_length=50,
        choices=core.METAFIELD_TYPE,
        default=core.METAFIELD_TYPE[0][0],
        db_index=True,
    )
    is_required = models.BooleanField(null=False, default=False)

    # Generic relation to any object
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The type of object this metafield is attached to",
    )
    object_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
        help_text="The ID of the object this metafield is attached to",
    )
    content_object = GenericForeignKey("content_type", "object_id")

    # Related fields
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )

    @classmethod
    def access_by(cls, context, manager: str = "objects"):
        """Custom access control for metafields.

        Metafield uses GenericForeignKey and has no direct 'org' FK,
        so the default OrganizationAccess filter (which references org__id)
        cannot be applied. Instead, we scope via created_by directly.
        """
        if isinstance(context, dict):
            user = context.get("user", context)
            org = context.get("org")
        else:
            user = getattr(context, "user", context)
            org = getattr(context, "org", None)

        user_id = getattr(user, "id", None)
        queryset = getattr(cls, manager, cls.objects)

        # Use truthiness (not identity) to handle SimpleLazyObject wrapping None
        if org:
            return queryset.filter(
                models.Q(created_by__in=org.users.all())
            )

        return queryset.filter(models.Q(created_by__id=user_id))

    @property
    def object_type(self):
        return "metafield"

    def clean(self):
        """Validate the value based on the metafield type."""
        super().clean()
        if self.value is not None:
            self._validate_value()

    def _validate_value(self):
        """Validate value based on metafield type."""
        if self.type == core.MetafieldType.text:
            if not isinstance(self.value, str):
                raise ValidationError(f"Value must be a string for type 'text'")

        elif self.type == core.MetafieldType.number:
            if not isinstance(self.value, (int, float)):
                raise ValidationError(f"Value must be a number for type 'number'")

        elif self.type == core.MetafieldType.boolean:
            if not isinstance(self.value, bool):
                raise ValidationError(f"Value must be a boolean for type 'boolean'")

        elif self.type == core.MetafieldType.json:
            # JSON can be any valid JSON value (dict, list, string, number, boolean, null)
            try:
                if isinstance(self.value, str):
                    json.loads(self.value)
            except (json.JSONDecodeError, TypeError):
                raise ValidationError(f"Value must be valid JSON for type 'json'")

        elif self.type == core.MetafieldType.date:
            if isinstance(self.value, str):
                try:
                    datetime.strptime(self.value, '%Y-%m-%d')
                except ValueError:
                    raise ValidationError(f"Value must be a valid date (YYYY-MM-DD) for type 'date'")
            else:
                raise ValidationError(f"Value must be a date string (YYYY-MM-DD) for type 'date'")

        elif self.type == core.MetafieldType.date_time:
            if isinstance(self.value, str):
                try:
                    datetime.fromisoformat(self.value.replace('Z', '+00:00'))
                except ValueError:
                    raise ValidationError(f"Value must be a valid ISO datetime for type 'date_time'")
            else:
                raise ValidationError(f"Value must be a datetime string for type 'date_time'")

        elif self.type == core.MetafieldType.password:
            if not isinstance(self.value, str):
                raise ValidationError(f"Value must be a string for type 'password'")

    def get_parsed_value(self):
        """Return the value parsed according to its type."""
        if self.value is None:
            return None

        if self.type == core.MetafieldType.text:
            return str(self.value)

        elif self.type == core.MetafieldType.number:
            return self.value

        elif self.type == core.MetafieldType.boolean:
            return bool(self.value)

        elif self.type == core.MetafieldType.json:
            if isinstance(self.value, str):
                try:
                    return json.loads(self.value)
                except json.JSONDecodeError:
                    return self.value
            return self.value

        elif self.type == core.MetafieldType.date:
            if isinstance(self.value, str):
                try:
                    return datetime.strptime(self.value, '%Y-%m-%d').date()
                except ValueError:
                    return self.value
            return self.value

        elif self.type == core.MetafieldType.date_time:
            if isinstance(self.value, str):
                try:
                    return datetime.fromisoformat(self.value.replace('Z', '+00:00'))
                except ValueError:
                    return self.value
            return self.value

        elif self.type == core.MetafieldType.password:
            return str(self.value)

        return self.value
