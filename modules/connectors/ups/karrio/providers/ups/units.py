import karrio.lib as lib
import karrio.core.units as units
import karrio.core.utils as utils
import typing

PRESET_DEFAULTS = dict(
    dimension_unit="IN",
    weight_unit="LB",
)
COUNTRY_PREFERED_UNITS = dict(
    US=(units.WeightUnit.LB, units.DimensionUnit.IN),
)


class PackagePresets(utils.Enum):
    ups_small_express_box = units.PackagePreset(
        **dict(weight=30.0, width=13.0, height=11.0, length=2.0), **PRESET_DEFAULTS
    )
    ups_medium_express_box = units.PackagePreset(
        **dict(weight=30.0, width=16.0, height=11.0, length=3.0), **PRESET_DEFAULTS
    )
    ups_large_express_box = units.PackagePreset(
        **dict(weight=30.0, width=18.0, height=13.0, length=3.0), **PRESET_DEFAULTS
    )
    ups_express_tube = units.PackagePreset(
        **dict(width=38.0, height=6.0, length=6.0), **PRESET_DEFAULTS
    )
    ups_express_pak = units.PackagePreset(
        **dict(width=16.0, height=11.75, length=1.5), **PRESET_DEFAULTS
    )
    ups_world_document_box = units.PackagePreset(
        **dict(width=17.5, height=12.5, length=3.0), **PRESET_DEFAULTS
    )


class LabelType(utils.Enum):
    PDF_6x4 = ("PNG", 6, 4)
    PDF_8x4 = ("PNG", 8, 4)
    ZPL_6x4 = ("ZPL", 6, 4)

    """ Unified Label type mapping """
    PDF = PDF_6x4
    ZPL = ZPL_6x4


class Incoterm(utils.StrEnum):
    CFR = "Cost and Freight"
    CIF = "Cost Insurance and Freight"
    CIP = "Carriage and Insurance Paid"
    CPT = "Carriage Paid To"
    DAF = "Delivered at Frontier"
    DDP = "Delivery Duty Paid"
    DDU = "Delivery Duty Unpaid"
    DEQ = "Delivered Ex Quay"
    DES = "Delivered Ex Ship"
    EXW = "Ex Works"
    FAS = "Free Alongside Ship"
    FCA = "Free Carrier"
    FOB = "Free On Board"


class CustomsContentType(utils.StrEnum):
    sale = "SALE"
    gift = "GIFT"
    sample = "SAMPLE"
    repair = "REPAIR"
    return_merchandise = "RETURN"
    inter_company_data = "INTERCOMPANYDATA"
    other = "Any other reason"

    """ Unified Content type mapping """
    documents = other
    merchandise = sale


class WeightUnit(utils.StrEnum):
    KG = "KGS"
    LB = "LBS"


class PackagingType(utils.StrEnum):
    ups_unknown = "00"
    ups_letter = "01"
    ups_customer_supplied_package = "02"
    ups_tube = "03"
    ups_pak = "04"
    ups_ups_express_box = "21"
    ups_ups_25_kg_box = "24"
    ups_ups_10_kg_box = "25"
    ups_pallet = "30"
    ups_small_express_box = "2a"
    ups_medium_express_box = "2b"
    ups_large_express_box = "2c"
    ups_flats = "56"
    ups_parcels = "57"
    ups_bpm = "58"
    ups_first_class = "59"
    ups_priority = "60"
    ups_machineables = "61"
    ups_irregulars = "62"
    ups_parcel_post = "63"
    ups_bpm_parcel = "64"
    ups_media_mail = "65"
    ups_bpm_flat = "66"
    ups_standard_flat = "67"

    """ unified Packaging type mapping  """
    envelope = ups_letter
    pak = ups_pak
    tube = ups_tube
    pallet = ups_pallet
    small_box = ups_small_express_box
    medium_box = ups_medium_express_box
    your_packaging = ups_customer_supplied_package


class ConnectionConfig(utils.Enum):
    cost_center = utils.OptionEnum("cost_center")
    merchant_id = utils.OptionEnum("merchant_id")
    enforce_zpl = utils.OptionEnum("enforce_zpl", bool)
    label_type = utils.OptionEnum("label_type", LabelType)
    shipping_options = utils.OptionEnum("shipping_options", list)
    shipping_services = utils.OptionEnum("shipping_services", list)


