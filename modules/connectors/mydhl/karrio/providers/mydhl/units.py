
import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """ Carrier specific packaging types """
    mydhl_card_envelope_imperial = "1CE"
    mydhl_box_2_cube = "2BC"
    mydhl_box_2_pizza = "2BP"
    mydhl_box_2_shoe = "2BX"
    mydhl_box_3 = "3BX"
    mydhl_box_4 = "4BX"
    mydhl_box_5_jumbo_small = "5BX"
    mydhl_box_6 = "6BX"
    mydhl_box_7 = "7BX"
    mydhl_box_8_jumbo_large = "8BX"
    mydhl_card_envelope = "CE1"
    mydhl_tube_large = "TBL"
    mydhl_tube_small = "TBS"
    mydhl_wine_box_1_bottle = "WB1"
    mydhl_wine_box_2_bottles = "WB2"
    mydhl_wine_box_3_bottles = "WB3"
    mydhl_wine_box_6_bottles = "WB6"
    mydhl_express_envelope = "XPD"

    """ Unified Packaging type mapping """
    envelope = mydhl_express_envelope
    pak = mydhl_box_2_pizza
    tube = mydhl_tube_small
    small_box = mydhl_box_3
    medium_box = mydhl_box_5_jumbo_small
    large_box = mydhl_box_8_jumbo_large
    your_packaging = mydhl_box_2_pizza


class ShippingService(lib.StrEnum):
    """ Carrier specific services """
    # Map product codes to service names
    mydhl_express_worldwide = "P"
    mydhl_express_12_00 = "T"
    mydhl_express_domestic = "N"
    mydhl_medical_express = "Q"
    mydhl_express_easy = "8"

    # Additional services by code
    mydhl_jetline = "J"
    mydhl_sprintline = "R"
    mydhl_express_9_00 = "Y"
    mydhl_economy_select = "W"
    mydhl_express_10_30 = "X"
    mydhl_globalmail = "G"
    mydhl_same_day = "S"


