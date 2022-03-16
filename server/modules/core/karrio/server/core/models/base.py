import pydoc
from uuid import uuid4
from django.conf import settings


ACCESS_METHOD = getattr(
    settings,
    "KARRIO_ENTITY_ACCESS_METHOD",
    "karrio.server.core.middleware.WideAccess",
)
get_access_filter = pydoc.locate(ACCESS_METHOD)()


def uuid(prefix: str = None):
    return f'{prefix or ""}{uuid4().hex}'


class ControlledAccessModel:
    @classmethod
    def access_by(cls, context):
        if hasattr(cls, "created_by"):
            key = "created_by"
        else:
            key = "user"

        return cls.objects.filter(get_access_filter(context, key))
