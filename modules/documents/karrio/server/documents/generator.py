import io
import copy
import json
import typing
import base64
import decimal
import datetime
import jinja2
import jinja2.sandbox
import markupsafe
import urllib.parse
import weasyprint
from django.db.models import Sum
import weasyprint.text.fonts as fonts

import karrio.lib as lib
from karrio.server.conf import settings
from karrio.server.core.logging import logger
import karrio.server.documents.utils as utils
import karrio.server.core.dataunits as dataunits
import karrio.server.orders.models as order_models
import karrio.server.manager.models as manager_models
import karrio.server.documents.models as document_models
import karrio.server.orders.serializers as orders_serializers
import karrio.server.manager.serializers as manager_serializers
from karrio.server.serializers.abstract import RequestContext, get_object_context

FONT_CONFIG = fonts.FontConfiguration()
PAGE_SEPARATOR = '<p style="page-break-before: always"></p>'
REMOTE_STYLESHEET_URL = "https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css"
ASSET_FETCH_TIMEOUT = 10  # seconds
ASSET_MAX_BYTES = 5 * 1024 * 1024
_asset_fetcher_class = None


def _https_origin(url) -> str | None:
    """``https://host[:port]`` of an https URL (host lower-cased, default port
    and a trailing dot dropped), or None for anything else."""
    try:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme.lower() != "https" or "@" in parts.netloc or not parts.hostname:
            return None
        port = parts.port
    except ValueError:
        return None
    host = parts.hostname.rstrip(".")
    return f"https://{host}" + ("" if port in (None, 443) else f":{port}")


def allowed_asset_origins() -> set:
    """Origins the operator allows documents to load assets from
    (DOCUMENT_ASSET_ALLOWED_ORIGINS). The built-in stylesheet is allowed by its exact
    URL only: its CDN serves any package, so its origin is not an allowlist entry."""
    extra = getattr(settings, "DOCUMENT_ASSET_ALLOWED_ORIGINS", None) or []
    return {origin for origin in map(_https_origin, extra) if origin}


def asset_fetcher():
    """A fresh fetcher for what a rendered document references: stylesheets,
    images, attachments (one per render: a fetcher keeps per-request state).

    The HTML is built from user-authored templates and user data, so whatever it
    references was chosen by a user. WeasyPrint's default fetcher reads file:// paths
    into the PDF (``<link rel="attachment" href="file:///...">``) and requests any
    http(s) URL from the server. This one fetches only data: URIs, the built-in
    stylesheet's exact URL and https URLs on an operator-allowed origin, does not
    follow redirects, and has a timeout and a size cap.
    Anything else raises: refused assets are skipped, except a refused @color-profile
    source, which fails the render. weasyprint is imported here, not at module import,
    like everywhere else in this module.
    """
    global _asset_fetcher_class

    if _asset_fetcher_class is None:
        import weasyprint.urls

        class DocumentAssetFetcher(weasyprint.urls.URLFetcher):
            def __init__(self):
                super().__init__(
                    timeout=ASSET_FETCH_TIMEOUT,
                    allowed_protocols=("data", "https"),
                    allow_redirects=False,
                )

            def fetch(self, url, headers=None):
                scheme = url.split(":", 1)[0].strip().lower()
                if scheme == "data":
                    return super().fetch(url, headers)

                if url != REMOTE_STYLESHEET_URL and _https_origin(url) not in allowed_asset_origins():
                    host = lib.failsafe(lambda: urllib.parse.urlsplit(url).hostname)
                    logger.warning("Document asset refused", scheme=scheme, host=host)
                    raise ValueError("Document asset refused")

                response = super().fetch(url, headers)
                try:
                    body = response.read(ASSET_MAX_BYTES + 1)
                finally:
                    response.close()
                if len(body) > ASSET_MAX_BYTES:
                    raise ValueError("Document asset too large")

                return weasyprint.urls.URLFetcherResponse(response.url, body, response.headers, response.status)

        _asset_fetcher_class = DocumentAssetFetcher

    return _asset_fetcher_class()

