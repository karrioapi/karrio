import karrio.lib as lib
import karrio.core.units as units


class LabelType(lib.Flag):
    PDF_6x4 = ("GIF", 6, 4)
    PDF_8x4 = ("GIF", 8, 4)
    ZPL_6x4 = ("ZPL", 6, 4)

    """ Unified Label type mapping """
    PDF = PDF_6x4
    ZPL = ZPL_6x4


class Incoterm(lib.Enum):
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


class WeightUnit(lib.Enum):
    KG = "KGS"
    LB = "LBS"


class PackagingType(lib.Flag):
    ups_bag = "BAG"
    ups_bal = "BAL"
    ups_bale = "Bale"
    ups_bar = "BAR"
    ups_barrel = "Barrel"
    ups_bdl = "BDL"
    ups_bundle = "Bundle"
    ups_bin = "BIN"
    ups_box = "BOX"
    ups_bsk = "BSK"
    ups_basket = "Basket"
    ups_bun = "BUN"
    ups_bunch = "Bunch"
    ups_cab = "CAB"
    ups_cabinet = "Cabinet"
    ups_can = "CAN"
    ups_car = "CAR"
    ups_carrier = "Carrier"
    ups_cas = "CAS"
    ups_case = "Case"
    ups_cby = "CBY"
    ups_carboy = "Carboy"
    ups_con = "CON"
    ups_container = "Container"
    ups_crt = "CRT"
    ups_crate = "Crate"
    ups_csk = "CSK"
    ups_cask = "Cask"
    ups_ctn = "CTN"
    ups_carton = "Carton"
    ups_cyl = "CYL"
    ups_cylinder = "Cylinder"
    ups_drm = "DRM"
    ups_drum = "Drum"
    ups_loo = "LOO"
    ups_loose = "Loose"
    ups_oth = "OTH"
    ups_other = "Other"
    ups_pal = "PAL"
    ups_pail = "Pail"
    ups_pcs = "PCS"
    ups_pieces = "Pieces"
    ups_pkg = "PKG"
    ups_package = "Package"
    ups_pln = "PLN"
    ups_pipe_line = "Pipe Line"
    ups_plt = "PLT"
    ups_pallet = "Pallet"
    ups_rck = "RCK"
    ups_rack = "Rack"
    ups_rel = "REL"
    ups_reel = "Reel"
    ups_rol = "ROL"
    ups_roll = "Roll"
    ups_skd = "SKD"
    ups_skid = "Skid"
    ups_spl = "SPL"
    ups_spool = "Spool"
    ups_tbe = "TBE"
    ups_tube = "Tube"
    ups_tnk = "TNK"
    ups_tank = "Tank"
    ups_unt = "UNT"
    ups_unit = "Unit"
    ups_vpk = "VPK"
    ups_van_pack = "Van Pack"
    ups_wrp = "WRP"
    ups_wrapped = "Wrapped"

    """ unified Packaging type mapping  """
    envelope = ups_other
    pak = ups_other
    tube = ups_tube
    pallet = ups_pallet
    small_box = ups_other
    medium_box = ups_other
    your_packaging = ups_other


class PaymentType(lib.Flag):
    prepaid = "10"
    bill_to_third_party = "30"
    freight_collect = "40"

    """ Unified Payment type mapping """

    sender = prepaid
    recipient = freight_collect
    third_party = bill_to_third_party


class ShippingService(lib.Enum):
    ups_tforce_freight_ltl = "308"
    ups_tforce_freight_ltl_guaranteed = "309"
    ups_tforce_freight_ltl_guaranteed_am = "334"
    ups_tforce_standard_ltl = "349"