class ServiceCode(utils.StrEnum):
    ups_express = "07"
    ups_standard = "11"
    ups_worldwide_expedited = "08"
    ups_worldwide_express_plus = "54"
    ups_worldwide_saver = "65"

    ups_worldwide_express_freight = "96"
    ups_worldwide_express_freight_midday = "71"
    ups_worldwide_economy_ddu = "17"
    ups_worldwide_economy_ddp = "72"

    ups_2nd_day_air = "02"
    ups_2nd_day_air_am = "59"
    ups_3_day_select = "12"
    ups_ground = "03"
    ups_next_day_air = "01"
    ups_next_day_air_early = "14"
    ups_next_day_air_saver = "13"
    ups_access_point_economy = "70"

    """ Service type correspondence """

    ups_expedited_ca = ups_2nd_day_air
    ups_express_saver_ca = ups_next_day_air_saver
    ups_3_day_select_ca_us = ups_3_day_select
    ups_access_point_economy_ca = ups_access_point_economy
    ups_express_ca = ups_next_day_air
    ups_express_early_ca = ups_next_day_air_early
    ups_express_saver_intl_ca = ups_worldwide_saver
    ups_standard_ca = ups_standard
    ups_worldwide_expedited_ca = ups_worldwide_expedited
    ups_worldwide_express = ups_express
    ups_worldwide_express_ca = ups_express
    ups_worldwide_express_plus_ca = ups_worldwide_express_plus
    ups_express_early_ca_us = ups_worldwide_express_plus

    ups_access_point_economy_eu = ups_access_point_economy
    ups_expedited_eu = ups_worldwide_expedited
    ups_express_eu = ups_express
    ups_standard_eu = ups_standard
    ups_worldwide_express_plus_eu = ups_worldwide_express_plus
    ups_worldwide_saver_eu = ups_worldwide_saver

    ups_access_point_economy_mx = ups_access_point_economy
    ups_expedited_mx = ups_worldwide_expedited
    ups_express_mx = ups_express
    ups_standard_mx = ups_standard
    ups_worldwide_express_plus_mx = ups_worldwide_express_plus
    ups_worldwide_saver_mx = ups_worldwide_saver

    ups_access_point_economy_pl = ups_access_point_economy
    ups_today_dedicated_courrier_pl = "83"
    ups_today_express_pl = "85"
    ups_today_express_saver_pl = "86"
    ups_today_standard_pl = "82"
    ups_expedited_pl = ups_worldwide_expedited
    ups_express_pl = ups_express
    ups_express_plus_pl = ups_worldwide_express_plus
    ups_express_saver_pl = ups_worldwide_saver
    ups_standard_pl = ups_standard

    ups_2nd_day_air_pr = ups_2nd_day_air
    ups_ground_pr = ups_ground
    ups_next_day_air_pr = ups_next_day_air
    ups_next_day_air_early_pr = ups_next_day_air_early
    ups_worldwide_expedited_pr = ups_worldwide_expedited
    ups_worldwide_express_pr = ups_express
    ups_worldwide_express_plus_pr = ups_worldwide_express_plus
    ups_worldwide_saver_pr = ups_worldwide_saver

    ups_express_12_00_de = "74"


