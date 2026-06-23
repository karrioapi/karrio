"""Dynamic configuration editable on runtime powered by django-constance."""

import importlib.util

import karrio.references as ref
import karrio.server.settings.base as base
from decouple import config
from karrio.server.settings.email import (
    EMAIL_FROM_ADDRESS,
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST_USER,
    EMAIL_PORT,
    EMAIL_USE_TLS,
)

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_DATABASE_PREFIX = "constance:core:"

DATA_ARCHIVING_SCHEDULE = config("DATA_ARCHIVING_SCHEDULE", default=168, cast=int)

GOOGLE_CLOUD_API_KEY = config("GOOGLE_CLOUD_API_KEY", default="")
CANADAPOST_ADDRESS_COMPLETE_API_KEY = config("CANADAPOST_ADDRESS_COMPLETE_API_KEY", default="")

# data retention env in days
ORDER_DATA_RETENTION = config("ORDER_DATA_RETENTION", default=183, cast=int)
TRACKER_DATA_RETENTION = config("TRACKER_DATA_RETENTION", default=183, cast=int)
SHIPMENT_DATA_RETENTION = config("SHIPMENT_DATA_RETENTION", default=183, cast=int)
API_LOGS_DATA_RETENTION = config("API_LOGS_DATA_RETENTION", default=92, cast=int)

# background tracking max active age
TRACKER_MAX_ACTIVE_DAYS = config("TRACKER_MAX_ACTIVE_DAYS", default=90, cast=int)

