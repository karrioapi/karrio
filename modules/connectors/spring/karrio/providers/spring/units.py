import csv
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class ConnectionConfig(lib.Enum):
    """Carrier connection configuration options."""

    label_format = lib.OptionEnum("label_format", str, "PDF")


class LabelFormat(lib.StrEnum):
    """Spring label formats."""

    PDF = "PDF"
    PNG = "PNG"
    ZPL300 = "ZPL300"  # ZPL 300 dpi
    ZPL200 = "ZPL200"  # ZPL 203 dpi
    ZPL = "ZPL"  # alias for ZPL300
    EPL = "EPL"  # EPL 203 dpi


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class CustomsContentType(lib.StrEnum):
    """Spring customs declaration types."""

    sale_of_goods = "SaleOfGoods"
    documents = "Documents"
    gift = "Gift"
    returned_goods = "ReturnedGoods"
    commercial_sample = "CommercialSample"


class CustomsDuty(lib.StrEnum):
    """Spring customs duty types."""

    DDU = "DDU"  # Delivered Duty Unpaid (default)
    DDP = "DDP"  # Delivered Duty Paid (Spring Clear)


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    # Routed services (auto-select best carrier based on destination/weight)
    spring_tracked = "TRCK"
    spring_signature = "SIGN"
    spring_untracked = "UNTR"
    spring_collect = "CLLCT"

    # Express and special services
    spring_express = "EXPR"
    spring_import = "IMPRT"
    spring_back_returns = "BACK"
    spring_back_tracked = "BACKT"
    spring_no_label = "NOLABEL"

    # PostNL Parcel services
    spring_postnl_parcel_eu = "PPLEU"
    spring_postnl_parcel_benelux = "PPND"
    spring_postnl_parcel_benelux_sign = "PPNDS"
    spring_postnl_parcel_benelux_no_neighbor = "PPHD"
    spring_postnl_parcel_benelux_sign_no_neighbor = "PPHDS"
    spring_postnl_parcel_benelux_upu = "PPLUP"
    spring_postnl_parcel_globalpack_ems = "PPLGE"
    spring_postnl_parcel_globalpack_upu = "PPLGU"
    spring_postnl_parcel_epg = "PPLEP"
    spring_postnl_parcel_epg_noneu = "PPNEU"
    spring_postnl_lightweight_china = "PPLLW"
    spring_postnl_collect_service = "PPLCS"

    # PostNL Packet services (< 2kg)
    spring_postnl_packet_tracked = "PPTT"
    spring_postnl_packet_registered = "PPTR"
    spring_postnl_packet_non_tracked = "PPNT"
    spring_postnl_packet_boxable_bag_trace = "PPBBT"
    spring_postnl_packet_bag_trace = "PPBT"
    spring_postnl_packet_boxable_tracked = "PPBTT"
    spring_postnl_packet_boxable_non_tracked = "PPBNT"

    # Royal Mail services
    spring_royal_mail_tracked_24 = "RM24"
    spring_royal_mail_tracked_24_sign = "RM24S"
    spring_royal_mail_tracked_48 = "RM48"
    spring_royal_mail_tracked_48_2 = "RM482"
    spring_royal_mail_tracked_48_sign = "RM48S"

    # Sending services (Spain/Portugal)
    spring_sending_mainland = "SEND"
    spring_sending_islands = "SEND2"

    # Italian Post services
    spring_italian_post_crono = "ITCR"
    spring_italian_post_crono_express = "ITCRX"

    # German services
    spring_dpd_de = "DPDDE"
    spring_hermes_sign = "HEHDS"
    spring_hermes_collect = "HEDCS"

    # French services
    spring_colis_prive = "CPHD"
    spring_colis_prive_sign = "CPHDS"

    # Spring Commercial services
    spring_com_standard = "SCST"
    spring_com_standard_sign = "SCSTS"
    spring_com_express = "SCEX"
    spring_com_express_sign = "SCEXS"

    # USA services
    spring_usa_parcel_ground = "UPGR"
    spring_usa_parcel_ground_sign = "UPGRS"
    spring_usa_parcel_express = "UPEX"
    spring_usa_parcel_express_sign = "UPEXS"
    spring_usa_parcel_max = "UPMA"
    spring_usa_parcel_max_sign = "UPMAS"
    spring_usa_parcel_ground_dg = "UPDG"
    spring_usa_parcel_ground_dg_sign = "UDGS"
    spring_usa_parcel_plus_ground_dg = "UPPDG"
    spring_usa_parcel_plus_ground_dg_sign = "UPDGS"

    # Other carrier services
    spring_packeta = "PACHD"
    spring_mailalliance_boxable = "MABNT"
    spring_austrian_post = "ATEHD"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # Spring-specific options
    spring_customs_duty = lib.OptionEnum("CustomsDuty")
    spring_declaration_type = lib.OptionEnum("DeclarationType")
    spring_dangerous_goods = lib.OptionEnum("DangerousGoods", bool)
    spring_shipping_value = lib.OptionEnum("ShippingValue", float)
    spring_display_id = lib.OptionEnum("DisplayId")
    spring_invoice_number = lib.OptionEnum("InvoiceNumber")
    spring_order_reference = lib.OptionEnum("OrderReference")
    spring_order_date = lib.OptionEnum("OrderDate")

    # Consignor tax/customs identifiers
    spring_consignor_vat = lib.OptionEnum("ConsignorVat")
    spring_consignor_eori = lib.OptionEnum("ConsignorEori")
    spring_consignor_nl_vat = lib.OptionEnum("ConsignorNlVat")
    spring_consignor_eu_eori = lib.OptionEnum("ConsignorEuEori")
    spring_consignor_gb_eori = lib.OptionEnum("ConsignorGbEori")
    spring_consignor_ioss = lib.OptionEnum("ConsignorIoss")
    spring_consignor_local_tax_number = lib.OptionEnum("ConsignorLocalTaxNumber")

    # Return label options (BACK service)
    spring_export_carrier_name = lib.OptionEnum("ExportCarrierName")
    spring_export_awb = lib.OptionEnum("ExportAwb")

    # Collect service option
    spring_pudo_location_id = lib.OptionEnum("PudoLocationId")

    """ Unified Option type mapping """
    dangerous_goods = spring_dangerous_goods
    shipment_date = spring_order_date


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    """
    Spring tracking event codes mapped to Karrio unified statuses.
    Based on Spring XBS API documentation section 3.
    """

    pending = [
        "0",  # PARCEL CREATED
        "12",  # PREPARATION PROCESS
    ]
    on_hold = [
        "40",  # IN CUSTOMS
        "41",  # CUSTOMS EXCEPTION
        "31",  # DELIVERY EXCEPTION – ACTION REQUIRED
    ]
    delivered = [
        "100",  # DELIVERED
        "101",  # DELIVERED TO DESTINATION COUNTRY
    ]
    in_transit = [
        "15",  # COLLECTION TRANSPORT
        "18",  # COLLECTION
        "19",  # PROCESSING DEPOT
        "20",  # ACCEPTED
        "21",  # INTERNATIONAL TRANSPORT
        "22",  # CROSSDOCK
        "25",  # END OF TRACKING UPDATES
        "93",  # AT LOCAL DEPOT LMC
        "2101",  # IN TRANSIT - EXPORTED
        "2102",  # ITEM RELEASED FROM CUSTOMS
        "2103",  # IN TRANSIT - IMPORTED
        "9101",  # AT TRANSFER DEPOT LMC
        "9102",  # IN TRANSIT
        "9999",  # INFORMATION
    ]
    delivery_failed = [
        "91",  # DELIVERY ATTEMPTED
        "111",  # LOST OR DESTROYED
        "1001",  # ITEM INCOMPLETE DATA
        "4106",  # CONSIGNMENT CANCELLED
    ]
    delivery_delayed = [
        "9302",  # DELIVERY EXCEPTION - DELAYED
    ]
    out_for_delivery = [
        "9301",  # OUT FOR DELIVERY
    ]
    ready_for_pickup = [
        "92",  # DELIVERY AWAITING COLLECTION
    ]
    return_to_sender = [
        "124",  # RETURN IN TRANSIT
        "125",  # RETURN RECEIVED
        "12406",  # RETURN DELIVERED BY CARRIER
        "12501",  # RETURN RECEIVED - REFUSED
        "12502",  # RETURN RECEIVED - UNDELIVERABLE
        "12503",  # RETURN RECEIVED - DAMAGED
        "12504",  # RETURN RECEIVED - NOT COLLECTED
        "12505",  # RETURN RECEIVED - ACCORDING TO AGREEMENT
        "12506",  # RETURN RECEIVED - DESTROYED
    ]