class ServiceZone(utils.Enum):
    ups_standard = ["11", "US"]
    ups_worldwide_express = ["07", "US"]
    ups_worldwide_expedited = ["08", "US"]
    ups_worldwide_express_plus = ["54", "US"]
    ups_worldwide_saver = ["65", "US"]
    ups_2nd_day_air = ["02", "US"]
    ups_2nd_day_air_am = ["59", "US"]
    ups_3_day_select = ["12", "US"]
    ups_ground = ["03", "US"]
    ups_next_day_air = ["01", "US"]
    ups_next_day_air_early = ["14", "US"]
    ups_next_day_air_saver = ["13", "US"]

    ups_expedited_ca = ["02", "CA"]
    ups_express_saver_ca = ["13", "CA"]
    ups_3_day_select_ca_us = ["12", "CA"]
    ups_access_point_economy_ca = ["70", "CA"]
    ups_express_ca = ["01", "CA"]
    ups_express_early_ca = ["14", "CA"]
    ups_express_saver_intl_ca = ["65", "CA"]
    ups_standard_ca = ["11", "CA"]
    ups_worldwide_expedited_ca = ["08", "CA"]
    ups_worldwide_express_ca = ["07", "CA"]
    ups_worldwide_express_plus_ca = ["54", "CA"]
    ups_express_early_ca_us = ["54", "CA"]

    ups_access_point_economy_eu = ["70", "EU"]
    ups_expedited_eu = ["08", "EU"]
    ups_express_eu = ["07", "EU"]
    ups_standard_eu = ["11", "EU"]
    ups_worldwide_express_plus_eu = ["54", "EU"]
    ups_worldwide_saver_eu = ["65", "EU"]

    ups_access_point_economy_mx = ["70", "MX"]
    ups_expedited_mx = ["08", "MX"]
    ups_express_mx = ["07", "MX"]
    ups_standard_mx = ["11", "MX"]
    ups_worldwide_express_plus_mx = ["54", "MX"]
    ups_worldwide_saver_mx = ["65", "MX"]

    ups_access_point_economy_pl = ["70", "PL"]
    ups_today_dedicated_courrier_pl = ["83", "PL"]
    ups_today_express_pl = ["85", "PL"]
    ups_today_express_saver_pl = ["86", "PL"]
    ups_today_standard_pl = ["82", "PL"]
    ups_expedited_pl = ["08", "PL"]
    ups_express_pl = ["07", "PL"]
    ups_express_plus_pl = ["54", "PL"]
    ups_express_saver_pl = ["65", "PL"]
    ups_standard_pl = ["11", "PL"]

    ups_2nd_day_air_pr = ["02", "PR"]
    ups_ground_pr = ["03", "PR"]
    ups_next_day_air_pr = ["01", "PR"]
    ups_next_day_air_early_pr = ["14", "PR"]
    ups_worldwide_expedited_pr = ["08", "PR"]
    ups_worldwide_express_pr = ["07", "PR"]
    ups_worldwide_express_plus_pr = ["54", "PR"]
    ups_worldwide_saver_pr = ["65", "PR"]

    ups_express_12_00_de = ["74", "DE"]

    @classmethod
    def find(cls, service_type, country_code):
        for service in cls:
            if service_type == service.value[0] and country_code == service.value[1]:
                return ShippingService.map(service.name)
        return ServiceCode.map(service_type)