class ShippingOption(lib.Enum):
    """ Carrier specific options """
    mydhl_saturday_delivery = lib.OptionEnum("AA")
    mydhl_emergency_situation = lib.OptionEnum("CR")
    mydhl_diplomatic_mail = lib.OptionEnum("CG")
    mydhl_duty_tax_paid = lib.OptionEnum("DD")
    mydhl_receiver_paid = lib.OptionEnum("DE")
    mydhl_import_billing = lib.OptionEnum("DT")
    mydhl_duty_tax_importer = lib.OptionEnum("DU")
    mydhl_gogreen_climate_neutral = lib.OptionEnum("EE")
    mydhl_gogreen_plus_carbon_reduced = lib.OptionEnum("FE")
    mydhl_fuel_surcharge = lib.OptionEnum("FF")
    mydhl_packaging = lib.OptionEnum("GG")
    mydhl_dry_ice = lib.OptionEnum("HC")
    mydhl_lithium_ion_pi966_section_ii = lib.OptionEnum("HD")
    mydhl_dangerous_goods = lib.OptionEnum("HE")
    mydhl_excepted_quantities = lib.OptionEnum("HH")
    mydhl_consumer_commodities = lib.OptionEnum("HK")
    mydhl_lithium_metal = lib.OptionEnum("HM")
    mydhl_active_data_logger = lib.OptionEnum("HT")
    mydhl_not_restricted_dangerous_goods = lib.OptionEnum("HU")
    mydhl_lithium_ion_pi967_section_ii = lib.OptionEnum("HV")
    mydhl_lithium_metal_pi970_section_ii = lib.OptionEnum("HW")
    mydhl_magnetized_material = lib.OptionEnum("HX")
    mydhl_shipment_insurance = lib.OptionEnum("II")
    mydhl_verbal_notification = lib.OptionEnum("JA")
    mydhl_verbal_notification_alternative = lib.OptionEnum("JD")
    mydhl_courier_time_window = lib.OptionEnum("JY")
    mydhl_cold_storage = lib.OptionEnum("LG")
    mydhl_sanctions_routing = lib.OptionEnum("LU")
    mydhl_hold_for_collection = lib.OptionEnum("LX")
    mydhl_address_correction = lib.OptionEnum("MA")
    mydhl_neutral_delivery = lib.OptionEnum("NN")
    mydhl_remote_area_delivery = lib.OptionEnum("OO")
    mydhl_account_number_change = lib.OptionEnum("PA")
    mydhl_origin_duties_taxes = lib.OptionEnum("PD")
    mydhl_proactive_response = lib.OptionEnum("PH")
    mydhl_third_party_consignee = lib.OptionEnum("PJ")
    mydhl_direct_injection = lib.OptionEnum("PK")
    mydhl_prelodged = lib.OptionEnum("PL")
    mydhl_duty_payment_service = lib.OptionEnum("PM")
    mydhl_broker_notification = lib.OptionEnum("PO")
    mydhl_pre_advice = lib.OptionEnum("PP")
    mydhl_e_mail_notification = lib.OptionEnum("PQ")
    mydhl_email_notification_receiver = lib.OptionEnum("PR")
    mydhl_premium_sensor_service = lib.OptionEnum("PT")
    mydhl_data_staging = lib.OptionEnum("PU")
    mydhl_broker_instruction = lib.OptionEnum("PV")
    mydhl_security_validation = lib.OptionEnum("PW")
    mydhl_express_pickup = lib.OptionEnum("PZ")
    mydhl_qr_code = lib.OptionEnum("QA")
    mydhl_saturday_pickup = lib.OptionEnum("SF")
    mydhl_signature_release = lib.OptionEnum("SX")
    mydhl_top_third_floor = lib.OptionEnum("TF")
    mydhl_after_hours_delivery = lib.OptionEnum("TK")
    mydhl_time_critical = lib.OptionEnum("TT")
    mydhl_split_delivery = lib.OptionEnum("TV")
    mydhl_waybill_breakbulk = lib.OptionEnum("WB")
    mydhl_waybill_document = lib.OptionEnum("WD")
    mydhl_economy_select_non_doc = lib.OptionEnum("WE")
    mydhl_economy_select_doc = lib.OptionEnum("WF")
    mydhl_piece_tags = lib.OptionEnum("WG")
    mydhl_non_standard_handling = lib.OptionEnum("WH")
    mydhl_delivery_signature = lib.OptionEnum("WI")
    mydhl_piece_tag_barcode = lib.OptionEnum("WJ")
    mydhl_piece_tag_customer = lib.OptionEnum("WK")
    mydhl_delivery_signature_waived = lib.OptionEnum("WL")
    mydhl_non_conveyables = lib.OptionEnum("WM")
    mydhl_delivery_receipt = lib.OptionEnum("WO")
    mydhl_secure_storage = lib.OptionEnum("WS")
    mydhl_non_stackable = lib.OptionEnum("WT")
    mydhl_delivery_signature_alternative = lib.OptionEnum("WY")
    mydhl_broker_selection = lib.OptionEnum("XB")
    mydhl_shipment_value_protection = lib.OptionEnum("XE")
    mydhl_dangerous_goods_notification = lib.OptionEnum("XJ")
    mydhl_delivery_payment_service = lib.OptionEnum("XK")
    mydhl_additional_handling = lib.OptionEnum("XX")
    mydhl_clearance_data_modification = lib.OptionEnum("YC")

    """ Unified Option type mapping """
    insurance = mydhl_shipment_insurance
    signature_confirmation = mydhl_delivery_signature
    hold_for_pickup = mydhl_hold_for_collection
    saturday_delivery = mydhl_saturday_delivery
    dangerous_goods = mydhl_dangerous_goods
    email_notification = mydhl_e_mail_notification


class MeasurementUnit(lib.StrEnum):
    """ Unit of measurement """
    metric = "metric"
    imperial = "imperial"


class WeightUnit(lib.StrEnum):
    """ Weight unit """
    KG = "kg"
    LB = "lb"


class DimensionUnit(lib.StrEnum):
    """ Dimension unit """
    CM = "cm"
    IN = "in"


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
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]
