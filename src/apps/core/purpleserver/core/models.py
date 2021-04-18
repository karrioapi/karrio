import pydoc
from uuid import uuid4
from django.db import models
from django.conf import settings

ACCESS_METHOD = getattr(settings, 'PURPLSHIP_ENTITY_ACCESS_METHOD', 'purpleserver.core.middleware.WideAccess')
get_access_filter = pydoc.locate(ACCESS_METHOD)()


def uuid(prefix: str = None):
    return f'{prefix or ""}{uuid4().hex}'


class Entity(models.Model):
    class Meta:
        abstract = True

    id = models.CharField(max_length=50, primary_key=True, default=uuid, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class OwnedEntityManager(models.Manager):
    def access_with(self, user):
        return super().filter(get_access_filter(user))


class OwnedEntity(Entity):
    class Meta:
        abstract = True

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = OwnedEntityManager()