class ShippingService(utils.StrEnum):
    ups_standard = "UPS Standard"
    ups_worldwide_express = "UPS Worldwide Express"
    ups_worldwide_expedited = "UPS Worldwide Expedited"
    ups_worldwide_express_plus = "UPS Worldwide Express Plus"
    ups_worldwide_saver = "UPS Worldwide Saver"
    ups_2nd_day_air = "UPS 2nd Day Air"
    ups_2nd_day_air_am = "UPS 2nd Day Air A.M."
    ups_3_day_select = "UPS 3 Day Select"
    ups_ground = "UPS Ground"
    ups_next_day_air = "UPS Next Day Air"
    ups_next_day_air_early = "UPS Next Day Air Early"
    ups_next_day_air_saver = "UPS Next Day Air Saver"

    ups_expedited_ca = "UPS Expedited CA"
    ups_express_saver_ca = "UPS Express Saver CA"
    ups_3_day_select_ca_us = "UPS 3 Day Select CA US"
    ups_access_point_economy_ca = "UPS Access Point Economy CA"
    ups_express_ca = "UPS Express CA"
    ups_express_early_ca = "UPS Express Early CA"
    ups_express_saver_intl_ca = "UPS Express Saver Intl CA"
    ups_standard_ca = "UPS Standard CA"
    ups_worldwide_expedited_ca = "UPS Worldwide Expedited CA"
    ups_worldwide_express_ca = "UPS Worldwide Express CA"
    ups_worldwide_express_plus_ca = "UPS Worldwide Express Plus CA"
    ups_express_early_ca_us = "UPS Express Early CA US"

    ups_access_point_economy_eu = "UPS Access Point Economy EU"
    ups_expedited_eu = "UPS Expedited EU"
    ups_express_eu = "UPS Express EU"
    ups_standard_eu = "UPS Standard EU"
    ups_worldwide_express_plus_eu = "UPS Worldwide Express Plus EU"
    ups_worldwide_saver_eu = "UPS Worldwide Saver EU"

    ups_access_point_economy_mx = "UPS Access Point Economy MX"
    ups_expedited_mx = "UPS Expedited MX"
    ups_express_mx = "UPS Express MX"
    ups_standard_mx = "UPS Standard MX"
    ups_worldwide_express_plus_mx = "UPS Worldwide Express Plus MX"
    ups_worldwide_saver_mx = "UPS Worldwide Saver MX"

    ups_access_point_economy_pl = "UPS Access Point Economy PL"
    ups_today_dedicated_courrier_pl = "UPS Today Dedicated Courrier PL"
    ups_today_express_pl = "UPS Today Express PL"
    ups_today_express_saver_pl = "UPS Today Express Saver PL"
    ups_today_standard_pl = "UPS Today Standard PL"
    ups_expedited_pl = "UPS Expedited PL"
    ups_express_pl = "UPS Express PL"
    ups_express_plus_pl = "UPS Express Plus PL"
    ups_express_saver_pl = "UPS Express Saver PL"
    ups_standard_pl = "UPS Standard PL"

    ups_2nd_day_air_pr = "UPS 2nd Day Air PR"
    ups_ground_pr = "UPS Ground PR"
    ups_next_day_air_pr = "UPS Next Day Air PR"
    ups_next_day_air_early_pr = "UPS Next Day Air Early PR"
    ups_worldwide_expedited_pr = "UPS Worldwide Expedited PR"
    ups_worldwide_express_pr = "UPS Worldwide Express PR"
    ups_worldwide_express_plus_pr = "UPS Worldwide Express Plus PR"
    ups_worldwide_saver_pr = "UPS Worldwide Saver PR"

    ups_express_12_00_de = "UPS Express 12:00 DE"

    ups_worldwide_express_freight = "UPS Worldwide Express Freight"
    ups_worldwide_express_freight_midday = "UPS Worldwide Express Freight Midday"
    ups_worldwide_economy_ddu = "UPS Worldwide Economy DDU"
    ups_worldwide_economy_ddp = "UPS Worldwide Economy DDP"