class TrackingIncidentReason(lib.Enum):
    """Maps Spring exception codes to normalized incident reasons.

    Maps carrier-specific exception/status codes to standardized
    incident reasons for tracking events. The reason field helps
    identify why a delivery exception occurred.
    """

    # Carrier-caused issues
    carrier_parcel_lost = ["111"]  # LOST OR DESTROYED
    carrier_damaged_parcel = ["12503"]  # RETURN RECEIVED - DAMAGED

    # Consignee-caused issues
    consignee_refused = ["12501"]  # RETURN RECEIVED - REFUSED
    consignee_not_available = [
        "91",  # DELIVERY ATTEMPTED
        "12504",  # RETURN RECEIVED - NOT COLLECTED
    ]
    consignee_incorrect_address = ["12502"]  # RETURN RECEIVED - UNDELIVERABLE

    # Customs-related issues
    customs_delay = [
        "40",  # IN CUSTOMS
        "41",  # CUSTOMS EXCEPTION
    ]

    # Delivery exceptions
    delivery_exception_delayed = ["9302"]  # DELIVERY EXCEPTION - DELAYED
    delivery_exception_action_required = ["31"]  # DELIVERY EXCEPTION – ACTION REQUIRED
    delivery_exception_cancelled = ["4106"]  # CONSIGNMENT CANCELLED
    delivery_exception_incomplete_data = ["1001"]  # ITEM INCOMPLETE DATA

    # Return reasons
    return_by_agreement = ["12505"]  # RETURN RECEIVED - ACCORDING TO AGREEMENT
    return_destroyed = ["12506"]  # RETURN RECEIVED - DESTROYED

    # Unknown
    unknown = []


