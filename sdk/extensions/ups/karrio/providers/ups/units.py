import karrio.core.units as units
import karrio.core.utils as utils

PRESET_DEFAULTS = dict(
    dimension_unit="IN",
    weight_unit="LB",
)


class PackagePresets(utils.Flag):
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


class LabelType(utils.Flag):
    PDF_6x4 = ("PNG", 6, 4)
    PDF_8x4 = ("PNG", 8, 4)
    ZPL_6x4 = ("ZPL", 6, 4)

    """ Unified Label type mapping """
    PDF = PDF_6x4
    ZPL = ZPL_6x4


class Incoterm(utils.Enum):
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


class CustomsContentType(utils.Enum):
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


class WeightUnit(utils.Enum):
    KG = "KGS"
    LB = "LBS"


class PackagingType(utils.Flag):
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


class ShippingService(utils.Enum):
    ups_standard = utils.svcEnum("11")
    ups_worldwide_expedited = utils.svcEnum("8")
    ups_worldwide_express = utils.svcEnum("07")
    ups_worldwide_express_plus = utils.svcEnum("54")
    ups_worldwide_saver = utils.svcEnum("65")
    ups_worldwide_economy_ddp = utils.svcEnum("72")
    ups_worldwide_economy_ddu = utils.svcEnum("17")
    ups_2nd_day_air = utils.svcEnum("02")
    ups_2nd_day_air_am = utils.svcEnum("59")
    ups_3_day_select = utils.svcEnum("12")
    ups_expedited_mail_innovations = utils.svcEnum("M4")
    ups_first_class_mail = utils.svcEnum("M2")
    ups_ground = utils.svcEnum("03")
    ups_next_day_air = utils.svcEnum("01")
    ups_next_day_air_early = utils.svcEnum("14")
    ups_next_day_air_saver = utils.svcEnum("13")
    ups_priority_mail = utils.svcEnum("M3")
    # ups_expedited = utils.svcEnum("02")
    ups_express_saver = utils.svcEnum("13")
    ups_access_point_economy = utils.svcEnum("70")
    ups_express = utils.svcEnum("01")
    # ups_express_early = utils.svcEnum("14")
    # ups_express_saver = utils.svcEnum("65")
    ups_express_early = utils.svcEnum("54")
    ups_tm_worldwide_economy_ddp = utils.svcEnum("72")
    ups_tm_worldwide_economy_ddu = utils.svcEnum("17")
    ups_expedited = utils.svcEnum("08")
    # ups_express = utils.svcEnum("07")
    ups_express_12_00 = utils.svcEnum("74")
    ups_tm_economy_ddp = utils.svcEnum("72")
    ups_tm_economy_ddu = utils.svcEnum("17")
    ups_express_plus = utils.svcEnum("54")
    ups_today_dedicated_courier = utils.svcEnum("83")
    ups_today_express = utils.svcEnum("85")
    ups_today_express_saver = utils.svcEnum("86")
    ups_today_standard = utils.svcEnum("82")
    ups_worldwide_express_freight = utils.svcEnum("96")
    ups_priority_mail_innovations = utils.svcEnum("M5")
    ups_economy_mail_innovations = utils.svcEnum("M6")
    ups_worldwide_express_freight_mid_day = utils.svcEnum("71")


class ShippingOption(utils.Enum):
    ups_negotiated_rates_indicator = utils.OptionEnum("NegotiatedRatesIndicator", bool)
    ups_frs_shipment_indicator = utils.OptionEnum("FRSShipmentIndicator", bool)
    ups_rate_chart_indicator = utils.OptionEnum("RateChartIndicator", bool)
    ups_user_level_discount_indicator = utils.OptionEnum(
        "UserLevelDiscountIndicator", bool
    )
    ups_saturday_pickup_indicator = utils.OptionEnum(
        "SaturdayPickupIndicator", bool
    )
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
    ups_lift_gate_at_pickup_indicator = utils.OptionEnum("LiftGateAtPickupIndicator", bool)
    ups_hold_for_pickup_indicator = utils.OptionEnum("HoldForPickupIndicator", bool)
    ups_lift_gate_at_delivery_indicator = utils.OptionEnum("LiftGateAtDeliveryIndicator", bool)
    ups_drop_off_at_ups_facility_indicator = utils.OptionEnum("DropOffAtUPSFacilityIndicator", bool)

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
    """Apply default values to the given options.
    """
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
        return key in ShippingOption # type:ignore

    return units.ShippingOptions(_options, ShippingOption, items_filter=items_filter)


class UploadDocumentType(utils.Flag):
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