class ShippingOption(utils.Enum):
    # fmt: off
    ups_saturday_pickup_indicator = utils.OptionEnum("SaturdayPickupIndicator", bool)
    ups_saturday_delivery_indicator = utils.OptionEnum(
        "SaturdayDeliveryIndicator", bool
    )
    ups_sunday_delivery_indicator = utils.OptionEnum("SundayDeliveryIndicator", bool)
    ups_access_point_cod = utils.OptionEnum("AccessPointCOD", float)
    ups_deliver_to_addressee_only_indicator = utils.OptionEnum(
        "DeliverToAddresseeOnlyIndicator", bool
    )
    ups_direct_delivery_only_indicator = utils.OptionEnum(
        "DirectDeliveryOnlyIndicator", bool
    )
    ups_cod = utils.OptionEnum("COD", float)
    ups_return_of_document_indicator = utils.OptionEnum("ReturnOfDocumentIndicator", bool)
    ups_carbonneutral_indicator = utils.OptionEnum("UPScarbonneutralIndicator", bool)
    ups_certificate_of_origin_indicator = utils.OptionEnum(
        "CertificateOfOriginIndicator"
    )
    ups_shipper_export_declaration_indicator = utils.OptionEnum(
        "ShipperExportDeclarationIndicator", bool
    )
    ups_commercial_invoice_removal_indicator = utils.OptionEnum(
        "CommercialInvoiceRemovalIndicator", bool
    )
    ups_import_control = utils.OptionEnum("ImportControl", bool)
    ups_return_service = utils.OptionEnum("ReturnService", bool)
    ups_epra_indicator = utils.OptionEnum("EPRAIndicator", bool)
    ups_lift_gate_at_pickup_indicator = utils.OptionEnum(
        "LiftGateAtPickupIndicator", bool
    )
    ups_lift_gate_at_delivery_indicator = utils.OptionEnum(
        "LiftGateAtDeliveryIndicator", bool
    )
    ups_drop_off_at_ups_facility_indicator = utils.OptionEnum(
        "DropOffAtUPSFacilityIndicator", bool
    )
    ups_master_carton_indicator = utils.OptionEnum("MasterCartonIndicator", bool)
    ups_exchange_forward_indicator = utils.OptionEnum("ExchangeForwardIndicator", bool)
    ups_hold_for_pickup_indicator = utils.OptionEnum("HoldForPickupIndicator", bool)
    ups_dropoff_at_ups_facility_indicator = utils.OptionEnum(
        "DropoffAtUPSFacilityIndicator", bool
    )
    ups_lift_gate_for_pickup_indicator = utils.OptionEnum(
        "LiftGateForPickupIndicator", bool
    )
    ups_lift_gate_for_delivery_indicator = utils.OptionEnum(
        "LiftGateForDeliveryIndicator", bool
    )
    ups_sdl_shipment_indicator = utils.OptionEnum("SDLShipmentIndicator", bool)
    ups_item_disposal = utils.OptionEnum("ItemDisposal", bool)
    ups_available_services_option = utils.OptionEnum(
        "AvailableServicesOption",
        units.create_enum("AvailableServicesType", ["1", "2", "3"]),
    )
    ups_delivery_confirmation = utils.OptionEnum(
        "DeliveryConfirmation",
        units.create_enum("ConfirmationType", ["1", "2"]),
    )
    ups_delivery_confirmation_level = utils.OptionEnum(
        "DeliveryConfirmationLevel",
        units.create_enum("DeliveryConfirmationLevelType", ["P", "S"]),
    )
    ups_inside_delivery = utils.OptionEnum(
        "InsideDelivery", units.create_enum("InsideDeliveryType", ["01", "02", "03"])
    )

    ups_restricted_articles = utils.OptionEnum("RestrictedArticles", bool)
    ups_alcoholic_beverages_indicator = utils.OptionEnum("AlcoholicBeveragesIndicator", bool)
    ups_diagnostic_specimens_indicator = utils.OptionEnum("DiagnosticSpecimensIndicator", bool)
    ups_perishables_indicator = utils.OptionEnum("PerishablesIndicator", bool)
    ups_plants_indicator = utils.OptionEnum("PlantsIndicator", bool)
    ups_seeds_indicator = utils.OptionEnum("SeedsIndicator", bool)
    ups_special_exceptions_indicator = utils.OptionEnum("SpecialExceptionsIndicator", bool)
    ups_tobacco_indicator = utils.OptionEnum("TobaccoIndicator", bool)


    ups_negotiated_rates_indicator = utils.OptionEnum("NegotiatedRatesIndicator", bool)
    ups_frs_shipment_indicator = utils.OptionEnum("FRSShipmentIndicator", bool)
    ups_rate_chart_indicator = utils.OptionEnum("RateChartIndicator", bool)
    ups_user_level_discount_indicator = utils.OptionEnum("UserLevelDiscountIndicator", bool)
    ups_tpfc_negotiated_rates_indicator = utils.OptionEnum("TPFCNegotiatedRatesIndicator", bool)


    """ Custom option type """
    ups_access_point_pickup = utils.OptionEnum("01", bool)
    ups_access_point_delivery = utils.OptionEnum("02", bool)

    """ Unified Option type mapping """
    cash_on_delivery = ups_cod
    dangerous_good = ups_restricted_articles
    hold_at_location = ups_hold_for_pickup_indicator
    saturday_delivery = ups_saturday_delivery_indicator
    # fmt: on


class DeliveryConfirmationType(utils.StrEnum):
    signature_required = "1"  # DC-SR
    adult_signature_required = "2"  # DC-ASR