# paperless trade (ETD): the system-wide default commercial-invoice template
# BODY (HTML/Jinja), rendered inline when a merchant enables paperless_trade
# without supplying their own document or per-shipment invoice_template (e.g. the
# post_upload flow on GLS). It is the template *body*, not a slug — so a default
# always resolves without depending on a tenant-owned DocumentTemplate row. The
# render context exposes `shipment`, `line_items`, `carrier`, `orders`, plus
# `units`/`utils`/`lib`. Editable at runtime via Constance; clear it to opt out
# (the post_upload job then records an actionable `skipped` reason — D15).
DEFAULT_COMMERCIAL_INVOICE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Commercial Invoice</title>
  <style>
    * { box-sizing: border-box; }
    body { font-family: Arial, Helvetica, sans-serif; font-size: 10.5px; color: #1a1a1a; margin: 0; padding: 24px; }
    table { border-collapse: collapse; width: 100%; }
    .hd { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #111; padding-bottom: 6px; margin-bottom: 10px; }
    .hd h1 { font-size: 18px; margin: 0; letter-spacing: .5px; }
    .hd .sub { font-size: 10px; color: #555; text-align: right; line-height: 1.4; }
    .grid { table-layout: fixed; margin-bottom: 10px; }
    .grid td { vertical-align: top; width: 50%; border: 1px solid #bbb; padding: 7px 9px; }
    .box-title { font-size: 9px; font-weight: bold; text-transform: uppercase; letter-spacing: .6px; color: #666; border-bottom: 1px solid #ddd; padding-bottom: 3px; margin-bottom: 4px; }
    .name { font-weight: bold; font-size: 11px; }
    .row { line-height: 1.45; }
    .lbl { color: #666; }
    .meta { border: 1px solid #bbb; padding: 6px 9px; margin-bottom: 10px; }
    .meta .item { display: inline-block; margin-right: 22px; font-size: 10px; line-height: 1.7; }
    table.items { margin-bottom: 10px; }
    table.items thead { display: table-header-group; }
    table.items tr { page-break-inside: avoid; }
    table.items th, table.items td { border: 1px solid #bbb; padding: 5px 7px; }
    table.items th { background: #f2f2f2; font-size: 9px; text-transform: uppercase; letter-spacing: .4px; text-align: left; }
    table.items td { font-size: 10px; vertical-align: top; }
    .r { text-align: right; white-space: nowrap; }
    .c { text-align: center; }
    .sku { color: #777; font-size: 9px; }
    .foot { display: flex; justify-content: space-between; gap: 18px; page-break-inside: avoid; }
    .decl { flex: 1; font-size: 9.5px; color: #333; line-height: 1.5; }
    .sign { margin-top: 26px; border-top: 1px solid #999; width: 210px; padding-top: 3px; color: #666; font-size: 9px; }
    table.tot { width: 280px; }
    table.tot td { padding: 3px 8px; font-size: 10px; }
    table.tot td.k { color: #555; text-align: right; }
    table.tot td.v { text-align: right; white-space: nowrap; border-left: 1px solid #eee; }
    table.tot tr.grand td { font-weight: bold; font-size: 11px; border-top: 2px solid #111; }
  </style>
</head>
<body>
  {% set c = shipment.customs or {} %}
  {% set co = c.options or {} %}
  {% set items = c.commodities or [] %}
  {% set ns = namespace(sub=0.0, cur='', wt=0.0, wu='') %}
  {% for it in items %}
    {% set q = (it.quantity or 1)|float %}
    {% set u = (it.value_amount or 0)|float %}
    {% set ns.sub = ns.sub + (q * u) %}
    {% set ns.cur = it.value_currency or ns.cur %}
  {% endfor %}
  {% for p in (shipment.parcels or []) %}
    {% set ns.wt = ns.wt + (p.weight or 0)|float %}
    {% set ns.wu = p.weight_unit or ns.wu %}
  {% endfor %}
  {% set currency = ns.cur or (c.duty.currency if c.duty else '') or (shipment.options.currency if shipment.options else '') %}

  <div class="hd">
    <h1>COMMERCIAL INVOICE</h1>
    <div class="sub">
      {% if shipment.tracking_number %}Shipment ID: <b>{{ shipment.tracking_number }}</b><br/>{% endif %}
      {% if shipment.created_at %}{{ shipment.created_at[:10] }}{% endif %}
    </div>
  </div>

  <table class="grid"><tr>
    <td>
      <div class="box-title">Exporter / From</div>
      <div class="name">{{ shipment.shipper.company_name or shipment.shipper.person_name or '-' }}</div>
      {% if shipment.shipper.company_name and shipment.shipper.person_name %}<div class="row">{{ shipment.shipper.person_name }}</div>{% endif %}
      <div class="row">{{ shipment.shipper.address_line1 }}{% if shipment.shipper.address_line2 %}, {{ shipment.shipper.address_line2 }}{% endif %}</div>
      <div class="row">{{ shipment.shipper.postal_code }} {{ shipment.shipper.city }}{% if shipment.shipper.state_code %}, {{ shipment.shipper.state_code }}{% endif %}</div>
      <div class="row">{{ shipment.shipper.country_code }}</div>
      {% if shipment.shipper.phone_number %}<div class="row"><span class="lbl">Tel:</span> {{ shipment.shipper.phone_number }}</div>{% endif %}
      {% if shipment.shipper.email %}<div class="row"><span class="lbl">Email:</span> {{ shipment.shipper.email }}</div>{% endif %}
      {% if shipment.shipper.federal_tax_id %}<div class="row"><span class="lbl">Tax ID:</span> {{ shipment.shipper.federal_tax_id }}</div>{% endif %}
      {% if co.vat_registration_number %}<div class="row"><span class="lbl">VAT No:</span> {{ co.vat_registration_number }}</div>{% endif %}
      {% if co.eori_number %}<div class="row"><span class="lbl">EORI No:</span> {{ co.eori_number }}</div>{% endif %}
    </td>
    <td>
      <div class="box-title">Consignee / Ship To</div>
      <div class="name">{{ shipment.recipient.company_name or shipment.recipient.person_name or '-' }}</div>
      {% if shipment.recipient.company_name and shipment.recipient.person_name %}<div class="row">{{ shipment.recipient.person_name }}</div>{% endif %}
      <div class="row">{{ shipment.recipient.address_line1 }}{% if shipment.recipient.address_line2 %}, {{ shipment.recipient.address_line2 }}{% endif %}</div>
      <div class="row">{{ shipment.recipient.postal_code }} {{ shipment.recipient.city }}{% if shipment.recipient.state_code %}, {{ shipment.recipient.state_code }}{% endif %}</div>
      <div class="row">{{ shipment.recipient.country_code }}</div>
      {% if shipment.recipient.phone_number %}<div class="row"><span class="lbl">Tel:</span> {{ shipment.recipient.phone_number }}</div>{% endif %}
      {% if shipment.recipient.email %}<div class="row"><span class="lbl">Email:</span> {{ shipment.recipient.email }}</div>{% endif %}
      {% if shipment.recipient.federal_tax_id %}<div class="row"><span class="lbl">Tax ID / VAT No:</span> {{ shipment.recipient.federal_tax_id }}</div>{% endif %}
    </td>
  </tr></table>

  <div class="meta">
    {% if c.invoice %}<span class="item"><span class="lbl">Invoice No:</span> {{ c.invoice }}</span>{% endif %}
    {% if c.invoice_date %}<span class="item"><span class="lbl">Invoice Date:</span> {{ c.invoice_date }}</span>{% endif %}
    {% if shipment.reference %}<span class="item"><span class="lbl">Reference:</span> {{ shipment.reference }}</span>{% endif %}
    {% if c.incoterm %}<span class="item"><span class="lbl">Incoterm:</span> {{ c.incoterm }}</span>{% endif %}
    {% if c.content_type %}<span class="item"><span class="lbl">Reason for Export:</span> {{ c.content_type|replace('_', ' ')|title }}</span>{% endif %}
    {% if shipment.service %}<span class="item"><span class="lbl">Service:</span> {{ shipment.service|replace('_', ' ')|title }}</span>{% endif %}
  </div>

  <table class="items">
    <thead>
      <tr>
        <th class="c">#</th>
        <th>Description of Goods</th>
        <th>HS Code</th>
        <th class="c">Origin</th>
        <th class="r">Qty</th>
        <th class="r">Unit Value</th>
        <th class="r">Total Value</th>
      </tr>
    </thead>
    <tbody>
      {% for it in items %}
      {% set q = (it.quantity or 1)|float %}
      {% set u = (it.value_amount or 0)|float %}
      <tr>
        <td class="c">{{ loop.index }}</td>
        <td>{{ it.description or it.title or '-' }}{% if it.sku %}<div class="sku">SKU: {{ it.sku }}</div>{% endif %}</td>
        <td>{{ it.hs_code or '-' }}</td>
        <td class="c">{{ it.origin_country or shipment.shipper.country_code or '-' }}</td>
        <td class="r">{{ q|int }}</td>
        <td class="r">{{ "%.2f"|format(u) }} {{ it.value_currency or currency }}</td>
        <td class="r">{{ "%.2f"|format(q * u) }} {{ it.value_currency or currency }}</td>
      </tr>
      {% else %}
      <tr><td colspan="7" class="c" style="color:#999; padding:14px;">No commodities declared</td></tr>
      {% endfor %}
    </tbody>
  </table>

  <div class="foot">
    <div class="decl">
      <b>Declaration:</b> I/We hereby certify that the information on this invoice is true and correct and that the contents of this shipment are as stated above.
      {% if c.signer %}<div style="margin-top:6px;"><span class="lbl">Signed by:</span> {{ c.signer }}</div>{% endif %}
      <div class="sign">Signature &amp; Date</div>
    </div>
    <table class="tot">
      <tr><td class="k">Subtotal</td><td class="v">{{ "%.2f"|format(ns.sub) }} {{ currency }}</td></tr>
      {% if c.duty and c.duty.declared_value %}<tr><td class="k">Declared Value</td><td class="v">{{ "%.2f"|format(c.duty.declared_value|float) }} {{ c.duty.currency or currency }}</td></tr>{% endif %}
      <tr class="grand"><td class="k">Total</td><td class="v">{{ "%.2f"|format(ns.sub) }} {{ currency }}</td></tr>
      <tr><td class="k">Currency</td><td class="v">{{ currency or '-' }}</td></tr>
      <tr><td class="k">Total Packages</td><td class="v">{{ (shipment.parcels or [])|length or 1 }}</td></tr>
      {% if ns.wt %}<tr><td class="k">Total Weight</td><td class="v">{{ "%.2f"|format(ns.wt) }} {{ ns.wu }}</td></tr>{% endif %}
    </table>
  </div>
</body>
</html>
"""

PAPERLESS_DEFAULT_INVOICE_TEMPLATE = config(
    "PAPERLESS_DEFAULT_INVOICE_TEMPLATE", default=DEFAULT_COMMERCIAL_INVOICE_TEMPLATE
)

# registry config
ENABLE_ALL_PLUGINS_BY_DEFAULT = config("ENABLE_ALL_PLUGINS_BY_DEFAULT", default=bool(base.DEBUG), cast=bool)

# Feature flags config — always present with False default when module is absent
FEATURE_FLAGS_CONFIG = {
    "AUDIT_LOGGING": (
        base.AUDIT_LOGGING if importlib.util.find_spec("karrio.server.audit") is not None else False,
        "Audit logging",
        bool,
    ),
    "ALLOW_SIGNUP": (
        base.ALLOW_SIGNUP,
        "Allow signup",
        bool,
    ),
    "ALLOW_ADMIN_APPROVED_SIGNUP": (
        base.ALLOW_ADMIN_APPROVED_SIGNUP,
        "Allow admin approved signup",
        bool,
    ),
    "ALLOW_MULTI_ACCOUNT": (
        base.ALLOW_MULTI_ACCOUNT,
        "Allow multi account",
        bool,
    ),
    "ADMIN_DASHBOARD": (
        base.ADMIN_DASHBOARD if importlib.util.find_spec("karrio.server.admin") is not None else False,
        "Admin dashboard",
        bool,
    ),
    "MULTI_ORGANIZATIONS": (
        base.MULTI_ORGANIZATIONS if importlib.util.find_spec("karrio.server.orgs") is not None else False,
        "Multi organizations",
        bool,
    ),
    "ORDERS_MANAGEMENT": (
        base.ORDERS_MANAGEMENT if importlib.util.find_spec("karrio.server.orders") is not None else False,
        "Orders management",
        bool,
    ),
    "APPS_MANAGEMENT": (
        base.APPS_MANAGEMENT if importlib.util.find_spec("karrio.server.apps") is not None else False,
        "Apps management",
        bool,
    ),
    "DOCUMENTS_MANAGEMENT": (
        base.DOCUMENTS_MANAGEMENT if importlib.util.find_spec("karrio.server.documents") is not None else False,
        "Documents management",
        bool,
    ),
    "DATA_IMPORT_EXPORT": (
        base.DATA_IMPORT_EXPORT if importlib.util.find_spec("karrio.server.data") is not None else False,
        "Data import export",
        bool,
    ),
    "WORKFLOW_MANAGEMENT": (
        base.WORKFLOW_MANAGEMENT if importlib.util.find_spec("karrio.server.automation") is not None else False,
        "Workflow management",
        bool,
    ),
    "SHIPPING_RULES": (
        base.SHIPPING_RULES if importlib.util.find_spec("karrio.server.automation") is not None else False,
        "Shipping rules",
        bool,
    ),
    "SHIPPING_METHODS": (
        base.SHIPPING_METHODS if importlib.util.find_spec("karrio.server.shipping") is not None else False,
        "Shipping methods",
        bool,
    ),
    "ADVANCED_ANALYTICS": (
        base.ADVANCED_ANALYTICS if importlib.util.find_spec("karrio.server.analytics") is not None else False,
        "Advanced analytics",
        bool,
    ),
    "PERSIST_SDK_TRACING": (
        base.PERSIST_SDK_TRACING,
        "Persist SDK tracing",
        bool,
    ),
    "CLOSED_BETA_ENABLED": (
        config("CLOSED_BETA_ENABLED", default=False, cast=bool),
        "Enable closed beta mode — only invited KAccounts can onboard",
        bool,
    ),
}

# Update fieldsets to only include existing feature flags
FEATURE_FLAGS_FIELDSET = list(FEATURE_FLAGS_CONFIG.keys())

# Plugin registry
ref.collect_failed_plugins_data()
PLUGIN_REGISTRY = {
    "ENABLE_ALL_PLUGINS_BY_DEFAULT": (
        ENABLE_ALL_PLUGINS_BY_DEFAULT,
        "Enable all plugins by default",
        bool,
    ),
    **{
        f"{ext.upper()}_ENABLED": (
            config(f"{ext.upper()}_ENABLED", default=True, cast=bool),
            f"{metadata.get('label')} plugin",
            bool,
        )
        for ext, metadata in ref.PLUGIN_METADATA.items()
    },
}

# Collect plugin system configs from ref.SYSTEM_CONFIGS
# Format: Dict[str, Tuple[default_value, description, type]]
PLUGIN_SYSTEM_CONFIG = {
    key: (config(key, default=default_value, cast=value_type), description, value_type)
    for key, (default_value, description, value_type) in ref.SYSTEM_CONFIGS.items()
}
PLUGIN_SYSTEM_CONFIG_FIELDSETS = {
    f"{metadata.get('label')} Config": tuple(metadata.get("system_config", {}).keys())
    for _, metadata in ref.PLUGIN_METADATA.items()
    if metadata.get("system_config")
}


# Aggregate all config sections into CONSTANCE_CONFIG
CONSTANCE_CONFIG = {
    "EMAIL_USE_TLS": (
        EMAIL_USE_TLS,
        "Determine whether the configuration support TLS",
        bool,
    ),
    "EMAIL_HOST_USER": (
        EMAIL_HOST_USER,
        "The authentication user (email). e.g: admin@karrio.io",
        str,
    ),
    "EMAIL_HOST_PASSWORD": (EMAIL_HOST_PASSWORD, "The authentication password", str),
    "EMAIL_HOST": (EMAIL_HOST, "The mail server host. e.g: smtp.gmail.com", str),
    "EMAIL_PORT": (
        EMAIL_PORT,
        "The mail server port. e.g: 465 (SSL required) or 587 (TLS required)",
        int,
    ),
    "EMAIL_FROM_ADDRESS": (
        EMAIL_FROM_ADDRESS,
        "Email sent from. e.g: noreply@karrio.io",
        str,
    ),
    "GOOGLE_CLOUD_API_KEY": (GOOGLE_CLOUD_API_KEY, "A Google GeoCoding API key", str),
    "CANADAPOST_ADDRESS_COMPLETE_API_KEY": (
        CANADAPOST_ADDRESS_COMPLETE_API_KEY,
        "The Canada Post AddressComplete service API Key",
        str,
    ),
    "ORDER_DATA_RETENTION": (
        ORDER_DATA_RETENTION,
        "Order data retention period (in days)",
        int,
    ),
    "TRACKER_DATA_RETENTION": (
        TRACKER_DATA_RETENTION,
        "Trackers data retention period (in days)",
        int,
    ),
    "SHIPMENT_DATA_RETENTION": (
        SHIPMENT_DATA_RETENTION,
        "Shipment data retention period (in days)",
        int,
    ),
    "API_LOGS_DATA_RETENTION": (
        API_LOGS_DATA_RETENTION,
        "API request and SDK tracing logs retention period (in days)",
        int,
    ),
    "TRACKER_MAX_ACTIVE_DAYS": (
        TRACKER_MAX_ACTIVE_DAYS,
        "Maximum age (in days) for active background tracking. Trackers created more than this many days ago will be retired from polling and their status set to 'unknown'.",
        int,
    ),
    "PAPERLESS_DEFAULT_INVOICE_TEMPLATE": (
        PAPERLESS_DEFAULT_INVOICE_TEMPLATE,
        "Default commercial-invoice template BODY (HTML/Jinja) rendered for "
        "paperless-trade (ETD) shipments when the merchant supplies neither a "
        "document nor a per-shipment invoice_template. Render context exposes "
        "`shipment`, `line_items`, `carrier`, `orders`. Clear to opt out.",
        str,
    ),
    **FEATURE_FLAGS_CONFIG,
    **PLUGIN_REGISTRY,
    **PLUGIN_SYSTEM_CONFIG,
}

CONSTANCE_CONFIG_FIELDSETS = {
    "Email Config": (
        "EMAIL_USE_TLS",
        "EMAIL_HOST_USER",
        "EMAIL_HOST_PASSWORD",
        "EMAIL_HOST",
        "EMAIL_PORT",
        "EMAIL_FROM_ADDRESS",
    ),
    "Address Validation Service": (
        "GOOGLE_CLOUD_API_KEY",
        "CANADAPOST_ADDRESS_COMPLETE_API_KEY",
    ),
    "Data Retention": (
        "ORDER_DATA_RETENTION",
        "TRACKER_DATA_RETENTION",
        "SHIPMENT_DATA_RETENTION",
        "API_LOGS_DATA_RETENTION",
        "TRACKER_MAX_ACTIVE_DAYS",
    ),
    "Paperless Trade": ("PAPERLESS_DEFAULT_INVOICE_TEMPLATE",),
    "Feature Flags": tuple(FEATURE_FLAGS_FIELDSET),
    "Registry Config": ("ENABLE_ALL_PLUGINS_BY_DEFAULT",),
    "Registry Plugins": tuple([k for k in PLUGIN_REGISTRY if k not in ("ENABLE_ALL_PLUGINS_BY_DEFAULT",)]),
    **PLUGIN_SYSTEM_CONFIG_FIELDSETS,
}
