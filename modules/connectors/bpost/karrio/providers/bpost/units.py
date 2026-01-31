import csv
import pathlib
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


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


class LabelType(lib.Enum):
    PDF_A4 = ("A4", "application/vnd.bpost.shm-label-pdf-v3+XML")
    PDF_A6 = ("A6", "application/vnd.bpost.shm-label-pdf-v3+XML")
    PNG_A4 = ("A4", "application/vnd.bpost.shm-label-image-v3+XML")
    PNG_A6 = ("A6", "application/vnd.bpost.shm-label-image-v3+XML")

    """ Unified Label type mapping """
    PDF = PDF_A4
    ZPL = PDF_A4
    PNG = PNG_A4


class CustomsContentType(lib.Enum):
    documents = "DOCUMENTS"
    gift = "GIFT"
    sample = "SAMPLE"
    returned = "RETURNED"
    goods = "GOODS"
    other = "OTHER"

    """ Unified Label type mapping """
    merchandise = goods
    return_merchandise = returned


class ConnectionConfig(lib.Enum):
    cost_center = lib.OptionEnum("cost_center")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    lang = lib.OptionEnum("lang", lib.units.create_enum("Lang", ["FR", "EN"]))


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    # fmt: off
    # nationalBox > atHome
    bpack_24h_pro = "bpack 24h Pro"
    bpack_24h_business = "bpack 24h business"
    bpack_bus = "bpack Bus"
    bpack_pallet = "bpack Pallet"
    bpack_easy_retour = "bpack Easy Retour"
    bpack_xl = "bpack XL"

    # nationalBox > atBpost
    bpack_bpost = "bpack@bpost"

    # nationalBox > at24-7
    bpack_24_7 = "bpack 24/7"

    # internationalBox > international
    bpack_world_business = "bpack World Business"
    bpack_world_express_pro = "bpack World Express Pro"
    bpack_europe_business = "bpack Europe Business"
    bpack_world_easy_return = "bpack World Easy Return"

    # internationalBox > atIntPugo
    bpack_bpost_international = "bpack@bpost international"

    # internationalBox > atIntlParcelDepot
    bpack_24_7_international = "bpack 24/7 international"
    # fmt: on

    @classmethod
    def method(cls, svc: str, is_international: bool) -> str:
        _methods = dict(
            atHome=[
                cls.bpack_24h_pro.value,  # type: ignore
                cls.bpack_24h_business.value,  # type: ignore
                cls.bpack_bus.value,  # type: ignore
                cls.bpack_pallet.value,  # type: ignore
                cls.bpack_easy_retour.value,  # type: ignore
                cls.bpack_xl.value,  # type: ignore
            ],
            atBpost=[
                cls.bpack_bpost.value,  # type: ignore
            ],
            at24_7=[
                cls.bpack_24_7.value,  # type: ignore
            ],
            bpostOnAppointment=[],
            international=[
                cls.bpack_world_business.value,  # type: ignore
                cls.bpack_world_express_pro.value,  # type: ignore
                cls.bpack_europe_business.value,  # type: ignore
                cls.bpack_world_easy_return.value,  # type: ignore
            ],
            atIntlHome=[],
            atIntlPugo=[
                cls.bpack_bpost_international.value,  # type: ignore
            ],
            atIntlParcelDepot=[
                cls.bpack_24_7_international.value,  # type: ignore
            ],
        )
        _method = next(
            (method for method, services in _methods.items() if svc in services),
            None,
        )

        if _method is None and is_international:
            return "atIntlHome"

        if _method is None and not is_international:
            return "atHome"

        return _method


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    # fmt: off
    bpost_info_distributed = lib.OptionEnum("infoDistributed", meta=dict(category="NOTIFICATION"))
    bpost_info_next_day = lib.OptionEnum("infoNextDay", meta=dict(category="NOTIFICATION"))
    bpost_info_reminder = lib.OptionEnum("infoReminder", meta=dict(category="NOTIFICATION"))
    bpost_keep_me_informed = lib.OptionEnum("keepMeInformed", meta=dict(category="NOTIFICATION"))
    bpost_automatic_second_presentation = lib.OptionEnum("automaticSecondPresentation", bool, meta=dict(category="DELIVERY_OPTIONS"))
    bpost_fragile = lib.OptionEnum("fragile", bool)
    bpost_insured = lib.OptionEnum("insured", meta=dict(category="INSURANCE"))
    bpost_signed = lib.OptionEnum("signed", bool, meta=dict(category="SIGNATURE"))
    bpost_time_slot_delivery = lib.OptionEnum("timeSlotDelivery", bool, meta=dict(category="DELIVERY_OPTIONS"))
    bpost_saturday_delivery = lib.OptionEnum("saturdayDelivery", bool, meta=dict(category="DELIVERY_OPTIONS"))
    bpost_sunday_delivery = lib.OptionEnum("sundayDelivery", bool, meta=dict(category="DELIVERY_OPTIONS"))
    bpost_same_day_delivery = lib.OptionEnum("sameDayDelivery", bool, meta=dict(category="DELIVERY_OPTIONS"))
    bpost_cod = lib.OptionEnum("cod", lib.to_money, meta=dict(category="COD"))
    bpost_preferred_delivery_window = lib.OptionEnum("preferredDeliveryWindow", meta=dict(category="DELIVERY_OPTIONS"))
    bpost_full_service = lib.OptionEnum("fullService", bool)
    bpost_door_step_plus_service = lib.OptionEnum("doorStepPlusService", meta=dict(category="DELIVERY_OPTIONS"))
    bpost_ultra_late_in_evening_delivery = lib.OptionEnum("ultraLateInEveningDelivery", bool, meta=dict(category="DELIVERY_OPTIONS"))
    # fmt: on

    """ Custom options """

    bpost_pugo_id = lib.OptionEnum("pugoId", meta=dict(category="PUDO"))
    bpost_pugo_name = lib.OptionEnum("pugoName", meta=dict(category="PUDO"))
    bpost_pugo_address = lib.OptionEnum("pugoAddress", lib.to_dict, meta=dict(category="PUDO"))
    bpost_parcels_depot_id = lib.OptionEnum("parcelsDepotId", meta=dict(category="PUDO"))
    bpost_parcels_depot_name = lib.OptionEnum("parcelsDepotName", meta=dict(category="PUDO"))
    bpost_parcels_depot_address = lib.OptionEnum("parcelsDepotAddress", lib.to_dict, meta=dict(category="PUDO"))
    bpost_parcel_return_instructions = lib.OptionEnum("parcelReturnInstructions", meta=dict(category="RETURN"))

    """ Unified Option type mapping """
    insurance = bpost_insured
    cash_on_delivery = bpost_cod
    signature_confirmation = bpost_signed
    saturday_delivery = bpost_saturday_delivery


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    if (
        "bpost_pugo_address" in options or "bpost_parcels_depot_address" in options
    ) and "hold_at_location_address" not in options:
        options.update(
            dict(
                hold_at_location=True,
                hold_at_location_address=(
                    options.get("bpost_pugo_address")
                    or options.get("bpost_parcels_depot_address")
                ),
            )
        )

    def items_filter(key: str) -> bool:
        return key in ShippingOption and "pugo" not in key and "parcels" not in key and key not in ["bpost_parcel_return_instructions"]  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


