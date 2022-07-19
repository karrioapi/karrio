import json
import threading
from django.db.models import Q
from django.http import HttpResponse
from karrio.core.utils import Tracer
from karrio.server.conf import settings


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
            self._save_tracing_records(request, schema=settings.schema)
            del self._threadmap[threading.get_ident()]
        except KeyError:
            pass

        return response

    def _save_tracing_records(self, request, schema: str = None):
        from karrio.server.tracing.utils import save_tracing_records

        save_tracing_records(request, schema=schema)

    @classmethod
    def get_current_request(cls):
        return cls._threadmap.get(threading.get_ident())


class NonHtmlDebugToolbarMiddleware:
    """
    The Django Debug Toolbar usually only works for views that return HTML.
    This middleware wraps any non-HTML response in HTML if the request
    has a 'debug' query parameter (e.g. http://localhost/foo?debug)
    Special handling for json (pretty printing) and
    binary data (only show data length)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.GET.get("debug") == "":
            if response["Content-Type"] == "application/octet-stream":
                new_content = (
                    "<html><body>Binary Data, "
                    "Length: {}</body></html>".format(len(response.content))
                )
                response = HttpResponse(new_content)
            elif response["Content-Type"] != "text/html":
                content = response.content
                try:
                    json_ = json.loads(content)
                    content = json.dumps(json_, sort_keys=True, indent=2)
                except ValueError:
                    pass
                response = HttpResponse(
                    "<html><body><pre>{}" "</pre></body></html>".format(content)
                )

        return response
