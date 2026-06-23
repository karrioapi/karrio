import base64
import datetime

import karrio.core as core
import karrio.core.errors as errors
import karrio.lib as lib


class Settings(core.Settings):
    """GLS Group connection settings."""

    client_id: str
    client_secret: str
    contact_id: str = None

    @property
    def carrier_name(self):
        return "gls"

    @property
    def server_url(self):
        return "https://api-sandbox.gls-group.net" if self.test_mode else "https://api.gls-group.net"

    @property
    def shipment_api_url(self):
        return f"{self.server_url}/shipit-farm/v1/backend"

    @property
    def tracking_api_url(self):
        return f"{self.server_url}/track-and-trace-v1"

    @property
    def customs_api_url(self):
        return f"{self.server_url}/customs-management/export/public/v3"

    @property
    def document_management_url(self):
        return f"{self.server_url}/document-management/v1"

    @property
    def auth_url(self):
        return f"{self.server_url}/oauth2/v2/token"

    @property
    def access_token(self):
        cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"

        return self.connection_cache.thread_safe(
            refresh_func=lambda: login(self),
            cache_key=cache_key,
            buffer_minutes=30,
        ).get_state()

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def connection_app_identifier(self) -> str | None:
        return (
            self.connection_config.app_identifier.state
            or self.connection_system_config.get("GLS_APP_IDENTIFIER")
            or None
        )


def login(settings: Settings):
    """OAuth2 client_credentials grant."""
    import karrio.providers.gls.error as error

    credentials = f"{settings.client_id}:{settings.client_secret}"
    basic_auth = base64.b64encode(credentials.encode("utf-8")).decode("ascii")

    result = lib.request(
        url=settings.auth_url,
        trace=settings.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {basic_auth}",
        },
        data="grant_type=client_credentials",
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages=messages)

    expiry = datetime.datetime.now() + datetime.timedelta(seconds=float(response.get("expires_in", 0)))
    return {**response, "expiry": lib.fdatetime(expiry)}


class ConnectionConfig(lib.Enum):
    """GLS Group connection configuration."""

    template_name = lib.OptionEnum("template_name", str)
    app_identifier = lib.OptionEnum(
        "app_identifier",
        str,
        meta=dict(configurable=False),
    )
    parcel_shop_default_type = lib.OptionEnum(
        "parcel_shop_default_type",
        lib.units.create_enum("ParcelShopType", ["LOCKER", "SHOP", "SHOPINSHOP"]),
    )
    parcel_shop_default_radius = lib.OptionEnum("parcel_shop_default_radius", int)
    parcel_shop_default_max_results = lib.OptionEnum("parcel_shop_default_max_results", int)
    submit_customs_consignment = lib.OptionEnum("submit_customs_consignment", bool, default=False)


def extract_parcel_shops(response) -> list[dict]:
    """Normalise a ParcelShop finder response to a list of shop dicts. See SPECS.md."""
    if isinstance(response, list):
        return [shop for shop in response if isinstance(shop, dict)]
    if not isinstance(response, dict):
        return []
    listed = response.get("ParcelShop")
    if isinstance(listed, list):
        return [shop for shop in listed if isinstance(shop, dict)]
    if isinstance(listed, dict):
        return [listed]
    if "ParcelShopID" in response:
        return [response]
    return []


def normalize_opening_hours(working_days) -> list[dict]:
    """Flatten ``WorkingDay[].OpeningHours.OpeningHours[]`` to ``[{day, from_time, to_time}]``."""
    if not isinstance(working_days, list):
        return []
    return [
        dict(
            day=entry.get("DayOfWeek"),
            from_time=_format_ms_time(window.get("From")),
            to_time=_format_ms_time(window.get("To")),
        )
        for entry in working_days
        if isinstance(entry, dict)
        for window in ((entry.get("OpeningHours") or {}).get("OpeningHours") or [])
        if isinstance(window, dict)
    ]