STYLESHEETS = [
    weasyprint.CSS(url=REMOTE_STYLESHEET_URL, url_fetcher=asset_fetcher()),
    weasyprint.CSS(
        string="""
        @page { margin: 1cm }
        @font-face {
            font-family: 'system';
            src: local('Arial');
        }
        body { font-family: 'system', sans-serif; }
    """,
        url_fetcher=asset_fetcher(),
    ),
]
UNITS = {
    "PAGE_SEPARATOR": markupsafe.Markup(PAGE_SEPARATOR),  # noqa: S704 - a constant of ours
    "CountryISO": lib.units.CountryISO.as_dict(),
    **dataunits.REFERENCE_MODELS,
}
# Templates may build and change their own lists and dicts; the module-level data
# every render shares (UNITS, the samples) is protected by giving each document
# its own copy instead (_shared_render_data). Autoescape: data printed into the
# HTML is text, never markup (an address line cannot add tags to the document).
SANDBOXED_ENV = jinja2.sandbox.SandboxedEnvironment(autoescape=True)

# Values a template may hold as they are: immutable, and their methods take no
# callables, so none of them leads back into the application.
PLAIN_SCALARS = (
    str,
    int,
    float,
    bool,
    type(None),
    decimal.Decimal,
    datetime.datetime,
    datetime.date,
    datetime.time,
)