class ShippingOption(lib.Enum):
    ups_freight_linear_feet = lib.OptionEnum("LinearFeet", bool)
    ups_freight_alternate_rate_option = lib.OptionEnum("AlternateRateOption", bool)
    ups_freight_on_call_pickup_indicator = lib.OptionEnum("OnCallPickupIndicator", bool)
    ups_freight_call_before_delivery_indicator = lib.OptionEnum(
        "CallBeforeDeliveryIndicator", bool
    )
    ups_freight_holiday_delivery_indicator = lib.OptionEnum(
        "HolidayDeliveryIndicator", bool
    )
    ups_freight_inside_delivery_indicator = lib.OptionEnum(
        "InsideDeliveryIndicator", bool
    )
    ups_freight_residential_delivery_indicator = lib.OptionEnum(
        "ResidentialDeliveryIndicator", bool
    )
    ups_freight_weekend_delivery_indicator = lib.OptionEnum(
        "WeekendDeliveryIndicator", bool
    )
    ups_freight_lift_gate_required_indicator = lib.OptionEnum(
        "LiftGateRequiredIndicator", bool
    )
    ups_freight_limited_access_delivery_indicator = lib.OptionEnum(
        "LimitedAccessDeliveryIndicator", bool
    )
    ups_freight_extreme_length_indicator = lib.OptionEnum(
        "ExtremeLengthIndicator", bool
    )
    ups_freight_freezable_protection_indicator = lib.OptionEnum(
        "FreezableProtectionIndicator", bool
    )
    ups_freight_time_in_transit_indicator = lib.OptionEnum(
        "TimeInTransitIndicator", bool
    )
    ups_freight_gpf_accesorial_rate_indicator = lib.OptionEnum(
        "GPFAccesorialRateIndicator", bool
    )
    ups_freight_density_eligible_indicator = lib.OptionEnum(
        "DensityEligibleIndicator", bool
    )
    ups_freight_ajusted_height = lib.OptionEnum("AdjustedHeight", float)

    freight_class = lib.OptionEnum("freight_class")


def shipping_options_initializer(
    options: dict,
    package_options: units.Options = None,
) -> units.Options:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    return units.ShippingOptions(_options, ShippingOption)


class PickupOption(lib.Enum):
    ups_freight_third_party_indicator = lib.OptionEnum("ThirdPartyIndicator", bool)
    ups_freight_freezable_protection_indicator = lib.OptionEnum(
        "FreezableProtectionIndicator", bool
    )
    ups_freight_limited_access_pickup_indicator = lib.OptionEnum(
        "LimitedAccessPickupIndicator", bool
    )
    ups_freight_limited_access_delivery_indicator = lib.OptionEnum(
        "LimitedAccessDeliveryIndicator", bool
    )
    ups_freight_extreme_length_indicator = lib.OptionEnum(
        "ExtremeLengthIndicator", bool
    )

    recipient_postal_code = lib.OptionEnum("recipient_postal_code")
    recipient_country_code = lib.OptionEnum("recipient_country_code")


class UploadDocumentType(lib.Flag):
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
    other = ups_other_document


class RateType(lib.Enum):
    fuel_surcharge = "2"
    arrival_notification = "ADV_NOTF"
    amount_after_discount = "AFTR_DSCNT"
    border_processing_fee = "CA_BORDER"
    custom_manifest_fee = "CA_CSTM_MNFST"
    collect_on_delivery_fee = "COD"
    deficit_rate = "DEFICITRATE"
    deficit_weight = "DEFICITWGHT"
    deficit_charge = "DFCT_AMT"
    discounted_amount = "DSCNT"
    discount_rate_as_a_percentage = "DSCNT_RATE"
    extreme_length = "EXC_LEN"
    excess_declared_value_charges = "EXLI"
    freezable_protection = "FREEZE_PROT"
    guaranteed_service_charges = "GUAR_SERVICE"
    hazardous_materials_charge = "HAZMAT"
    high_cost_service_area_surcharge = "HICST"
    holiday_weekend_pickup_or_delivery = "HOL_WE_PU_DEL"
    inside_pickup_delivery = "INSD_PU_DEL"
    custom_charge = "L_UPGF_016"
    liftgate_fee = "LIFTGATE"
    limited_access_pickup_delivery = "LIM_ACC_PU_DEL"
    gross_charges = "LND_GROSS"
    minimum_charge_applies = "MINCHARGE"
    ocean_fuel_surcharge = "OFUELSURCHG"
    residential_pickup_delivery = "RESI_PU_DEL"
    remote_location_fee = "RMTLOC"
    sorting_and_segregation = "SORTSEG"
    total_island_charges = "TOTI"
    total_ocean_charges = "TOTO"
