from karrio.core import units
from karrio.core.utils import Flag, Enum
from karrio.core.utils.enum import OptionEnum


class UnitOfMeasurement(Enum):
    K = "K"
    L = "L"
    KC = "KC"
    KM = "KM"
    LI = "LI"
    LF = "LF"


class Category(Enum):
    parcel = "Parcel"
    freight = "Freight"
    distribution = "Distribution"
    logistics = "Logistics"


class Purpose(Enum):
    com = "COM"
    per = "PER"
    doc = "DOC"
    ret = "RET"

    """ Unified Customs Content Type mapping """

    documents = doc
    gift = per
    sample = per
    merchandise = com
    return_merchandise = ret
    other = per


class PaymentType(Flag):
    prepaid = "Prepaid"
    third_party = "ThirdParty"
    collect = "Collect"

    """ Unified Payment Type mapping """

    sender = prepaid
    recipient = collect


class ParcelType(Flag):
    dicom_barrel = "Barrel"
    dicom_bundle = "Bundle"
    dicom_box = "Box"
    dicom_crate = "Crate"
    dicom_full_load = "FullLoad"
    dicom_mixed = "Mixed"
    dicom_other = "Other"
    dicom_piece = "Piece"
    dicom_skid = "Skid"
    dicom_tube = "Tube"
    dicom_envelope = "Envelope"
    dicom_maxpak = "Maxpak"
    dicom_pallet = "Pallet"

    """ Unified Packaging type mapping """

    envelope = dicom_envelope
    pak = dicom_maxpak
    tube = dicom_tube
    pallet = dicom_pallet
    small_box = dicom_box
    medium_box = dicom_box
    your_packaging = dicom_other


class Service(Enum):  # DeliveryType
    dicom_air_delivery = "AIR"
    dicom_ground_delivery = "GRD"


class ShippingOption(Enum):
    dicom_common_declared_value = OptionEnum("DCV")
    dicom_common_dangerous_goods = OptionEnum("DGG")
    dicom_common_residential_delivery = OptionEnum("PHD")
    dicom_common_tradeshow_delivery = OptionEnum("TRD")
    dicom_common_signature_not_required = OptionEnum("SNR")
    dicom_parcel_ca_hold_for_pickup = OptionEnum("HFP")
    dicom_parcel_ca_non_conveyable = OptionEnum("NCV")
    dicom_parcel_ca_residential_delivery_signature = OptionEnum("PHDS")
    dicom_parcel_ca_weekend_delivery = OptionEnum("WKD")
    dicom_freight_construction_site_delivery = OptionEnum("CNSTD")
    dicom_freight_collect_on_delivery = OptionEnum("COD")
    dicom_freight_heating = OptionEnum("HEAT")
    dicom_freight_inside_delivery = OptionEnum("IDEL")
    dicom_freight_residential_delivery_signature = OptionEnum("PHDS")
    dicom_freight_residential_pickup = OptionEnum("PHPU")
    dicom_freight_tailgate_delivery = OptionEnum("TGT")
    dicom_freight_tailgate_pickup = OptionEnum("TGTPU")
    dicom_parcel_us_adult_signature = OptionEnum("ADLSIG")
    dicom_parcel_us_direct_signature = OptionEnum("DIRSIG")
    dicom_parcel_us_saturday_delivery = OptionEnum("SAT")
    dicom_parcel_us_sunday_delivery = OptionEnum("SUN")
    dicom_parcel_us_residential_delivery_signature = OptionEnum("PHDS")
    dicom_parcel_us_earliest_possible = OptionEnum("EP")
    dicom_parcel_us_priority_service = OptionEnum("PR")
    dicom_parcel_us_pouch_service = OptionEnum("PO")
    dicom_parcel_us_pallet_service_pa = OptionEnum("PA")
    dicom_parcel_us_pallet_service_rap = OptionEnum("RAP")
    dicom_parcel_us_pallet_service_nd = OptionEnum("ND")


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


class Surcharge(Flag):
    dicom_common_base = "BAS"
    dicom_common_declared_value = "DCV"
    dicom_common_dangerous_goods = "DGG"
    dicom_common_other_charge = "OTH"
    dicom_common_residential_delivery = "PHD"
    dicom_common_tradeshow_delivery = "TRD"
    dicom_parcel_ca_collect_on_delivery = "COD"
    dicom_parcel_ca_collect = "COL"
    dicom_parcel_ca_chain_of_signature = "COS"
    dicom_parcel_ca_dangerous_goods = "DGA"
    dicom_parcel_ca_hold_for_pickup = "HFP"
    dicom_parcel_ca_multi_pieces = "MPC"
    dicom_parcel_ca_non_conveyable = "NCV"
    dicom_parcel_ca_residential_delivery_signature = "PHS"
    dicom_parcel_ca_over_36_inches = "O36"
    dicom_parcel_ca_over_44_inches = "O44"
    dicom_parcel_ca_over_96_inches = "O96"
    dicom_parcel_ca_overweight = "OVW"
    dicom_parcel_ca_signature_not_required = "SNR"
    dicom_parcel_ca_trade_show = "TRD"
    dicom_parcel_ca_weekend_delivery = "WKD"
    dicom_parcel_ca_weekend_kilometers = "WKK"
    dicom_parcel_ca_zone = "ZON"
    dicom_parcel_ca_ontario_minimum_wage = "SMO"
    dicom_parcel_ca_overweight_shipment = "OWS"
    dicom_freight_construction_site_delivery = "CNSTD"
    dicom_freight_collect_on_delivery = "COD"
    dicom_freight_congestion_pickup = "CPU"
    dicom_freight_heating = "HEAT"
    dicom_freight_inside_delivery = "IDEL"
    dicom_freight_pan_am_games_delivery = "PADL"
    dicom_freight_pan_am_games_pickup = "PAPU"
    dicom_freight_residential_delivery_signature = "PHDS"
    dicom_freight_residential_pickup = "PHPU"
    dicom_freight_promo_cash = "PRC"
    dicom_freight_promo_pourcent = "PRP"
    dicom_freight_single_pickup = "SPU"
    dicom_freight_tailgate_delivery = "TGT"
    dicom_freight_tailgate_pickup = "TGTPU"