class DeliveryConfirmationLevel(utils.Enum):
    PACKAGE = "P"  # Package level
    SHIPMENT = "S"  # Shipment level

    @classmethod
    def get_level(cls, origin: str, destination: str) -> str:
        # US50 to US50/PR -> Package level
        if origin == "US" and destination in ["US", "PR"]:
            return cls.PACKAGE.value  # type: ignore
        # US50 to CA/VI/Intl -> Shipment level
        elif origin == "US" and destination in ["CA", "VI"]:
            return cls.SHIPMENT.value  # type: ignore
        elif origin == "US":  # Intl other than CA, PR, VI
            return cls.SHIPMENT.value  # type: ignore
        # CA to US50/PR/VI -> Shipment level
        elif origin == "CA" and destination in ["US", "PR", "VI"]:
            return cls.SHIPMENT.value  # type: ignore
        # CA to CA -> Package level
        elif origin == "CA" and destination == "CA":
            return cls.PACKAGE.value  # type: ignore
        # CA to Intl other than US50, PR, VI -> Shipment level
        elif origin == "CA":
            return cls.SHIPMENT.value  # type: ignore
        # PR to US50/PR -> Package level
        elif origin == "PR" and destination in ["US", "PR"]:
            return cls.PACKAGE.value  # type: ignore
        # PR to CA/VI -> Shipment level
        elif origin == "PR" and destination in ["CA", "VI"]:
            return cls.SHIPMENT.value  # type: ignore
        # PR to Intl other than US50, CA, VI -> Shipment level
        elif origin == "PR":
            return cls.SHIPMENT.value  # type: ignore
        # International-supported origin countries to any destination -> Shipment level
        return cls.SHIPMENT.value  # type: ignore


class DeliveryConfirmationAvailability(utils.Enum):
    # US50 origin
    US_DOMESTIC = ["US", "US", ["1", "2"], "1"]  # Both available, prefer SR
    US_PR = ["US", "PR", ["1", "2"], "1"]  # Both available, prefer SR
    US_CA = ["US", "CA", ["1", "2"], "1"]  # Both available, prefer SR
    US_VI = ["US", "VI", ["1", "2"], "1"]  # Both available, prefer SR
    US_INTL = ["US", "INTL", ["1", "2"], "1"]  # Both available, prefer SR

    # Canada origin
    CA_US = ["CA", "US", ["1", "2"], "1"]  # Both available, prefer SR
    CA_PR = ["CA", "PR", ["1", "2"], "1"]  # Both available, prefer SR
    CA_VI = ["CA", "VI", ["1", "2"], "1"]  # Both available, prefer SR
    CA_CA = ["CA", "CA", ["1", "2"], "2"]  # Both available, prefer ASR for domestic
    CA_INTL = ["CA", "INTL", ["1", "2"], "1"]  # Both available, prefer SR

    # Puerto Rico origin
    PR_US = ["PR", "US", ["1", "2"], "1"]  # Both available, prefer SR
    PR_PR = ["PR", "PR", ["1", "2"], "1"]  # Both available, prefer SR
    PR_CA = ["PR", "CA", ["1", "2"], "1"]  # Both available, prefer SR
    PR_VI = ["PR", "VI", ["1", "2"], "1"]  # Both available, prefer SR
    PR_INTL = ["PR", "INTL", ["1", "2"], "1"]  # Both available, prefer SR

    # International origin
    INTL_ALL = ["INTL", "ALL", ["1", "2"], "1"]  # Both available, prefer SR

    @classmethod
    def get_available_types(cls, origin: str, destination: str) -> typing.List[str]:
        for member in cls.__members__.values():
            if member.value[0] == origin and member.value[1] == destination:
                return member.value[2]
            elif member.value[0] == origin and member.value[1] == "ALL":
                return member.value[2]
            elif member.value[0] == "INTL" and origin not in ["US", "CA", "PR"]:
                return member.value[2]
        return []

    @classmethod
    def get_preferred_type(cls, origin: str, destination: str) -> str:
        for member in cls.__members__.values():
            if member.value[0] == origin and member.value[1] == destination:
                return member.value[3]
            elif member.value[0] == origin and member.value[1] == "ALL":
                return member.value[3]
            elif member.value[0] == "INTL" and origin not in ["US", "CA", "PR"]:
                return member.value[3]
        return "1"  # Default to signature required


