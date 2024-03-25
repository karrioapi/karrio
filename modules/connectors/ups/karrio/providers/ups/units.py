import karrio.core.units as units
import karrio.core.utils as utils

PRESET_DEFAULTS = dict(
    dimension_unit="IN",
    weight_unit="LB",
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
    label_type = utils.OptionEnum("label_type")
    cost_center = utils.OptionEnum("cost_center")
    merchant_id = utils.OptionEnum("merchant_id")
    enforce_zpl = utils.OptionEnum("enforce_zpl", bool)
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
    ups_negotiated_rates_indicator = utils.OptionEnum("NegotiatedRatesIndicator", bool)
    ups_frs_shipment_indicator = utils.OptionEnum("FRSShipmentIndicator", bool)
    ups_rate_chart_indicator = utils.OptionEnum("RateChartIndicator", bool)
    ups_user_level_discount_indicator = utils.OptionEnum(
        "UserLevelDiscountIndicator", bool
    )
    ups_saturday_pickup_indicator = utils.OptionEnum("SaturdayPickupIndicator", bool)
    ups_saturday_delivery_indicator = utils.OptionEnum(
        "SaturdayDeliveryIndicator", bool
    )
    ups_access_point_cod = utils.OptionEnum("AccessPointCOD", float)
    ups_deliver_to_addressee_only_indicator = utils.OptionEnum(
        "DeliverToAddresseeOnlyIndicator"
    )
    ups_direct_delivery_only_indicator = utils.OptionEnum("DirectDeliveryOnlyIndicator")
    ups_cod = utils.OptionEnum("COD", float)
    ups_delivery_confirmation = utils.OptionEnum("DeliveryConfirmation")
    ups_return_of_document_indicator = utils.OptionEnum("ReturnOfDocumentIndicator")
    ups_carbonneutral_indicator = utils.OptionEnum("UPScarbonneutralIndicator")
    ups_certificate_of_origin_indicator = utils.OptionEnum(
        "CertificateOfOriginIndicator"
    )
    ups_restricted_articles = utils.OptionEnum("RestrictedArticles")
    ups_shipper_export_declaration_indicator = utils.OptionEnum(
        "ShipperExportDeclarationIndicator", bool
    )
    ups_commercial_invoice_removal_indicator = utils.OptionEnum(
        "CommercialInvoiceRemovalIndicator", bool
    )
    ups_import_control = utils.OptionEnum("ImportControl", bool)
    ups_return_service = utils.OptionEnum("ReturnService", bool)
    ups_sdl_shipment_indicator = utils.OptionEnum("SDLShipmentIndicator", bool)
    ups_epra_indicator = utils.OptionEnum("EPRAIndicator", bool)
    ups_lift_gate_at_pickup_indicator = utils.OptionEnum(
        "LiftGateAtPickupIndicator", bool
    )
    ups_hold_for_pickup_indicator = utils.OptionEnum("HoldForPickupIndicator", bool)
    ups_lift_gate_at_delivery_indicator = utils.OptionEnum(
        "LiftGateAtDeliveryIndicator", bool
    )
    ups_drop_off_at_ups_facility_indicator = utils.OptionEnum(
        "DropOffAtUPSFacilityIndicator", bool
    )

    """ Custom option type """
    ups_access_point_pickup = utils.OptionEnum("01", bool)
    ups_access_point_delivery = utils.OptionEnum("02", bool)

    """ Unified Option type mapping """
    cash_on_delivery = ups_cod
    dangerous_good = ups_restricted_articles
    hold_at_location = ups_hold_for_pickup_indicator


def shipping_options_initializer(
    options: dict,
    package_options: units.Options = None,
) -> units.Options:
    """Apply default values to the given options."""
    _options = options.copy()
    _has_pickup_options = (
        "hold_at_location" in _options
        or "ups_epra_indicator" in _options
        or "ups_access_point_pickup" in _options
        or "ups_hold_for_pickup_indicator" in _options
        or "ups_lift_gate_at_pickup_indicator" in _options
    )
    _has_delivery_options = (
        "ups_access_point_delivery" in _options
        or "ups_lift_gate_at_delivery_indicator" in _options
        or "ups_drop_off_at_ups_facility_indicator" in _options
        or "ups_deliver_to_addressee_only_indicator" in _options
    )

    if package_options is not None:
        _options.update(package_options.content)

    if _has_pickup_options:
        _options.update(pickup_options=True)

    if _has_delivery_options:
        _options.update(delivery_options=True)

    if "signature_required" in _options:
        _options.update(
            delivery_options=_options.get("ups_delivery_confirmation") or "01"
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
