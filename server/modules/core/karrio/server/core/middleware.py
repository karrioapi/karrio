import threading
from django.db.models import Q
from karrio.core.utils import Tracer


class CreatorAccess:
    def __call__(self, context, key: str = "created_by", **kwargs) -> Q:
        user_key = f"{key}_id"
        user = getattr(context, "user", None)

        return Q(**{user_key: getattr(user, "id", None)})


class WideAccess:
    def __call__(self, *args, **kwargs) -> Q:
        return Q()


class UserToken:
    def __call__(self, context, **kwargs) -> dict:
        return dict(user=getattr(context, "user", context))


class SessionContext:
    _threadmap: dict = {}

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.tracer = Tracer()
        self._threadmap[threading.get_ident()] = request

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        try:
            self._save_tracing_records(request)
            del self._threadmap[threading.get_ident()]
        except KeyError:
            pass

        return response

    def _save_tracing_records(self, request):
        from karrio.server.tracing.utils import save_tracing_records

        save_tracing_records(request)

    @classmethod
    def get_current_request(cls):
        return cls._threadmap[threading.get_ident()]