def shipping_options_initializer(
    options: dict,
    package_options: units.Options = None,
    destination_country: str = None,
    origin_country: str = None,
) -> units.Options:
    """Apply default values to the given options."""
    _options = options.copy()
    _has_pickup_options = lib.identity(
        "hold_at_location" in _options
        or "ups_epra_indicator" in _options
        or "ups_access_point_pickup" in _options
        or "ups_hold_for_pickup_indicator" in _options
        or "ups_lift_gate_at_pickup_indicator" in _options
    )
    _has_delivery_options = lib.identity(
        "ups_access_point_delivery" in _options
        or "ups_lift_gate_at_delivery_indicator" in _options
        or "ups_drop_off_at_ups_facility_indicator" in _options
        or "ups_deliver_to_addressee_only_indicator" in _options
    )
    _has_signature_required = lib.identity(
        "signature_confirmation" in _options or "ups_delivery_confirmation" in _options
    )
    _has_dangerous_goods = lib.identity(
        "dangerous_good" in _options
        or "ups_alcoholic_beverages_indicator" in _options
        or "ups_diagnostic_specimens_indicator" in _options
        or "ups_perishables_indicator" in _options
        or "ups_plants_indicator" in _options
        or "ups_seeds_indicator" in _options
        or "ups_special_exceptions_indicator" in _options
        or "ups_tobacco_indicator" in _options
    )

    if package_options is not None:
        _options.update(package_options.content)

    if _has_pickup_options:
        _options.update(pickup_options=True)

    if _has_delivery_options:
        _options.update(delivery_options=True)

    if _has_signature_required and origin_country and destination_country:
        dc_type = _options.get("ups_delivery_confirmation")
        available_types = DeliveryConfirmationAvailability.get_available_types(
            origin_country, destination_country
        )
        preferred_type = DeliveryConfirmationAvailability.get_preferred_type(
            origin_country, destination_country
        )
        dc_level = DeliveryConfirmationLevel.get_level(
            origin_country, destination_country
        )

        # Validate and adjust delivery confirmation type if needed
        if dc_type and dc_type not in available_types:
            dc_type = preferred_type  # Use preferred type if current is not available
        elif not dc_type and _has_signature_required:
            dc_type = preferred_type  # Use preferred type if none specified

        _options.update(
            ups_delivery_confirmation=dc_type, ups_delivery_confirmation_level=dc_level
        )

    if _has_dangerous_goods and not "ups_restricted_articles" in _options:
        _options.update(
            ups_restricted_articles=lib.identity(
                _options.get("ups_restricted_articles") or "Y"
            )
        )

    # Define carrier option filter.
    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type:ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


class UploadDocumentType(utils.StrEnum):
    ups_authorization_form = "001"
    ups_commercial_invoice = "002"
    ups_certificate_of_origin = "003"
    ups_export_accompanying_document = "004"
    ups_export_license = "005"
    ups_import_permit = "006"
    ups_one_time_nafta = "007"
    ups_other_document = "008"
    ups_power_of_attorney = "009"
    ups_packing_list = "010"
    ups_sed_document = "011"
    ups_shipper_letter_of_instruction = "012"
    ups_declaration = "013"

    """ Unified upload document type mapping """
    certificate_of_origin = ups_certificate_of_origin
    commercial_invoice = ups_commercial_invoice
    pro_forma_invoice = ups_other_document
    packing_list = ups_packing_list
    other = ups_other_document


class TrackingStatus(utils.Enum):
    on_hold = ["X"]
    pending = ["MP"]
    delivered = ["D"]
    in_transit = [""]
    delivery_failed = ["RS"]
    out_for_delivery = ["OT"]


