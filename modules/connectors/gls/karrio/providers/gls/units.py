import csv
import datetime
import pathlib

import karrio.core.models as models
import karrio.core.units as units
import karrio.lib as lib
import karrio.schemas.gls.customs_consignment_request as gls_customs

# GLS-mandated billing marker. Sent as ``Shipment.Middleware`` on every
# request. See SPECS.md "Mandatory wire-shape facts".
MIDDLEWARE = "JTLviaGLS"

SYSTEM_CONFIG = {
    "GLS_APP_IDENTIFIER": (
        "",
        "Source-software marker GLS shows in their logs (Shipment.Identifier)",
        str,
    ),
}


_BOTH = ["gls_parcel", "gls_express"]
_EXPRESS_ONLY = ["gls_express"]


class ParcelShopType(lib.StrEnum):
    """GLS ParcelShop network types (rest_parcel_shop.html ``ParcelShopType``)."""

    LOCKER = "LOCKER"
    SHOP = "SHOP"
    SHOPINSHOP = "SHOPINSHOP"


LOCATION_TYPE_TO_PARCEL_SHOP_TYPE = {
    "locker": ParcelShopType.LOCKER.value,
    "parcel_shop": ParcelShopType.SHOP.value,
    "shop": ParcelShopType.SHOP.value,
    "shop_in_shop": ParcelShopType.SHOPINSHOP.value,
}


class PackagingType(lib.StrEnum):
    """GLS Group specific packaging types"""

    gls_parcel = "PARCEL"
    gls_envelope = "ENVELOPE"
    gls_pallet = "PALLET"

    """Unified Packaging type mapping"""
    envelope = gls_envelope
    pak = gls_parcel
    small_box = gls_parcel
    medium_box = gls_parcel
    your_packaging = gls_parcel
    pallet = gls_pallet


class ShippingService(lib.StrEnum):
    """GLS Group specific services."""

    gls_parcel = "PARCEL"
    gls_express = "EXPRESS"