class TrackingStatus(lib.Enum):
    on_hold = [
        "B00",
        "B01",
        "B02",
        "C00",
        "I03",
        "I10",
        "I11",
        "I12",
        "I18",
        "I19",
        "I58",
        "I61",
        "I66",
        "I67",
        "I68",
        "I72",
        "I88",
        "L00",
    ]
    delivered = ["U00", "U01", "U02", "U03", "U04", "U05", "U06", "U07", "U08"]
    in_transit = ["B04", "N14", "R00", "R01", "R02", "R03", "R04", "R05", "T00"]
    delivery_failed = [
        "B03",
        "B04",
        "B05",
        "B06",
        "B07",
        "B08",
        "B09",
        "B10",
        "B11",
        "B12",
        "B13",
        "B18",
        "B23",
        "B24",
        "B28",
        "R11",
        "R12",
        "T03",
        "S00",
    ]
    delivery_delayed = [
        "N01",
        "N02",
        "N03",
        "N04",
        "N05",
        "N06",
        "N07",
        "N08",
        "N10",
        "N11",
        "N12",
        "N13",
        "N16",
        "N28",
        "N32",
        "N91",
        "N92",
        "N93",
        "N94",
        "N95",
        "N96",
        "P00",
    ]
    ready_for_pickup = ["N74", "R13"]


class TrackingIncidentReason(lib.Enum):
    """Maps Bpost exception codes to normalized TrackingIncidentReason."""
    carrier_damaged_parcel = ["B05", "B08"]
    consignee_refused = ["B03", "B23"]
    consignee_not_home = ["B04", "N01", "N02"]
    consignee_business_closed = ["N03"]
    consignee_incorrect_address = ["B06", "B07", "B09", "B10"]
    customs_delay = ["B00", "B01", "B02"]
    delivery_exception_hold = ["B11", "B12", "B13", "B18", "B24", "B28"]
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
                service_name="Bpost Standard Service",
                service_code="bpost_standard_service",
                currency="EUR",
                domicile=True,
                zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
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