# from https://developer.ups.com/api/reference/rating/appendix?loc=en_US
class SurchargeType(utils.StrEnum):
    additional_handling = "100"
    cod = "110"
    delivery_confirmation = "120"
    ship_delivery_confirmation = "121"
    pkg_email_ship_notification = "153"
    pkg_email_return_notification = "154"
    pkg_email_inbound_return_notification = "155"
    pkg_email_quantum_view_ship_notification = "156"
    pkg_email_quantum_view_exception_notification = "157"
    pkg_email_quantum_view_delivery_notification = "158"
    pkg_fax_inbound_return_notification = "165"
    pkg_fax_quantum_view_ship_notification = "166"
    ship_email_erl_notification = "171"
    ship_email_ship_notification = "173"
    ship_email_return_notification = "174"
    ship_email_inbound_return_notification = "175"
    ship_email_quantum_view_ship_notification = "176"
    ship_email_quantum_view_exception_notification = "177"
    ship_email_quantum_view_delivery_notification = "178"
    ship_email_quantum_view_notify = "179"
    ship_ups_access_point_notification = "187"
    ship_eei_filing_notification = "188"
    ship_uap_shipper_notification = "189"
    extended_area = "190"
    haz_mat = "199"
    dry_ice = "200"
    isc_seeds = "201"
    isc_perishables = "202"
    isc_tobacco = "203"
    isc_plants = "204"
    isc_alcoholic_beverages = "205"
    isc_biological_substances = "206"
    isc_special_exceptions = "207"
    hold_for_pickup = "220"
    origin_certificate = "240"
    print_return_label = "250"
    export_license_verification = "258"
    print_n_mail = "260"
    residential_address = "270"
    return_service_1_attempt = "280"
    return_service_3_attempt = "290"
    saturday_delivery = "300"
    saturday_international_processing_fee = "310"
    electronic_return_label = "350"
    quantum_view_notify_delivery = "372"
    ups_prepared_sed_form = "374"
    fuel_surcharge = "375"
    delivery_area = "376"
    large_package = "377"
    shipper_pays_duty_tax = "378"
    shipper_pays_duty_tax_unpaid = "379"
    express_plus_surcharge = "380"
    insurance = "400"
    ship_additional_handling = "401"
    shipper_release = "402"
    check_to_shipper = "403"
    ups_proactive_response = "404"
    german_pickup = "405"
    german_road_tax = "406"
    extended_area_pickup = "407"
    return_of_document = "410"
    peak_season = "430"
    peak_season_surcharge_large_package = "431"
    peak_season_surcharge_additional_handling = "432"
    ship_large_package = "440"
    carbon_neutral = "441"
    pkg_qv_in_transit_notification = "442"
    ship_qv_in_transit_notification = "443"
    import_control = "444"
    commercial_invoice_removal = "445"
    import_control_electronic_label = "446"
    import_control_print_label = "447"
    import_control_print_and_mail_label = "448"
    import_control_one_pick_up_attempt_label = "449"
    import_control_three_pick_up_attempt_label = "450"
    refrigeration = "452"
    pac_1_a_box_1 = "454"
    pac_3_a_box_1 = "455"
    pac_1_a_box_2 = "456"
    pac_3_a_box_2 = "457"
    pac_1_a_box_3 = "458"
    pac_3_a_box_3 = "459"
    pac_1_a_box_4 = "460"
    pac_3_a_box_4 = "461"
    pac_1_a_box_5 = "462"
    pac_3_a_box_5 = "463"
    exchange_print_return_label = "464"
    exchange_forward = "465"
    ship_prealert_notification = "466"
    committed_delivery_window = "470"
    security_surcharge = "480"
    customer_transaction_fee = "492"
    shipment_cod = "500"
    lift_gate_for_pickup = "510"
    lift_gate_for_delivery = "511"
    drop_off_at_ups_facility = "512"
    ups_premium_care = "515"
    oversize_pallet = "520"
    mi_dual_label_return = "524"
    freight_delivery_surcharge = "530"
    freight_pickup_surcharge = "531"
    direct_to_retail = "540"
    direct_delivery_only = "541"
    deliver_to_addressee_only = "542"
    direct_to_retail_cod = "543"
    retail_access_point = "544"
    shipping_ticket_notification = "545"
    electronic_package_release_authentication = "546"
    pay_at_store = "547"
    icod_notification = "548"
    item_disposal = "550"
    uk_border_fee = "551"
    master_carton = "552"
    simple_rate_accessorial = "553"
    ups_premier_gold = "555"
    ups_premier_silver = "556"
    ups_premier_platinum = "557"
    ddu_oversize = "558"