def to_plain(value):
    """Deep-convert render data to dicts, lists and plain scalars (PLAIN_SCALARS).

    Everything a template sees goes through here, so a template can reach data and
    nothing else. Serializer output in particular is a ``ReturnDict`` that carries
    ``.serializer.instance``: the live model row, and from it the whole ORM. Keys stay
    str or int; tuples and sets become lists; str subclasses (marked-safe strings,
    enums) become plain text; anything else becomes its text.
    """
    if type(value) in PLAIN_SCALARS:
        return value
    if isinstance(value, str):
        return str.__str__(value)
    if isinstance(value, int) and not isinstance(value, bool):
        return int(value)  # int subclasses (IntEnum) -> int
    if isinstance(value, float):
        return float(value)
    if isinstance(value, dict):
        return {(key if type(key) in (str, int) else str(key)): to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [to_plain(item) for item in value]
    return str(value)


def _template_failsafe(callable=None, warning: str | None = None):
    """``lib.failsafe`` for templates: it never calls an arbitrary callable.

    The real ``lib.failsafe`` calls its argument outside the sandbox, so the sandbox's
    ``alters_data`` and attribute rules never applied to whatever it was handed. Stored
    templates may still use the name, so it stays: a Jinja macro (rendered inside the
    sandbox) is invoked with errors swallowed, plain data is returned as it is, and
    anything else is refused as ``None``. The parameter keeps lib.failsafe's name, so
    ``lib.failsafe(callable=...)`` in a stored template still works.
    """
    value = callable
    if isinstance(value, jinja2.runtime.Macro):
        try:
            return value()
        except Exception:  # noqa: BLE001 - failsafe semantics: a failing macro yields None
            return None
    if type(value) in PLAIN_SCALARS or isinstance(value, (dict, list)):
        return to_plain(value)
    return None


def _template_to_dict(value, clear_empty: bool | None = None):
    # ``lib.to_dict`` serialises an arbitrary object's ``__dict__``; templates only
    # ever hand it data.
    return lib.to_dict(value if isinstance(value, (str, bytes)) else _template_to_json(value), clear_empty=clear_empty)


def _template_to_json(value) -> str:
    # Same output format as ``lib.to_json`` for data, without its ``__dict__`` walk.
    return json.dumps(to_plain(value), sort_keys=True, indent=4, default=str)


class _TemplateNamespace:
    """A fixed set of helpers a user-authored document template may reach by name.

    Jinja2's sandbox governs what a template can reach by walking an object
    graph: it blocks ``{{ "".__class__.__mro__ }}``. It has nothing to say about
    a callable handed to it directly: whatever is put in the render globals is
    callable, and anything reachable as an attribute of it is too.

    Passing ``karrio.lib`` in whole therefore handed every template author
    ``lib.request`` (any URL), ``lib.load_file_content`` (any path the server
    can read) and the modules ``lib`` re-exports. Templates are authored by
    users and rendered server-side, so that is a file read and an SSRF whose
    result ends up in a document the author downloads.

    Names are listed rather than filtered, so a helper becomes reachable only
    when somebody decides it should be, and an unlisted one fails loudly.
    """

    def __init__(self, label: str, **members):
        self._label = label
        self._members = members

    def __getattr__(self, name: str):
        try:
            return self.__dict__["_members"][name]
        except KeyError:
            # SecurityError rather than AttributeError: the sandbox turns an
            # AttributeError into an undefined value, and the author would not
            # learn that the name was withheld or what is available instead.
            raise jinja2.exceptions.SecurityError(
                f"'{self.__dict__['_label']}.{name}' is not available in document templates. "
                f"Available: {', '.join(sorted(self.__dict__['_members']))}"
            ) from None

    def __contains__(self, name: str) -> bool:
        return name in self._members

    def __repr__(self) -> str:
        return f"<{self._label} template helpers>"


# Formatting and lookup only. Every entry is a function or plain data, never a
# module: ``lib.units`` looks like a table of enums but re-exports ``pathlib``
# and ``karrio.core.utils``, which would hand back the file read and the HTTP
# client through a longer path. Templates get reference data from ``units``.
TEMPLATE_LIB = _TemplateNamespace(
    "lib",
    failsafe=_template_failsafe,
    identity=lib.identity,
    join=lib.join,
    text=lib.text,
    to_dict=_template_to_dict,
    to_json=_template_to_json,
    to_int=lib.to_int,
    to_list=lib.to_list,
    to_decimal=lib.to_decimal,
    to_money=lib.to_money,
    to_slug=lib.to_slug,
    to_date=lib.to_date,
    fdate=lib.fdate,
    ftime=lib.ftime,
    fdatetime=lib.fdatetime,
    flocaltime=lib.flocaltime,
    format_decimal=lib.format_decimal,
    to_country_name=lib.to_country_name,
    to_state_name=lib.to_state_name,
)

# ``documents.utils`` re-exports ``lib`` (and ``io``/``base64``), so narrowing
# only the ``lib`` global would leave ``utils.lib.load_file_content`` open.
TEMPLATE_UTILS = _TemplateNamespace(
    "utils",
    create_barcode=utils.create_barcode,
    generate_code=utils.generate_code,
    date_format=utils.date_format,
    datetime=utils.datetime,
    ORDER_SAMPLE=utils.ORDER_SAMPLE,
    SHIPMENT_SAMPLE=utils.SHIPMENT_SAMPLE,
)


def _shared_render_data() -> dict:
    """This document's own copy of the module-level data every render reads, so a
    template that changes it cannot change what the next document sees."""
    return dict(
        units=copy.deepcopy(UNITS),
        utils=_TemplateNamespace("utils", **copy.deepcopy(TEMPLATE_UTILS._members)),
    )


def _render_data(ctx: dict, metadata: dict, shared: dict) -> dict:
    """Everything a tenant-authored template sees: the context and metadata as plain
    data, the document's shared data, and the fixed helper namespace."""
    return {
        **to_plain(ctx),
        "metadata": to_plain(metadata),
        **shared,
        "lib": TEMPLATE_LIB,
    }


def _render(jinja_template, data: dict) -> str:
    """The one place a tenant-authored template is rendered, from _render_data."""
    return jinja_template.render(**data)


def render_pdf(content: str) -> io.BytesIO:
    """The one place rendered document HTML becomes a PDF: assets only through
    asset_fetcher()."""
    buffer = io.BytesIO()
    weasyprint.HTML(string=content, url_fetcher=asset_fetcher()).write_pdf(
        buffer,
        stylesheets=STYLESHEETS,
        font_config=FONT_CONFIG,
        optimize_size=("fonts", "images"),
    )
    return buffer


class TemplateRenderingError(Exception):
    """Custom exception for template rendering errors"""

    def __init__(self, message, line_number=None, template_error=None):
        self.message = message
        self.line_number = line_number
        self.template_error = template_error
        super().__init__(self.message)


class Documents:
    @staticmethod
    def generate(
        template: str,
        data: dict = {},
        related_object: str = None,
        **kwargs,
    ) -> io.BytesIO:
        options = kwargs.get("options") or {}
        metadata = kwargs.get("metadata") or {}
        context = kwargs.get("context")

        # Build contexts based on related_object and provided data
        shipment_contexts = data.get("shipments_context") or lib.identity(
            get_shipments_context(data["shipments"], context)
            if "shipments" in data and related_object == "shipment"
            else []
        )
        order_contexts = data.get("orders_context") or lib.identity(
            get_orders_context(data["orders"], context)
            if "orders" in data and related_object == "order"
            else []
        )

        # For generic contexts, include the full data structure
        generic_contexts = data.get("generic_context") or lib.identity(
            [{"data": data}] if related_object is None else []
        )

        # If no specific contexts are provided but we have a related_object, create a context with the data
        if not shipment_contexts and not order_contexts and not generic_contexts:
            # For fallback cases, always wrap data to maintain legacy behavior
            generic_contexts = [{"data": data}]

        filename = lib.identity(
            dict(filename=kwargs.get("doc_name")) if kwargs.get("doc_name") else {}
        )

        shared = _shared_render_data()

        def safe_render_prefetch(render_data):
            """Safely render prefetch templates with error handling"""
            result = {}
            for key, value in options.get("prefetch", {}).items():
                try:
                    template_obj = SANDBOXED_ENV.from_string(value)
                    rendered = _render(template_obj, render_data)
                    # Rendered by the same autoescaping environment: its data is
                    # already escaped, and its own markup is the author's.
                    result[key] = markupsafe.Markup(rendered or "")  # noqa: S704 - autoescaped output
                except jinja2.TemplateError as e:
                    # Log the error but continue with empty string
                    result[key] = ""
            return result

        try:
            jinja_template = SANDBOXED_ENV.from_string(template)
        except jinja2.TemplateSyntaxError as e:
            raise TemplateRenderingError(
                f"Template syntax error: {e.message}",
                line_number=e.lineno,
                template_error=e,
            )

        all_contexts = shipment_contexts + order_contexts + generic_contexts

        # If no contexts are available, create a default one
        if not all_contexts:
            all_contexts = [{"data": data} if data else {}]

        rendered_pages = []
        for ctx in all_contexts:
            try:
                # Plain data once per page; prefetch renders against the same data
                render_data = _render_data(ctx, metadata, shared)
                prefetch = safe_render_prefetch(render_data)

                rendered_page = _render(jinja_template, {**render_data, "prefetch": prefetch})
                rendered_pages.append(rendered_page)
            except jinja2.UndefinedError as e:
                raise TemplateRenderingError(
                    f"Template variable error: {str(e)}. Available variables: {list(ctx.keys())}",
                    template_error=e,
                )
            except jinja2.TemplateRuntimeError as e:
                raise TemplateRenderingError(
                    f"Template runtime error: {str(e)}",
                    line_number=getattr(e, "lineno", None),
                    template_error=e,
                )
            except jinja2.TemplateError as e:
                raise TemplateRenderingError(
                    f"Template error: {str(e)}",
                    line_number=getattr(e, "lineno", None),
                    template_error=e,
                )
            except Exception as e:
                raise TemplateRenderingError(
                    f"Unexpected error during template rendering: {str(e)}",
                    template_error=e,
                )

        content = PAGE_SEPARATOR.join(rendered_pages)

        # Handle PDF generation errors
        try:
            return render_pdf(content)
        except Exception as e:
            raise TemplateRenderingError(
                f"PDF generation error: {str(e)}", template_error=e
            )

    @staticmethod
    def generate_template(
        document: document_models.DocumentTemplate,
        data: dict,
        **kwargs,
    ) -> io.BytesIO:
        return Documents.generate(
            template=document.template,
            data=data,
            options=document.options,
            metadata=document.metadata,
            related_object=document.related_object,
            **kwargs,
        )

    @staticmethod
    def generate_shipment_document(slug: str, shipment, **kwargs) -> dict:
        # The shipment's own owner is the scope: the template and the orders it reads
        # resolve only within the organisation the shipment belongs to.
        context = get_object_context(shipment)
        template = _accessible(document_models.DocumentTemplate, context).get(slug=slug)
        # Get carrier from kwargs or from shipment.carrier (JSON snapshot)
        carrier = kwargs.get("carrier") or getattr(shipment, "carrier", None)
        params = dict(
            shipments_context=[
                dict(
                    shipment=manager_serializers.Shipment(shipment).data,
                    line_items=get_shipment_item_contexts(shipment, context),
                    carrier=get_carrier_context(carrier),
                    orders=orders_serializers.Order(
                        get_shipment_order_contexts(shipment, context),
                        many=True,
                    ).data,
                )
            ]
        )
        document = Documents.generate_template(template, params).getvalue()

        return dict(
            doc_format="PDF",
            doc_name=f"{template.name}.pdf",
            doc_type=(template.metadata or {}).get("doc_type") or "commercial_invoice",
            doc_file=base64.b64encode(document).decode("utf-8"),
        )


# -----------------------------------------------------------
# contexts data parsers
# -----------------------------------------------------------
# region


def get_shipments_context(
    shipment_ids: str, context: typing.Optional[RequestContext] = None
) -> typing.List[dict]:
    if shipment_ids == "sample":
        return [utils.SHIPMENT_SAMPLE]

    ids = shipment_ids.split(",")
    shipments = _accessible(manager_models.Shipment, context).filter(id__in=ids)

    return [
        dict(
            shipment=manager_serializers.Shipment(shipment).data,
            line_items=get_shipment_item_contexts(shipment, context),
            # Get carrier from shipment.carrier (JSON snapshot)
            carrier=get_carrier_context(getattr(shipment, "carrier", None)),
            orders=orders_serializers.Order(
                get_shipment_order_contexts(shipment, context), many=True
            ).data,
        )
        for shipment in shipments
    ]


def get_shipment_item_contexts(
    shipment, context: typing.Optional[RequestContext] = None
):
    """Get line items from orders related to the shipment.

    Since line_items is now a JSONField on Order, we query orders related
    to the shipment through the M2M relationship and extract line items.
    """
    # Get orders related to this shipment through M2M
    orders = _accessible(order_models.Order, context).filter(shipments=shipment)

    all_items = []
    for order in orders:
        line_items = order.line_items or []
        for item in line_items:
            all_items.append({
                **item,
                "order": orders_serializers.Order(order).data,
            })

    return all_items


def get_shipment_order_contexts(
    shipment, context: typing.Optional[RequestContext] = None
):
    """Get orders related to the shipment through M2M relationship."""
    return (
        _accessible(order_models.Order, context)
        .filter(shipments=shipment)
        .order_by("-order_date")
        .distinct()
    )


def get_carrier_context(carrier=None):
    if carrier is None:
        return {}

    # Handle both carrier objects and JSON snapshots
    if isinstance(carrier, dict):
        return carrier
    return carrier.data.to_dict()


def get_orders_context(
    order_ids: str, context: typing.Optional[RequestContext] = None
) -> typing.List[dict]:
    if order_ids == "sample":
        return [utils.ORDER_SAMPLE]

    ids = order_ids.split(",")
    orders = _accessible(order_models.Order, context).filter(id__in=ids)

    return [
        dict(
            order=orders_serializers.Order(order).data,
        )
        for order in orders
    ]


def _accessible(model, context: typing.Optional[RequestContext]):
    # Rows only resolve for the context they belong to; without one, nothing resolves.
    return model.objects.none() if context is None else model.access_by(context)


# endregion