def _format_ms_time(value) -> str | None:
    """ms-since-midnight + 1h → ``HH:MM`` (rest_parcel_shop.html)."""
    if value is None or not isinstance(value, (int, float)):
        return None
    minutes = (int(value) // 60000 + 60) % (24 * 60)
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def parse_error_response(response):
    """Wrap GLS error responses (JSON body or header-only) into a JSON envelope."""
    content = lib.failsafe(lambda: lib.decode(response.read()))

    if any(content or ""):
        parsed = lib.failsafe(lambda: lib.to_dict(content))
        if parsed is not None:
            return content
        return lib.to_json(
            dict(
                errors=[
                    dict(
                        code=str(response.code),
                        message=content,
                    )
                ]
            )
        )

    error_code = lib.failsafe(lambda: response.headers.get("error"))
    message = lib.failsafe(lambda: response.headers.get("message"))

    if error_code or message:
        return lib.to_json(
            dict(
                errors=[
                    dict(
                        code=error_code or str(response.code),
                        message=message or response.reason,
                    )
                ]
            )
        )

    return lib.to_json(dict(errors=[dict(code=str(response.code), message=response.reason)]))


# -----------------------------------------------------------------------------
# Paperless trade (post_upload) transport helpers — the verbose multi-step wire
# orchestration behind ``Proxy.upload_document``, kept here so the proxy stays a
# thin list of interface methods. Each sources its tracer from ``settings`` (so
# every call still groups under the same request_log_id).
# -----------------------------------------------------------------------------


def extract_parcel_numbers(shipment_response) -> list[str]:
    r"""Pull the customs-linkable parcel identifiers from createParcels.

    The Customs Consignment v3 ``parcelNumbers`` field validates against
    ``^(\d{11}|[A-Z0-9]{8})$`` — the ShipIT ``TrackID`` matches; the
    ``ParcelNumber`` (12 digits) does not. See SPECS.md."""
    data = lib.failsafe(lambda: lib.to_dict(shipment_response)) or {}
    created = (data.get("CreatedShipment") or {}) if isinstance(data, dict) else {}
    parcels = created.get("ParcelData") or []
    return [p.get("TrackID") for p in parcels if isinstance(p, dict) and p.get("TrackID")]


def upload_one_document(settings: Settings, envelope: dict, document: dict) -> dict:
    """Run a single Document Management prepare-upload + S3 PUT cycle for one
    ``DocumentFile`` (steps 1–2 of the paperless ``upload_document`` chain)."""
    prepared_raw = lib.failsafe(
        lambda: lib.request(
            url=f"{settings.document_management_url}/documents/customs/prepare-upload",
            data=lib.to_json(envelope),
            trace=settings.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {settings.access_token}",
            },
            on_error=parse_error_response,
        )
    )
    prepared = (lib.failsafe(lambda: lib.to_dict(prepared_raw)) or {}) if prepared_raw else {}
    upload_url = prepared.get("uploadURL")
    if upload_url and document.get("doc_file"):
        content_type = (
            "application/pdf" if (document.get("doc_format") or "pdf").lower() == "pdf" else "application/octet-stream"
        )
        lib.failsafe(
            lambda: lib.request(
                url=upload_url,
                data=base64.b64decode(document["doc_file"]),
                trace=settings.trace_as("json"),
                method="PUT",
                headers={"Content-Type": content_type},
            )
        )
    prepared["displayFileName"] = document.get("doc_name")
    return prepared


def post_customs_consignment(settings: Settings, prepare_upload_responses: list[dict], ctx: dict) -> dict | None:
    """Step 3 of the ``upload_document`` chain — fire the Customs Consignment v3
    POST with ``parcelNumbers`` (the ShipIT TrackID) + ``linkedDocuments`` (the
    documentIds from the prepare-upload responses). Returns the customs response
    (success body or parsed error envelope) so the parser can surface a
    rejection; returns ``None`` when no customs payload was built (see
    ``document.document_upload_request``)."""
    consignment = (ctx or {}).get("customs_consignment")
    if consignment is None:
        return None

    track_id = ctx.get("tracking_number")
    if not track_id:
        return None

    consignment.parcelNumbers = [track_id]

    document_ids = [
        r.get("documentId") for r in (prepare_upload_responses or []) if isinstance(r, dict) and r.get("documentId")
    ]
    if document_ids:
        from karrio.schemas.gls.customs_consignment_request import LinkedDocumentType

        consignment.linkedDocuments = [LinkedDocumentType(documentId=doc_id) for doc_id in document_ids]

    response = lib.request(
        url=f"{settings.customs_api_url}/customs-consignments",
        data=lib.to_json(lib.to_dict(consignment)),
        trace=settings.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.access_token}",
        },
        on_error=parse_error_response,
    )
    return (lib.failsafe(lambda: lib.to_dict(response)) or None) if response else None