class ShippingOption(lib.Enum):
    """GLS Group specific options — mirrors the doxygen service catalog. See SPECS.md."""

    # --- Shipment-level flag services (w/o attributes) ---

    gls_saturday_delivery = lib.OptionEnum(
        "service_Saturday",
        bool,
        help="Saturday delivery",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_flex_delivery = lib.OptionEnum(
        "service_flexdelivery",
        bool,
        help="Notify recipient about delivery options",
        meta=dict(category="NOTIFICATION", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_addressee_only = lib.OptionEnum(
        "service_addresseeonly",
        bool,
        help="Delivery only to the addressee (no neighbour delivery)",
        meta=dict(category="SIGNATURE", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_signature_service = lib.OptionEnum(
        "service_signature",
        bool,
        help="Require signature upon delivery",
        meta=dict(category="SIGNATURE", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_guaranteed24 = lib.OptionEnum(
        "service_guaranteed24",
        bool,
        help="Guaranteed delivery within 24 hours",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_t24 = lib.OptionEnum(
        "service_t24",
        bool,
        help="T24 transit service (Carrier-defined)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_t48 = lib.OptionEnum(
        "service_t48",
        bool,
        help="T48 transit service (Carrier-defined)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_tyre = lib.OptionEnum(
        "service_tyre",
        bool,
        help="Tyre handling (Parcel/Express)",
        meta=dict(configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_private_delivery = lib.OptionEnum(
        "service_privatedelivery",
        bool,
        help="Private delivery (residential routing)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_inbound_logistics = lib.OptionEnum(
        "service_inbound",
        bool,
        help="Inbound logistics",
        meta=dict(configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_document_return = lib.OptionEnum(
        "service_documentreturn",
        bool,
        help="Document return service",
        meta=dict(category="RETURN", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_complete_delivery_consignment = lib.OptionEnum(
        "service_completedeliveryconsignment",
        bool,
        help="Complete-delivery consignment service",
        meta=dict(configurable=True, service_level=True, compatible_services=_BOTH),
    )

    # --- Time-definite slots (resolved via time_definite_service_name) ---

    gls_time_definite_service = lib.OptionEnum(
        "TimeDefiniteService",
        str,
        help="Time-definite slot — one of service_0800, _0900, _1000, _1200, _1300, "
        "service_saturday_0900, _saturday_1000, _saturday_1200",
        meta=dict(
            category="DELIVERY_OPTIONS", configurable=True, service_level=True, compatible_services=_EXPRESS_ONLY
        ),
    )

    # --- Shipment-level attribute services ---

    gls_shop_delivery = lib.OptionEnum(
        "service_shopdelivery",
        bool,
        help="Delivery to a GLS ParcelShop",
        meta=dict(category="PUDO", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_shop_id = lib.OptionEnum(
        "ParcelShopID",
        str,
        help="GLS ParcelShop ID ({partnerID}-{localID})",
        meta=dict(category="PUDO", configurable=True, service_level=False, compatible_services=_BOTH),
    )

    gls_deposit_service = lib.OptionEnum(
        "service_deposit",
        bool,
        help="Deliver to a predefined deposit location",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_deposit_description = lib.OptionEnum(
        "PlaceOfDeposit",
        str,
        help="Place of deposit (free text, max 60 chars; letterbox variant max 121)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False, compatible_services=_BOTH),
    )

    gls_ident_pin_service = lib.OptionEnum(
        "service_identpin",
        bool,
        help="Identification by 4-digit PIN at delivery",
        meta=dict(category="SIGNATURE", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_ident_pin = lib.OptionEnum(
        "PIN",
        str,
        help="4-digit PIN the consignee must enter to receive the parcel",
        meta=dict(category="SIGNATURE", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_ident_pin_birthdate = lib.OptionEnum(
        "IdentPinBirthdate",
        str,
        help="Optional consignee birthdate for IdentPin (YYYY-MM-DD)",
        meta=dict(category="SIGNATURE", configurable=True, service_level=False, compatible_services=_BOTH),
    )

    gls_ident_service = lib.OptionEnum(
        "service_ident",
        bool,
        help="Identification by birthdate + name at delivery",
        meta=dict(category="SIGNATURE", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_ident_birthdate = lib.OptionEnum(
        "IdentBirthdate",
        str,
        help="Consignee birthdate (YYYY-MM-DD)",
        meta=dict(category="SIGNATURE", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_ident_firstname = lib.OptionEnum(
        "IdentFirstname",
        str,
        help="Consignee first name",
        meta=dict(category="SIGNATURE", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_ident_lastname = lib.OptionEnum(
        "IdentLastname",
        str,
        help="Consignee last name",
        meta=dict(category="SIGNATURE", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_ident_nationality = lib.OptionEnum(
        "IdentNationality",
        str,
        help="Consignee nationality (ISO country code)",
        meta=dict(category="SIGNATURE", configurable=True, service_level=False, compatible_services=_BOTH),
    )

    gls_delivery_at_work_service = lib.OptionEnum(
        "service_deliveryatwork",
        bool,
        help="Delivery at recipient's workplace",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_dax_recipient_name = lib.OptionEnum(
        "DaxRecipientName",
        str,
        help="DeliveryAtWork recipient name (defaults to recipient.person_name)",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_dax_alternate_recipient = lib.OptionEnum(
        "DaxAlternateRecipientName",
        str,
        help="DeliveryAtWork alternate recipient",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_dax_building = lib.OptionEnum(
        "DaxBuilding",
        str,
        help="DeliveryAtWork building number",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_dax_floor = lib.OptionEnum(
        "DaxFloor",
        str,
        help="DeliveryAtWork floor number",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_dax_room = lib.OptionEnum(
        "DaxRoom",
        str,
        help="DeliveryAtWork room number",
        meta=dict(category="DELIVERY_OPTIONS", configurable=True, service_level=False, compatible_services=_BOTH),
    )

    gls_intercompany_service = lib.OptionEnum(
        "service_intercompany",
        bool,
        help="Intercompany service — uses payload.return_address for the second leg",
        meta=dict(configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_intercompany_number_of_labels = lib.OptionEnum(
        "IntercompanyNumberOfLabels",
        int,
        help="Number of intercompany labels (defaults to 1)",
        meta=dict(configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_intercompany_expected_weight = lib.OptionEnum(
        "IntercompanyExpectedWeight",
        float,
        help="Expected weight of the intercompany return shipment (kg)",
        meta=dict(configurable=True, service_level=False, compatible_services=_BOTH),
    )

    gls_exchange_service = lib.OptionEnum(
        "service_exchange",
        bool,
        help="Exchange service — uses payload.return_address for the exchange leg",
        meta=dict(configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_exchange_expected_weight = lib.OptionEnum(
        "ExchangeExpectedWeight",
        float,
        help="Expected weight of the exchange return shipment (kg)",
        meta=dict(configurable=True, service_level=False, compatible_services=_BOTH),
    )

    # --- Shipment-level return services ---

    gls_pick_and_return = lib.OptionEnum(
        "service_pickandreturn",
        bool,
        help="Pickup at recipient + return to shipper",
        meta=dict(category="RETURN", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_pick_and_ship = lib.OptionEnum(
        "service_pickandship",
        bool,
        help="Pickup at shipper + ship to recipient",
        meta=dict(category="RETURN", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_shop_return = lib.OptionEnum(
        "service_shopreturn",
        bool,
        help="Pre-printed return label inside the package",
        meta=dict(category="RETURN", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_return_enabled = lib.OptionEnum(
        "ReturnService",
        bool,
        help="Karrio unified return-label flag (maps onto ShopReturn)",
        meta=dict(category="RETURN", configurable=True, service_level=True, compatible_services=_BOTH),
    )

    # --- Per-ShipmentUnit attribute services ---

    gls_cash_service = lib.OptionEnum(
        "service_cash",
        bool,
        help="Cash on delivery (per unit) — amount sourced from `cash_on_delivery`",
        meta=dict(category="COD", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_cash_reason = lib.OptionEnum(
        "CashReason",
        str,
        help="Reason for the cash service (mandatory, max 160 chars)",
        meta=dict(category="COD", configurable=True, service_level=False, compatible_services=_BOTH),
    )

    gls_hazardous_goods_service = lib.OptionEnum(
        "service_hazardousgoods",
        bool,
        help="Hazardous goods (per unit)",
        meta=dict(category="DANGEROUS_GOOD", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_hazardous_goods_haz_no = lib.OptionEnum(
        "GLSHazNo",
        str,
        help="GLS hazardous-goods identifier (max 8 alphanumeric)",
        meta=dict(category="DANGEROUS_GOOD", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_hazardous_goods_weight = lib.OptionEnum(
        "HazardousGoodsWeight",
        float,
        help="Weight of the hazardous-goods item (kg, > 0)",
        meta=dict(category="DANGEROUS_GOOD", configurable=True, service_level=False, compatible_services=_BOTH),
    )

    gls_ex_works_service = lib.OptionEnum(
        "service_exworks",
        bool,
        help="ExWorks service (per unit)",
        meta=dict(configurable=True, service_level=True, compatible_services=_BOTH),
    )

    gls_limited_quantity = lib.OptionEnum(
        "service_limitedquantities",
        bool,
        help="Limited-quantity dangerous goods (per unit)",
        meta=dict(category="DANGEROUS_GOOD", configurable=True, service_level=True, compatible_services=_BOTH),
    )
    gls_limited_quantity_weight = lib.OptionEnum(
        "LimitedQuantityWeight",
        float,
        help="LQ weight (kg, > 0)",
        meta=dict(category="DANGEROUS_GOOD", configurable=True, service_level=False, compatible_services=_BOTH),
    )

    # --- Pickup / sporadic collection (used only by pickup/create.py) ---

    gls_pickup_product = lib.OptionEnum(
        "PickupProduct",
        str,
        help="Sporadic-pickup product (PARCEL / EXPRESS / FREIGHT / PHARMA / PHARMAPLUS)",
        meta=dict(category="PICKUP", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_contains_haz_goods = lib.OptionEnum(
        "ContainsHazGoods",
        bool,
        help="Sporadic-pickup contains hazardous goods",
        meta=dict(category="PICKUP", configurable=True, service_level=False, compatible_services=_BOTH),
    )

    # --- Per-shipment override for the connection-level Contact-ID ---

    gls_contact_id = lib.OptionEnum(
        "ContactID",
        str,
        help="Override the connection-level Contact-ID for this shipment",
        meta=dict(category="GENERAL", configurable=True, service_level=False, compatible_services=_BOTH),
    )

    # --- karrio standard option mappings ---

    insurance = lib.OptionEnum(
        "insurance",
        float,
        help="Insurance value — drives AddonLiability Amount",
        meta=dict(category="INSURANCE", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    cash_on_delivery = lib.OptionEnum(
        "cash_on_delivery",
        float,
        help="COD amount — drives the Cash service Amount when gls_cash_service is on",
        meta=dict(category="COD", configurable=True, service_level=False, compatible_services=_BOTH),
    )
    gls_paperless_trade = lib.OptionEnum(
        "paperless_trade",
        bool,
        help="Enable paperless trade — connector uploads invoice + submits customs after label creation",
        meta=dict(
            category="PAPERLESS",
            flow="post_upload",
            configurable=True,
            service_level=False,
            compatible_services=_BOTH,
        ),
    )
    saturday_delivery = gls_saturday_delivery
    dangerous_good = gls_limited_quantity
    paperless_trade = gls_paperless_trade
    doc_files = lib.OptionEnum(
        "doc_files", list[models.DocumentFile], meta=dict(category="PAPERLESS", compatible_services=_BOTH)
    )
    doc_references = lib.OptionEnum(
        "doc_references", list[models.DocumentDetails], meta=dict(category="PAPERLESS", compatible_services=_BOTH)
    )


EU_MEMBER_STATES = frozenset(
    {
        "AT",
        "BE",
        "BG",
        "HR",
        "CY",
        "CZ",
        "DK",
        "EE",
        "FI",
        "FR",
        "DE",
        "GR",
        "HU",
        "IE",
        "IT",
        "LV",
        "LT",
        "LU",
        "MT",
        "NL",
        "PL",
        "PT",
        "RO",
        "SK",
        "SI",
        "ES",
        "SE",
    }
)

CUSTOMS_NON_EU_NEIGHBOURS = frozenset({"GB", "CH", "NO", "LI"})


def is_international(shipper_country: str | None, recipient_country: str | None) -> bool:
    """True when the shipment crosses a border."""
    if not shipper_country or not recipient_country:
        return False
    return shipper_country.upper() != recipient_country.upper()


def is_customs_destination(country_code: str | None) -> bool:
    """True when the destination needs the Customs Consignment v3 second call."""
    if not country_code:
        return False
    cc = country_code.upper()
    return cc not in EU_MEMBER_STATES or cc in CUSTOMS_NON_EU_NEIGHBOURS


def normalize_commodity_code(hs_code: str | None) -> str | None:
    """Strip non-digits from an HS code. GLS validates ``^\\d{8}(\\d{2})?$``."""
    if not hs_code:
        return None
    digits = "".join(ch for ch in str(hs_code) if ch.isdigit())
    return digits or None


def split_phone(phone: str | None) -> tuple[str | None, str | None]:
    """Split an E.164 phone (``+CC NSN``) into ``(country_prefix, national_number)``.
    GLS Customs v3 expects the prefix WITH a leading ``+`` (example: ``"+49"``)."""
    if not phone:
        return None, None
    try:
        import phonenumbers as _pn

        p = _pn.parse(phone, None) if str(phone).startswith("+") else _pn.parse(f"+{phone}", None)
        return f"+{p.country_code}", str(p.national_number)
    except Exception:
        return None, str(phone)


def build_customs_consignment_request(
    payload,
    customs,
    shipper,
    recipient,
    incoterm_code: str | None,
    default_currency: str,
    customs_opts: dict | None = None,
):
    """Shape normalized customs info into a GLS Customs Consignment v3 request.

    ``parcelNumbers`` is filled by the proxy from the shipment response. See SPECS.md.
    """
    commodities = list(customs.commodities or [])
    if not commodities:
        return None

    weight_unit_code = WeightUnit.KG.value
    quantity_unit_code = "PCE"

    currency = customs.duty.currency or default_currency
    # Prefer the explicit ``customs_opts`` arg so this builder works with both
    # a ``ShipmentRequest`` payload (shipment_request call site, which still
    # reads from ``payload.customs.options``) and a ``DocumentUploadRequest``
    # payload (the document_upload_request call site, which passes the raw
    # options dict in directly because the request type has no
    # ``.customs`` attribute).
    customs_opts = customs_opts or ((payload.customs.options if getattr(payload, "customs", None) else None) or {})

    line_quantities = [float(c.quantity or 1) for c in commodities]
    line_weights = [float(c.weight or 0) * q for c, q in zip(commodities, line_quantities, strict=True)]
    line_values = [float(c.value_amount or 0) * q for c, q in zip(commodities, line_quantities, strict=True)]
    total_weight = sum(line_weights)
    total_value = sum(line_values)

    shipper_prefix, shipper_number = split_phone(shipper.phone_number)
    recipient_prefix, recipient_number = split_phone(recipient.phone_number)

    return gls_customs.CustomsConsignmentRequestType(
        glsIncotermCode=incoterm_code,
        customerReference=payload.reference,
        totalGrossWeight=gls_customs.TotalGrossWeightType(amount=total_weight or None, unit=weight_unit_code),
        exporter=gls_customs.ExporterType(
            address=gls_customs.AddressType(
                name1=shipper.company_name or shipper.person_name,
                name2=shipper.person_name if shipper.company_name else None,
                street1=shipper.address_line1,
                houseNumber=shipper.street_number,
                postcode=shipper.postal_code,
                city1=shipper.city,
                stateOrRegion=shipper.state_code,
                countryCode=shipper.country_code,
            ),
            contactPerson=gls_customs.ContactPersonType(
                name=shipper.person_name,
                emailAddress=shipper.email,
                phoneCountryPrefix=shipper_prefix,
                phoneNumber=shipper_number,
            ),
            eoriNumber=customs_opts.get("shipper_eori") or getattr(shipper, "eori_number", None),
            taxId=shipper.tax_id,
            isCommercial=True,
        ),
        importer=gls_customs.ImporterType(
            address=gls_customs.AddressType(
                name1=recipient.company_name or recipient.person_name,
                name2=recipient.person_name if recipient.company_name else None,
                street1=recipient.address_line1,
                houseNumber=recipient.street_number,
                postcode=recipient.postal_code,
                city1=recipient.city,
                stateOrRegion=recipient.state_code,
                countryCode=recipient.country_code,
            ),
            contactPerson=gls_customs.ContactPersonType(
                name=recipient.person_name,
                emailAddress=recipient.email,
                phoneCountryPrefix=recipient_prefix,
                phoneNumber=recipient_number,
            ),
            eoriNumber=customs_opts.get("recipient_eori") or getattr(recipient, "eori_number", None),
            taxId=recipient.tax_id,
            isCommercial=bool(recipient.company_name),
        ),
        invoice=gls_customs.InvoiceType(
            invoiceNumber=customs.invoice or payload.reference or "",
            invoiceDate=lib.fdate(customs.invoice_date) or datetime.date.today().isoformat(),
            totalGoodsValue=gls_customs.ValueType(amount=total_value or None, currency=currency),
        ),
        lineItems=[
            gls_customs.LineItemType(
                # Line-level totals (per-unit × quantity) so the API's
                # `sum(lineItems[*].grossWeight) == totalGrossWeight` and
                # `sum(lineItems[*].valueInInvoiceCurrency) == invoice.totalGoodsValue.amount`
                # consistency checks pass.
                quantity=gls_customs.TotalGrossWeightType(amount=q, unit=quantity_unit_code),
                # statisticalQuantity is a plain number per the v3 schema; the unit
                # is implied by the commodityCode (e.g. NAR for textiles).
                statisticalQuantity=q or None,
                commodityCode=normalize_commodity_code(c.hs_code),
                goodsDescription=c.description or c.title,
                countryOfOrigin=c.origin_country or shipper.country_code,
                valueInInvoiceCurrency=line_values[i] or None,
                grossWeight=gls_customs.TotalGrossWeightType(amount=line_weights[i] or None, unit=weight_unit_code),
                netWeight=gls_customs.TotalGrossWeightType(amount=line_weights[i] or None, unit=weight_unit_code),
            )
            for i, (c, q) in enumerate(zip(commodities, line_quantities, strict=True))
        ],
    )


# Generic flag services on ``Shipment.Service[]``. See SPECS.md.
SHIPMENT_FLAG_OPTIONS = (
    "gls_saturday_delivery",
    "gls_flex_delivery",
    "gls_addressee_only",
    "gls_signature_service",
    "gls_guaranteed24",
    "gls_t24",
    "gls_t48",
    "gls_tyre",
    "gls_private_delivery",
    "gls_inbound_logistics",
    "gls_document_return",
    "gls_complete_delivery_consignment",
)

TIME_DEFINITE_SERVICES = frozenset(
    {
        "service_0800",
        "service_0900",
        "service_1000",
        "service_1200",
        "service_1300",
        "service_saturday_0900",
        "service_saturday_1000",
        "service_saturday_1200",
    }
)


def time_definite_service_name(value) -> str:
    """Resolve the GLS time-definite ``ServiceName``.

    Unrecognised values fall back to ``service_1200``.
    """
    return value if isinstance(value, str) and value in TIME_DEFINITE_SERVICES else "service_1200"


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """Apply default values to the given options."""
    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """GLS Group tracking status mapping - based on ecitrackandtrace.yaml ParcelDTO.status enum."""

    pending = ["PLANNEDPICKUP", "INPICKUP", "PREADVICE"]
    in_transit = ["INTRANSIT", "INWAREHOUSE"]
    out_for_delivery = ["INDELIVERY"]
    delivered = ["DELIVERED", "DELIVEREDPS", "FINAL"]
    delivery_failed = ["NOTPICKEDUP", "NOTDELIVERED"]
    cancelled = ["CANCELED"]
    ready_for_pickup = ["DELIVEREDPS"]


class UploadDocumentType(lib.Enum):
    """Karrio document types → GLS ``documentType`` enum. See SPECS.md."""

    gls_commercial_invoice = "COMMERCIAL_INVOICE"
    gls_multiple_invoices = "MULTIPLE_INVOICES"
    gls_proof_of_preference = "PROOF_OF_PREFERENCE"
    gls_packing_list = "PACKING_LIST"
    gls_export_declaration = "EXPORT_DECLARATION"
    gls_t_paper = "T_PAPER"
    gls_customs_receipt = "CUSTOMS_RECEIPT"
    gls_charge_back_import_cust_invoice = "CHARGE_BACK_IMPORT_CUST_INVOICE"
    gls_import_entry_advice = "IMPORT_ENTRY_ADVICE"

    """Karrio standard unified document type mapping"""
    commercial_invoice = gls_commercial_invoice
    certificate_of_origin = gls_proof_of_preference
    pro_forma_invoice = gls_commercial_invoice
    packing_list = gls_packing_list
    other = gls_commercial_invoice


class Incoterm(lib.StrEnum):
    """karrio Incoterm → GLS 2-digit ``glsIncotermCode``. See SPECS.md."""

    DDP = "10"
    DAP = "20"
    DDU = "20"
    EXW = "20"


class WeightUnit(lib.StrEnum):
    """GLS wire weight-unit code (Customs Consignment v3)."""

    KG = "KGM"


class DimensionUnit(lib.StrEnum):
    """Dimension unit mapping"""

    CM = "cm"
    IN = "in"


def load_services_from_csv() -> list:
    """
    Load service definitions from CSV file.
    CSV format: service_code,service_name,zone_label,country_codes,min_weight,max_weight,max_length,max_width,max_height,rate,currency,transit_days,domicile,international
    """
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"

    if not csv_path.exists():
        return [
            models.ServiceLevel(
                service_name="GLS Parcel",
                service_code="gls_parcel",
                currency="EUR",
                domicile=True,
                zones=[models.ServiceZone(rate=0.0)],
            )
        ]

    services_dict: dict[str, dict] = {}

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            service_name = row["service_name"]
            karrio_service_code = ShippingService.map(service_code).name_or_key

            row_min_weight = float(row["min_weight"]) if row.get("min_weight") else None
            row_max_weight = float(row["max_weight"]) if row.get("max_weight") else None

            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": service_name,
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "EUR"),
                    "min_weight": row_min_weight,
                    "max_weight": row_max_weight,
                    "max_length": (float(row["max_length"]) if row.get("max_length") else None),
                    "max_width": (float(row["max_width"]) if row.get("max_width") else None),
                    "max_height": (float(row["max_height"]) if row.get("max_height") else None),
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": row.get("domicile", "").lower() == "true",
                    "international": (True if row.get("international", "").lower() == "true" else None),
                    "zones": [],
                }
            else:
                current = services_dict[karrio_service_code]
                if row_min_weight is not None and (
                    current["min_weight"] is None or row_min_weight < current["min_weight"]
                ):
                    current["min_weight"] = row_min_weight
                if row_max_weight is not None and (
                    current["max_weight"] is None or row_max_weight > current["max_weight"]
                ):
                    current["max_weight"] = row_max_weight
                if row.get("domicile", "").lower() == "true":
                    current["domicile"] = True
                if row.get("international", "").lower() == "true":
                    current["international"] = True

            country_codes = [c.strip() for c in row.get("country_codes", "").split(",") if c.strip()]

            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=row_min_weight,
                max_weight=row_max_weight,
                transit_days=(int(row["transit_days"].split("-")[0]) if row.get("transit_days") else None),
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    return [models.ServiceLevel(**service_data) for service_data in services_dict.values()]


DEFAULT_SERVICES = load_services_from_csv()