def load_services_from_csv() -> list:
    """
    Load service definitions from CSV file.
    CSV format: service_code,service_name,zone_label,country_codes,min_weight,max_weight,max_length,max_width,max_height,rate,currency,transit_days,domicile,international
    """
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"

    if not csv_path.exists():
        # Fallback to simple default if CSV doesn't exist
        return [
            models.ServiceLevel(
                service_name="Spring Tracked",
                service_code="spring_tracked",
                currency="EUR",
                international=True,
                zones=[models.ServiceZone(rate=0.0)],
            )
        ]

    # Group zones by service
    services_dict: dict[str, dict] = {}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            service_name = row["service_name"]

            # Map carrier service code to karrio service code
            karrio_service_code = ShippingService.map(service_code).name_or_key

            # Initialize service if not exists
            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": service_name,
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "EUR"),
                    "min_weight": (
                        float(row["min_weight"]) if row.get("min_weight") else None
                    ),
                    "max_weight": (
                        float(row["max_weight"]) if row.get("max_weight") else None
                    ),
                    "max_length": (
                        float(row["max_length"]) if row.get("max_length") else None
                    ),
                    "max_width": (
                        float(row["max_width"]) if row.get("max_width") else None
                    ),
                    "max_height": (
                        float(row["max_height"]) if row.get("max_height") else None
                    ),
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": (row.get("domicile") or "").lower() == "true",
                    "international": (
                        True if (row.get("international") or "").lower() == "true" else None
                    ),
                    "zones": [],
                }

            # Parse country codes
            country_codes = [
                c.strip() for c in row.get("country_codes", "").split(",") if c.strip()
            ]

            # Create zone
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                transit_days=(
                    int(row["transit_days"]) if row.get("transit_days") else None
                ),
                country_codes=country_codes if country_codes else None,
            )

            services_dict[karrio_service_code]["zones"].append(zone)

    # Convert to ServiceLevel objects
    return [
        models.ServiceLevel(**service_data) for service_data in services_dict.values()
    ]


DEFAULT_SERVICES = load_services_from_csv()
